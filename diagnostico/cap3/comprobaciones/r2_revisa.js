#!/usr/bin/env node
// R2 · revisión visual del cap. 3 tras la ronda (copia de diag/graficas_revisa.js con otra carpeta de capturas,
// sin las capturas de fórmulas y tablas, que esta ronda no toca). Original: (adaptado de diagnostico/cap2/diag/revisa.js): capturas por elemento, estados extremos de los
// simuladores y medidas, a 1200, 800 y 375 px. Chrome sin ventana por CDP.
// Uso: node diagnostico/cap3/comprobaciones/r2_revisa.js   (BASE=http://127.0.0.1:<puerto>/capitulo-3-modelos-ar-ma-arma.html)
const fs = require('fs');
const path = require('path');
const { Chrome, espera } = require('../diag/chrome');

const DIAG = __dirname;
const OUT = path.resolve(DIAG, '..', 'capturas', 'r2');
const BASE = process.env.BASE || 'http://127.0.0.1:8773/capitulo-3-modelos-ar-ma-arma.html';
const PUERTO = Number(process.env.CDP || 9283);

// ---------------------------------------------------------------- en página
// Medidas de un lienzo con Chart.js: escalas, rótulos solapados, leyenda, área.
const AYUDANTES = `
window.__r1 = x => Math.round(x * 10) / 10;
window.__medirGrafico = function (cv) {
  const r1 = window.__r1;
  const ch = Chart.getChart(cv);
  const r = cv.getBoundingClientRect();
  const info = { aria: cv.getAttribute('aria-label'), role: cv.getAttribute('role'), w: r1(r.width), h: r1(r.height), right: r1(r.right) };
  if (!ch) return info;
  info.tipo = ch.config.type;
  info.datasets = ch.data.datasets.map((d, k) => ({ label: d.label, type: d.type || ch.config.type, color: d.borderColor, bg: d.backgroundColor,
    bw: d.borderWidth, dash: d.borderDash || null, visible: ch.isDatasetVisible(k), n: (d.data || []).length,
    primero: (d.data || [])[0], pr: d.pointRadius,
    datos: (d.data || []).length <= 30 ? (d.data || []).map(v => typeof v === 'number' ? Math.round(v * 1e4) / 1e4 : v) : null,
    rango: (d.data || []).length && typeof d.data[0] === 'number' ? [Math.min(...d.data), Math.max(...d.data)] : null }));
  // Puntos de dispersión: ¿dentro del área de dibujo?
  if (ch.config.type === 'scatter') {
    info.puntos = ch.data.datasets.map((d, k) => ({ k, d })).filter(o => (o.d.data || []).length <= 3 && !o.d.showLine || o.d.label === '').map(o => {
      const meta = ch.getDatasetMeta(o.k);
      return { label: o.d.label, datos: o.d.data, px: meta.data.map(p => [r1(p.x), r1(p.y)]),
        dentro: meta.data.map(p => p.x >= ch.chartArea.left - 0.5 && p.x <= ch.chartArea.right + 0.5 && p.y >= ch.chartArea.top - 0.5 && p.y <= ch.chartArea.bottom + 0.5),
        recorte: meta.data.map(p => { const rr = (o.d.pointRadius || 0) + (o.d.borderWidth || 0);
          return Math.min(p.x - ch.chartArea.left, ch.chartArea.right - p.x, p.y - ch.chartArea.top, ch.chartArea.bottom - p.y) < rr; }) };
    });
  }
  const lg = ch.legend;
  info.legend = { display: ch.options.plugins.legend.display !== false,
    items: lg && lg.legendItems ? lg.legendItems.map(x => x.text) : [], h: lg ? r1(lg.height) : 0,
    lineas: lg && lg.lineWidths ? lg.lineWidths.length : 0 };
  info.area = { w: r1(ch.chartArea.width), h: r1(ch.chartArea.height), left: r1(ch.chartArea.left), right: r1(ch.chartArea.right) };
  const ctx = ch.ctx;
  info.escalas = Object.values(ch.scales).map(s => {
    const e = { id: s.id, type: s.type, title: s.options.title?.display ? s.options.title.text : null,
      min: s.min, max: s.max, nTicks: s.ticks.length,
      ticks: s.ticks.map(t => t.label).filter(x => x !== '' && x != null).map(String).slice(0, 40),
      valoresTicks: s.ticks.map(t => t.value).slice(0, 40),
      w: r1(s.width), h: r1(s.height) };
    // Solapes de rótulos en el eje horizontal
    if (s.isHorizontal()) {
      const items = s.getLabelItems ? s.getLabelItems(ch.chartArea) : [];
      const cajas = items.map(it => {
        ctx.save(); ctx.font = it.font.string;
        const lab = Array.isArray(it.label) ? it.label.join(' ') : String(it.label);
        const w = ctx.measureText(lab).width; ctx.restore();
        const x = it.options.translation[0];
        const al = it.options.textAlign;
        const left = al === 'left' ? x : al === 'right' ? x - w : x - w / 2;
        return { lab, left: r1(left), right: r1(left + w), font: it.font.string };
      }).sort((a, b) => a.left - b.left);
      let minGap = Infinity; const solapes = [];
      for (let i = 1; i < cajas.length; i++) {
        const g = cajas[i].left - cajas[i - 1].right;
        minGap = Math.min(minGap, g);
        if (g < 3) solapes.push(cajas[i - 1].lab + '|' + cajas[i].lab + ' (' + r1(g) + ' px)');
      }
      e.minGap = cajas.length > 1 ? r1(minGap) : null;
      e.solapes = solapes;
      e.fuenteTicks = cajas[0]?.font || null;
      e.fuenteCargada = cajas[0] ? document.fonts.check(cajas[0].font) : null;
      e.fuera = cajas.filter(c => c.left < 0 || c.right > r.width + 1).map(c => c.lab);
    } else {
      const items = s.getLabelItems ? s.getLabelItems(ch.chartArea) : [];
      e.fuenteTicks = items[0]?.font?.string || null;
      e.fuenteCargada = items[0] ? document.fonts.check(items[0].font.string) : null;
    }
    return e;
  });
  // Bandas del correlograma: rectas de referencia (datasets de línea dentro de un gráfico de barras)
  if (ch.config.type === 'bar') {
    info.rectas = ch.data.datasets.map((d, k) => ({ k, d })).filter(o => (o.d.type || 'bar') === 'line').map(o => {
      const meta = ch.getDatasetMeta(o.k);
      const xs = meta.data.map(p => p.x);
      return { label: o.d.label, valor: o.d.data[0], color: o.d.borderColor,
        x0: r1(Math.min(...xs)), x1: r1(Math.max(...xs)), y: r1(meta.data[0]?.y) };
    });
    info.barras = ch.data.datasets.filter(d => (d.type || 'bar') === 'bar').map(d => ({ label: d.label, color: d.backgroundColor,
      max: Math.max(...d.data.map(Math.abs)), n: d.data.length }));
    // ancho de una barra en píxeles
    const m0 = ch.getDatasetMeta(0);
    info.anchoBarra = m0.data[0] ? r1(m0.data[0].width) : null;
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
  const katex = [...mc.querySelectorAll('.katex-display')].map((d, i) => {
    const k = d.querySelector('.katex');
    const cont = d.closest('.formula, .definition, .note, .warning, .simulador') || d.parentElement;
    const r = d.getBoundingClientRect();
    return { i, sw: k ? k.scrollWidth : 0, cw: d.clientWidth, contCw: cont.clientWidth, ox: getComputedStyle(d).overflowX,
      right: r1(r.right), dentro: cont.className.split(' ')[0],
      txt: d.textContent.replace(/\\s+/g, ' ').slice(0, 70) };
  }).filter(x => x.sw > x.cw + 1);
  const katexLinea = [...mc.querySelectorAll('.katex')].filter(k => !k.closest('.katex-display')).map(k => {
    const r = k.getBoundingClientRect();
    const host = k.closest('p, li, td, th, h4, .simulador-intro, label, span') || k.parentElement;
    const hr = host.getBoundingClientRect();
    return { right: r1(r.right), w: r1(r.width), hostRight: r1(hr.right), txt: k.textContent.slice(0, 50) };
  }).filter(x => x.w && x.right > x.hostRight + 1);
  const tablas = [...mc.querySelectorAll('table')].map((t, i) => ({ i, sw: t.scrollWidth, cw: t.clientWidth,
    parentCw: t.parentElement.clientWidth, caption: (t.caption?.textContent || '').trim().slice(0, 60) })).filter(t => t.sw > t.cw + 1 || t.sw > t.parentCw + 1);
  const desbordan = [];
  mc.querySelectorAll('*').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width && r.right > W + 1) {
      let p = el.parentElement, externo = true;
      while (p && p !== mc) { if (p.getBoundingClientRect().right > W + 1) { externo = false; break; } p = p.parentElement; }
      if (externo) desbordan.push({ tag: el.tagName, cls: String(el.className).slice(0, 50), right: r1(r.right),
        txt: (el.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 50) });
    }
  });
  // Lo que asoma por la derecha de <main> (overflow:hidden) sin un contenedor desplazable que lo recoja
  const main = document.getElementById('main-content');
  const mR = main.getBoundingClientRect().right;
  const recortados = [];
  mc.querySelectorAll('*').forEach(el => {
    const r = el.getBoundingClientRect();
    if (!r.width || r.right <= mR + 1) return;
    let p = el.parentElement, recogido = false, externo = true;
    while (p && p !== main) {
      const ox = getComputedStyle(p).overflowX;
      const pr = p.getBoundingClientRect().right;
      if (pr > mR + 1) { externo = false; break; }
      if (ox === 'auto' || ox === 'scroll' || ox === 'hidden') { recogido = true; break; }
      p = p.parentElement;
    }
    if (externo && !recogido) recortados.push({ tag: el.tagName, cls: String(el.className).slice(0, 40), sobra: r1(r.right - mR),
      txt: (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 50) });
  });
  const sims = [...mc.querySelectorAll('[data-simulador]')].map(s => {
    const h4 = s.querySelector('h4');
    const hijos = h4 ? [...h4.childNodes].filter(n => n.nodeType === 1 || n.textContent.trim()).length : 0;
    const lect = s.querySelector('.simulador-lectura');
    const r = s.getBoundingClientRect();
    return { sim: s.dataset.simulador, w: r1(r.width), right: r1(r.right), sw: s.scrollWidth, cw: s.clientWidth,
      h4: h4 ? { txt: h4.textContent.trim(), h: r1(h4.getBoundingClientRect().height), hijos } : null,
      lectura: lect ? { ariaLive: lect.getAttribute('aria-live'), role: lect.getAttribute('role'),
        txt: lect.textContent.replace(/\\s+/g, ' ').trim(), h: r1(lect.getBoundingClientRect().height) } : null,
      controles: [...s.querySelectorAll('input, select')].map(inp => ({ tipo: inp.type || inp.tagName, id: inp.id,
        label: inp.id ? (document.querySelector('label[for="' + inp.id + '"]')?.textContent || null) : (inp.closest('label')?.textContent || null),
        min: inp.min, max: inp.max, step: inp.step, value: inp.value, w: r1(inp.getBoundingClientRect().width) })),
      etiquetas: [...s.querySelectorAll('.grafico-etiqueta')].map(e => e.textContent.replace(/\\s+/g, ' ').trim()),
      alturas: [...s.querySelectorAll('.grafico-wrapper')].map(g => r1(g.getBoundingClientRect().height)) };
  });
  return { modulo: currentModuleId, ancho: W, innerWidth: window.innerWidth,
    docSw: document.documentElement.scrollWidth, mainW: Math.round(mc.getBoundingClientRect().width),
    mainCw: mc.clientWidth, mainRight: r1(mR), recortados, canv, katex, katexLinea, tablas, desbordan, sims };
})()`;

