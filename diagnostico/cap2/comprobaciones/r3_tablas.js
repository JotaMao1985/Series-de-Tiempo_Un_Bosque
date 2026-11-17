#!/usr/bin/env node
// R3 · la pista de que una tabla sigue. Capítulos 2 a 6, módulo a módulo, a 1200, 1024, 800 y 375 px.
// Por cada tabla visible: si se desplaza (bloque con scrollWidth > clientWidth), si lleva la clase
// `tabla-sigue-der`, si <main> la corta sin barra, y —llevándola al final— si la clase se quita y
// aparece `tabla-sigue-izq`. Además: errores de consola, excepciones y errores de KaTeX por módulo.
// Guarda una captura de la primera tabla que se desplaza de cada capítulo y ancho.
// Uso: node r3_tablas.js http://127.0.0.1:8731/ [puerto_cdp]  > r3_tablas.out
const fs = require('fs'); const path = require('path');
const { Chrome, espera } = require('../diag/chrome');
const [BASE, PUERTO] = process.argv.slice(2);
const ARCH = { 2: 'capitulo-2-estacionariedad-acf-pacf.html', 3: 'capitulo-3-modelos-ar-ma-arma.html', 4: 'capitulo-4-modelos-arima.html', 5: 'capitulo-5-sarima.html', 6: 'capitulo-6-pronostico-evaluacion.html' };
const ANCHOS = [1200, 1024, 800, 375];
const CAPTURAS = path.join(__dirname, '..', 'capturas', 'r3');
const MEDIR = `(async () => {
  const main = document.getElementById('main-content'); const mR = main.getBoundingClientRect().right;
  const sal = [];
  for (const [i, t] of [...mainContent.querySelectorAll('table')].entries()) {
    const r = t.getBoundingClientRect();
    if (!r.width) continue;
    const ranking = !!t.closest('.tabla-ranking');
    const bloque = getComputedStyle(t).display === 'block';
    const desplaza = bloque && t.scrollWidth > t.clientWidth + 1;
    const propia = getComputedStyle(t).overflowX; let recogida = propia === 'auto' || propia === 'scroll', p = t.parentElement;
    while (p && p !== main && !recogida) { const ox = getComputedStyle(p).overflowX; if (ox === 'auto' || ox === 'scroll' || ox === 'hidden') recogida = true; p = p.parentElement; }
    const filas = Math.max(...[...t.querySelectorAll(':scope > thead, :scope > tbody, :scope > tr')].map(g => g.getBoundingClientRect().width), 0);
    const recorte = (!recogida && Math.max(r.right, r.left + filas) - mR > 1);
    const f = { i, ranking, desplaza, recorte, der0: t.classList.contains('tabla-sigue-der'), izq0: t.classList.contains('tabla-sigue-izq'),
      mascara: getComputedStyle(t).maskImage !== 'none' };
    if (desplaza) {
      t.scrollLeft = t.scrollWidth; await new Promise(r => setTimeout(r, 120));
      f.derFin = t.classList.contains('tabla-sigue-der'); f.izqFin = t.classList.contains('tabla-sigue-izq');
      t.scrollLeft = 0; await new Promise(r => setTimeout(r, 120));
      f.derVuelta = t.classList.contains('tabla-sigue-der'); f.izqVuelta = t.classList.contains('tabla-sigue-izq');
    }
    sal.push(f);
  }
  return { tablas: sal, katex: document.querySelectorAll('#content-area .katex-error').length };
})()`;
(async () => {
  const c = await Chrome.lanzar(Number(PUERTO || 9281));
  let total = 0, desplazan = 0, mal = 0, recortes = 0, katex = 0; const capturadas = new Set();
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable'); await c.enviar('Log.enable');
    for (const cap of [2, 3, 4, 5, 6]) {
      for (const w of ANCHOS) {
        await c.enviar('Emulation.setDeviceMetricsOverride', w === 375 ? { width: 375, height: 812, deviceScaleFactor: 2, mobile: true } : { width: w, height: 1000, deviceScaleFactor: 1, mobile: false });
        await c.enviar('Page.navigate', { url: 'about:blank' }); await espera(150);
        c.contexto = `cap${cap} ${w}`;
        await c.enviar('Page.navigate', { url: BASE + ARCH[cap] + '?t=' + Date.now() + '#modulo-1' });
        await c.esperaHasta("typeof courseData !== 'undefined' && typeof renderMathInElement === 'function' && document.querySelector('#content-area > *')", 30000);
        await c.evalua('document.fonts.ready.then(() => 1)');
        const n = await c.evalua('courseData.modules.length');
        let nT = 0, nD = 0; const fallos = [];
        for (let m = 1; m <= n; m++) {
          c.contexto = `cap${cap} ${w} M${m}`;
          await c.evalua(`loadModule(${m}), 1`); await espera(700);
          const r = await c.evalua(MEDIR);
          katex += r.katex; if (r.katex) fallos.push(`M${m}: ${r.katex} errores de KaTeX`);
          for (const t of r.tablas) {
            if (t.ranking) continue;
            nT++; if (t.recorte) { recortes++; fallos.push(`M${m} tabla ${t.i}: cortada por <main>`); }
            if (t.desplaza) {
              nD++;
              const bien = t.der0 && !t.izq0 && t.mascara && !t.derFin && t.izqFin && t.derVuelta && !t.izqVuelta;
              if (!bien) { mal++; fallos.push(`M${m} tabla ${t.i}: se desplaza y la pista falla ${JSON.stringify(t)}`); }
              const clave = `${cap}-${w}`;
              if (!capturadas.has(clave) && w !== 1200 && w !== 1024) {
                capturadas.add(clave);
                const caja = await c.evalua(`(() => { const t = mainContent.querySelectorAll('table')[${t.i}]; t.scrollIntoView({ block: 'center' }); const r = t.getBoundingClientRect(); return { x: Math.max(0, r.left - 12), y: Math.max(0, r.top - 12 + scrollY), w: r.width + 24, h: Math.min(r.height + 24, 700) }; })()`);
                await espera(300);
                const png = await c.enviar('Page.captureScreenshot', { format: 'png', clip: { x: caja.x, y: caja.y, width: caja.w, height: caja.h, scale: 1 }, captureBeyondViewport: true });
                fs.writeFileSync(path.join(CAPTURAS, `tabla-sigue-c${cap}-m${m}-${w}.png`), Buffer.from(png.data, 'base64'));
              }
            } else if (t.der0 || t.izq0 || t.mascara) { mal++; fallos.push(`M${m} tabla ${t.i}: no se desplaza y lleva la pista ${JSON.stringify(t)}`); }
          }
        }
        total += nT; desplazan += nD;
        console.log(`cap. ${cap} · ${String(w).padStart(4)} px · ${n} módulos · ${nT} tablas, ${nD} se desplazan${fallos.length ? '' : ' · sin fallos'}`);
        fallos.forEach(f => console.log('    !! ' + f));
      }
    }
    const ev = c.eventos.filter(e => !/favicon/.test(e.txt));
    console.log(`\n${total} tablas × ancho medidas (sin las .tabla-ranking); ${desplazan} se desplazan; pista incoherente en ${mal}; cortadas por <main>: ${recortes}; errores de KaTeX: ${katex}`);
    console.log(`eventos de consola (errores, avisos, excepciones): ${ev.length}`);
    ev.forEach(e => console.log('   ', e.cuando, '·', e.txt.slice(0, 300)));
  } finally { await c.cerrar(); }
  process.exit(mal || recortes || katex ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
