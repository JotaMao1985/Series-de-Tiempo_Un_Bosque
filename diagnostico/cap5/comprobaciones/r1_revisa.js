#!/usr/bin/env node
// R1 del capítulo 5 · revisión por HTTP de los módulos, a 1200 y 375 px (adaptado del guion del cap. 4).
// Levanta su propio servidor (8765) y su Chrome sin ventana (CDP 9278), recorre los doce módulos y
// mide: errores de consola, .katex-error, «$» sin renderizar, KaTeX dentro de <pre> y desbordamiento
// horizontal, con los paneles plegados abiertos. Comprueba además las lecturas de dos simuladores que
// cambiaron (sobrediferenciación estacional, pesos ψ del airline y calendario) y guarda capturas de lo tocado.
// Uso: node diagnostico/cap5/comprobaciones/r1_revisa.js > diagnostico/cap5/comprobaciones/r1_revisa.out
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const { Chrome, espera } = require('../diag/chrome');

const RAIZ = path.resolve(__dirname, '..', '..', '..');
const OUT = path.resolve(__dirname, '..', 'capturas', 'r1');
const PUERTO_HTTP = 8765, PUERTO_CDP = 9278;
const BASE = `http://127.0.0.1:${PUERTO_HTTP}/capitulo-5-sarima.html`;

async function capturar(c, sel, archivo, indice = 0) {
  const rect = await c.evalua(`(() => { const el = document.querySelectorAll(${JSON.stringify(sel)})[${indice}];
    if (!el) return null; el.scrollIntoView({ behavior: 'instant', block: 'start' });
    const r = el.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height }; })()`);
  if (!rect) { console.log('   (sin elemento para ' + archivo + ')'); return; }
  await espera(1000);
  const r = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
    clip: { x: Math.max(0, rect.x - 6), y: Math.max(0, rect.y - 6), width: rect.w + 12, height: rect.h + 12, scale: 1 } });
  fs.writeFileSync(path.join(OUT, archivo), Buffer.from(r.data, 'base64'));
}

// índice del primer elemento de `sel` cuyo texto contiene `aguja`
const indice = (c, sel, aguja) => c.evalua(`[...document.querySelectorAll(${JSON.stringify(sel)})].findIndex(e => e.textContent.includes(${JSON.stringify(aguja)}))`);

const MEDIR = `(() => {
  const m = document.getElementById('content-area') || document.querySelector('main');
  const sueltos = [];
  const w = document.createTreeWalker(m, NodeFilter.SHOW_TEXT);
  for (let n = w.nextNode(); n; n = w.nextNode()) {
    const p = n.parentElement; if (!p || p.closest('pre, code, script, style, .katex, textarea')) continue;
    if (/\\$[^$]/.test(n.textContent) || /\\\\(frac|phi|theta|rho|sqrt|sum|hat|nabla)/.test(n.textContent)) sueltos.push(n.textContent.trim().slice(0, 80));
  }
  const anchos = [...m.querySelectorAll('table, pre, .katex-display, .formula, canvas, .note, .warning, .definition, .diagram')]
    .filter(e => e.offsetParent !== null)
    .filter(e => { const r = e.getBoundingClientRect(); return r.right > innerWidth + 1 && !e.closest('pre') && getComputedStyle(e).overflowX === 'visible'
      && ![...(function*(){ let a = e.parentElement; while (a && a !== m) { yield a; a = a.parentElement; } })()].some(a => /auto|scroll|hidden/.test(getComputedStyle(a).overflowX)); })
    .map(e => e.tagName + '.' + e.className.toString().slice(0, 30));
  return { katexError: m.querySelectorAll('.katex-error').length, katex: m.querySelectorAll('.katex').length,
    katexEnPre: m.querySelectorAll('pre .katex').length, sueltos, pagina: document.documentElement.scrollWidth, ventana: innerWidth,
    seSalen: anchos, bloques: m.querySelectorAll('pre code').length, simuladores: m.querySelectorAll('[data-simulador]').length,
    graficos: [...m.querySelectorAll('canvas')].filter(cv => Chart.getChart(cv)).length, lienzos: m.querySelectorAll('canvas').length };
})()`;

