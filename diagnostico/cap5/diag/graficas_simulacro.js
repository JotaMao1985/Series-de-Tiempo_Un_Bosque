#!/usr/bin/env node
// Figuras SVG del simulacro (M12) del cap. 5: tamaño, recorte, contenedor, nombre accesible y tamaño real de su texto,
// a 1200, 800 y 375 px. Uso: node diagnostico/cap5/diag/graficas_simulacro.js > diagnostico/cap5/diag/graficas_simulacro.out
const { Chrome, espera } = require('./chrome');
const BASE = process.env.BASE || 'http://127.0.0.1:8765/capitulo-5-sarima.html';
(async () => {
  const c = await Chrome.lanzar(9278);
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable');
    for (const [w, h, dsf, mob] of [[1200, 1000, 1, false], [800, 1000, 1, false], [375, 812, 2, true]]) {
      await c.enviar('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: dsf, mobile: mob });
      await c.enviar('Page.navigate', { url: BASE + '#modulo-12' });
      await espera(600);
      await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined'", 30000);
      await c.evalua('document.fonts.ready.then(() => 1)');
      await c.evalua('loadModule(12), 1'); await espera(1200);
      // Empezar para que aparezcan caso y preguntas, si hace falta
      await c.evalua(`(() => { const b = document.querySelector('.simulacro-empezar'); if (b) b.click(); return 1; })()`); await espera(800);
      const r = await c.evalua(`[...document.querySelectorAll('#main-content .simulacro svg')].map((s, i) => {
        const r = s.getBoundingClientRect(); const vb = s.viewBox && s.viewBox.baseVal;
        let p = s.parentElement, cont = null; while (p) { const ox = getComputedStyle(p).overflowX; if (ox !== 'visible') { cont = { cls: String(p.className).slice(0, 40), ox, cw: p.clientWidth, sw: p.scrollWidth }; break; } p = p.parentElement; }
        const textos = [...s.querySelectorAll('text')];
        const tam = textos.map(t => t.getBoundingClientRect().height).filter(x => x > 0);
        const guion = textos.map(t => t.textContent).filter(x => /^-\\d|^-\\./.test(x));
        return { i, w: Math.round(r.width), h: Math.round(r.height), right: Math.round(r.right), vbW: vb ? vb.width : null,
          escala: vb && vb.width ? Math.round(r.width / vb.width * 100) / 100 : null, cont,
          role: s.getAttribute('role'), aria: s.getAttribute('aria-label'), title: s.querySelector('title')?.textContent || null,
          nTextos: textos.length, textoMinPx: tam.length ? Math.round(Math.min(...tam) * 10) / 10 : null, guion: guion.slice(0, 5),
          rotulo: (s.closest('figure')?.querySelector('figcaption')?.textContent || '').slice(0, 60) };
      })`);
      console.log(`\n### ${w} px · innerWidth ${await c.evalua('innerWidth')} · docSw ${await c.evalua('document.documentElement.scrollWidth')}`);
      r.forEach(x => console.log(JSON.stringify(x)));
    }
    console.log('\neventos:', JSON.stringify(c.eventos));
  } finally { await c.cerrar(); }
})().then(() => process.exit(0)).catch(e => { console.error(e); process.exit(1); });
