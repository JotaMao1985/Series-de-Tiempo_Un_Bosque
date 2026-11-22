#!/usr/bin/env node
// Verificación independiente de la R2 del cap. 4 (gráficas y simuladores). Adaptado de
// diagnostico/cap4/diag/graficas_revisa.js (la revisión que dio graficas.md): mismas medidas, más estados
// y detalle de la leyenda (forma de cada muestra). Chrome sin ventana por CDP, puerto 9280.
// Uso: BASE=http://127.0.0.1:8766/capitulo-4-modelos-arima.html node v2_revisa.js
const fs = require('fs');
const path = require('path');
const { Chrome, espera } = require('../diag/chrome');

const AQUI = __dirname;
const OUT = path.join(AQUI, '../capturas/v2');
const BASE = process.env.BASE || 'http://127.0.0.1:8766/capitulo-4-modelos-arima.html';
const PUERTO = 9280;
const CAPTURAR = process.env.CAPTURAR !== '0';
const SOLO = process.env.SOLO ? process.env.SOLO.split(',') : null;      // lista de simuladores
const ANCHOS = process.env.ANCHOS ? process.env.ANCHOS.split(',') : ['1200', '800', '375'];
const SALIDA = process.env.SALIDA || path.join(AQUI, 'v2_medidas.json');

const AYUDANTES = `
window.__r1 = x => Math.round(x * 10) / 10;
window.__medirGrafico = function (cv) {
  const r1 = window.__r1;
  const ch = Chart.getChart(cv);
  const r = cv.getBoundingClientRect();
  const info = { aria: cv.getAttribute('aria-label'), role: cv.getAttribute('role'), w: r1(r.width), h: r1(r.height) };
  if (!ch) return info;
  info.tipo = ch.config.type;
  info.datasets = ch.data.datasets.map((d, k) => ({ k, label: d.label, tipo: d.type || ch.config.type, color: d.borderColor, bg: d.backgroundColor,
    bw: d.borderWidth, dash: d.borderDash || null, visible: ch.isDatasetVisible(k), n: (d.data || []).length, clip: d.clip, showLine: d.showLine,
    pointStyle: d.pointStyle, pr: d.pointRadius, fill: d.fill,
    rango: (() => { const v = (d.data || []).map(x => x && typeof x === 'object' ? x.y : x).filter(x => x !== null && x !== undefined);
      if (!v.length) return null; if (v.some(x => typeof x !== 'number' || !Number.isFinite(x))) return [null, null]; return [Math.min(...v), Math.max(...v)]; })(),
    nulos: (d.data || []).filter(x => x === null).length }));
  const lg = ch.legend;
  const lab = ch.options.plugins.legend.labels || {};
  info.legend = { display: ch.options.plugins.legend.display !== false,
    items: lg && lg.legendItems ? lg.legendItems.map(x => ({ text: x.text, fill: typeof x.fillStyle === 'string' ? x.fillStyle : '(obj)',
      stroke: typeof x.strokeStyle === 'string' ? x.strokeStyle : '(obj)', lw: x.lineWidth, dash: x.lineDash || null, ps: x.pointStyle, hidden: x.hidden, di: x.datasetIndex })) : [],
    h: lg ? r1(lg.height) : 0, lineas: lg && lg.lineWidths ? lg.lineWidths.length : 0,
    opciones: { usePointStyle: lab.usePointStyle, boxWidth: lab.boxWidth, boxHeight: lab.boxHeight, pointStyleWidth: lab.pointStyleWidth } };
  info.area = { w: r1(ch.chartArea.width), h: r1(ch.chartArea.height), top: r1(ch.chartArea.top), bottom: r1(ch.chartArea.bottom), left: r1(ch.chartArea.left), right: r1(ch.chartArea.right) };
  info.legendBox = lg ? { top: r1(lg.top), bottom: r1(lg.bottom) } : null;
  const ctx = ch.ctx;
  info.escalas = Object.values(ch.scales).map(s => {
    const e = { id: s.id, type: s.type, title: s.options.title?.display ? s.options.title.text : null,
      min: s.min, max: s.max, nTicks: s.ticks.length,
      ticks: s.ticks.map(t => Array.isArray(t.label) ? t.label.join('|') : t.label).map(x => x == null ? '' : String(x)),
      valoresTicks: s.ticks.map(t => t.value),
      w: r1(s.width), h: r1(s.height), rot: s.labelRotation,
      guion: s.ticks.map(t => String(t.label)).filter(x => /^-\\d|^-\\./.test(x)),
      rejillaCero: typeof s.options.grid.color === 'function',
      autoSkip: s.options.ticks.autoSkip };
    if (s.type === 'category') e.nCategorias = s.getLabels().length;
    if (s.isHorizontal()) {
      const items = s.getLabelItems ? s.getLabelItems(ch.chartArea) : [];
      const cajas = items.map(it => {
        ctx.save(); ctx.font = it.font.string;
        const lab2 = Array.isArray(it.label) ? it.label.join(' ') : String(it.label);
        const w = Math.max(...(Array.isArray(it.label) ? it.label : [it.label]).map(t => ctx.measureText(String(t)).width)); ctx.restore();
        const x = it.options.translation[0];
        const al = it.options.textAlign;
        const left = al === 'left' ? x : al === 'right' ? x - w : x - w / 2;
        return { lab: lab2, left: r1(left), right: r1(left + w) };
      }).sort((a, b) => a.left - b.left);
      let minGap = Infinity; const solapes = [];
      for (let i = 1; i < cajas.length; i++) {
        const g = cajas[i].left - cajas[i - 1].right;
        minGap = Math.min(minGap, g);
        if (g < 3) solapes.push(cajas[i - 1].lab + '|' + cajas[i].lab + ' (' + r1(g) + ' px)');
      }
      e.minGap = cajas.length > 1 ? r1(minGap) : null;
      e.solapes = solapes;
      e.nRotulados = cajas.length;
      e.fuera = cajas.filter(c => c.left < -1 || c.right > r.width + 1).map(c => c.lab);
    }
    return e;
  });
  {
    const rr = v => Array.isArray(v) ? Math.max(0, ...v) : (v || 0);
    info.puntos = ch.data.datasets.map((d, k) => ({ k, d })).filter(o => ch.isDatasetVisible(o.k) && (o.d.showLine === false || rr(o.d.pointRadius) >= 4)).map(o => {
      const meta = ch.getDatasetMeta(o.k);
      const filas = [];
      meta.data.forEach((p, j) => {
        const rad = (Array.isArray(o.d.pointRadius) ? o.d.pointRadius[j] : (o.d.pointRadius ?? 3)) || 0;
        if (!rad || p.skip || p.y == null || Number.isNaN(p.y)) return;
        const margen = Math.min(p.x - ch.chartArea.left, ch.chartArea.right - p.x, p.y - ch.chartArea.top, ch.chartArea.bottom - p.y);
        filas.push({ j, x: r1(p.x), y: r1(p.y), margen: r1(margen), rad, pasaElBorde: margen < rad });
      });
      return { label: o.d.label, k: o.k, clip: o.d.clip, n: filas.length, pasan: filas.filter(f => f.pasaElBorde), todos: filas.length <= 8 ? filas : undefined };
    });
  }
  if (ch.config.type === 'bar') {
    info.rectas = ch.data.datasets.map((d, k) => ({ k, d })).filter(o => (o.d.type || 'bar') === 'line').map(o => {
      return { label: o.d.label, valor: o.d.data[0], color: o.d.borderColor, dash: o.d.borderDash || null };
    });
    info.barras = ch.data.datasets.filter(d => (d.type || 'bar') === 'bar').map(d => ({ label: d.label,
      colores: Array.isArray(d.backgroundColor) ? Array.from(new Set(d.backgroundColor)) : d.backgroundColor,
      n: d.data.length, minBarLength: d.minBarLength }));
  }
  return info;
};
true;
`;