// Estados por simulador: [nombre, [acciones]] con acción = ['range', índice, valor] | ['select', índice, valor] | ['check', índice, bool]
// Acción: ['range', índice, valor] | ['select', índice, valor] | ['check', índice, bool] | ['click', texto del botón]
const R = (...pares) => pares.map(([i, v]) => ['range', i, v]);
const ESTADOS = {
  'panel-ar-teorico': ['ar1_pos', 'ar1_neg', 'ar2_real', 'ar2_comp'].map(v => [v, [['select', 0, v]]]),
  'triangulo-ar2': [
    ['ruido', R([0, 0], [1, 0])],
    ['ar2comp-1.40-0.75', R([0, 1.4], [1, -0.75])],
    ['casi-raiz-0.50-0.49', R([0, 0.5], [1, 0.49])],
    ['raiz-unitaria-0.50-0.50', R([0, 0.5], [1, 0.5])],
    ['borde-phi2-1', R([0, 0], [1, -1])],
    ['esquina-2.0-1.0', R([0, 2], [1, -1])],
    ['fuera-max-2.2-1.2', R([0, 2.2], [1, 1.2])],
    ['fuera-min-2.2-1.2', R([0, -2.2], [1, -1.2])],
    ['fuera-complejo-1.4-1.05', R([0, 1.4], [1, -1.05])],
  ],
  'panel-ma-teorico': ['ma1_pos', 'ma1_neg', 'ma2'].map(v => [v, [['select', 0, v]]]),
  'rho1-theta-ma1': [
    ['theta0', R([0, 0])], ['theta0.05', R([0, 0.05])], ['theta0.20', R([0, 0.2])], ['theta0.50', R([0, 0.5])],
    ['theta1', R([0, 1])], ['theta-1', R([0, -1])], ['theta5', R([0, 5])], ['theta-5', R([0, -5])], ['theta-0.25', R([0, -0.25])],
  ],
  'dualidad-psi-pi': [
    ['ar1-0.8-h1', R([0, 0.8], [1, 0], [2, 1])],
    ['ar1-0.8-h12', R([0, 0.8], [1, 0], [2, 12])],
    ['redundante-0.5-0.5', R([0, 0.5], [1, -0.5], [2, 4])],
    ['theta1-frontera', R([0, 0.8], [1, 1], [2, 4])],
    ['theta1.05', R([0, 0.8], [1, 1.05], [2, 4])],
    ['theta2-phi0.95', R([0, 0.95], [1, 2], [2, 12])],
    ['theta-2-phi-0.95', R([0, -0.95], [1, -2], [2, 12])],
    ['phi0.95-theta0', R([0, 0.95], [1, 0], [2, 12])],
  ],
  'laboratorio-arma': [
    ['T60', R([4, 60])],
    ['T1000', R([4, 1000])],
    ['redundante-0.5-0.5', R([0, 0.5], [1, 0], [2, -0.5], [3, 0], [4, 200])],
    ['casi-redundante-0.5-0.45', R([0, 0.5], [1, 0], [2, -0.45], [3, 0], [4, 200])],
    ['phi1-1.0', R([0, 1.0], [1, 0], [2, 0], [3, 0], [4, 200])],
    ['phi1-1.5', R([0, 1.5], [1, 0], [2, 0], [3, 0], [4, 200])],
    ['phi1-0.95-T1000', R([0, 0.95], [1, 0], [2, 0], [3, 0], [4, 1000])],
    ['ar2-1.5-0.95', R([0, 1.5], [1, -0.95], [2, 0], [3, 0], [4, 200])],
    ['ma-no-invertible-1.5', R([0, 0], [1, 0], [2, 1.5], [3, 0], [4, 200])],
    ['max-todo', R([0, 1.5], [1, 0.95], [2, 1.5], [3, 0.95], [4, 1000])],
    ['inicial-otra-realizacion', [...R([0, 0.7], [1, 0], [2, 0.5], [3, 0], [4, 200]), ['click', 'Otra realización']]],
  ],
  'teorica-vs-muestral': ['ar1_pos', 'ma1_pos', 'arma11'].map(v => [v, [['select', 0, v]]]),
  'diagnostico-residuales': ['arma10', 'arma20', 'arma30', 'arma21'].map(v => [v, [['select', 0, v]]]),
  'manchas-transformada': ['cruda', 'raiz'].map(v => [v, [['select', 0, v]]]),
  'manchas-impulso': [['h1', R([0, 1])], ['h6', R([0, 6])], ['h11', R([0, 11])], ['h24', R([0, 24])]],
};