const LECTURA = sim => `(() => { const r = document.querySelector('[data-simulador="${sim}"]');
  return r ? r.querySelector('.simulador-lectura').textContent.replace(/\\s+/g, ' ').trim() : null; })()`;

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const srv = spawn('python3', ['-m', 'http.server', String(PUERTO_HTTP), '--bind', '127.0.0.1', '--directory', path.join(RAIZ, 'Htmls_Series')], { stdio: 'ignore' });
  await espera(1200);
  const c = await Chrome.lanzar(PUERTO_CDP);
  let fallos = 0;
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable'); await c.enviar('Log.enable');
    for (const modo of [{ nombre: '1200', width: 1200, height: 1000, dsf: 1, mobile: false }, { nombre: '375', width: 375, height: 812, dsf: 2, mobile: true }]) {
      await c.enviar('Emulation.setDeviceMetricsOverride', { width: modo.width, height: modo.height, deviceScaleFactor: modo.dsf, mobile: modo.mobile });
      c.contexto = 'carga ' + modo.nombre;
      await c.enviar('Page.navigate', { url: BASE });
      await c.esperaHasta(`typeof loadModule === 'function' && typeof Chart !== 'undefined' && typeof DATOS_CAP5 !== 'undefined'`, 20000);
      await espera(1500);
      console.log(`\n===== ${modo.nombre} px =====`);
      for (let n = 1; n <= 12; n++) {
        c.contexto = `M${n} @${modo.nombre}`;
        await c.evalua(`loadModule(${n}), 'ok'`);
        await espera(1300);
        // abrir los paneles plegados (derivaciones, pistas y soluciones) para medirlos también
        await c.evalua(`(() => { document.querySelectorAll('#content-area .ejercicio-panel[hidden], #content-area .derivacion-panel[hidden]').forEach(e => e.hidden = false);
          document.querySelectorAll('#content-area details').forEach(d => d.open = true); return 1; })()`);
        await espera(400);
        const m = await c.evalua(MEDIR);
        const mal = m.katexError || m.katexEnPre || m.sueltos.length || m.pagina > m.ventana + 1 || m.seSalen.length;
        if (mal) fallos++;
        console.log(`M${String(n).padStart(2)}: katex ${m.katex} · katex-error ${m.katexError} · katex en <pre> ${m.katexEnPre} · «$» sueltos ${m.sueltos.length}` +
          ` · ancho de página ${m.pagina}/${m.ventana} · elementos que se salen ${m.seSalen.length} · bloques ${m.bloques} · simuladores ${m.simuladores}` +
          ` · gráficos ${m.graficos}/${m.lienzos}${mal ? '   <-- REVISAR ' + JSON.stringify({ s: m.sueltos, a: m.seSalen }) : ''}`);
        const v = modo.nombre;
        const desliza = (sim, k, valor) => c.evalua(`(() => { const i = document.querySelectorAll('[data-simulador="${sim}"] input[type=range]')[${k}];
          i.value = ${valor}; i.dispatchEvent(new Event('input', { bubbles: true })); return 1; })()`);
        const interruptor = (sim, k, on) => c.evalua(`(() => { const i = document.querySelectorAll('[data-simulador="${sim}"] input[type=checkbox]')[${k}];
          if (i.checked !== ${on}) i.click(); return i.checked; })()`);
        if (n === 1) await capturar(c, '[data-simulador="mapa-firma"] .simulador-intro', `m1-intro-${v}.png`);
        if (n === 2) await capturar(c, '#content-area p', `m2-regalo-${v}.png`, await indice(c, '#content-area p', 'La ACF pide algo más'));
        if (n === 3) {
          await capturar(c, '#content-area p', `m3-varianza-${v}.png`, await indice(c, '#content-area p', 'no decide'));
          await capturar(c, '#content-area .diagram', `m3-sobredif-tabla-${v}.png`, await indice(c, '#content-area .diagram', 'Distancia a'));
          for (const d of [0, 1, 2]) {
            await desliza('sobrediferenciacion-estacional', 0, d); await espera(500);
            console.log(`   sobrediferenciacion-estacional D = ${d}:`, await c.evalua(LECTURA('sobrediferenciacion-estacional')));
          }
          await capturar(c, '[data-simulador="sobrediferenciacion-estacional"]', `m3-simulador-D2-${v}.png`);
        }
        if (n === 4) await capturar(c, '#content-area p', `m4-producto-${v}.png`, await indice(c, '#content-area p', 'dos millonésimas'));
        if (n === 5) {
          console.log('   airline-pesos (inicial):', await c.evalua(LECTURA('airline-pesos')));
          await capturar(c, '[data-simulador="airline-pesos"]', `m5-simulador-inicial-${v}.png`);
          for (const T of [0, -0.95]) {
            await desliza('airline-pesos', 1, T); await espera(500);
            console.log(`   airline-pesos Θ = ${T}:`, await c.evalua(LECTURA('airline-pesos')));
          }
          await capturar(c, '#content-area p', `m5-largo-plazo-${v}.png`, await indice(c, '#content-area p', 'no aguanta a largo plazo'));
          await capturar(c, '#content-area .derivacion-resultado', `m5-derivacion-${v}.png`);
        }
        if (n === 6) await capturar(c, '#content-area p', `m6-bic-${v}.png`, await indice(c, '#content-area p', 'castiga más cada parámetro'));
        if (n === 7) {
          await capturar(c, '#content-area .diagram', `m7-etapas-${v}.png`);
          await capturar(c, '#content-area p', `m7-invertibilidad-${v}.png`, await indice(c, '#content-area p', 'se lee en $') >= 0 ? await indice(c, '#content-area p', 'se lee en $') : await indice(c, '#content-area p', 'La invertibilidad, y con ella'));
        }
        if (n === 8) {
          await capturar(c, '#content-area .diagram', `m8-trm-${v}.png`, await indice(c, '#content-area .diagram', 'Ajuste forzado'));
          await capturar(c, '#content-area .note', `m8-arbitraje-${v}.png`, await indice(c, '#content-area .note', 'arbitraje'));
        }
        if (n === 9) {
          console.log('   calendario (inicial, días):', await c.evalua(LECTURA('calendario-regresores')));
          await interruptor('calendario-regresores', 0, false); await interruptor('calendario-regresores', 1, true); await espera(600);
          console.log('   calendario (solo Semana Santa):', await c.evalua(LECTURA('calendario-regresores')));
          await capturar(c, '[data-simulador="calendario-regresores"]', `m9-solo-pascua-${v}.png`);
          await interruptor('calendario-regresores', 0, true); await espera(600);
          console.log('   calendario (días + Semana Santa):', await c.evalua(LECTURA('calendario-regresores')));
        }
        if (n === 10) await capturar(c, '#content-area p', `m10-365-${v}.png`, await indice(c, '#content-area p', 'ensayar un'));
        if (n === 11) {
          await capturar(c, '#content-area p', `m11-fuga-${v}.png`, await indice(c, '#content-area p', 'ventaja indebida'));
          // a 375 px y escala 2 las soluciones son demasiado altas para una captura: solo a 1200
          if (v === '1200') { await capturar(c, '#c5e1-sol', `m11-ej1-solucion-${v}.png`); await capturar(c, '#c5e3-sol', `m11-ej3-solucion-${v}.png`); }
        }
        if (n === 12) await capturar(c, '#content-area', `m${n}-${v}.png`);   // el M11 entero es demasiado alto para una captura
      }
    }
    console.log('\n===== consola =====');
    const ev = c.eventos.filter(e => !/favicon/.test(e.txt));
    console.log(ev.length ? ev.map(e => `[${e.cuando}] ${e.txt}`).join('\n') : 'sin errores ni avisos de consola');
    if (ev.length) fallos++;
    console.log(`\n${fallos ? 'HAY ' + fallos + ' COSAS QUE REVISAR' : 'TODO EN ORDEN'}`);
  } finally {
    await c.cerrar(); srv.kill();
  }
  process.exit(fallos ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
