#!/usr/bin/env node
// R2 · los dos gráficos del quiz del M10 (AUTOEVALUACIONES['cap4']) a 1200, 800 y 375 px: captura con espera larga tras
// llevarlos a la vista (en r2_revisa.js la captura del quiz salía en blanco aunque los lienzos estaban pintados), píxeles
// pintados, área de dibujo y `aria-label` completo. Uso: BASE=... CDP=9277 node r2_quiz.js
const fs = require('fs');
const path = require('path');
const { Chrome, espera } = require('../diag/chrome');
const BASE = process.env.BASE || 'http://127.0.0.1:8764/capitulo-4-modelos-arima.html';
const OUT = path.resolve(__dirname, '..', 'capturas', 'r2');
(async () => {
  const c = await Chrome.lanzar(Number(process.env.CDP || 9277));
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable');
    for (const [nombre, w, h, dsf, mobile] of [['1200', 1200, 1000, 1, false], ['800', 800, 1000, 1, false], ['375', 375, 812, 2, true]]) {
      await c.enviar('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: dsf, mobile });
      await c.enviar('Page.navigate', { url: BASE + '#modulo-1' });
      await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined' && typeof renderMathInElement === 'function'", 30000);
      await c.evalua('document.fonts.ready.then(() => 1)');
      await c.evalua(`(() => { Chart.defaults.animation = false; Chart.defaults.animations = {}; return 1; })()`);
      await c.evalua(`loadModule(10), 1`); await espera(1500);
      await c.evalua(`(() => { const st = document.createElement('style'); st.textContent = 'header.usta-header{position:static!important} #sidebarToggle,#scrollToTopBtn{visibility:hidden!important}'; document.head.appendChild(st); return 1; })()`);
      const n = await c.evalua(`document.querySelectorAll('.quiz-grafico').length`);
      for (let q = 0; q < n; q++) {
        await c.evalua(`(() => { document.querySelectorAll('.quiz-grafico')[${q}].closest('.quiz-pregunta').scrollIntoView({behavior:'instant', block:'start'}); return 1; })()`);
        await espera(1200);
        // la captura es la pantalla real, con la pregunta arriba (recortar por el recuadro del elemento salía corrido en este módulo)
        const info = await c.evalua(`(() => { const cv = document.querySelectorAll('.quiz-grafico canvas')[${q}]; const ch = Chart.getChart(cv);
          const px = cv.getContext('2d').getImageData(0, 0, cv.width, cv.height).data; let k = 0; for (let i = 3; i < px.length; i += 4) if (px[i]) k++;
          return { pintados: k, area: ch.chartArea.height, leyenda: ch.legend.legendItems.map(x => x.text), renglones: ch.legend.lineWidths.length, aria: cv.getAttribute('aria-label') }; })()`);
        const r = await c.enviar('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync(path.join(OUT, `m10-quiz-grafico${q + 1}-${nombre}.png`), Buffer.from(r.data, 'base64'));
        console.log(nombre, 'gráfico', q + 1, JSON.stringify(info));
      }
    }
    console.log('eventos de la página (sin el favicon):', JSON.stringify(c.eventos.filter(e => !/favicon/.test(e.txt))));
  } finally { await c.cerrar(); }
})().then(() => process.exit(0)).catch(e => { console.error(e); process.exit(1); });
