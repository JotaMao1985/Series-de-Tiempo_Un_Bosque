#!/usr/bin/env node
// R2b · todas las tablas de los capítulos 2 a 6, módulo a módulo, a 1200, 1024, 900, 800 y 375 px:
// ancho de la caja, ancho de sus filas, si llena su contenedor, si <main> la corta sin barra y si
// se desplaza. Sirve para HEAD (servido aparte) y para el árbol de trabajo.
// Uso: node r2b_tablas.js <BASE_URL> <etiqueta> [puerto_cdp]   → r2b_tablas_<etiqueta>.json
const fs = require('fs'); const path = require('path');
const { Chrome, espera } = require('../diag/chrome');
const [BASE, ETIQ, PUERTO] = process.argv.slice(2);
const ARCH = { 2: 'capitulo-2-estacionariedad-acf-pacf.html', 3: 'capitulo-3-modelos-ar-ma-arma.html', 4: 'capitulo-4-modelos-arima.html', 5: 'capitulo-5-sarima.html', 6: 'capitulo-6-pronostico-evaluacion.html' };
const ANCHOS = [1200, 1024, 900, 800, 375];
const MEDIR = `(() => {
  const main = document.getElementById('main-content'); const mR = main.getBoundingClientRect().right;
  const r1 = x => Math.round(x * 10) / 10;
  return [...mainContent.querySelectorAll('table')].map((t, i) => {
    const r = t.getBoundingClientRect();
    if (!r.width) return { i, oculta: true };
    const filas = Math.max(...[...t.querySelectorAll(':scope > thead, :scope > tbody, :scope > tr')].map(g => g.getBoundingClientRect().width), 0);
    const caja = t.parentElement; const e = getComputedStyle(caja);
    const hueco = caja.clientWidth - parseFloat(e.paddingLeft) - parseFloat(e.paddingRight);
    const propia = getComputedStyle(t).overflowX;
    let recogida = propia === 'auto' || propia === 'scroll', p = caja;
    while (p && p !== main && !recogida) { const ox = getComputedStyle(p).overflowX; if (ox === 'auto' || ox === 'scroll' || ox === 'hidden') recogida = true; p = p.parentElement; }
    const sobra = Math.max(r.right, r.left + filas) - mR;
    return { i, cls: t.className, ranking: !!t.closest('.tabla-ranking'), display: getComputedStyle(t).display, caja: r1(r.width), filas: r1(filas), hueco: r1(hueco),
      llena: filas >= Math.min(hueco, r.width) - 2, recorte: (!recogida && sobra > 1) ? r1(sobra) : 0, desplaza: t.scrollWidth > t.clientWidth + 1,
      cab: [...t.querySelectorAll('th')].slice(0, 4).map(th => th.textContent.trim().slice(0, 14)).join(' | ') };
  });
})()`;
(async () => {
  const c = await Chrome.lanzar(Number(PUERTO || 9275));
  const sal = {};
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable'); await c.enviar('Log.enable');
    for (const cap of [2, 3, 4, 5, 6]) {
      sal[cap] = {};
      for (const w of ANCHOS) {
        await c.enviar('Emulation.setDeviceMetricsOverride', w === 375 ? { width: 375, height: 812, deviceScaleFactor: 2, mobile: true } : { width: w, height: 1000, deviceScaleFactor: 1, mobile: false });
        await c.enviar('Page.navigate', { url: 'about:blank' }); await espera(150);
        await c.enviar('Page.navigate', { url: BASE + ARCH[cap] + '?t=' + Date.now() + '#modulo-1' });
        await c.esperaHasta("typeof courseData !== 'undefined' && typeof renderMathInElement === 'function' && document.querySelector('#content-area > *')", 30000);
        await c.evalua('document.fonts.ready.then(() => 1)');
        const n = await c.evalua('courseData.modules.length');
        sal[cap][w] = {};
        for (let m = 1; m <= n; m++) {
          await c.evalua(`loadModule(${m}), 1`); await espera(700);
          sal[cap][w][m] = await c.evalua(MEDIR);
        }
        console.log(`cap${cap} ${w}: ${n} módulos`);
      }
    }
    sal.eventos = c.eventos.filter(e => !/favicon/.test(e.txt));
  } finally { await c.cerrar(); }
  fs.writeFileSync(path.join(__dirname, `r2b_tablas_${ETIQ}.json`), JSON.stringify(sal));
  console.log('listo; eventos:', sal.eventos.length);
  process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
