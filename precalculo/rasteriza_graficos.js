#!/usr/bin/env node
//
// rasteriza_graficos.js — los gráficos de las preguntas del preparcial, a PNG
//
// Material de Series de Tiempo 2026-II (20948).
//
//   node precalculo/rasteriza_graficos.js [--url <base>] [--destino <carpeta>]
//
// Los ítems de tipo `grafico` no se pueden exportar a Brightspace como están:
// son un <canvas> que Chart.js pinta en el navegador. Este guion abre el
// preparcial en Chrome sin ventana, recorre los módulos que llevan quiz,
// espera a que cada gráfico se pinte y guarda el lienzo como PNG.
//
// Se rasteriza el canvas REAL en vez de volver a dibujar la figura con otra
// herramienta. Redibujarla obliga a declarar por segunda vez qué serie va en
// qué eje, y esa segunda declaración se desincroniza del material sin que nada
// falle: la pregunta seguiría importando bien, con la figura equivocada. Aquí
// la imagen es, por construcción, la que el estudiante vio.
//
// Cuatro cosas que no son opcionales, heredadas del guion equivalente de
// Diseño de Experimentos, que las aprendió fallando:
//
//   1. `--window-size` explícito y `innerWidth` comprobado ANTES de medir. Una
//      pestaña en segundo plano tiene innerWidth = 0 y todos los lienzos salen
//      de 0 px: no da error, da imágenes vacías.
//   2. Fondo BLANCO debajo. Chart.js dibuja sobre transparente; en Brightspace
//      el PNG quedaría sobre el color del tema y las líneas oscuras
//      desaparecerían.
//   3. Se cuentan los píxeles con tinta. Un lienzo puede tener el tamaño
//      correcto y estar en blanco, y sin esta cuenta el banco viajaría con un
//      rectángulo vacío que nadie ve hasta el examen.
//   4. Las animaciones se apagan. Capturar a media animación da una figura
//      a medio dibujar, y el fallo es intermitente.
//
// Sale: <destino>/<bloque>_<n>.png, uno por ítem de tipo `grafico` de CADA
//       documento que se le pase, más
//       <destino>/inventario.json con el tamaño y la tinta de cada uno.

const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawn } = require('child_process');

const AQUI = __dirname;
const RAIZ = path.resolve(AQUI, '..');

const arg = (nombre, pordefecto) => {
  const i = process.argv.indexOf(nombre);
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : pordefecto;
};

const BASE = arg('--url', 'http://localhost:8731/');
const autoprueba = process.argv.includes('--autoprueba');
// Varias páginas en una sola sesión de Chrome, y un solo inventario. Los PNG
// se nombran por BLOQUE —`bloque-d_3`, `cap2_1`— y los bloques no se repiten
// entre documentos, así que comparten carpeta sin pisarse. Separarlos en una
// carpeta por página obligaría al exportador a saber en cuál buscar cada uno.
const PAGINAS = arg('--paginas', 'preparcial-corte-1.html').split(',').map(x => x.trim());
const DESTINO = path.resolve(RAIZ, arg('--destino', 'precalculo/salidas/graficos'));
const PUERTO = 9223;
const ANCHO = 1440, ALTO = 1100;

// Los módulos NO se declaran aquí: se leen de `courseData.modules` en la
// página. Declararlos obliga a acordarse de este archivo cada vez que el
// preparcial gane o pierda un módulo, y olvidarlo no da error — da un banco
// al que le faltan gráficos en silencio.
//
// Y dentro de cada módulo se captura POR CONTENEDOR `[data-quiz]`, no por
// módulo entero. El bloque es la clave con la que `exporta_brightspace.py`
// nombra los ítems, así que los PNG salen con ese mismo nombre y no hace
// falta un segundo convenio para casarlos. Capturar por módulo funcionaba
// solo mientras cada módulo tuviera un quiz: con dos, los lienzos del
// segundo se numeran a continuación de los del primero y cada pregunta
// acaba con la figura de otra. Eso importa sin un solo error.

const CHROME = [
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
  '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
].find(p => fs.existsSync(p));

