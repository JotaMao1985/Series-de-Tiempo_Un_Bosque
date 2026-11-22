#!/usr/bin/env node
// Iconos de Font Awesome que no se dibujan (glifo vacío) en los 12 módulos del cap. 4, a 1200 px.
// Uso: node diagnostico/cap4/diag/graficas_iconos.js > diagnostico/cap4/diag/graficas_iconos.out
const { Chrome, espera } = require('./chrome');
const BASE = process.env.BASE || 'http://127.0.0.1:8762/capitulo-4-modelos-arima.html';
(async () => {
  const c = await Chrome.lanzar(9275);
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable');
    await c.enviar('Emulation.setDeviceMetricsOverride', { width: 1200, height: 1000, deviceScaleFactor: 1, mobile: false });
    await c.enviar('Page.navigate', { url: BASE + '#modulo-1' });
    await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined'", 30000);
    await c.evalua('document.fonts.ready.then(() => 1)');
    const css = await c.evalua(`[...document.querySelectorAll('link[rel=stylesheet]')].map(l => l.href).filter(h => /font-awesome/.test(h))`);
    console.log('hoja:', css);
    const vacios = {};
    for (let n = 1; n <= 12; n++) {
      await c.evalua(`loadModule(${n}), 1`); await espera(900);
      const r = await c.evalua(`[...document.querySelectorAll('#main-content i[class*="fa-"], .usta-header i[class*="fa-"], aside i[class*="fa-"]')].map(i => {
        const cont = getComputedStyle(i, '::before').content;
        return { cls: i.className, cont, w: Math.round(i.getBoundingClientRect().width), dentro: (i.closest('h4,h3,button,.simulador')||{}).className || (i.closest('h4,h3,button')||{}).tagName || '' };
      }).filter(x => !x.cont || x.cont === 'none' || x.cont === '""' || x.cont === 'normal')`);
      r.forEach(x => { const k = x.cls; vacios[k] = vacios[k] || []; vacios[k].push('M' + n); });
    }
    console.log(JSON.stringify(vacios, null, 1));
  } finally { await c.cerrar(); }
})().then(() => process.exit(0)).catch(e => { console.error(e); process.exit(1); });