async function aplicar(c, sim, acciones) {
  for (const [tipo, idx, val] of acciones) {
    const ix = JSON.stringify(idx), v = JSON.stringify(val);
    const cuerpo = {
      range: `const i = raiz.querySelectorAll('input[type=range]')[${ix}]; i.value = ${v}; i.dispatchEvent(new Event('input', { bubbles: true }));`,
      select: `const s = raiz.querySelectorAll('select')[${ix}]; s.value = ${v}; s.dispatchEvent(new Event('change', { bubbles: true }));`,
      check: `const k = raiz.querySelectorAll('input[type=checkbox]')[${ix}]; if (k.checked !== ${v}) { k.checked = ${v}; k.dispatchEvent(new Event('change', { bubbles: true })); }`,
      click: `[...raiz.querySelectorAll('button')].find(x => x.textContent.trim() === ${ix}).click();`,
    }[tipo];
    await c.evalua(`(() => { const raiz = document.querySelector('[data-simulador="${sim}"]'); ${cuerpo} return 1; })()`);
    await espera(120);
  }
  await espera(250);
}

async function capturar(c, sel, archivo, { padre = null, indice = 0 } = {}) {
  const rect = await c.evalua(`(() => {
    let el = document.querySelectorAll(${JSON.stringify(sel)})[${indice}];
    if (!el) return null;
    ${padre ? `el = el.closest(${JSON.stringify(padre)}) || el;` : ''}
    el.scrollIntoView({ behavior: 'instant', block: 'start' });
    const r = el.getBoundingClientRect();
    return { x: r.left + window.scrollX, y: r.top + window.scrollY, w: r.width, h: r.height };
  })()`);
  if (!rect) return null;
  await espera(200);
  const pad = 6;
  const r = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
    clip: { x: Math.max(0, rect.x - pad), y: Math.max(0, rect.y - pad), width: rect.w + 2 * pad, height: rect.h + 2 * pad, scale: 1 } });
  fs.writeFileSync(path.join(OUT, archivo), Buffer.from(r.data, 'base64'));
  return archivo;
}

