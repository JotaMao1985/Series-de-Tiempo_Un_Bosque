#!/usr/bin/env node
// Vista real (sin recorte por elemento) de la tabla del M6 que <main> corta a 800 px.
const fs = require('fs'); const path = require('path');
const { Chrome, espera } = require('./chrome');
(async () => {
  const c = await Chrome.lanzar(9266);
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable');
    await c.enviar('Emulation.setDeviceMetricsOverride', { width: 800, height: 1000, deviceScaleFactor: 1, mobile: false });
    await c.enviar('Page.navigate', { url: 'http://localhost:8731/capitulo-2-estacionariedad-acf-pacf.html#modulo-6' });
    await c.esperaHasta(`typeof currentModuleId !== 'undefined' && currentModuleId === 6 && document.querySelectorAll('#content-area table').length > 1`, 20000);
    await espera(1500);
    const info = await c.evalua(`(() => { const t = document.querySelectorAll('#content-area table')[1];
      window.scrollTo(0, t.getBoundingClientRect().top + window.scrollY - 120); const m = document.getElementById('main-content').getBoundingClientRect();
      const r = t.getBoundingClientRect(); return { tablaRight: r.right, mainRight: m.right, tablaW: r.width, cabeceras: [...t.querySelectorAll('th')].map(th => th.textContent.trim()) }; })()`);
    await espera(400);
    const v = await c.enviar('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.resolve(__dirname, '..', 'capturas', 'm6-tabla1-vista-800.png'), Buffer.from(v.data, 'base64'));
    console.log(JSON.stringify(info));
  } finally { await c.cerrar(); }
  process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
