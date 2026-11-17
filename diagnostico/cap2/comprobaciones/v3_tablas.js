#!/usr/bin/env node
// Verificador independiente R3 · la pista de las tablas desplazables, medida de otra manera que r3_tablas.js:
//  - qué texto VISIBLE queda bajo el desvanecido (caracteres cuya caja cae en los 3.5rem del borde);
//  - cuánto se desplaza de verdad la tabla (resto) frente al ancho del desvanecido;
//  - tablas que se desplazan por un CONTENEDOR (no por sí mismas): ¿llevan pista?;
//  - tablas dentro de paneles plegados (pista/solución): al abrirlos, ¿se marca?;
//  - capturas: la primera tabla que se desplaza, al principio y a mitad; y la de menor resto.
// Uso: node v3_tablas.js http://localhost:8731/ [puerto_cdp] > v3_tablas.out
const fs = require('fs'); const path = require('path');
const { Chrome, espera } = require('../diag/chrome');
const [BASE, PUERTO] = process.argv.slice(2);
const ARCH = { 2: 'capitulo-2-estacionariedad-acf-pacf.html', 3: 'capitulo-3-modelos-ar-ma-arma.html', 4: 'capitulo-4-modelos-arima.html', 5: 'capitulo-5-sarima.html', 6: 'capitulo-6-pronostico-evaluacion.html' };
const ANCHOS = [1200, 1024, 800, 375];
const CAPT = path.join(__dirname, '..', 'capturas', 'r3v');
fs.mkdirSync(CAPT, { recursive: true });

const MEDIR = `(() => {
  const main = document.getElementById('main-content');
  const rem = parseFloat(getComputedStyle(document.documentElement).fontSize);
  const sal = [];
  [...mainContent.querySelectorAll('table')].forEach((t, i) => {
    const r = t.getBoundingClientRect();
    if (!r.width || t.closest('.tabla-ranking')) return;
    const bloque = getComputedStyle(t).display === 'block';
    const resto = bloque ? t.scrollWidth - t.clientWidth - t.scrollLeft : 0;
    // contenedor que se desplaza (entre la tabla y <main>)
    let cont = null, p = t.parentElement;
    while (p && p !== main) { const ox = getComputedStyle(p).overflowX;
      if ((ox === 'auto' || ox === 'scroll') && p.scrollWidth > p.clientWidth + 1) { cont = p.className || p.tagName; break; } p = p.parentElement; }
    const der = t.classList.contains('tabla-sigue-der'), izq = t.classList.contains('tabla-sigue-izq');
    // texto visible bajo el desvanecido derecho
    let bajo = 0, bajoTxt = '', visibles = 0;
    if (der) {
      const x0 = r.left + t.clientWidth - 3.5 * rem, x1 = r.left + t.clientWidth;
      const w = document.createTreeWalker(t, NodeFilter.SHOW_TEXT);
      let n; const rg = document.createRange();
      while ((n = w.nextNode())) {
        const s = n.textContent; if (!s.trim()) continue;
        for (let k = 0; k < s.length; k++) { if (!s[k].trim()) continue;
          rg.setStart(n, k); rg.setEnd(n, k + 1); const b = rg.getBoundingClientRect();
          if (!b.width) continue;
          const cx = b.left + b.width / 2;
          if (cx >= r.left && cx <= x1) { visibles++; if (cx >= x0) { bajo++; if (bajoTxt.length < 40) bajoTxt += s[k]; } } }
      }
    }
    const txt = (t.querySelector('caption')?.textContent || t.textContent).trim().slice(0, 60);
    const oculta = !!t.closest('[hidden]');
    sal.push({ i, bloque, resto: Math.round(resto), ancho: Math.round(t.clientWidth), cont, der, izq, bajo, visibles, bajoTxt, txt, fade: 3.5 * rem });
  });
  return sal;
})()`;

async function captura(c, idx, nombre, scroll) {
  const caja = await c.evalua(`(() => { const t = mainContent.querySelectorAll('table')[${idx}]; t.scrollIntoView({ block: 'center' });
    ${scroll === 'mitad' ? 't.scrollLeft = (t.scrollWidth - t.clientWidth) / 2;' : 't.scrollLeft = 0;'}
    const r = t.getBoundingClientRect(); return { x: Math.max(0, r.left - 12), y: Math.max(0, r.top - 12 + scrollY), w: r.width + 24, h: Math.min(r.height + 24, 600) }; })()`);
  await espera(350);
  const png = await c.enviar('Page.captureScreenshot', { format: 'png', clip: { x: caja.x, y: caja.y, width: caja.w, height: caja.h, scale: 1 }, captureBeyondViewport: true });
  fs.writeFileSync(path.join(CAPT, nombre), Buffer.from(png.data, 'base64'));
  await c.evalua(`(() => { mainContent.querySelectorAll('table')[${idx}].scrollLeft = 0; return 1; })()`);
}

