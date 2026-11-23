#!/usr/bin/env node
// V3 · verificación visual independiente de la R3 del capítulo 4, por HTTP, a 1200 y 375 px.
// Servidor propio en 8771 (python3 -m http.server sobre Htmls_Series) y Chrome sin ventana por CDP en 9301; ambos se cierran al final.
// Recorre los doce módulos con derivaciones, pistas y soluciones abiertas y mide: errores/avisos de consola, .katex-error, «$» sin
// componer, KaTeX dentro de <pre>, desbordamiento horizontal, simuladores sin pintar y con la lectura vacía, que cada par de pestañas
// R/Python cambie de verdad, que los recuadros nuevos existan y se vean, y los minutos de la barra lateral. Capturas en
// diagnostico/cap4/capturas/v3/ (ignorada por git).
// Uso: node diagnostico/cap4/comprobaciones/v3_revisa.js > diagnostico/cap4/comprobaciones/v3_revisa.out
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const { Chrome, espera } = require('../diag/chrome');

const RAIZ = path.resolve(__dirname, '..', '..', '..');
const OUT = path.resolve(__dirname, '..', 'capturas', 'v3');
const PUERTO_HTTP = 8771, PUERTO_CDP = 9301;
const BASE = `http://127.0.0.1:${PUERTO_HTTP}/capitulo-4-modelos-arima.html`;

async function capturar(c, sel, archivo, indice = 0) {
  const rect = await c.evalua(`(() => { const el = document.querySelectorAll(${JSON.stringify(sel)})[${indice}];
    if (!el) return null; el.scrollIntoView({ behavior: 'instant', block: 'start' });
    const r = el.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height }; })()`);
  if (!rect) { console.log('   (sin elemento para ' + archivo + ')'); return; }
  await espera(900);
  const r = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
    clip: { x: Math.max(0, rect.x - 6), y: Math.max(0, rect.y - 6), width: rect.w + 12, height: Math.min(rect.h + 12, 2400), scale: 1 } });
  fs.writeFileSync(path.join(OUT, archivo), Buffer.from(r.data, 'base64'));
}
const indice = (c, sel, aguja) => c.evalua(`[...document.querySelectorAll(${JSON.stringify(sel)})].findIndex(e => e.textContent.includes(${JSON.stringify(aguja)}))`);

