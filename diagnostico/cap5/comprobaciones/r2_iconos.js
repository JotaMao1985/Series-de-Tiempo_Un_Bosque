#!/usr/bin/env node
// R2 del cap. 5 (copia de diagnostico/cap4/comprobaciones/r2_iconos.js) · ¿qué iconos de Font Awesome 6.0.0 se dibujan? Prueba candidatos sobre la hoja que carga el capítulo
// (cdnjs, 6.0.0) y lista los vacíos de los 12 módulos del cap. 5. Uso:
//   BASE=http://127.0.0.1:8768/Htmls_Series/capitulo-5-sarima.html CDP=9278 node r2_iconos.js
const { Chrome, espera } = require('../diag/chrome');
const BASE = process.env.BASE || 'http://127.0.0.1:8768/Htmls_Series/capitulo-5-sarima.html';
const CANDIDATOS = (process.env.ICONOS || 'ranking-star,trophy,medal,award,list-ol,ranking,arrow-down-1-9,arrow-up-wide-short,chart-line,table-cells,ice-cream,cubes,store,grip,triangle-exclamation,wave-square,stairs,sliders,ban,calendar-days').split(',');
(async () => {
  const c = await Chrome.lanzar(Number(process.env.CDP || 9278));
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable');
    await c.enviar('Emulation.setDeviceMetricsOverride', { width: 1200, height: 1000, deviceScaleFactor: 1, mobile: false });
    await c.enviar('Page.navigate', { url: BASE + '#modulo-1' });
    await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined'", 30000);
    await c.evalua('document.fonts.ready.then(() => 1)');
    await espera(500);
    console.log('hoja:', JSON.stringify(await c.evalua(`[...document.querySelectorAll('link[rel=stylesheet]')].map(l => l.href).filter(h => /font-awesome/.test(h))`)));
    const r = await c.evalua(`(${JSON.stringify(CANDIDATOS)}).map(n => { const i = document.createElement('i'); i.className = 'fas fa-' + n; document.body.appendChild(i);
      const cont = getComputedStyle(i, '::before').content; const w = Math.round(i.getBoundingClientRect().width); i.remove();
      return n + ': ' + (cont && cont !== 'none' && cont !== 'normal' && cont !== '""' ? 'SE DIBUJA ' + cont + ' (' + w + ' px)' : 'vacío'); })`);
    console.log(r.join('\n'));
    // y los de los h4 de los 12 módulos (cualquiera que quede vacío)
    const vacios = {};
    for (let n = 1; n <= 12; n++) {
      await c.evalua(`loadModule(${n}), 1`); await espera(700);
      const lista = await c.evalua(`[...document.querySelectorAll('#main-content i[class*="fa-"], .usta-header i[class*="fa-"], aside i[class*="fa-"]')].map(i => ({ cls: i.className, cont: getComputedStyle(i, '::before').content }))
        .filter(x => !x.cont || x.cont === 'none' || x.cont === '""' || x.cont === 'normal')`);
      lista.forEach(x => { (vacios[x.cls] = vacios[x.cls] || []).push('M' + n); });
    }
    console.log('iconos vacíos en los 12 módulos:', JSON.stringify(vacios));
  } finally { await c.cerrar(); }
})().then(() => process.exit(0)).catch(e => { console.error(e); process.exit(1); });
