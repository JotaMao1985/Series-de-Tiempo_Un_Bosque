#!/usr/bin/env node
// Regresión de las leyendas nuevas del armazón (crearGraficoLinea) en los caps. 2, 3, 5 y 6 (y el 4): para cada
// lienzo de cada módulo, en el estado inicial y moviendo cada control un paso a la vez, guarda leyenda (texto, forma
// de la muestra, trazo), nº de conjuntos de datos, área de dibujo y si el lienzo tiene tinta. Se corre sobre la versión
// de HEAD (servidor 8767) y sobre el árbol (8766) y se comparan con v2_regresion_compara.py.
// Uso: BASE=http://127.0.0.1:8766/capitulo-2-estacionariedad-acf-pacf.html ETIQ=nuevo-cap2 ANCHO=1200 node v2_regresion.js
const fs = require('fs');
const path = require('path');
const { Chrome, espera } = require('../diag/chrome');

const BASE = process.env.BASE;
const ETIQ = process.env.ETIQ;
const ANCHO = Number(process.env.ANCHO || 1200);
const PUERTO = Number(process.env.PUERTO || 9280);
const OUT = path.join(__dirname, 'v2_regresion_' + ETIQ + '-' + ANCHO + '.json');

const AYUDA = `
window.__leer = function () {
  const r1 = x => Math.round(x * 10) / 10;
  return [...mainContent.querySelectorAll('canvas')].map((cv, i) => {
    const ch = Chart.getChart(cv);
    const o = { i, sim: cv.closest('[data-simulador]')?.dataset.simulador || (cv.closest('.quiz') ? 'quiz' : (cv.closest('[class*=mapa]') ? 'mapa' : null)),
      w: r1(cv.getBoundingClientRect().width), h: r1(cv.getBoundingClientRect().height), aria: cv.getAttribute('aria-label') };
    if (!ch) { o.sinChart = true; return o; }
    o.tipo = ch.config.type;
    o.nDatasets = ch.data.datasets.length;
    o.datasets = ch.data.datasets.map(d => ({ label: d.label, tipo: d.type || ch.config.type, dash: d.borderDash || null, fill: d.fill === undefined ? null : (typeof d.fill === 'object' ? 'obj' : d.fill), showLine: d.showLine, ps: d.pointStyle || null, n: (d.data || []).length }));
    const lg = ch.legend;
    o.legend = { display: ch.options.plugins.legend.display !== false,
      items: lg && lg.legendItems ? lg.legendItems.map(x => ({ text: x.text, ps: x.pointStyle, dash: x.lineDash || null, lw: x.lineWidth, hidden: x.hidden,
        fill: typeof x.fillStyle === 'string' ? x.fillStyle : '(obj)', stroke: typeof x.strokeStyle === 'string' ? x.strokeStyle : '(obj)' })) : [],
      h: lg ? r1(lg.height) : 0, lineas: lg && lg.lineWidths ? lg.lineWidths.length : 0,
      boxWidth: ch.options.plugins.legend.labels.boxWidth, pointStyleWidth: ch.options.plugins.legend.labels.pointStyleWidth,
      usePointStyle: ch.options.plugins.legend.labels.usePointStyle };
    o.area = { w: r1(ch.chartArea.width), h: r1(ch.chartArea.height) };
    // ¿tiene tinta?
    try {
      const ctx = cv.getContext('2d'); const w = cv.width, h = cv.height;
      const dat = ctx.getImageData(0, 0, w, h).data; let n = 0;
      for (let k = 3; k < dat.length; k += 4) if (dat[k] > 0) n++;
      o.tinta = Math.round(1e4 * n / (w * h)) / 1e4;
      // y dentro del área de dibujo
      const a = ch.chartArea; const dpr = cv.width / cv.getBoundingClientRect().width;
      let m = 0, tot = 0;
      for (let yy = Math.floor(a.top * dpr); yy < Math.floor(a.bottom * dpr); yy += 2)
        for (let xx = Math.floor(a.left * dpr); xx < Math.floor(a.right * dpr); xx += 2) { tot++; if (dat[(yy * w + xx) * 4 + 3] > 0) m++; }
      o.tintaArea = tot ? Math.round(1e4 * m / tot) / 1e4 : 0;
    } catch (e) { o.tinta = 'err ' + e.message; }
    return o;
  });
};
window.__controles = function (sim) {
  const raiz = document.querySelector('[data-simulador="' + sim + '"]');
  return [...raiz.querySelectorAll('input[type=range], select, input[type=checkbox]')].map((el, k) => ({ k, tipo: el.type || el.tagName.toLowerCase(),
    min: el.min, max: el.max, step: el.step, valor: el.type === 'checkbox' ? el.checked : el.value,
    opciones: el.tagName === 'SELECT' ? [...el.options].map(o => o.value) : null }));
};
window.__poner = function (sim, k, v) {
  const raiz = document.querySelector('[data-simulador="' + sim + '"]');
  const el = [...raiz.querySelectorAll('input[type=range], select, input[type=checkbox]')][k];
  if (el.type === 'checkbox') { el.checked = v; el.dispatchEvent(new Event('change', { bubbles: true })); }
  else { el.value = v; el.dispatchEvent(new Event(el.tagName === 'SELECT' ? 'change' : 'input', { bubbles: true })); }
  return 1;
};
true;
`;