const espera = ms => new Promise(r => setTimeout(r, ms));

// ------------------------------------------------------------------ CDP

class Chrome {
  constructor(ws) { this.ws = ws; this.id = 0; this.pendientes = new Map(); }

  static async abrir(puerto) {
    let objetivo = null;
    for (let i = 0; i < 80 && !objetivo; i++) {
      try {
        const lista = await (await fetch(`http://127.0.0.1:${puerto}/json/list`)).json();
        objetivo = lista.find(t => t.type === 'page' && t.webSocketDebuggerUrl);
      } catch (e) { /* aún no levantó */ }
      if (!objetivo) await espera(250);
    }
    if (!objetivo) throw new Error('Chrome no expuso ninguna pestaña en el puerto de depuración');
    const ws = new WebSocket(objetivo.webSocketDebuggerUrl);
    await new Promise((ok, mal) => {
      ws.onopen = ok;
      ws.onerror = () => mal(new Error('no se pudo abrir el WebSocket de CDP'));
    });
    const c = new Chrome(ws);
    ws.onmessage = ev => {
      const m = JSON.parse(ev.data);
      if (m.id && c.pendientes.has(m.id)) {
        const { ok, mal } = c.pendientes.get(m.id);
        c.pendientes.delete(m.id);
        m.error ? mal(new Error(m.error.message)) : ok(m.result);
      }
    };
    return c;
  }

  enviar(method, params = {}) {
    const id = ++this.id;
    return new Promise((ok, mal) => {
      this.pendientes.set(id, { ok, mal });
      this.ws.send(JSON.stringify({ id, method, params }));
      setTimeout(() => {
        if (this.pendientes.has(id)) {
          this.pendientes.delete(id);
          mal(new Error(`${method}: sin respuesta en 60 s`));
        }
      }, 60000);
    });
  }

  // Espera a que una expresión de la página sea cierta. Dormir un rato fijo
  // funciona hasta el día que no: si el servidor está caído o la página tarda,
  // el guion sigue adelante y falla más abajo con un error que no señala la
  // causa.
  async esperaHasta(expresion, ms, quejaSiNo) {
    const hasta = Date.now() + ms;
    for (;;) {
      try {
        if (await this.evalua(expresion)) return true;
      } catch (e) { /* la página aún no tiene ni ámbito */ }
      if (Date.now() > hasta) throw new Error(quejaSiNo);
      await espera(200);
    }
  }

  async evalua(expresion) {
    const r = await this.enviar('Runtime.evaluate', {
      expression: expresion, awaitPromise: true, returnByValue: true,
    });
    if (r.exceptionDetails) {
      throw new Error('la página lanzó: ' +
        (r.exceptionDetails.exception?.description || r.exceptionDetails.text));
    }
    return r.result.value;
  }
}

// ------------------------------------------------- lo que corre en la página

// Apaga las animaciones de Chart.js ANTES de que se pinte nada (nota 4).
const SIN_ANIMACION = `
  (() => {
    if (typeof Chart === 'undefined') return 'no hay Chart.js';
    Chart.defaults.animation = false;
    Chart.defaults.animations = {};
    Chart.defaults.transitions = { active: { animation: { duration: 0 } } };
    return 'animaciones apagadas';
  })()`;

// El simulacro no pinta nada hasta que se pulsa «Empezar»: se pulsa en una
// evaluación aparte y se espera, porque `dibujar` corre dentro de un
// requestAnimationFrame y capturar en la misma vuelta da el lienzo en blanco.
const ARRANCA_SIMULACRO = `
  (() => {
    const b = [...document.querySelectorAll('button')]
      .find(x => /empezar el simulacro/i.test(x.textContent));
    if (!b) return 'no encontré el botón de arranque';
    b.click();
    return 'simulacro arrancado';
  })()`;

