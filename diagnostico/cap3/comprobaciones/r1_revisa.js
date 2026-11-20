#!/usr/bin/env node
// R1 del capítulo 3 · revisión por HTTP de los módulos tocados, a 1200 y 375 px.
// Levanta su propio servidor, recorre los once módulos y mide: errores de consola, .katex-error,
// «$» sin renderizar, KaTeX dentro de <pre>, desbordamiento horizontal y, en el Módulo 9, que
// ninguna barra de los psi se salga del envolvente dibujado.
// Uso: node diagnostico/cap3/comprobaciones/r1_revisa.js > diagnostico/cap3/comprobaciones/r1_revisa.out
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const { Chrome, espera } = require('../diag/chrome');

const RAIZ = path.resolve(__dirname, '..', '..', '..');
const OUT = path.resolve(__dirname, '..', 'capturas', 'r1');
const PUERTO_HTTP = 8767, PUERTO_CDP = 9277;
const BASE = `http://127.0.0.1:${PUERTO_HTTP}/capitulo-3-modelos-ar-ma-arma.html`;

async function capturar(c, sel, archivo, indice = 0) {
  const rect = await c.evalua(`(() => { const el = document.querySelectorAll(${JSON.stringify(sel)})[${indice}];
    if (!el) return null; el.scrollIntoView({ behavior: 'instant', block: 'start' });
    const r = el.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height }; })()`);
  if (!rect) { console.log('   (sin elemento para ' + archivo + ')'); return; }
  await espera(1200);
  const r = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
    clip: { x: Math.max(0, rect.x - 6), y: Math.max(0, rect.y - 6), width: rect.w + 12, height: rect.h + 12, scale: 1 } });
  fs.writeFileSync(path.join(OUT, archivo), Buffer.from(r.data, 'base64'));
}

const MEDIR = `(() => {
  const m = document.getElementById('content-area') || document.querySelector('main');
  const sueltos = [];
  const w = document.createTreeWalker(m, NodeFilter.SHOW_TEXT);
  for (let n = w.nextNode(); n; n = w.nextNode()) {
    const p = n.parentElement; if (!p || p.closest('pre, code, script, style, .katex, textarea')) continue;
    if (/\\$[^$]/.test(n.textContent) || /\\\\(frac|phi|theta|rho|sqrt|sum)/.test(n.textContent)) sueltos.push(n.textContent.trim().slice(0, 80));
  }
  const anchos = [...m.querySelectorAll('table, pre, .katex-display, .formula, canvas, .note, .warning, .definition')]
    .filter(e => e.offsetParent !== null)
    .filter(e => { const r = e.getBoundingClientRect(); return r.right > innerWidth + 1 && !e.closest('pre') && getComputedStyle(e).overflowX === 'visible'
      && ![...(function*(){ let a = e.parentElement; while (a && a !== m) { yield a; a = a.parentElement; } })()].some(a => /auto|scroll|hidden/.test(getComputedStyle(a).overflowX)); })
    .map(e => e.tagName + '.' + e.className.toString().slice(0, 30));
  return { katexError: m.querySelectorAll('.katex-error').length, katex: m.querySelectorAll('.katex').length,
    katexEnPre: m.querySelectorAll('pre .katex').length, sueltos, pagina: document.documentElement.scrollWidth, ventana: innerWidth,
    seSalen: anchos, bloques: m.querySelectorAll('pre code').length, simuladores: m.querySelectorAll('[data-simulador]').length,
    graficos: [...m.querySelectorAll('canvas')].filter(cv => Chart.getChart(cv)).length, lienzos: m.querySelectorAll('canvas').length };
})()`;

const IMPULSO = `(() => {
  const raiz = document.querySelector('[data-simulador="manchas-impulso"]');
  const ch = Chart.getChart(raiz.querySelectorAll('canvas')[0]);
  const psi = ch.data.datasets[0].data, env = ch.data.datasets[1].data;
  const y = ch.scales.y;
  return { etiquetas: ch.data.datasets.map(d => d.label), n: psi.length,
    fueraDelEnvolvente: psi.filter((v, j) => Math.abs(v) > env[j] + 1e-12).length,
    fueraDeRj: psi.filter((v, j) => Math.abs(v) > env[j] / env[0] + 1e-12).length,
    env0: env[0], env1: env[1], ejeY: [y.min, y.max], envolventeDentroDelEje: env[0] <= y.max && -env[0] >= y.min,
    leyenda: ch.legend.legendItems.map(x => x.text),
    lectura: raiz.querySelector('.simulador-lectura').textContent.replace(/\\s+/g, ' ').trim() };
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
      await c.esperaHasta(`typeof loadModule === 'function' && typeof Chart !== 'undefined' && typeof DATOS_CAP3 !== 'undefined'`, 20000);
      await espera(1500);
      console.log(`\n===== ${modo.nombre} px =====`);
      for (let n = 1; n <= 11; n++) {
        c.contexto = `M${n} @${modo.nombre}`;
        await c.evalua(`loadModule(${n}), 'ok'`);
        await espera(1300);
        // abrir los paneles plegados (derivaciones, pistas y soluciones) para medirlos también
        await c.evalua(`(() => { document.querySelectorAll('#content-area [hidden]').forEach(e => { if (e.classList.contains('ejercicio-panel')) e.hidden = false; });
          document.querySelectorAll('#content-area details').forEach(d => d.open = true); return 1; })()`);
        await espera(300);
        const m = await c.evalua(MEDIR);
        const mal = m.katexError || m.katexEnPre || m.sueltos.length || m.pagina > m.ventana + 1 || m.seSalen.length;
        if (mal) fallos++;
        console.log(`M${String(n).padStart(2)}: katex ${m.katex} · katex-error ${m.katexError} · katex en <pre> ${m.katexEnPre} · «$» sueltos ${m.sueltos.length}` +
          ` · ancho de página ${m.pagina}/${m.ventana} · elementos que se salen ${m.seSalen.length} · bloques ${m.bloques} · simuladores ${m.simuladores}` +
          ` · gráficos ${m.graficos}/${m.lienzos}${mal ? '   <-- REVISAR ' + JSON.stringify({ s: m.sueltos, a: m.seSalen }) : ''}`);
        if (n === 9) {
          const im = await c.evalua(IMPULSO);
          console.log('   manchas-impulso:', JSON.stringify(im));
          if (im.fueraDelEnvolvente || !im.envolventeDentroDelEje) fallos++;
          await capturar(c, '[data-simulador="manchas-impulso"]', `m9-impulso-${modo.nombre}.png`);
          await capturar(c, '[data-simulador="manchas-transformada"]', `m9-transformada-${modo.nombre}.png`);
          const notas = await c.evalua(`[...document.querySelectorAll('#content-area .note, #content-area .warning')].map((e, i) => [i, e.textContent.trim().slice(0, 28)])`);
          for (const [i, t] of notas) {
            if (/Otra fórmula|De qué serie|Ojo con la media|Estas bandas|cuadrado\\?/.test(t)) {
              const sel = '#content-area .note, #content-area .warning';
              await capturar(c, sel, `m9-nota${i}-${modo.nombre}.png`, i);
            }
          }
        }
        if (n === 10) await capturar(c, '#c3e3-sol', `m10-ej3-solucion-${modo.nombre}.png`);
        if (n === 8) {
          const i = await c.evalua(`[...document.querySelectorAll('#content-area .warning')].findIndex(e => e.textContent.includes('la conclusión cambia'))`);
          await capturar(c, '#content-area .warning', `m8-residuales-${modo.nombre}.png`, i);
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
