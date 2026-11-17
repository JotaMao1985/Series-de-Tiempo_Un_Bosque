#!/usr/bin/env node
// R3b (tras la verificación) · la pista de que una tabla sigue, con el desvanecido de ancho variable.
// Además de lo que medía r3_tablas.js: el ancho del desvanecido de cada tabla que se desplaza y cuántos textos
// de celda ENTEROS a la vista quedan debajo de él (tiene que ser 0), al principio, a mitad y al final.
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
const CAPTURAS = path.join(__dirname, '..', 'capturas', 'r3b');
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
    const bajo = () => { const u = r.left + t.clientLeft, v = u + t.clientWidth; const rg = document.createRange();
      const fd = t.classList.contains('tabla-sigue-der') ? parseFloat(t.style.getPropertyValue('--sigue-der')) : 0;
      const fi = t.classList.contains('tabla-sigue-izq') ? parseFloat(t.style.getPropertyValue('--sigue-izq')) : 0;
      let n = 0; t.querySelectorAll('th, td').forEach(c => { rg.selectNodeContents(c); const b = rg.getBoundingClientRect();
        if (!b.width || b.left < u - 0.5 || b.right > v + 0.5) return;
        if (b.right > v - fd + 0.5 || b.left < u + fi - 0.5) n++; });
      return { n, fd, fi }; };
    const f = { i, ranking, desplaza, recorte, resto: t.scrollWidth - t.clientWidth, der0: t.classList.contains('tabla-sigue-der'), izq0: t.classList.contains('tabla-sigue-izq'),
      mascara: getComputedStyle(t).maskImage !== 'none' };
    if (desplaza) {
      f.ini = bajo();
      t.scrollLeft = (t.scrollWidth - t.clientWidth) / 2; await new Promise(r => setTimeout(r, 120)); f.mitad = bajo();
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
  let total = 0, desplazan = 0, mal = 0, recortes = 0, katex = 0, tapados = 0, tenues = 0, pocoResto = 0; const anchos = []; const capturadas = new Set(); const detalle = [];
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
              if (t.ini.n || t.mitad.n) { tapados++; fallos.push(`M${m} tabla ${t.i}: ${t.ini.n} + ${t.mitad.n} textos enteros bajo el desvanecido`); }
              anchos.push(t.ini.fd); if (t.ini.fd < 8 && t.resto >= 8) tenues++; if (t.resto < 56) pocoResto++; if (t.ini.fd > t.resto + 0.5) { tapados++; fallos.push(`M${m} tabla ${t.i}: desvanecido ${t.ini.fd} > resto ${t.resto}`); }
              detalle.push(`cap${cap} ${w} M${m} t${t.i}: resto ${Math.round(t.resto)} px · desvanecido ${t.ini.fd} px (a mitad: ${t.mitad.fi} y ${t.mitad.fd})`);
              if (!bien) { mal++; fallos.push(`M${m} tabla ${t.i}: se desplaza y la pista falla ${JSON.stringify(t)}`); }
              const clave = `${cap}-${w}`;
              const pedido = ['5-800-12-5', '5-375-7-3', '4-800-8-1', '3-800-8-1', '2-800-6-1', '2-375-7-2'].includes(`${cap}-${w}-${m}-${t.i}`);
              if (pedido) {
                capturadas.add(clave);
                const caja = await c.evalua(`(() => { const t = mainContent.querySelectorAll('table')[${t.i}]; t.scrollIntoView({ block: 'center' }); const r = t.getBoundingClientRect(); return { x: Math.max(0, r.left - 12), y: Math.max(0, r.top - 12 + scrollY), w: r.width + 24, h: Math.min(r.height + 24, 700) }; })()`);
                await espera(300);
                const png = await c.enviar('Page.captureScreenshot', { format: 'png', clip: { x: caja.x, y: caja.y, width: caja.w, height: caja.h, scale: 1 }, captureBeyondViewport: true });
                fs.writeFileSync(path.join(CAPTURAS, `c${cap}-m${m}-t${t.i}-${w}.png`), Buffer.from(png.data, 'base64'));
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
    anchos.sort((a, b) => a - b);
    console.log(`textos enteros bajo el desvanecido: ${tapados} tablas (debe ser 0)`);
    console.log(`ancho del desvanecido derecho al principio: mínimo ${anchos[0]}, mediana ${anchos[anchos.length >> 1]}, máximo ${anchos[anchos.length - 1]} px; menor de 8 px, faltando 8 px o más, en ${tenues} de ${anchos.length}; tablas a las que les faltan menos de 56 px: ${pocoResto}`);
    console.log(`eventos de consola (errores, avisos, excepciones): ${ev.length}`);
    ev.forEach(e => console.log('   ', e.cuando, '·', e.txt.slice(0, 300)));
  } finally { await c.cerrar(); }
  console.log('\n--- detalle ---'); detalle.forEach(d => console.log(d));
  process.exit(mal || recortes || katex || tapados ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