const MEDIR = `(() => {
  const m = document.getElementById('content-area');
  const sueltos = [];
  const w = document.createTreeWalker(m, NodeFilter.SHOW_TEXT);
  for (let n = w.nextNode(); n; n = w.nextNode()) {
    const p = n.parentElement; if (!p || p.closest('pre, code, script, style, .katex, textarea')) continue;
    if (/\\$[^$]/.test(n.textContent) || /\\\\(frac|phi|theta|rho|sqrt|sum|hat|nabla|beta|alpha)/.test(n.textContent)) sueltos.push(n.textContent.trim().slice(0, 80));
  }
  const padres = e => { const r = []; let a = e.parentElement; while (a && a !== m) { r.push(a); a = a.parentElement; } return r; };
  const seSalen = [...m.querySelectorAll('table, pre, .katex-display, .formula, canvas, .note, .warning, .definition, .diagram, p, ul')]
    .filter(e => e.offsetParent !== null && !e.closest('pre'))
    .filter(e => e.getBoundingClientRect().right > innerWidth + 1 && getComputedStyle(e).overflowX === 'visible'
      && !padres(e).some(a => /auto|scroll|hidden/.test(getComputedStyle(a).overflowX)))
    .map(e => e.tagName + '.' + e.className.toString().slice(0, 30));
  const simSinPintar = [...m.querySelectorAll('[data-simulador] canvas')].filter(cv => !Chart.getChart(cv)).length;
  const lecturaVacia = [...m.querySelectorAll('[data-simulador] .simulador-lectura')].filter(l => l.textContent.trim().length < 3).length;
  const tabs = [...m.querySelectorAll('.code-tabs')];
  return { katexError: m.querySelectorAll('.katex-error').length, katex: m.querySelectorAll('.katex').length,
    katexEnPre: m.querySelectorAll('pre .katex').length, sueltos, pagina: document.documentElement.scrollWidth, ventana: innerWidth,
    seSalen, bloques: m.querySelectorAll('pre code').length, simuladores: m.querySelectorAll('[data-simulador]').length,
    graficos: [...m.querySelectorAll('canvas')].filter(cv => Chart.getChart(cv)).length, lienzos: m.querySelectorAll('canvas').length, simSinPintar, lecturaVacia,
    tabs: tabs.length, h3: [...m.querySelectorAll('h3')].map(h => h.textContent.replace(/\\s+/g, ' ').trim()) };
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
      console.log('typeof tailwind (debe ser undefined):', await c.evalua(`typeof tailwind`));
      console.log('courseData:', await c.evalua(`courseData.modules.map(m => m.id + ':' + m.duration).join(' · ')`));
      console.log('barra lateral (texto de los enlaces):', await c.evalua(`[...document.querySelectorAll('#sidebar a, nav a, #module-list *')].map(e => e.textContent.replace(/\\s+/g, ' ').trim()).filter(t => /min/.test(t)).filter((t, i, a) => a.indexOf(t) === i).slice(0, 14).join(' | ')`));
      for (let n = 1; n <= 12; n++) {
        c.contexto = `M${n} @${modo.nombre}`;
        await c.evalua(`loadModule(${n}), 'ok'`);
        await espera(1300);
        await c.evalua(`(() => { document.querySelectorAll('#content-area .ejercicio-panel[hidden], #content-area .derivacion-panel[hidden]').forEach(e => e.hidden = false);
          document.querySelectorAll('#content-area details').forEach(d => d.open = true); return 1; })()`);
        await espera(400);
        const m = await c.evalua(MEDIR);
        const mal = m.katexError || m.katexEnPre || m.sueltos.length || m.pagina > m.ventana + 1 || m.seSalen.length || m.simSinPintar || m.lecturaVacia;
        if (mal) fallos++;
        console.log(`M${String(n).padStart(2)}: katex ${m.katex} · katex-error ${m.katexError} · katex en <pre> ${m.katexEnPre} · «$» sueltos ${m.sueltos.length}` +
          ` · ancho ${m.pagina}/${m.ventana} · se salen ${m.seSalen.length} · bloques ${m.bloques} · pares de pestañas ${m.tabs} · simuladores ${m.simuladores}` +
          ` · gráficos ${m.graficos}/${m.lienzos} (sin pintar ${m.simSinPintar}; lectura vacía ${m.lecturaVacia})${mal ? '   <-- REVISAR ' + JSON.stringify({ s: m.sueltos, a: m.seSalen }) : ''}`);
        if (n === 1 || n === 3 || n === 10) console.log('   h3 de M' + n + ': ' + m.h3.join(' · '));
        // cada par de pestañas: clic en Python, comprobar; clic en R, comprobar
        const resTabs = await c.evalua(`(async () => { const out = []; const espera = ms => new Promise(r => setTimeout(r, ms));
          for (const t of document.querySelectorAll('#content-area .code-tabs')) {
            const bp = t.querySelector('.code-tab-btn[data-lang="python"]'), br = t.querySelector('.code-tab-btn[data-lang="r"]');
            bp.click(); await espera(60);
            const py = !t.querySelector('.code-tab-panel[data-lang="python"]').hidden && t.querySelector('.code-tab-panel[data-lang="r"]').hidden;
            const pyTxt = t.querySelector('.code-tab-panel[data-lang="python"] code').textContent.length;
            br.click(); await espera(60);
            const r = !t.querySelector('.code-tab-panel[data-lang="r"]').hidden && t.querySelector('.code-tab-panel[data-lang="python"]').hidden;
            out.push([t.querySelector('.code-tabs-nav').getAttribute('aria-label'), py, r, pyTxt, !!t.querySelector('.code-tab-panel[data-lang="python"] .token, .code-tab-panel[data-lang="python"] code[class*="language"]')]);
          } return out; })()`);
        const malTabs = resTabs.filter(x => !x[1] || !x[2]);
        if (malTabs.length) { fallos++; }
        console.log(`   pestañas R/Python: ${resTabs.length} pares, cambian bien ${resTabs.length - malTabs.length}${malTabs.length ? '   <-- FALLAN ' + JSON.stringify(malTabs) : ''}`);
        const v = modo.nombre;
        if (n === 1) {
          await capturar(c, '#content-area h3', `m1-casos-${v}.png`, await indice(c, '#content-area h3', 'Casos particulares'));
          await capturar(c, '#content-area .code-tabs', `m1-bloque-${v}.png`);
        }
        if (n === 3) {
          await capturar(c, '#content-area .diagram', `m3-evidencias-${v}.png`);
          await capturar(c, '#content-area .warning', `m3-ndiffs-${v}.png`, await indice(c, '#content-area .warning', 'tres respuestas'));
          await capturar(c, '[data-simulador="escalon-vs-raiz"] .simulador-intro', `m3-intro-${v}.png`);
          await capturar(c, '#content-area .code-tabs', `m3-bloque-${v}.png`);
        }
        if (n === 4) {
          await capturar(c, '[data-simulador="identificacion-nilo"]', `m4-simulador-${v}.png`);
          await capturar(c, '#content-area .note', `m4-nota-${v}.png`);
        }
        if (n === 6) {
          await capturar(c, '[data-simulador="explorador-modelos"] .simulador-intro', `m6-intro-${v}.png`);
          await capturar(c, '#content-area .note', `m6-nota-${v}.png`, await indice(c, '#content-area .note', 'Lo que enseña el explorador'));
          await capturar(c, '#content-area .formula', `m6-formula-${v}.png`);
        }
        if (n === 10) {
          await capturar(c, '#content-area .diagram', `m10-nilo-${v}.png`);
          const iPuente = await indice(c, '#content-area .code-tabs', 'auto.arima(lap');
          await capturar(c, '#content-area .code-tabs', `m10-puente-r-${v}.png`, iPuente);
          await c.evalua(`document.querySelectorAll('#content-area .code-tabs')[${iPuente}].querySelector('.code-tab-btn[data-lang="python"]').click(), 1`);
          await espera(500);
          await capturar(c, '#content-area .code-tabs', `m10-puente-py-${v}.png`, iPuente);
          await capturar(c, '#content-area .note', `m10-resultado-${v}.png`, await indice(c, '#content-area .note', 'aceptado tal cual'));
          await capturar(c, '#content-area .definition', `m10-resumen-${v}.png`, await indice(c, '#content-area .definition', 'Lo que hay que llevarse'));
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
