#!/usr/bin/env node
// Verificador independiente R2: captura tablas concretas en HEAD y ahora, al mismo ancho.
// Uso: node v2_tablas.js cap:módulo:índice:ancho [...]
const fs = require('fs'); const path = require('path');
const { Chrome, espera } = require('../diag/chrome');
const ARCH = { 2: 'capitulo-2-estacionariedad-acf-pacf.html', 3: 'capitulo-3-modelos-ar-ma-arma.html', 4: 'capitulo-4-modelos-arima.html', 5: 'capitulo-5-sarima.html', 6: 'capitulo-6-pronostico-evaluacion.html' };
const BASES = { head: 'http://127.0.0.1:8813', ahora: 'http://127.0.0.1:8731' };
const OUT = path.resolve(__dirname, '..', 'capturas', 'r2v', 'tablas');
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const c = await Chrome.lanzar(9297);
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable');
    for (const arg of process.argv.slice(2)) {
      const [cap, n, i, w] = arg.split(':').map(Number);
      for (const [et, base] of Object.entries(BASES)) {
        await c.enviar('Emulation.setDeviceMetricsOverride', { width: w, height: w === 375 ? 812 : 900, deviceScaleFactor: w === 375 ? 2 : 1, mobile: w === 375 });
        await c.enviar('Page.navigate', { url: `${base}/${ARCH[cap]}#modulo-1` });
        await espera(700);
        await c.esperaHasta("typeof courseData !== 'undefined' && typeof renderMathInElement === 'function'", 30000);
        await c.evalua('document.fonts.ready.then(() => 1)');
        await c.evalua(`(() => { const s = document.createElement('style'); s.textContent = 'header.usta-header{position:static!important} #sidebarToggle,#scrollToTopBtn{visibility:hidden!important}'; document.head.appendChild(s); loadModule(${n}); return 1; })()`);
        await espera(1300);
        const r = await c.evalua(`(() => { const t = mainContent.querySelectorAll('table')[${i}]; t.scrollIntoView({behavior:'instant', block:'center'}); const p = t.parentElement.getBoundingClientRect(); const b = t.getBoundingClientRect(); return {x:p.left+scrollX, y:b.top+scrollY, w:p.width, h:Math.min(b.height, 700)}; })()`);
        await espera(150);
        const s = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: r.x - 6, y: r.y - 6, width: r.w + 12, height: r.h + 12, scale: 1 } });
        const nom = `c${cap}-m${n}-tabla${i}-${w}-${et}.png`;
        fs.writeFileSync(path.join(OUT, nom), Buffer.from(s.data, 'base64'));
        console.log(nom);
      }
    }
  } finally { await c.cerrar(); }
})().then(() => process.exit(0)).catch(e => { console.error(e); process.exit(1); });