const CAPTURA = `
  (() => {
    if (window.innerWidth < 1024) {
      return { error: 'innerWidth = ' + window.innerWidth + ', hacen falta 1024 o más' };
    }
    const raiz = document.querySelector('main') || document.body;
    const cajas = [...raiz.querySelectorAll('[data-quiz], [data-simulacro]')];
    const bloques = [];

    for (const caja of cajas) {
      const esSimulacro = caja.hasAttribute('data-simulacro');
      const bloque = esSimulacro ? 'simulacro' : caja.dataset.quiz;

      // Cuántos gráficos DECLARA el bloque. \`AUTOEVALUACIONES\` y
      // \`SIMULACRO\` son \`const\` de nivel superior del guion de la página:
      // viven en el ámbito léxico global y NO cuelgan de \`window\`, así que se
      // leen por su nombre. Si el bloque no tiene registro —el \`data-quiz\`
      // de ejemplo del componente— se devuelve null y no se exige nada.
      let declarados = null;
      if (esSimulacro) {
        if (typeof SIMULACRO === 'object' && SIMULACRO && SIMULACRO.items) {
          declarados = SIMULACRO.items.filter(p => p.tipo === 'grafico').length;
        }
      } else {
        const registro = (typeof AUTOEVALUACIONES === 'object' ? AUTOEVALUACIONES : {})[bloque];
        if (registro) declarados = registro.filter(p => p.tipo === 'grafico').length;
      }

      const lienzos = [...caja.querySelectorAll('.quiz-grafico canvas')];
      const imagenes = [], problemas = [];

      lienzos.forEach((canvas, k) => {
        const w = canvas.width, h = canvas.height;
        if (!w || !h) { problemas.push('lienzo ' + (k + 1) + ': ' + w + '×' + h); return; }

        const plano = document.createElement('canvas');
        plano.width = w; plano.height = h;
        const ctx = plano.getContext('2d');
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, w, h);
        ctx.drawImage(canvas, 0, 0);

        const datos = ctx.getImageData(0, 0, w, h).data;
        let tinta = 0;
        for (let i = 0; i < datos.length; i += 4) {
          if (datos[i] !== 255 || datos[i+1] !== 255 || datos[i+2] !== 255) tinta++;
        }
        const pct = (100 * tinta) / (w * h);
        if (pct < 1) problemas.push('lienzo ' + (k + 1) + ': solo ' + pct.toFixed(2) + ' % con tinta');

        imagenes.push({ orden: k, ancho: w, alto: h, tinta: Number(pct.toFixed(2)),
                        dataURI: plano.toDataURL('image/png') });
      });

      bloques.push({ bloque, declarados, encontrados: lienzos.length, problemas, imagenes });
    }

    return { innerWidth: window.innerWidth, bloques };
  })()`;

// Lo mismo que CAPTURA pero SIN codificar ni un PNG: por bloque, cuántos
// gráficos declara y cuántos lienzos hay. Es exactamente lo que compara el
// guardián, así que es lo único que la autoprueba necesita mirar — y evita
// volver a codificar ocho imágenes para comprobar una resta.
const RECUENTO = `
  (() => {
    const raiz = document.querySelector('main') || document.body;
    return [...raiz.querySelectorAll('[data-quiz], [data-simulacro]')].map(caja => {
      const esSimulacro = caja.hasAttribute('data-simulacro');
      const bloque = esSimulacro ? 'simulacro' : caja.dataset.quiz;
      let declarados = null;
      if (esSimulacro) {
        if (typeof SIMULACRO === 'object' && SIMULACRO && SIMULACRO.items) {
          declarados = SIMULACRO.items.filter(p => p.tipo === 'grafico').length;
        }
      } else {
        const registro = (typeof AUTOEVALUACIONES === 'object' ? AUTOEVALUACIONES : {})[bloque];
        if (registro) declarados = registro.filter(p => p.tipo === 'grafico').length;
      }
      return { bloque, declarados,
               encontrados: caja.querySelectorAll('.quiz-grafico canvas').length };
    });
  })()`;

