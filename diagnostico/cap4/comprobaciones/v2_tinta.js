#!/usr/bin/env node
// ¿Algún lienzo del cap. 4 queda en blanco tras cambiar de estado? Mide la tinta de cada lienzo (píxeles no transparentes)
// 300 ms y 1500 ms después de cada cambio, a 1200, 800 y 375 px, en el árbol (8766) y en HEAD (8767).
const fs = require('fs'); const path = require('path');
const { Chrome, espera } = require('../diag/chrome');
const PTO = process.env.PTO || '8766';
const SIMS = {
  'nilo-y-diferencia': [['select', 0, ['0', '1', '2']]],
  'escalon-vs-raiz': [['range', 0, [0, 100, 300]]],
  'identificacion-nilo': [['select', 0, ['0', '1', '2']]],
  'explorador-modelos': [['range', 1, [0, 1, 2]]],
  'traza-auto-arima': [['range', 0, [1, 9, 18]], ['check', 0, [true, false]]],
  'sobrediferenciacion': [['range', 0, [0, 1, 2, 3]]],
  'forma-pronostico': [['select', 0, ['d0', 'd1', 'd1_deriva', 'd2']]],
  'pesos-psi-sigma': [['range', 0, [1, 15, 30]]],
  'trm-identificacion': [['select', 0, ['0', '1']]],
  'trm-abanico': [['range', 0, [1, 24, 36]]],
  'puente-estacional': [['select', 0, ['no', 'si']]],
};
const MOD = { 'nilo-y-diferencia': 1, 'escalon-vs-raiz': 3, 'identificacion-nilo': 4, 'explorador-modelos': 6, 'traza-auto-arima': 7, 'sobrediferenciacion': 8, 'forma-pronostico': 9, 'pesos-psi-sigma': 9, 'trm-identificacion': 10, 'trm-abanico': 10, 'puente-estacional': 10 };
const TINTA = sim => `(() => [...document.querySelector('[data-simulador="${sim}"]').querySelectorAll('canvas')].map(cv => {
  const w = cv.width, h = cv.height; if (!w || !h) return { w, h, tinta: -1 };
  const d = cv.getContext('2d', { willReadFrequently: true }).getImageData(0, 0, w, h).data; let n = 0; for (let k = 3; k < d.length; k += 4) if (d[k] > 0) n++;
  const ch = Chart.getChart(cv); return { w, h, tinta: Math.round(1e4 * n / (w * h)) / 1e4, hayChart: !!ch, a: ch ? [Math.round(ch.chartArea.width), Math.round(ch.chartArea.height)] : null };
}))()`;
async function main() {
  const c = await Chrome.lanzar(Number(process.env.CDP || 9288));
  const malos = []; let total = 0;
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable');
    for (const [ancho, alto, dsf, mob] of [[1200, 1000, 1, false], [800, 1000, 1, false], [375, 812, 2, true]]) {
      await c.enviar('Emulation.setDeviceMetricsOverride', { width: ancho, height: alto, deviceScaleFactor: dsf, mobile: mob });
      await c.enviar('Page.navigate', { url: `http://127.0.0.1:${PTO}/capitulo-4-modelos-arima.html#modulo-1` });
      await espera(600);
      await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined' && typeof renderMathInElement === 'function'", 30000);
      await c.evalua('document.fonts.ready.then(() => 1)');
      // sin desactivar la animación: es lo que ve el estudiante
      for (const [sim, controles] of Object.entries(SIMS)) {
        await c.evalua(`loadModule(${MOD[sim]}), 1`); await espera(1300);
        const t0 = await c.evalua(TINTA(sim)); total++;
        t0.forEach((t, i) => { if (!(t.tinta > 0.01)) malos.push({ ancho, sim, estado: 'inicial', lienzo: i, cuando: '1300ms', t }); });
        for (const [tipo, idx, valores] of controles) {
          for (const v of valores) {
            await c.evalua(`(() => { const r = document.querySelector('[data-simulador="${sim}"]'); const els = r.querySelectorAll('input[type=range], select, input[type=checkbox]');
              const sel = ${JSON.stringify(tipo)} === 'range' ? r.querySelectorAll('input[type=range]')[${idx}] : ${JSON.stringify(tipo)} === 'select' ? r.querySelectorAll('select')[${idx}] : r.querySelectorAll('input[type=checkbox]')[${idx}];
              if (${JSON.stringify(tipo)} === 'check') { sel.checked = ${JSON.stringify(v)}; sel.dispatchEvent(new Event('change', { bubbles: true })); }
              else { sel.value = ${JSON.stringify(v)}; sel.dispatchEvent(new Event(${JSON.stringify(tipo)} === 'select' ? 'change' : 'input', { bubbles: true })); } return 1; })()`);
            await espera(300);
            const a = await c.evalua(TINTA(sim)); await espera(1200); const b = await c.evalua(TINTA(sim)); total++;
            [[a, '300ms'], [b, '1500ms']].forEach(([arr, cuando]) => arr.forEach((t, i) => { if (!(t.tinta > 0.01)) malos.push({ ancho, sim, estado: `${tipo}${idx}=${v}`, lienzo: i, cuando, t }); }));
          }
        }
      }
    }
  } finally { await c.cerrar(); }
  console.log(`PTO ${PTO}: ${total} estados medidos, lienzos en blanco: ${malos.length}`);
  malos.slice(0, 30).forEach(m => console.log(JSON.stringify(m)));
}
main().then(() => process.exit(0)).catch(e => { console.error(e.stack); process.exit(1); });
