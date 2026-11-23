#!/usr/bin/env node
// R3 del capítulo 4 · revisión por HTTP de los módulos, a 1200 y 375 px.
// Levanta su propio servidor (8764) y su Chrome sin ventana (CDP 9277), recorre los doce módulos y mide:
// errores de consola, .katex-error, «$» sin renderizar, KaTeX dentro de <pre>, desbordamiento horizontal
// y que cada lienzo de simulador tenga su gráfico, con los paneles plegados abiertos. Comprueba además el
// orden de los <h3> del Módulo 10, los minutos de la barra lateral y el cambio de pestaña R/Python del
// bloque nuevo del puente, y guarda capturas de lo tocado (diagnostico/cap4/capturas/r3/, ignorada por git).
// Uso: node diagnostico/cap4/comprobaciones/r3_revisa.js > diagnostico/cap4/comprobaciones/r3_revisa.out
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const { Chrome, espera } = require('../diag/chrome');

const RAIZ = path.resolve(__dirname, '..', '..', '..');
const OUT = path.resolve(__dirname, '..', 'capturas', 'r3');
const PUERTO_HTTP = 8764, PUERTO_CDP = 9277;
const BASE = `http://127.0.0.1:${PUERTO_HTTP}/capitulo-4-modelos-arima.html`;

async function capturar(c, sel, archivo, indice = 0) {
  const rect = await c.evalua(`(() => { const el = document.querySelectorAll(${JSON.stringify(sel)})[${indice}];
    if (!el) return null; el.scrollIntoView({ behavior: 'instant', block: 'start' });
    const r = el.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height }; })()`);
  if (!rect) { console.log('   (sin elemento para ' + archivo + ')'); return; }
  await espera(900);
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
  const pintados = [...m.querySelectorAll('canvas')].filter(cv => Chart.getChart(cv));
  const sinPintar = [...m.querySelectorAll('[data-simulador] canvas')].filter(cv => !Chart.getChart(cv)).length;
  return { katexError: m.querySelectorAll('.katex-error').length, katex: m.querySelectorAll('.katex').length,
    katexEnPre: m.querySelectorAll('pre .katex').length, sueltos, pagina: document.documentElement.scrollWidth, ventana: innerWidth,
    seSalen: anchos, bloques: m.querySelectorAll('pre code').length, simuladores: m.querySelectorAll('[data-simulador]').length,
    graficos: pintados.length, lienzos: m.querySelectorAll('canvas').length, sinPintar,
    h3: [...m.querySelectorAll('h3')].map(h => h.textContent.replace(/\\s+/g, ' ').trim()) };
})()`;

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
      console.log('typeof tailwind (debe ser undefined: la hoja va compilada):', await c.evalua(`typeof tailwind`));
      console.log('minutos de la barra lateral:', await c.evalua(`courseData.modules.map(m => m.id + ':' + m.duration).join(' · ')`));
      for (let n = 1; n <= 12; n++) {
        c.contexto = `M${n} @${modo.nombre}`;
        await c.evalua(`loadModule(${n}), 'ok'`);
        await espera(1300);
        // abrir los paneles plegados (derivaciones, pistas y soluciones) para medirlos también
        await c.evalua(`(() => { document.querySelectorAll('#content-area .ejercicio-panel[hidden], #content-area .derivacion-panel[hidden]').forEach(e => e.hidden = false);
          document.querySelectorAll('#content-area details').forEach(d => d.open = true); return 1; })()`);
        await espera(400);
        const m = await c.evalua(MEDIR);
        const mal = m.katexError || m.katexEnPre || m.sueltos.length || m.pagina > m.ventana + 1 || m.seSalen.length || m.sinPintar;
        if (mal) fallos++;
        console.log(`M${String(n).padStart(2)}: katex ${m.katex} · katex-error ${m.katexError} · katex en <pre> ${m.katexEnPre} · «$» sueltos ${m.sueltos.length}` +
          ` · ancho de página ${m.pagina}/${m.ventana} · elementos que se salen ${m.seSalen.length} · bloques ${m.bloques} · simuladores ${m.simuladores}` +
          ` · gráficos ${m.graficos}/${m.lienzos} (simuladores sin pintar: ${m.sinPintar})${mal ? '   <-- REVISAR ' + JSON.stringify({ s: m.sueltos, a: m.seSalen }) : ''}`);
        if (n === 10) console.log('   h3 del M10, en orden:\n     · ' + m.h3.join('\n     · '));
        const v = modo.nombre;
        if (n === 1) {
          await capturar(c, '#content-area h3', `m1-casos-${v}.png`, await indice(c, '#content-area h3', 'Casos particulares'));
          await capturar(c, '#content-area .code-tabs', `m1-bloque-${v}.png`);
        }
        if (n === 3) {
          await capturar(c, '#content-area .diagram', `m3-evidencias-${v}.png`);
          await capturar(c, '[data-simulador="escalon-vs-raiz"] .simulador-intro', `m3-intro-${v}.png`);
          await capturar(c, '#content-area .code-tabs', `m3-bloque-${v}.png`);
        }
        if (n === 4) {
          await capturar(c, '[data-simulador="identificacion-nilo"] .simulador-intro', `m4-intro-${v}.png`);
          await capturar(c, '#content-area .note', `m4-nota-${v}.png`);
        }
        if (n === 5) await capturar(c, '#content-area .definition', `m5-regla-${v}.png`);
        if (n === 6) {
          await capturar(c, '[data-simulador="explorador-modelos"] .simulador-intro', `m6-intro-${v}.png`);
          await capturar(c, '#content-area .note', `m6-nota-${v}.png`, await indice(c, '#content-area .note', 'Lo que enseña el explorador'));
          await capturar(c, '#content-area .formula', `m6-formula-${v}.png`);
        }
        if (n === 10) {
          await capturar(c, '#content-area .diagram', `m10-nilo-${v}.png`);
          const iPuente = await indice(c, '#content-area .code-tabs', 'auto.arima(lap');
          await capturar(c, '#content-area .code-tabs', `m10-puente-r-${v}.png`, iPuente);
          await c.evalua(`(() => { const t = document.querySelectorAll('#content-area .code-tabs')[${iPuente}];
            t.querySelector('.code-tab-btn[data-lang="python"]').click(); return 1; })()`);
          await espera(500);
          console.log('   pestaña Python del puente visible:', await c.evalua(`(() => { const t = document.querySelectorAll('#content-area .code-tabs')[${iPuente}];
            const p = t.querySelector('.code-tab-panel[data-lang="python"]'); const r = t.querySelector('.code-tab-panel[data-lang="r"]'); return !p.hidden && r.hidden; })()`));
          await capturar(c, '#content-area .code-tabs', `m10-puente-py-${v}.png`, iPuente);
          await capturar(c, '#content-area p', `m10-cobertura-${v}.png`, await indice(c, '#content-area p', 'los dos intervalos se cumplen'));
          await capturar(c, '#content-area .note', `m10-resultado-${v}.png`, await indice(c, '#content-area .note', 'aceptado tal cual'));
        }
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
