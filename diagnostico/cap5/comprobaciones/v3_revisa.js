#!/usr/bin/env node
// V3 (verificador de la R3 del cap. 5) · revision por HTTP a 1200 y 375 px. Servidor propio en 8769 y Chrome sin
// ventana por CDP en 9281 (los cierra al acabar). Capturas solo en diagnostico/cap5/capturas/v3/.
// Uso: node diagnostico/cap5/comprobaciones/v3_revisa.js > diagnostico/cap5/comprobaciones/v3_revisa.out
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const { Chrome, espera } = require('../diag/chrome');
const RAIZ = path.resolve(__dirname, '..', '..', '..');
const OUT = path.resolve(__dirname, '..', 'capturas', 'v3');
const BASE = 'http://127.0.0.1:8769/capitulo-5-sarima.html';
async function capturar(c, expr, archivo) {
  const rect = await c.evalua(`(() => { const el = ${expr}; if (!el) return null; el.scrollIntoView({ block: 'start' });
    const r = el.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height }; })()`);
  if (!rect) { console.log('   (sin elemento para ' + archivo + ')'); return; }
  await espera(700);
  const r = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
    clip: { x: Math.max(0, rect.x - 6), y: Math.max(0, rect.y - 6), width: rect.w + 12, height: Math.min(rect.h + 12, 3000), scale: 1 } });
  fs.writeFileSync(path.join(OUT, archivo), Buffer.from(r.data, 'base64'));
}
const pTexto = aguja => `[...document.querySelectorAll('#content-area p, #content-area .warning, #content-area .note')].find(e => e.textContent.includes(${JSON.stringify(aguja)}))`;
const LECT = s => `(() => { const r = document.querySelector('[data-simulador="${s}"] .simulador-lectura'); return r ? r.textContent.replace(/\\s+/g,' ').trim() : null; })()`;
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const srv = spawn('python3', ['-m', 'http.server', '8769', '--bind', '127.0.0.1', '--directory', path.join(RAIZ, 'Htmls_Series')], { stdio: 'ignore' });
  await espera(1200);
  const c = await Chrome.lanzar(9281);
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable'); await c.enviar('Log.enable');
    for (const modo of [{ n: '1200', w: 1200, h: 1000, d: 1, m: false }, { n: '375', w: 375, h: 812, d: 2, m: true }]) {
      await c.enviar('Emulation.setDeviceMetricsOverride', { width: modo.w, height: modo.h, deviceScaleFactor: modo.d, mobile: modo.m });
      c.contexto = 'carga ' + modo.n;
      await c.enviar('Page.navigate', { url: BASE });
      await c.esperaHasta(`typeof loadModule === 'function' && typeof Chart !== 'undefined' && typeof DATOS_CAP5 !== 'undefined'`, 20000);
      await espera(1500);
      console.log(`\n===== ${modo.n} px =====`);
      for (let n = 1; n <= 12; n++) {
        c.contexto = `M${n} @${modo.n}`;
        await c.evalua(`loadModule(${n}), 'ok'`); await espera(1200);
        const k = await c.evalua(`(() => { const a = document.getElementById('content-area');
          const anot = [...a.querySelectorAll('annotation')].map(x => x.textContent);
          const malas = anot.filter(t => /\\t|[\\x00-\\x08\\x0b\\x0c]/.test(t) || /(^|[^\\\\a-z])ext\\{/.test(t));
          const vis = [...a.querySelectorAll('.katex')].map(x => x.textContent).filter(t => /extAir|ext\\{/.test(t));
          return { katex: a.querySelectorAll('.katex').length, err: a.querySelectorAll('.katex-error').length, malas, vis,
                   ancho: document.documentElement.scrollWidth, vent: innerWidth,
                   graficos: [...a.querySelectorAll('canvas')].filter(cv => Chart.getChart(cv)).length, lienzos: a.querySelectorAll('canvas').length }; })()`);
        console.log(`M${n}: katex ${k.katex} · katex-error ${k.err} · anotaciones con tabulador/«ext{» ${k.malas.length}${k.malas.length ? ' ' + JSON.stringify(k.malas) + ' visible: ' + JSON.stringify(k.vis) : ''} · ancho ${k.ancho}/${k.vent} · graficos ${k.graficos}/${k.lienzos}`);
        if (n === 6) {
          console.log('   cierre del M6 (texto visible):', await c.evalua(`${pTexto('Con el modelo elegido y diagnosticado')}.textContent.replace(/\\s+/g,' ').trim()`));
          console.log('   lectura inicial del explorador:', await c.evalua(LECT('explorador-sarima')));
          await capturar(c, pTexto('Con el modelo elegido y diagnosticado'), `m6-cierre-${modo.n}.png`);
        }
        if (n === 10) {
          console.log('   lectura inicial de armonicos-K:', await c.evalua(LECT('armonicos-K')));
          await capturar(c, pTexto('Parámetros totales'), `m10-parametros-${modo.n}.png`);
        }
        for (const [mod, aria] of [[1, 'Ver la estacionalidad'], [9, null], [11, 'La comparación desde muchos orígenes']]) {
          if (n !== mod) continue;
          const t = await c.evalua(`(() => { const cts = [...document.querySelectorAll('#content-area .code-tabs')];
            const ct = ${aria ? `cts.find(x => x.querySelector('[aria-label="${aria}"]'))` : `cts.find(x => x.textContent.includes('Fuera de muestra'))`};
            if (!ct) return null; const vis = () => [...ct.querySelectorAll('.code-tab-panel')].map(p => p.dataset.lang + ':' + (!p.hidden && p.offsetParent !== null)).join();
            const a0 = vis(); ct.querySelector('button[data-lang="python"]').click(); const a1 = vis(); ct.querySelector('button[data-lang="r"]').click(); const a2 = vis();
            const pre = ct.querySelector('.code-tab-panel[data-lang="r"] pre'); const desb = pre.scrollWidth > pre.clientWidth;
            return { a0, a1, a2, prism: !!ct.querySelector('pre code .token'), preDesbordaDentro: desb, overflowPre: getComputedStyle(pre).overflowX }; })()`);
          console.log(`   pestañas M${mod}:`, JSON.stringify(t));
        }
        if (n === 11) {
          const t = await c.evalua(`(() => { const r = document.querySelector('.tabla-ranking[data-ranking="comparativa"]'); if (!r) return null;
            const tb = r.querySelector('table'); return { desc: (r.querySelector('.tabla-ranking-descripcion')||{}).textContent,
              cab: [...tb.tHead.rows[0].cells].map(x => x.textContent.trim()), filas: [...tb.tBodies[0].rows].map(f => [...f.cells].map(x => x.textContent.trim()).join(' | ')),
              pie: (r.querySelector('.tabla-ranking-pie')||{}).textContent }; })()`);
          console.log('   tabla ordenable:'); console.log(JSON.stringify(t, null, 1));
          console.log('   selects en el simulador:', await c.evalua(`document.querySelectorAll('[data-simulador="comparativa-particion"] select').length`));
          console.log('   lectura inicial:', await c.evalua(LECT('comparativa-particion')));
          await c.evalua(`(() => { document.querySelectorAll('[data-simulador="comparativa-particion"] input[type=checkbox]').forEach(i => { if (!i.checked) i.click(); }); return 1; })()`);
          await espera(400);
          console.log('   lectura con los ocho:', await c.evalua(LECT('comparativa-particion')));
          await capturar(c, `document.querySelector('[data-simulador="comparativa-particion"]')`, `m11-simulador-${modo.n}.png`);
          await capturar(c, `document.querySelector('.tabla-ranking[data-ranking="comparativa"]')`, `m11-tabla-${modo.n}.png`);
          await capturar(c, pTexto('Leída sin más'), `m11-veredicto-${modo.n}.png`);
          console.log('   orden del M11 (h3 y primeras palabras de cada bloque):');
          console.log(await c.evalua(`[...document.querySelector('#content-area .animate-fade-in').children].map(e => e.tagName + (e.className ? '.' + String(e.className).split(' ')[0] : '') + ': ' + e.textContent.replace(/\\s+/g,' ').trim().slice(0, 70)).join('\\n')`));
        }
      }
    }
    console.log('\n===== consola =====');
    const ev = c.eventos.filter(e => !/favicon/.test(e.txt));
    console.log(ev.length ? ev.map(e => `[${e.cuando}] ${e.txt}`).join('\n') : 'sin errores ni avisos de consola');
  } finally { await c.cerrar(); srv.kill(); }
})().catch(e => { console.error(e); process.exit(2); });
