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
// Sale: <destino>/<bloque>_<n>.png, uno por ítem de tipo `grafico`, más
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
const DESTINO = path.resolve(RAIZ, arg('--destino', 'precalculo/salidas/graficos_preparcial'));
const PAGINA = 'preparcial-corte-1.html';
const PUERTO = 9223;
const ANCHO = 1440, ALTO = 1100;

// Dónde vive cada quiz. El bloque es la clave con la que `exporta_brightspace.py`
// nombra los ítems, así que los PNG salen con ese mismo nombre y no hace falta
// un segundo convenio para casarlos.
const OBJETIVOS = [
  { modulo: 2, bloque: 'bloque-a' },
  { modulo: 3, bloque: 'bloque-b' },
  { modulo: 4, bloque: 'bloque-c' },
  { modulo: 5, bloque: 'bloque-d' },
  { modulo: 7, bloque: 'simulacro', arranca: true },
];

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

const captura = bloque => `
  (() => {
    if (window.innerWidth < 1024) {
      return { error: 'innerWidth = ' + window.innerWidth + ', hacen falta 1024 o más' };
    }
    const raiz = document.querySelector('main') || document.body;
    const lienzos = [...raiz.querySelectorAll('.quiz-grafico canvas')];
    const imagenes = [], problemas = [];

    lienzos.forEach((canvas, k) => {
      const w = canvas.width, h = canvas.height;
      if (!w || !h) { problemas.push('lienzo ' + k + ': ' + w + '×' + h); return; }

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
      if (pct < 1) problemas.push('lienzo ' + k + ': solo ' + pct.toFixed(2) + ' % con tinta');

      imagenes.push({ orden: k, ancho: w, alto: h, tinta: Number(pct.toFixed(2)),
                      dataURI: plano.toDataURL('image/png') });
    });

    return { bloque: ${JSON.stringify(bloque)}, innerWidth: window.innerWidth,
             lienzos: lienzos.length, problemas, imagenes };
  })()`;

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
  try {
    const c = await Chrome.abrir(PUERTO);
    await c.enviar('Page.enable');
    await c.enviar('Runtime.enable');

    const url = BASE.replace(/\/$/, '') + '/' + PAGINA;
    await c.enviar('Page.navigate', { url });
    // El documento monta los módulos en cuanto corre su script; medio segundo
    // basta y no hay evento mejor: `loadEventFired` llega antes de que el
    // módulo 1 esté pintado.
    await espera(1500);
    console.log('  ' + await c.evalua(SIN_ANIMACION));

    for (const { modulo, bloque, arranca } of OBJETIVOS) {
      await c.evalua(`loadModule(${modulo}), 'ok'`);
      await espera(1200);
      if (arranca) {
        console.log('  ' + await c.evalua(ARRANCA_SIMULACRO));
        await espera(1200);
      }
      const r = await c.evalua(captura(bloque));
      if (r.error) { problemas.push(`${bloque}: ${r.error}`); continue; }
      problemas = problemas.concat((r.problemas || []).map(p => `${bloque}: ${p}`));

      r.imagenes.forEach((img, k) => {
        const nombre = `${bloque}_${k + 1}.png`;
        const bytes = Buffer.from(img.dataURI.split(',')[1], 'base64');
        fs.writeFileSync(path.join(DESTINO, nombre), bytes);
        inventario.push({ archivo: nombre, bloque, orden: img.orden,
                          ancho: img.ancho, alto: img.alto, tinta: img.tinta,
                          bytes: bytes.length });
      });
      console.log(`  ${bloque}: ${r.imagenes.length} gráfico(s) · innerWidth ${r.innerWidth}`);
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

  console.log(`\n  ${inventario.length} PNG en ${path.relative(RAIZ, DESTINO)}/`);
  if (problemas.length) {
    console.error('\n  ✗ problemas:');
    problemas.forEach(p => console.error('      ' + p));
    process.exit(1);
  }
}

main().catch(e => { console.error('✗ ' + e.message); process.exit(1); });
