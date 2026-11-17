#!/usr/bin/env node
// Verificador independiente R2: gráficos del quiz del M9 del cap. 2 (rótulos, banda, aria-label) a 1200, 800 y 375 px.
const fs = require('fs'); const path = require('path');
const { Chrome, espera } = require('../diag/chrome');
const BASE = process.argv[2] || 'http://127.0.0.1:8731';
const ETQ = process.argv[3] || 'ahora';
const OUT = path.resolve(__dirname, '..', 'capturas', 'r2v', 'quiz');
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const c = await Chrome.lanzar(9295);
  const res = {};
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable'); await c.enviar('Log.enable');
    for (const [w, m] of [[1200, false], [800, false], [375, true]]) {
      await c.enviar('Emulation.setDeviceMetricsOverride', { width: w, height: m ? 812 : 1000, deviceScaleFactor: m ? 2 : 1, mobile: m });
      await c.enviar('Page.navigate', { url: `${BASE}/capitulo-2-estacionariedad-acf-pacf.html#modulo-9` });
      await espera(700);
      await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined'", 30000);
      await c.evalua('document.fonts.ready.then(() => 1)');
      await c.evalua(`(() => { Chart.defaults.animation = false; const s = document.createElement('style'); s.textContent = 'header.usta-header{position:static!important} #sidebarToggle,#scrollToTopBtn{visibility:hidden!important}'; document.head.appendChild(s); loadModule(9); return 1; })()`);
      await espera(1500);
      res[w] = await c.evalua(`({ quizzes: document.querySelectorAll('[data-quiz]').length, graficos: [...document.querySelectorAll('.quiz-grafico')].map(g => { const cv = g.querySelector('canvas'); const ch = Chart.getChart(cv);
        return { aria: cv.getAttribute('aria-label'), acf: ch ? ch.data.datasets[0].data.map(x => Math.round(x*100)/100) : null,
        rotulosX: ch ? ch.scales.x.getLabelItems(ch.chartArea).map(it => String(it.label)) : null,
        rotulosY: ch ? ch.scales.y.getLabelItems(ch.chartArea).map(it => String(it.label)) : null,
        anchoBarra: ch ? Math.round(ch.getDatasetMeta(0).data[0].width*10)/10 : null,
        banda: ch ? ch.data.datasets.filter(d => d.type === 'line').map(d => d.data[0]) : null,
        enunciado: g.closest('.quiz-pregunta').querySelector('.quiz-enunciado').textContent.slice(0, 80) }; }) })`);
      const n = res[w].graficos.length;
      for (let k = 0; k < n; k++) {
        const r = await c.evalua(`(() => { const el = document.querySelectorAll('.quiz-pregunta .quiz-grafico')[${k}].closest('.quiz-pregunta'); el.scrollIntoView({behavior:'instant'}); const b = el.getBoundingClientRect(); return {x:b.left+scrollX,y:b.top+scrollY,w:b.width,h:Math.min(b.height,700)}; })()`);
        await espera(150);
        const s = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: r.x, y: r.y, width: r.w, height: r.h, scale: 1 } });
        fs.writeFileSync(path.join(OUT, `${ETQ}-quiz${k + 1}-${w}.png`), Buffer.from(s.data, 'base64'));
      }
    }
  } finally { await c.cerrar(); }
  fs.writeFileSync(path.join(__dirname, `v2_quiz_${ETQ}.json`), JSON.stringify({ res, eventos: c.eventos }, null, 1));
  console.log(JSON.stringify({ res, eventos: c.eventos }, null, 1));
})().then(() => process.exit(0)).catch(e => { console.error(e); process.exit(1); });
