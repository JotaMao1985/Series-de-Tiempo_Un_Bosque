#!/usr/bin/env node
// Captura de la primera figura de paneles del simulacro (M12) a 800 y 375 px.
// Uso: node diagnostico/cap5/diag/graficas_simulacro_captura.js
const fs = require('fs'); const path = require('path');
const { Chrome, espera } = require('./chrome');
const BASE = 'http://127.0.0.1:8765/capitulo-5-sarima.html';
(async () => {
  const c = await Chrome.lanzar(9278);
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable');
    for (const [w, h, dsf, mob] of [[800, 1000, 1, false], [375, 812, 2, true], [1200, 1000, 1, false]]) {
      await c.enviar('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: dsf, mobile: mob });
      await c.enviar('Page.navigate', { url: BASE + '#modulo-12' }); await espera(600);
      await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined'", 30000);
      await c.evalua('document.fonts.ready.then(() => 1)'); await c.evalua('loadModule(12), 1'); await espera(1200);
      await c.evalua(`(() => { const st = document.createElement('style'); st.textContent = 'header.usta-header{position:static!important}'; document.head.appendChild(st); return 1; })()`);
      const rect = await c.evalua(`(() => { const s = document.querySelector('#main-content .simulacro svg'); const f = s.closest('figure') || s.parentElement.parentElement; f.scrollIntoView({block:'start'}); const r = f.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height }; })()`);
      await espera(300);
      const r = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: rect.x, y: rect.y, width: rect.w, height: Math.min(rect.h, 700), scale: 1 } });
      fs.writeFileSync(path.join(__dirname, '..', 'capturas', `m12-cap5-simulacro-figura1-${w}.png`), Buffer.from(r.data, 'base64'));
    }
  } finally { await c.cerrar(); }
})().then(() => process.exit(0)).catch(e => { console.error(e); process.exit(1); });
