#!/usr/bin/env node
// Revisión visual del cap. 2: capturas por elemento, estados extremos de los
// simuladores y medidas, a 1200, 800 y 375 px. Chrome sin ventana por CDP.
// Uso: node diagnostico/cap2/diag/revisa.js   (servidor en :8731 sirviendo Htmls_Series/)
const fs = require('fs');
const path = require('path');
const { Chrome, espera } = require('./chrome');

const DIAG = __dirname;
const OUT = path.resolve(DIAG, '..', 'capturas');
const BASE = process.env.BASE || 'http://localhost:8731/capitulo-2-estacionariedad-acf-pacf.html';
const PUERTO = 9263;

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
    primero: (d.data || [])[0], pr: d.pointRadius }));
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
const ESTADOS = {
  'explorador-acf-pacf': ['ruido_blanco', 'caminata', 'log_airpassengers', 'd_log_airpassengers', 'dd_log_airpassengers', 'trm', 'd_trm']
    .map(v => [v, [['select', 0, v]]]),
  'ar1-phi': [
    ['phi0', [['range', 0, 0], ['check', 0, false]]],
    ['phi050', [['range', 0, 0.5], ['check', 0, false]]],
    ['phi095', [['range', 0, 0.95], ['check', 0, false]]],
    ['phi100', [['range', 0, 1], ['check', 0, false]]],
    ['phi105', [['range', 0, 1.05], ['check', 0, false]]],
    ['phi0-dif', [['range', 0, 0], ['check', 0, true]]],
    ['phi100-dif', [['range', 0, 1], ['check', 0, true]]],
    ['phi105-dif', [['range', 0, 1.05], ['check', 0, true]]],
  ],
  'diferenciacion': ['trm', 'log_airpassengers', 'caminata'].flatMap(s => [0, 1, 2, 3].map(d =>
    [`${s}-d${d}`, [['select', 0, s], ['range', 0, d]]])),
  'box-cox': [['lam-1', [['range', 0, -1]]], ['lam-030', [['range', 0, -0.3]]], ['lam0', [['range', 0, 0]]],
    ['lam050', [['range', 0, 0.5]]], ['lam2', [['range', 0, 2]]]],
};

async function aplicar(c, sim, acciones) {
  for (const [tipo, idx, val] of acciones) {
    await c.evalua(`(() => {
      const raiz = document.querySelector('[data-simulador="${sim}"]');
      if ('${tipo}' === 'range') { const i = raiz.querySelectorAll('input[type=range]')[${idx}]; i.value = ${JSON.stringify(val)}; i.dispatchEvent(new Event('input', { bubbles: true })); }
      if ('${tipo}' === 'select') { const s = raiz.querySelectorAll('select')[${idx}]; s.value = ${JSON.stringify(val)}; s.dispatchEvent(new Event('change', { bubbles: true })); }
      if ('${tipo}' === 'check') { const k = raiz.querySelectorAll('input[type=checkbox]')[${idx}]; if (k.checked !== ${JSON.stringify(val)}) { k.checked = ${JSON.stringify(val)}; k.dispatchEvent(new Event('change', { bubbles: true })); } }
      return 1; })()`);
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
      for (let n = 1; n <= 9; n++) {
        await c.evalua(PONER_FIJOS);
        await cargarModulo(c, n);
        const med = await c.evalua(MEDIDAS(modo.width));
        salida.medidas[modo.nombre][n] = med;
        // Vista real (cabecera fija incluida) sobre el primer simulador, en teléfono y a 800
        if (modo.width < 1200 && med.sims.length) {
          await c.evalua(`(() => { document.querySelector('[data-simulador] canvas').scrollIntoView({behavior:'instant', block:'center'}); return 1; })()`);
          await espera(300);
          await vistaPantalla(c, `m${n}-vista-${modo.nombre}.png`);
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
        // Fórmulas en display que desbordan (las cinco primeras)
        for (const k of med.katex.slice(0, 5)) {
          await capturar(c, '.katex-display', `m${n}-formula${k.i}-${modo.nombre}.png`, { indice: k.i, padre: '.definition, .note, .warning, .formula' });
        }
        // Tablas que desbordan
        for (const t of med.tablas) {
          await capturar(c, 'table', `m${n}-tabla${t.i}-${modo.nombre}.png`, { indice: t.i });
        }
        console.log(`  ${modo.nombre} M${n}: ${med.sims.length} sim, ${med.canv.length} lienzos, ${med.katex.length} fórmulas que desbordan, docSw ${med.docSw}`);
      }
    }
    salida.eventos = c.eventos;
  } finally {
    await c.cerrar();
  }
  fs.writeFileSync(path.join(DIAG, 'medidas.json'), JSON.stringify(salida, null, 1));
  console.log('listo; eventos de consola:', salida.eventos ? salida.eventos.length : 'n/d');
}
main().then(() => process.exit(0)).catch(e => { console.error('✗ ' + e.stack); process.exit(1); });
