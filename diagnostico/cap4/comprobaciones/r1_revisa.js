#!/usr/bin/env node
// R1 del capítulo 4 · revisión por HTTP de los módulos, a 1200 y 375 px.
// Levanta su propio servidor (8763) y su Chrome sin ventana (CDP 9276), recorre los doce módulos y
// mide: errores de consola, .katex-error, «$» sin renderizar, KaTeX dentro de <pre> y desbordamiento
// horizontal, con los paneles plegados abiertos. Comprueba además las lecturas de dos simuladores que
// cambiaron (la forma del pronóstico y la sobrediferenciación) y guarda capturas de lo tocado.
// Uso: node diagnostico/cap4/comprobaciones/r1_revisa.js > diagnostico/cap4/comprobaciones/r1_revisa.out
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const { Chrome, espera } = require('../diag/chrome');

const RAIZ = path.resolve(__dirname, '..', '..', '..');
const OUT = path.resolve(__dirname, '..', 'capturas', 'r1');
const PUERTO_HTTP = 8763, PUERTO_CDP = 9276;
const BASE = `http://127.0.0.1:${PUERTO_HTTP}/capitulo-4-modelos-arima.html`;

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
      await c.esperaHasta(`typeof loadModule === 'function' && typeof Chart !== 'undefined' && typeof DATOS_CAP4 !== 'undefined'`, 20000);
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
        if (n === 1) await capturar(c, '[data-simulador="nilo-y-diferencia"] .simulador-intro', `m1-intro-${v}.png`);
        if (n === 2) await capturar(c, '#ciclo-box-jenkins-estimacion', `m2-estimacion-${v}.png`);
        if (n === 3) {
          await capturar(c, '#content-area .diagram', `m3-evidencias-${v}.png`);
          await capturar(c, '#content-area p', `m3-varianza-${v}.png`, await indice(c, '#content-area p', '¿Y la varianza'));
        }
        if (n === 5) await capturar(c, '#content-area p', `m5-deriva-${v}.png`, await indice(c, '#content-area p', 'modelo con deriva, que no es'));
        if (n === 7) await capturar(c, '#content-area .definition', `m7-algoritmo-${v}.png`);
        if (n === 8) {
          await capturar(c, '#content-area .diagram', `m8-tabla-${v}.png`);
          await capturar(c, '#content-area .warning', `m8-varianza-${v}.png`, await indice(c, '#content-area .warning', 'no es una evidencia aparte'));
          for (const d of [1, 2]) {
            await c.evalua(`(() => { const i = document.querySelector('[data-simulador="sobrediferenciacion"] input[type=range]');
              i.value = ${d}; i.dispatchEvent(new Event('input', { bubbles: true })); return 1; })()`);
            await espera(500);
            console.log(`   sobrediferenciacion d = ${d}:`, await c.evalua(LECTURA('sobrediferenciacion')));
          }
        }
        if (n === 9) {
          await capturar(c, '#content-area .diagram', `m9-formas-${v}.png`);
          await capturar(c, '#content-area .formula', `m9-limite-${v}.png`, await indice(c, '#content-area .formula', 'T+\\infty'));
          console.log('   forma-pronostico (d1):', await c.evalua(LECTURA('forma-pronostico')));
          console.log('   selector:', await c.evalua(`[...document.querySelectorAll('[data-simulador="forma-pronostico"] option')].map(o => o.textContent).join(' | ')`));
        }
        if (n === 10) {
          await capturar(c, '#content-area .diagram', `m10-nilo-${v}.png`);
          await capturar(c, '#content-area p', `m10-cobertura-${v}.png`, await indice(c, '#content-area p', 'contando juntos'));
          await capturar(c, '#c4e2-sol', `m10-ej2-solucion-${v}.png`);
          await capturar(c, '#c4e3-pista', `m10-ej3-pista-${v}.png`);
        }
        if (n === 11 || n === 12) await capturar(c, '#content-area', `m${n}-${v}.png`);
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