const MEDIDAS = ancho => `(() => {
  const W = ${ancho};
  const mc = mainContent;
  const r1 = window.__r1;
  const canv = [...mc.querySelectorAll('canvas')].map((cv, i) => Object.assign({ i,
    sim: cv.closest('[data-simulador]')?.dataset.simulador || (cv.closest('.quiz') ? 'quiz' : null) }, window.__medirGrafico(cv)));
  const sims = [...mc.querySelectorAll('[data-simulador]')].map(s => {
    const h4 = s.querySelector('h4');
    const ico = h4 ? h4.querySelector('i') : null;
    const lect = s.querySelector('.simulador-lectura');
    const r = s.getBoundingClientRect();
    return { sim: s.dataset.simulador, w: r1(r.width), sw: s.scrollWidth, cw: s.clientWidth,
      h4: h4 ? { txt: h4.textContent.trim(), h: r1(h4.getBoundingClientRect().height),
        icono: ico ? { cls: ico.className, ancho: r1(ico.getBoundingClientRect().width),
          before: getComputedStyle(ico, '::before').content, fam: getComputedStyle(ico).fontFamily, pesoFuente: getComputedStyle(ico).fontWeight } : null } : null,
      lectura: lect ? lect.textContent.replace(/\\s+/g, ' ').trim() : null,
      alturas: [...s.querySelectorAll('.grafico-wrapper')].map(g => r1(g.getBoundingClientRect().height)) };
  });
  return { modulo: currentModuleId, ancho: W, innerWidth: window.innerWidth, docSw: document.documentElement.scrollWidth, canv, sims };
})()`;

