#!/usr/bin/env node
// Capturas de la leyenda de los gráficos de línea en los caps. 2, 3, 5 y 6 (HEAD frente al árbol).
const fs = require('fs'); const path = require('path');
const { Chrome, espera } = require('../diag/chrome');
const OUT = path.join(__dirname, '../capturas/v2');
const CASOS = [
  ['2-estacionariedad-acf-pacf', 1, 'camino-aleatorio'],
  ['3-modelos-ar-ma-arma', 8, null],
  ['5-sarima', 7, 'pronostico-estacional'],
  ['5-sarima', 10, 'armonicos-K'],
  ['6-pronostico-evaluacion', 7, 'error-por-horizonte'],
  ['6-pronostico-evaluacion', 9, 'cobertura'],
];
async function main() {
  const c = await Chrome.lanzar(9284);
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable');
    await c.enviar('Emulation.setDeviceMetricsOverride', { width: 1200, height: 1000, deviceScaleFactor: 1, mobile: false });
    for (const [ver, pto] of [['nuevo', 8766], ['viejo', 8767]]) {
      for (const [cap, mod, sim] of CASOS) {
        await c.enviar('Page.navigate', { url: `http://127.0.0.1:${pto}/capitulo-${cap}.html#modulo-1` });
        await espera(600);
        await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined' && typeof renderMathInElement === 'function'", 30000);
        await c.evalua('document.fonts.ready.then(() => 1)');
        await c.evalua(`Chart.defaults.animation = false; loadModule(${mod}), 1`);
        await espera(1100);
        await c.evalua(`(() => { const s = document.createElement('style'); s.textContent = 'header.usta-header{position:static!important} #sidebarToggle,#scrollToTopBtn{visibility:hidden!important}'; document.head.appendChild(s); return 1; })()`);
        const n = await c.evalua(`document.querySelectorAll('[data-simulador] canvas').length`);
        const rects = await c.evalua(`[...mainContent.querySelectorAll('[data-simulador]')].filter(s => s.querySelector('canvas')).map(s => s.dataset.simulador)`);
        const objetivo = sim && rects.includes(sim) ? sim : rects[0];
        const rect = await c.evalua(`(() => { const el = document.querySelector('[data-simulador="${objetivo}"]'); el.scrollIntoView({block:'start'}); const r = el.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height }; })()`);
        await espera(300);
        const r = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: rect.x, y: rect.y, width: rect.w, height: Math.min(rect.h, 1100), scale: 1 } });
        fs.writeFileSync(path.join(OUT, `leyenda-${ver}-cap${cap.split('-')[0]}-m${mod}-${objetivo}.png`), Buffer.from(r.data, 'base64'));
        console.log(ver, cap, mod, objetivo, rects.join(','));
      }
    }
  } finally { await c.cerrar(); }
}
main().then(() => process.exit(0)).catch(e => { console.error(e.stack); process.exit(1); });