(async () => {
  const c = await Chrome.lanzar(Number(PUERTO || 9291));
  const resumen = { tablas: 0, desplazan: 0, sinPista: 0, pistaSinDesplazar: 0, contenedorSinPista: 0, restoMenorQueFade: 0, plegadasMal: 0 };
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable');
    for (const cap of [2, 3, 4, 5, 6]) {
      for (const w of ANCHOS) {
        await c.enviar('Emulation.setDeviceMetricsOverride', w === 375 ? { width: 375, height: 812, deviceScaleFactor: 2, mobile: true } : { width: w, height: 1000, deviceScaleFactor: 1, mobile: false });
        await c.enviar('Page.navigate', { url: 'about:blank' }); await espera(150);
        await c.enviar('Page.navigate', { url: BASE + ARCH[cap] + '?v=' + Date.now() });
        await c.esperaHasta("typeof courseData !== 'undefined' && typeof renderMathInElement === 'function' && document.querySelector('#content-area > *')", 30000);
        await c.evalua('document.fonts.ready.then(() => 1)');
        const n = await c.evalua('courseData.modules.length');
        let capturada = false, menor = null;
        const lineas = [];
        for (let m = 1; m <= n; m++) {
          await c.evalua(`loadModule(${m}), 1`); await espera(800);
          let tablas = await c.evalua(MEDIR);
          for (const t of tablas) {
            resumen.tablas++;
            const desplaza = t.resto > 1;
            if (desplaza) resumen.desplazan++;
            if (desplaza && !t.der) { resumen.sinPista++; lineas.push(`  M${m} t${t.i} se desplaza SIN pista · ${t.txt}`); }
            if (!desplaza && (t.der || t.izq)) { resumen.pistaSinDesplazar++; lineas.push(`  M${m} t${t.i} pista SIN desplazarse · ${t.txt}`); }
            if (t.cont && !t.der) { resumen.contenedorSinPista++; lineas.push(`  M${m} t${t.i} la desplaza un contenedor (${t.cont}) y no lleva pista · ${t.txt}`); }
            if (t.der) {
              lineas.push(`  M${m} t${t.i} resto ${t.resto}px de ${t.ancho}px visibles · desvanecido ${t.fade}px · texto visible bajo el desvanecido ${t.bajo}/${t.visibles} car. «${t.bajoTxt}» · ${t.txt}`);
              if (t.resto < t.fade) { resumen.restoMenorQueFade++; }
              if (!menor || t.resto < menor.resto) menor = { ...t, m };
              if (!capturada) {
                capturada = true;
                await captura(c, t.i, `c${cap}-m${m}-t${t.i}-${w}-inicio.png`, 'inicio');
                await captura(c, t.i, `c${cap}-m${m}-t${t.i}-${w}-mitad.png`, 'mitad');
              }
            }
          }
          // paneles plegados: abrir todos los botones de pista/solución y volver a medir
          const abiertos = await c.evalua(`(() => { let k = 0; mainContent.querySelectorAll('[hidden]').forEach(e => { if (e.querySelector('table') && !e.closest('.ciclo')) { e.hidden = false; k++; } }); return k; })()`);
          if (abiertos) {
            await espera(500);
            tablas = await c.evalua(MEDIR);
            for (const t of tablas) {
              const desplaza = t.resto > 1;
              if (desplaza !== t.der) { resumen.plegadasMal++; lineas.push(`  M${m} t${t.i} (panel abierto) desplaza=${desplaza} pista=${t.der} · ${t.txt}`); }
            }
          }
        }
        if (menor && menor.resto < menor.fade) {
          await c.evalua(`loadModule(${menor.m}), 1`); await espera(800);
          await captura(c, menor.i, `c${cap}-m${menor.m}-t${menor.i}-${w}-resto${menor.resto}.png`, 'inicio');
        }
        console.log(`cap. ${cap} · ${w} px`);
        lineas.forEach(l => console.log(l));
      }
    }
    console.log('\nRESUMEN', JSON.stringify(resumen));
  } finally { await c.cerrar(); }
})().catch(e => { console.error(e); process.exit(1); });