const R = (...pares) => pares.map(([i, v]) => ['range', i, v]);
const PQD = [];
for (let pp = 0; pp <= 2; pp++) for (let dd = 0; dd <= 2; dd++) for (let qq = 0; qq <= 2; qq++) PQD.push([pp, dd, qq]);
const CAPTURA_PQD = ['000', '021', '020', '122', '111', '202', '212', '011'];
const ESTADOS = {
  'nilo-y-diferencia': ['0', '1', '2'].map(v => [`d${v}`, [['select', 0, v]]]),
  'escalon-vs-raiz': [0, 5, 100, 150, 200, 245, 250, 300].map(b => [`beta${b}`, R([0, b])]),
  'identificacion-nilo': ['0', '1', '2'].map(v => [`d${v}`, [['select', 0, v]]]),
  'explorador-modelos': PQD.map(([pp, dd, qq]) => [`pdq${pp}${dd}${qq}`, R([0, pp], [1, dd], [2, qq]),
    { captura: CAPTURA_PQD.includes(`${pp}${dd}${qq}`) }]),
  'traza-auto-arima': [
    ['paso1', R([0, 1])], ['paso9', R([0, 9])], ['paso18', R([0, 18])],
    ['exh-paso18', [['check', 0, true]]], ['exh-paso1', [['range', 0, 1]]], ['exh-paso21', [['range', 0, 21]]],
    ['exh-paso27', [['range', 0, 27]]], ['exh-paso30', [['range', 0, 30]]],
    ['exh-paso42', [['range', 0, 42]]], ['vuelve-escalonada', [['check', 0, false]]],
  ],
  'sobrediferenciacion': [0, 1, 2, 3].map(d => [`d${d}`, R([0, d])]),
  'forma-pronostico': [
    ...['d0', 'd1', 'd1_deriva', 'd2'].map(v => [v, [['select', 0, v]]]),
    ['d2-sin-bandas', [['check', 0, false]]], ['d0-sin-bandas', [['select', 0, 'd0']]],
  ],
  'pesos-psi-sigma': [1, 2, 15, 30].map(h => [`h${h}`, R([0, h])]),
  'trm-identificacion': ['0', '1'].map(v => [`d${v}`, [['select', 0, v]]]),
  'trm-abanico': [1, 12, 24, 36].map(h => [`h${h}`, R([0, h])]),
  'puente-estacional': ['no', 'si'].map(v => [v, [['select', 0, v]]]),
};

async function aplicar(c, sim, acciones) {
  for (const [tipo, idx, val] of acciones) {
    const ix = JSON.stringify(idx), v = JSON.stringify(val);
    const cuerpo = {
      range: `const i = raiz.querySelectorAll('input[type=range]')[${ix}]; i.value = ${v}; i.dispatchEvent(new Event('input', { bubbles: true }));`,
      select: `const s = raiz.querySelectorAll('select')[${ix}]; s.value = ${v}; s.dispatchEvent(new Event('change', { bubbles: true }));`,
      check: `const k = raiz.querySelectorAll('input[type=checkbox]')[${ix}]; if (k.checked !== ${v}) { k.checked = ${v}; k.dispatchEvent(new Event('change', { bubbles: true })); }`,
    }[tipo];
    await c.evalua(`(() => { const raiz = document.querySelector('[data-simulador="${sim}"]'); ${cuerpo} return 1; })()`);
    await espera(100);
  }
  await espera(200);
}

async function capturar(c, sel, archivo, { padre = null, indice = 0 } = {}) {
  if (!CAPTURAR) return null;
  const rect = await c.evalua(`(() => {
    let el = document.querySelectorAll(${JSON.stringify(sel)})[${indice}];
    if (!el) return null;
    ${padre ? `el = el.closest(${JSON.stringify(padre)}) || el;` : ''}
    el.scrollIntoView({ behavior: 'instant', block: 'start' });
    const r = el.getBoundingClientRect();
    return { x: r.left + window.scrollX, y: r.top + window.scrollY, w: r.width, h: r.height };
  })()`);
  if (!rect) return null;
  await espera(150);
  const pad = 6;
  const r = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
    clip: { x: Math.max(0, rect.x - pad), y: Math.max(0, rect.y - pad), width: rect.w + 2 * pad, height: rect.h + 2 * pad, scale: 1 } });
  fs.writeFileSync(path.join(OUT, archivo), Buffer.from(r.data, 'base64'));
  return archivo;
}

async function cargarModulo(c, n) {
  c.contexto = `M${n}`;
  await c.evalua(`loadModule(${n}), 'ok'`);
  await espera(1000);
  await c.evalua(`(() => { let e = mainContent; while (e) { e.scrollLeft = 0; e = e.parentElement; } return 1; })()`);
  await c.evalua(`window.scrollTo({top:0, behavior:'instant'}), 1`);
  await espera(150);
}

