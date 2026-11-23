#!/usr/bin/env node
// V3 · lee la barra lateral renderizada (texto visible de cada módulo) y la compara con courseData. Servidor 8771, CDP 9301.
const path = require('path'); const { spawn } = require('child_process');
const { Chrome, espera } = require('../diag/chrome');
const RAIZ = path.resolve(__dirname, '..', '..', '..');
(async () => {
  const srv = spawn('python3', ['-m', 'http.server', '8771', '--bind', '127.0.0.1', '--directory', path.join(RAIZ, 'Htmls_Series')], { stdio: 'ignore' });
  await espera(1200);
  const c = await Chrome.lanzar(9301);
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable');
    await c.enviar('Emulation.setDeviceMetricsOverride', { width: 1200, height: 1000, deviceScaleFactor: 1, mobile: false });
    await c.enviar('Page.navigate', { url: 'http://127.0.0.1:8771/capitulo-4-modelos-arima.html' });
    await c.esperaHasta(`typeof loadModule === 'function'`, 20000); await espera(1500);
    const filas = await c.evalua(`[...document.querySelectorAll('*')].filter(e => e.children.length <= 3 && /^\\s*\\d+ min\\s*$/.test(e.textContent)).map(e => { const li = e.closest('li, a, button'); return (li ? li.textContent : e.textContent).replace(/\\s+/g, ' ').trim(); })`);
    console.log(filas.join('\n'));
    console.log('total de entradas con minutos en el DOM:', filas.length);
  } finally { await c.cerrar(); srv.kill(); }
})();
