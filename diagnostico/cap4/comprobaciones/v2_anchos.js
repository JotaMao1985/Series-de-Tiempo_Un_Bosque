#!/usr/bin/env node
// Anchos intermedios (el barrido principal usa 1200, 800 y 375): solapes de rótulos, líneas de leyenda y área, en los
// gráficos que cambiaron de comportamiento con la R2 (ΔAICc sin salto automático, σ_h con último rótulo, traza).
const fs = require('fs'); const path = require('path');
const { Chrome, espera } = require('../diag/chrome');
const BASE = process.env.BASE || 'http://127.0.0.1:8766/capitulo-4-modelos-arima.html';
const ANCHOS = (process.env.ANCHOS || '420,480,520,560,600,640,700,767,768,900,1024,1440').split(',').map(Number);
const MIDE = `(() => [...mainContent.querySelectorAll('canvas')].map(cv => {
  const ch = Chart.getChart(cv); if (!ch) return null; const ctx = ch.ctx;
  const sim = cv.closest('[data-simulador]')?.dataset.simulador || 'quiz';
  const ejes = Object.values(ch.scales).filter(s => s.isHorizontal()).map(s => {
    const items = s.getLabelItems(ch.chartArea).map(it => { ctx.save(); ctx.font = it.font.string;
      const t = Array.isArray(it.label) ? it.label : [it.label]; const w = Math.max(...t.map(x => ctx.measureText(String(x)).width)); ctx.restore();
      const x = it.options.translation[0]; return { l: x - w / 2, r: x + w / 2, t: t.join(' ') }; }).sort((a, b) => a.l - b.l);
    let gap = Infinity; for (let i = 1; i < items.length; i++) gap = Math.min(gap, items[i].l - items[i - 1].r);
    return { id: s.id, n: items.length, n_cat: s.type === 'category' ? s.getLabels().length : null, gap: items.length > 1 ? Math.round(gap * 10) / 10 : null, rot: s.labelRotation };
  });
  return { sim, w: Math.round(cv.getBoundingClientRect().width), area: [Math.round(ch.chartArea.width), Math.round(ch.chartArea.height)],
    leyenda: ch.legend ? ch.legend.lineWidths.length : 0, tipo: ch.config.type, indexAxis: ch.options.indexAxis || 'x', ejes };
}))()`;
async function main() {
  const c = await Chrome.lanzar(9286);
  const salida = {};
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable');
    for (const w of ANCHOS) {
      await c.enviar('Emulation.setDeviceMetricsOverride', { width: w, height: 900, deviceScaleFactor: 1, mobile: w < 500 });
      await c.enviar('Page.navigate', { url: BASE + '#modulo-1' });
      await espera(600);
      await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined'", 30000);
      await c.evalua('document.fonts.ready.then(() => 1)');
      await c.evalua(`Chart.defaults.animation = false; 1`);
      salida[w] = {};
      for (const [mod, sim, acciones] of [[6, 'explorador-modelos', [['range', 1, 2], ['range', 0, 0], ['range', 2, 0]]], [6, 'explorador-modelos', [['range', 1, 1], ['range', 0, 1], ['range', 2, 1]]],
        [7, 'traza-auto-arima', []], [9, 'pesos-psi-sigma', [['range', 0, 30]]], [9, 'forma-pronostico', []], [10, 'trm-abanico', [['range', 0, 36]]], [10, 'puente-estacional', []], [3, 'escalon-vs-raiz', []]]) {
        await c.evalua(`loadModule(${mod}), 1`); await espera(900);
        for (const [tipo, idx, val] of acciones) {
          await c.evalua(`(() => { const r = document.querySelector('[data-simulador="${sim}"]'); const i = r.querySelectorAll('input[type=range]')[${idx}]; i.value = ${val}; i.dispatchEvent(new Event('input', { bubbles: true })); return 1; })()`);
          await espera(120);
        }
        await espera(250);
        const m = (await c.evalua(MIDE)).filter(x => x && x.sim === sim);
        salida[w][sim + (acciones.length && sim === 'explorador-modelos' ? (acciones[0][2] === 2 ? '@d2' : '@d1') : '')] = m;
      }
    }
  } finally { await c.cerrar(); }
  fs.writeFileSync(path.join(__dirname, 'v2_anchos.json'), JSON.stringify(salida));
  for (const w of ANCHOS) {
    for (const [k, ms] of Object.entries(salida[w])) {
      ms.forEach((m, i) => console.log(`${w} ${k} c${i} lienzo ${m.w} ${m.indexAxis} area ${m.area.join('x')} leyenda ${m.leyenda}l ` + m.ejes.map(e => `${e.id}:n${e.n}/${e.n_cat ?? '-'} gap ${e.gap}`).join(' | ')));
    }
  }
}
main().then(() => process.exit(0)).catch(e => { console.error(e.stack); process.exit(1); });