// Quita un lienzo del bloque que se le diga. Solo lo usa `--autoprueba`: el
// descuadre entre lo declarado y lo encontrado es la avería que este guion
// existe para cazar, y una comprobación que nunca se ha visto fallar no está
// probada.
const QUITA_UN_LIENZO = bloque => `
  (() => {
    const caja = document.querySelector('[data-quiz="' + ${JSON.stringify(bloque)} + '"]');
    const uno = caja && caja.querySelector('.quiz-grafico canvas');
    if (!uno) return 'no había lienzo que quitar';
    uno.closest('.quiz-grafico').remove();
    return 'quitado un lienzo de ' + ${JSON.stringify(bloque)};
  })()`;

// ¿Hay un simulacro sin arrancar en el módulo que está a la vista?
const HAY_QUE_ARRANCAR = `
  !!document.querySelector('[data-simulacro]') &&
  [...document.querySelectorAll('button')].some(b => /empezar el simulacro/i.test(b.textContent))`;

// ------------------------------------------------------------------ principal

async function main() {
  if (!CHROME) {
    console.error('✗ No encontré Chrome, Chromium, Brave ni Edge en /Applications.');
    process.exit(1);
  }
  fs.mkdirSync(DESTINO, { recursive: true });

  const perfil = fs.mkdtempSync(path.join(os.tmpdir(), 'series-chrome-'));
  const proc = spawn(CHROME, [
    '--headless=new', `--remote-debugging-port=${PUERTO}`,
    `--user-data-dir=${perfil}`, `--window-size=${ANCHO},${ALTO}`,
    '--no-first-run', '--no-default-browser-check', '--disable-gpu',
    '--force-device-scale-factor=2', 'about:blank',
  ], { stdio: 'ignore' });

  const inventario = [];
  let problemas = [];
  let descuadreDetectado = null;
  const vistos = new Set();
  try {
    const c = await Chrome.abrir(PUERTO);
    await c.enviar('Page.enable');
    await c.enviar('Runtime.enable');

    for (const PAGINA of PAGINAS) {
    const url = BASE.replace(/\/$/, '') + '/' + PAGINA;
    if (PAGINAS.length > 1) console.log(`\n  · ${PAGINA}`);
    await c.enviar('Page.navigate', { url });
    // Se espera a que el guion del documento haya corrido —`courseData` es lo
    // primero que declara— en vez de dormir un rato fijo. `loadEventFired`
    // no sirve: llega antes de que el módulo 1 esté pintado.
    await c.esperaHasta("typeof courseData !== 'undefined'", 20000,
      `la página no llegó a ejecutar su guion en 20 s.\n        ` +
      `¿Está sirviéndose ${url}? El servidor de desarrollo es ` +
      `\`htmls-series\` en .claude/launch.json.`);

    // El documento carga Chart.js y KaTeX de un CDN, y `loadModule` llama a
    // `renderMathInElement` sin comprobar que exista. Si una de las dos no
    // llegó —red lenta, CDN caído— el guion moría con un ReferenceError que
    // no dice de qué va la cosa, o peor: dibujaba cero lienzos y el banco
    // salía sin figuras. Se esperan las dos y se nombra la que falte.
    await c.esperaHasta(
      "typeof Chart !== 'undefined' && typeof renderMathInElement === 'function'", 20000,
      'las librerías externas del documento no cargaron en 20 s. Falta ' +
      (await c.evalua("[typeof Chart === 'undefined' ? 'Chart.js' : null, " +
                      "typeof renderMathInElement !== 'function' ? 'KaTeX (auto-render)' : null]" +
                      ".filter(Boolean).join(' y ')") || 'alguna') +
      '.\n        Las dos vienen de un CDN: hace falta red para rasterizar.');
    console.log('  ' + await c.evalua(SIN_ANIMACION));

    const modulos = await c.evalua('courseData.modules.map(m => m.id)');
    console.log(`  ${modulos.length} módulos declarados en la página`);

    for (const modulo of modulos) {
      await c.evalua(`loadModule(${modulo}), 'ok'`);
      await espera(1200);

      // El simulacro no pinta nada hasta que se pulsa «Empezar». Se pregunta
      // al DOM en vez de llevarlo apuntado: así el guion no depende de en qué
      // módulo esté el simulacro hoy.
      if (await c.evalua(HAY_QUE_ARRANCAR)) {
        console.log('  ' + await c.evalua(ARRANCA_SIMULACRO));
        await espera(1200);
      }

      const r = await c.evalua(CAPTURA);
      if (r.error) { problemas.push(`módulo ${modulo}: ${r.error}`); continue; }

      for (const b of r.bloques) {
        problemas = problemas.concat((b.problemas || []).map(p => `${b.bloque}: ${p}`));

        if (vistos.has(b.bloque)) {
          problemas.push(`${b.bloque}: aparece en más de un módulo; el segundo ` +
                         `sobrescribiría los PNG del primero`);
          continue;
        }
        vistos.add(b.bloque);

        // La comprobación que justifica capturar por contenedor: si el bloque
        // declara N ítems de tipo `grafico` y no hay exactamente N lienzos, el
        // mapa imagen↔ítem que usa `exporta_brightspace.py` —el k-ésimo
        // gráfico del bloque es `<bloque>_k.png`— está descuadrado, y una
        // pregunta viajaría con la figura de otra sin dar un solo error.
        if (b.declarados !== null && b.declarados !== b.encontrados) {
          problemas.push(`${b.bloque}: declara ${b.declarados} ítem(s) de tipo ` +
                         `\`grafico\` y hay ${b.encontrados} lienzo(s)`);
        }

        b.imagenes.forEach((img, k) => {
          const nombre = `${b.bloque}_${k + 1}.png`;
          const bytes = Buffer.from(img.dataURI.split(',')[1], 'base64');
          fs.writeFileSync(path.join(DESTINO, nombre), bytes);
          inventario.push({ archivo: nombre, bloque: b.bloque, orden: img.orden,
                            ancho: img.ancho, alto: img.alto, tinta: img.tinta,
                            bytes: bytes.length });
        });

        if (b.encontrados || b.declarados) {
          console.log(`  módulo ${modulo} · ${b.bloque}: ${b.imagenes.length} gráfico(s)` +
                      (b.declarados !== null ? ` de ${b.declarados} declarado(s)` : ''));
        }

        // La autoprueba se hace sobre el primer bloque que traiga gráficos:
        // se le quita uno del DOM y se exige que el recuento lo note.
        if (autoprueba && !descuadreDetectado && b.declarados > 1 && !b.bloque.startsWith('sim')) {  // eslint-disable-line
          console.log('  ' + await c.evalua(QUITA_UN_LIENZO(b.bloque)));
          const roto = (await c.evalua(RECUENTO)).find(x => x.bloque === b.bloque);
          if (roto && roto.declarados !== null && roto.declarados !== roto.encontrados) {
            descuadreDetectado = `${roto.bloque}: ${roto.declarados} declarados, ` +
                                 `${roto.encontrados} encontrados`;
          }
        }
      }
    }
    }
  } finally {
    proc.kill();
    // Chrome sigue escribiendo su perfil un instante después del kill: borrarlo
    // en ese momento da ENOTEMPTY y tumbaría una captura que ya está bien.
    await espera(500);
    try { fs.rmSync(perfil, { recursive: true, force: true }); } catch (e) { /* da igual */ }
  }

  fs.writeFileSync(path.join(DESTINO, 'inventario.json'),
                   JSON.stringify({ base: BASE, imagenes: inventario }, null, 2));

  if (autoprueba) {
    if (!descuadreDetectado) {
      console.error('\n  ✗ autoprueba: quité un lienzo y el guion no se quejó. ' +
                    'El recuento declarado-contra-encontrado NO protege nada.');
      process.exit(1);
    }
    console.log(`  ✓ autoprueba: el descuadre se detecta — ${descuadreDetectado}`);
  }

  console.log(`\n  ${inventario.length} PNG en ${path.relative(RAIZ, DESTINO)}/`);
  if (problemas.length) {
    console.error('\n  ✗ problemas:');
    problemas.forEach(p => console.error('      ' + p));
    process.exit(1);
  }
}

main().catch(e => { console.error('✗ ' + e.message); process.exit(1); });