const QUITAR_FIJOS = `(() => { if (!document.getElementById('quitar-fijos')) { const st = document.createElement('style'); st.id = 'quitar-fijos';
  st.textContent = 'header.usta-header{position:static!important} #sidebarToggle,#scrollToTopBtn{visibility:hidden!important}'; document.head.appendChild(st); } return 1; })()`;
const PONER_FIJOS = `(() => { document.getElementById('quitar-fijos')?.remove(); return 1; })()`;

const LECTURA_SIM = sim => `(() => {
  const raiz = document.querySelector('[data-simulador="${sim}"]');
  const p = raiz.querySelector('.simulador-lectura');
  return { lectura: p ? p.textContent.replace(/\\s+/g, ' ').trim() : null,
    graficos: [...raiz.querySelectorAll('canvas')].map(cv => window.__medirGrafico(cv)) };
})()`;

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const c = await Chrome.lanzar(PUERTO);
  const salida = { base: BASE, fecha: new Date().toISOString(), medidas: {}, estados: {}, eventos: null };
  try {
    await c.enviar('Page.enable');
    await c.enviar('Runtime.enable');
    await c.enviar('Log.enable');
    const modos = [
      { nombre: '1200', width: 1200, height: 1000, dsf: 1, mobile: false },
      { nombre: '800', width: 800, height: 1000, dsf: 1, mobile: false },
      { nombre: '375', width: 375, height: 812, dsf: 2, mobile: true },
    ].filter(m => ANCHOS.includes(m.nombre));
    const MODS = process.env.MODULOS ? process.env.MODULOS.split(',').map(Number) : Array.from({ length: 12 }, (_, i) => i + 1);
    for (const modo of modos) {
      c.contexto = `carga ${modo.nombre}`;
      await c.enviar('Emulation.setDeviceMetricsOverride', { width: modo.width, height: modo.height, deviceScaleFactor: modo.dsf, mobile: modo.mobile });
      await c.enviar('Page.navigate', { url: BASE + '#modulo-1' });
      await espera(600);
      await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined' && typeof renderMathInElement === 'function'", 30000);
      await c.evalua('document.fonts.ready.then(() => 1)');
      await c.evalua(`(() => { Chart.defaults.animation = false; Chart.defaults.animations = {}; return 1; })()`);
      await c.evalua(AYUDANTES);
      await espera(400);
      salida.medidas[modo.nombre] = {};
      salida.estados[modo.nombre] = {};
      for (const n of MODS) {
        await c.evalua(PONER_FIJOS);
        await cargarModulo(c, n);
        const med = await c.evalua(MEDIDAS(modo.width));
        salida.medidas[modo.nombre][n] = med;
        await c.evalua(QUITAR_FIJOS);
        await espera(100);
        for (const s of med.sims) {
          const sim = s.sim;
          if (SOLO && !SOLO.includes(sim)) continue;
          await capturar(c, `[data-simulador="${sim}"]`, `m${n}-${sim}-${modo.nombre}.png`);
          salida.estados[modo.nombre][`${sim}:inicial`] = await c.evalua(LECTURA_SIM(sim));
          for (const [estado, acciones, op] of (ESTADOS[sim] || [])) {
            await aplicar(c, sim, acciones);
            if (!op || op.captura !== false) await capturar(c, `[data-simulador="${sim}"]`, `m${n}-${sim}-${estado}-${modo.nombre}.png`);
            salida.estados[modo.nombre][`${sim}:${estado}`] = await c.evalua(LECTURA_SIM(sim));
          }
          if (ESTADOS[sim]) { await cargarModulo(c, n); await c.evalua(QUITAR_FIJOS); }
        }
        const nq = await c.evalua(`document.querySelectorAll('.quiz-grafico').length`);
        for (let q = 0; q < nq; q++) {
          await capturar(c, '.quiz-grafico', `m${n}-quiz-grafico${q + 1}-${modo.nombre}.png`, { indice: q, padre: '.quiz-pregunta' });
        }
        console.log(`  ${modo.nombre} M${n}: ${med.sims.length} sim, ${med.canv.length} lienzos, docSw ${med.docSw}`);
      }
    }
    salida.eventos = c.eventos;
  } finally {
    await c.cerrar();
  }
  fs.writeFileSync(SALIDA, JSON.stringify(salida));
  console.log('listo; eventos de consola:', salida.eventos ? salida.eventos.length : 'n/d');
  if (salida.eventos && salida.eventos.length) console.log(JSON.stringify(salida.eventos.slice(0, 20), null, 1));
}
main().then(() => process.exit(0)).catch(e => { console.error('✗ ' + e.stack); process.exit(1); });