async function vistaPantalla(c, archivo) {
  const v = await c.enviar('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(OUT, archivo), Buffer.from(v.data, 'base64'));
}

async function cargarModulo(c, n) {
  c.contexto = `M${n}`;
  await c.evalua(`loadModule(${n}), 'ok'`);
  await espera(1100);
  // scrollIntoView() puede desplazar en horizontal un ancestro con overflow:hidden (main) al capturar una tabla
  await c.evalua(`(() => { let e = mainContent; while (e) { e.scrollLeft = 0; e = e.parentElement; } return 1; })()`);
  await c.evalua(`window.scrollTo({top:0, behavior:'instant'}), 1`);
  await espera(200);
}

const QUITAR_FIJOS = `(() => { if (!document.getElementById('quitar-fijos')) { const st = document.createElement('style'); st.id = 'quitar-fijos';
  st.textContent = 'header.usta-header{position:static!important} #sidebarToggle,#scrollToTopBtn{visibility:hidden!important}'; document.head.appendChild(st); } return 1; })()`;
const PONER_FIJOS = `(() => { document.getElementById('quitar-fijos')?.remove(); return 1; })()`;

const LECTURA_SIM = sim => `(() => {
  const raiz = document.querySelector('[data-simulador="${sim}"]');
  const p = raiz.querySelector('.simulador-lectura');
  return { lectura: p ? p.textContent.replace(/\\s+/g, ' ').trim() : null,
    outputs: [...raiz.querySelectorAll('output')].map(o => o.textContent),
    graficos: [...raiz.querySelectorAll('canvas')].map(cv => window.__medirGrafico(cv)) };
})()`;

// ---------------------------------------------------------------- principal
async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const c = await Chrome.lanzar(PUERTO);
  const salida = { base: BASE, fecha: new Date().toISOString(), medidas: {}, estados: {}, eventos: null };
  try {
    await c.enviar('Page.enable');
    await c.enviar('Runtime.enable');
    await c.enviar('Log.enable');
    await c.enviar('Network.enable');

    // 1) Fuentes del módulo de arranque
    // (la prueba de fuentes del módulo de arranque vive en fuentes.js)

    // 2) Recorrido por anchos
    const modos = [
      { nombre: '1200', width: 1200, height: 1000, dsf: 1, mobile: false },
      { nombre: '800', width: 800, height: 1000, dsf: 1, mobile: false },
      { nombre: '375', width: 375, height: 812, dsf: 2, mobile: true },
    ];
    for (const modo of modos) {
      c.contexto = `carga ${modo.nombre}`;
      await c.enviar('Emulation.setDeviceMetricsOverride', { width: modo.width, height: modo.height,
        deviceScaleFactor: modo.dsf, mobile: modo.mobile });
      await c.enviar('Page.navigate', { url: BASE + '#modulo-1' });
      await espera(600);
      await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined' && typeof renderMathInElement === 'function'", 30000);
      await c.evalua('document.fonts.ready.then(() => 1)');
      await c.evalua(`(() => { Chart.defaults.animation = false; Chart.defaults.animations = {}; return 1; })()`);
      await c.evalua(AYUDANTES);
      await espera(400);
      salida.medidas[modo.nombre] = {};
      salida.estados[modo.nombre] = {};
      for (let n = 1; n <= 11; n++) {
        await c.evalua(PONER_FIJOS);
        await cargarModulo(c, n);
        const med = await c.evalua(MEDIDAS(modo.width));
        salida.medidas[modo.nombre][n] = med;
        // Vista real (cabecera fija incluida) sobre el primer simulador, en teléfono y a 800
        if (modo.width < 1200) {
          const conLienzo = await c.evalua(`[...document.querySelectorAll('[data-simulador], .quiz-grafico')].filter(e => e.querySelector('canvas') || e.tagName === 'CANVAS' || e.classList.contains('quiz-grafico')).length`);
          for (let k = 0; k < conLienzo; k++) {
            await c.evalua(`(() => { const e = [...document.querySelectorAll('[data-simulador], .quiz-grafico')].filter(e => e.querySelector('canvas'))[${k}]; (e.querySelector('.simulador-controles') || e).scrollIntoView({behavior:'instant', block:'start'}); window.scrollBy(0, -70); return 1; })()`);
            await espera(300);
            await vistaPantalla(c, `m${n}-vista${k + 1}-${modo.nombre}.png`);
          }
        }
        await c.evalua(QUITAR_FIJOS);
        await espera(150);
        for (const s of med.sims) {
          const sim = s.sim;
          await capturar(c, `[data-simulador="${sim}"]`, `m${n}-${sim}-${modo.nombre}.png`);
          salida.estados[modo.nombre][`${sim}:inicial`] = await c.evalua(LECTURA_SIM(sim));
          for (const [estado, acciones] of (ESTADOS[sim] || [])) {
            await aplicar(c, sim, acciones);
            await capturar(c, `[data-simulador="${sim}"]`, `m${n}-${sim}-${estado}-${modo.nombre}.png`);
            salida.estados[modo.nombre][`${sim}:${estado}`] = await c.evalua(LECTURA_SIM(sim));
          }
          if (ESTADOS[sim]) { await cargarModulo(c, n); await c.evalua(QUITAR_FIJOS); }
        }
        // Gráficos del quiz
        const nq = await c.evalua(`document.querySelectorAll('.quiz-grafico').length`);
        for (let q = 0; q < nq; q++) {
          await capturar(c, '.quiz-grafico', `m${n}-quiz-grafico${q + 1}-${modo.nombre}.png`, { indice: q, padre: '.quiz-pregunta' });
        }
        console.log(`  ${modo.nombre} M${n}: ${med.sims.length} sim, ${med.canv.length} lienzos, ${med.katex.length} fórmulas que desbordan, docSw ${med.docSw}`);
      }
    }
    salida.eventos = c.eventos;
  } finally {
    await c.cerrar();
  }
  fs.writeFileSync(path.join(DIAG, 'r2_medidas.json'), JSON.stringify(salida, null, 1));
  console.log('listo; eventos de consola:', salida.eventos ? salida.eventos.length : 'n/d');
}
main().then(() => process.exit(0)).catch(e => { console.error('✗ ' + e.stack); process.exit(1); });
