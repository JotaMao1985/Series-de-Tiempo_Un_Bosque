#!/usr/bin/env node
// Verificador independiente R2: captura las fórmulas en partes del cap. 2 y las cajas que se
// desplazan (con la sombra de pista), a 800 y 375 px, en el capítulo indicado.
// Uso: node v2_formulas.js [BASE] [archivo] [módulos=2,3,4,5,6]
const fs = require('fs'); const path = require('path');
const { Chrome, espera } = require('../diag/chrome');
const BASE = process.argv[2] || 'http://127.0.0.1:8731';
const ARCH = process.argv[3] || 'capitulo-2-estacionariedad-acf-pacf.html';
const MODS = (process.argv[4] || '2,3,4,5,6').split(',').map(Number);
const ETQ = ARCH.slice(0, 11);
const OUT = path.resolve(__dirname, '..', 'capturas', 'r2v', 'formulas');
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const c = await Chrome.lanzar(9296);
  const res = [];
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable');
    for (const [w, m] of [[800, false], [375, true]]) {
      await c.enviar('Emulation.setDeviceMetricsOverride', { width: w, height: m ? 812 : 1000, deviceScaleFactor: m ? 2 : 1, mobile: m });
      await c.enviar('Page.navigate', { url: `${BASE}/${ARCH}#modulo-1` });
      await espera(700);
      await c.esperaHasta("typeof courseData !== 'undefined' && typeof renderMathInElement === 'function'", 30000);
      await c.evalua('document.fonts.ready.then(() => 1)');
      await c.evalua(`(() => { const s = document.createElement('style'); s.textContent = 'header.usta-header{position:static!important} #sidebarToggle,#scrollToTopBtn{visibility:hidden!important}'; document.head.appendChild(s); return 1; })()`);
      for (const n of MODS) {
        await c.evalua(`loadModule(${n}), 1`); await espera(1200);
        const objetivos = await c.evalua(`(() => { const out = []; const els = [...mainContent.querySelectorAll('.formula, .definition, .note, .warning, .exercise')];
          els.forEach((e, i) => { const partes = e.querySelector(':scope > .formula-partes, :scope > p + .formula-partes, .formula-partes');
            const desborda = e.scrollWidth > e.clientWidth + 1;
            if ((partes && partes.closest('.formula, .definition, .note, .warning, .exercise') === e) || desborda) out.push({ i, cls: e.className, desborda, sw: e.scrollWidth, cw: e.clientWidth, partes: !!partes, txt: e.textContent.replace(/\\s+/g,' ').trim().slice(0,50) }); });
          return out; })()`);
        for (const o of objetivos) {
          const r = await c.evalua(`(() => { const e = [...mainContent.querySelectorAll('.formula, .definition, .note, .warning, .exercise')][${o.i}]; e.scrollIntoView({behavior:'instant', block:'center'}); const b = e.getBoundingClientRect(); return {x:b.left+scrollX, y:b.top+scrollY, w:b.width, h:Math.min(b.height, 900)}; })()`);
          await espera(120);
          const s = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: r.x - 4, y: r.y - 4, width: r.w + 8, height: r.h + 8, scale: 1 } });
          const nombre = `${ETQ}-m${n}-${o.cls.split(' ')[0]}${o.i}-${w}.png`;
          fs.writeFileSync(path.join(OUT, nombre), Buffer.from(s.data, 'base64'));
          res.push(Object.assign({ w, n, nombre }, o));
        }
      }
    }
  } finally { await c.cerrar(); }
  res.forEach(r => console.log(r.w, 'M' + r.n, r.nombre, r.desborda ? `DESBORDA ${r.sw}/${r.cw}` : '', r.partes ? 'partes' : '', r.txt));
})().then(() => process.exit(0)).catch(e => { console.error(e); process.exit(1); });