async function main() {
  const c = await Chrome.lanzar(PUERTO);
  const res = { base: BASE, ancho: ANCHO, modulos: {}, eventos: null };
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable'); await c.enviar('Log.enable');
    await c.enviar('Emulation.setDeviceMetricsOverride', { width: ANCHO, height: ANCHO < 500 ? 812 : 1000, deviceScaleFactor: ANCHO < 500 ? 2 : 1, mobile: ANCHO < 500 });
    await c.enviar('Page.navigate', { url: BASE + '#modulo-1' });
    await espera(700);
    await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined' && typeof renderMathInElement === 'function'", 30000);
    await c.evalua('document.fonts.ready.then(() => 1)');
    await c.evalua(`(() => { Chart.defaults.animation = false; Chart.defaults.animations = {}; return 1; })()`);
    await c.evalua(AYUDA);
    const nMod = await c.evalua(`document.querySelectorAll('template[id^="module-"]').length`);
    res.nMod = nMod;
    for (let n = 1; n <= nMod; n++) {
      c.contexto = `M${n}`;
      await c.evalua(`loadModule(${n}), 1`);
      await espera(900);
      const base = await c.evalua('window.__leer()');
      const sims = await c.evalua(`[...mainContent.querySelectorAll('[data-simulador]')].map(s => s.dataset.simulador)`);
      const estados = { inicial: base };
      for (const sim of sims) {
        const ctrls = await c.evalua(`window.__controles(${JSON.stringify(sim)})`);
        for (const ct of ctrls) {
          let valores = [];
          if (ct.tipo === 'range') {
            const mn = Number(ct.min), mx = Number(ct.max), v0 = Number(ct.valor);
            valores = [...new Set([mn, mx, (mn + mx) / 2])].filter(v => v !== v0);
          } else if (ct.tipo === 'select') valores = ct.opciones.filter(v => v !== ct.valor);
          else if (ct.tipo === 'checkbox') valores = [!ct.valor];
          for (const v of valores) {
            await c.evalua(`window.__poner(${JSON.stringify(sim)}, ${ct.k}, ${JSON.stringify(v)})`);
            await espera(180);
            estados[`${sim}|c${ct.k}=${v}`] = await c.evalua('window.__leer()');
          }
          // restituir el valor inicial
          await c.evalua(`window.__poner(${JSON.stringify(sim)}, ${ct.k}, ${JSON.stringify(ct.valor)})`);
          await espera(150);
        }
      }
      res.modulos[n] = estados;
      console.log(`  ${ETIQ} ${ANCHO} M${n}: ${Object.keys(estados).length} estados`);
    }
    res.eventos = c.eventos;
  } finally { await c.cerrar(); }
  fs.writeFileSync(OUT, JSON.stringify(res));
  console.log('listo', OUT, 'eventos', res.eventos.length);
  if (res.eventos.length) console.log(JSON.stringify(res.eventos.slice(0, 10), null, 1));
}
main().then(() => process.exit(0)).catch(e => { console.error('✗ ' + e.stack); process.exit(1); });
