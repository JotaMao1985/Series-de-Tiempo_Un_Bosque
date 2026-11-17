#!/usr/bin/env node
// R2b · sonda suelta: evalúa una expresión en un módulo de un capítulo a un ancho dado.
// Uso: node r2b_sonda.js <cap> <módulo> <ancho> '<expresión JS>'
const { Chrome, espera } = require('../diag/chrome');
const ARCH = { 2: 'capitulo-2-estacionariedad-acf-pacf.html', 3: 'capitulo-3-modelos-ar-ma-arma.html', 4: 'capitulo-4-modelos-arima.html', 5: 'capitulo-5-sarima.html', 6: 'capitulo-6-pronostico-evaluacion.html' };
(async () => {
  const [cap, mod, ancho, expr] = process.argv.slice(2);
  const c = await Chrome.lanzar(Number(process.env.PUERTO || 9273));
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable');
    const w = Number(ancho);
    await c.enviar('Emulation.setDeviceMetricsOverride', w === 375 ? { width: 375, height: 812, deviceScaleFactor: 2, mobile: true } : { width: w, height: 1000, deviceScaleFactor: 1, mobile: false });
    await c.enviar('Page.navigate', { url: (process.env.SERVIDOR || 'http://localhost:8731/') + ARCH[cap] + '?s=' + Date.now() + '#modulo-' + mod });
    await c.esperaHasta(`typeof currentModuleId !== 'undefined' && currentModuleId === ${mod} && document.querySelector('#content-area > *')`, 30000);
    await c.evalua('document.fonts.ready.then(() => 1)'); await espera(1200);
    console.log(JSON.stringify(await c.evalua(expr), null, 1));
    console.log('eventos:', JSON.stringify(c.eventos.filter(e => !/favicon/.test(e.txt))));
  } finally { await c.cerrar(); }
  process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
