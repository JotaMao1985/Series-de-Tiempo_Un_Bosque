#!/usr/bin/env node
// R2 del capítulo 2 · capturas y medidas de los capítulos 2 a 6 a 1200, 800 y 375 px.
// Chrome sin ventana por CDP (cliente de ../diag/chrome.js). Lee por HTTP, nunca file://.
//
// Uso (servidor en :8731 sirviendo Htmls_Series/):
//   node diagnostico/cap2/comprobaciones/r2_capturas.js <etiqueta> [caps] [--sin-capturas] [--anchos=1200,800,375]
//   etiqueta: 'antes' | 'despues' | …   caps: '2,3,4,5,6' (por defecto, los cinco)
// Deja capturas/r2/<etiqueta>/capN-mM-<simulador>[-estado]-<ancho>.png y
// capturas/r2/medidas-<etiqueta>.json (lo resume r2_resumen.py).
const fs = require('fs');
const path = require('path');
const { Chrome, espera } = require('../diag/chrome');

const ARGS = process.argv.slice(2);
const ETIQUETA = ARGS.find(a => !a.startsWith('--') && !/^[\d,]+$/.test(a)) || 'despues';
const CAPS = (ARGS.find(a => /^[\d,]+$/.test(a)) || '2,3,4,5,6').split(',').map(Number);
const SIN_CAPTURAS = ARGS.includes('--sin-capturas');
const ANCHOS = (ARGS.find(a => a.startsWith('--anchos=')) || '--anchos=1200,800,375').slice(9).split(',').map(Number);
const PUERTO = Number(process.env.PUERTO || 9271);
const SERVIDOR = process.env.SERVIDOR || 'http://localhost:8731/';
const ARCHIVO = {
  2: 'capitulo-2-estacionariedad-acf-pacf.html', 3: 'capitulo-3-modelos-ar-ma-arma.html',
  4: 'capitulo-4-modelos-arima.html', 5: 'capitulo-5-sarima.html', 6: 'capitulo-6-pronostico-evaluacion.html'
};
const R2 = path.resolve(__dirname, '..', 'capturas', 'r2');
const OUT = path.join(R2, ETIQUETA);

// ---------------------------------------------------------------- en página
const AYUDANTES = `
window.__r1 = x => Math.round(x * 10) / 10;
window.__medirGrafico = function (cv) {
  const r1 = window.__r1;
  const ch = Chart.getChart(cv);
  const r = cv.getBoundingClientRect();
  const info = { aria: cv.getAttribute('aria-label'), w: r1(r.width), h: r1(r.height) };
  if (!ch) return info;
  info.tipo = ch.config.type;
  info.datasets = ch.data.datasets.map(d => ({ label: d.label, type: d.type || ch.config.type,
    color: Array.isArray(d.borderColor) ? 'varios' : d.borderColor,
    bg: Array.isArray(d.backgroundColor) ? 'varios' : d.backgroundColor, n: (d.data || []).length }));
  const lg = ch.legend;
  info.legend = { items: lg && lg.legendItems ? lg.legendItems.map(x => ({ t: x.text, ps: x.pointStyle || null, dash: (x.lineDash || []).length ? 1 : 0 })) : [],
    h: lg ? r1(lg.height) : 0, lineas: lg && lg.lineWidths ? lg.lineWidths.length : 0,
    cortada: !!(lg && lg.lineWidths && lg.lineWidths.some(w => w > lg.width + 0.5)) };
  info.area = { w: r1(ch.chartArea.width), h: r1(ch.chartArea.height) };
  const ctx = ch.ctx;
  info.escalas = Object.values(ch.scales).map(s => {
    const e = { id: s.id, type: s.type, title: s.options.title && s.options.title.display ? s.options.title.text : null,
      min: s.min, max: s.max,
      ticks: s.ticks.map(t => t.label).filter(x => x !== '' && x != null).map(String).slice(0, 60) };
    if (s.isHorizontal()) {
      const items = s.getLabelItems ? s.getLabelItems(ch.chartArea) : [];
      const cajas = items.map(it => {
        ctx.save(); ctx.font = it.font.string;
        const lab = Array.isArray(it.label) ? it.label.join(' ') : String(it.label);
        const w = ctx.measureText(lab).width; ctx.restore();
        const x = it.options.translation[0];
        const al = it.options.textAlign;
        const left = al === 'left' ? x : al === 'right' ? x - w : x - w / 2;
        return { lab, left: r1(left), right: r1(left + w), rot: it.options.rotation || 0 };
      }).filter(c => c.lab !== '').sort((a, b) => a.left - b.left);
      let minGap = Infinity; const solapes = [];
      for (let i = 1; i < cajas.length; i++) {
        const g = cajas[i].left - cajas[i - 1].right;
        minGap = Math.min(minGap, g);
        if (g < 3 && !cajas[i].rot) solapes.push(cajas[i - 1].lab + '|' + cajas[i].lab + ' (' + r1(g) + ' px)');
      }
      e.minGap = cajas.length > 1 ? r1(minGap) : null;
      e.solapes = solapes;
      e.fuera = cajas.filter(c => !c.rot && (c.left < -1 || c.right > r.width + 1)).map(c => c.lab);
    } else {
      e.tieneCero = s.ticks.some(t => t.value === 0);
      e.cruzaCero = s.min < 0 && s.max > 0;
    }
    return e;
  });
  if (ch.config.type === 'bar') {
    info.rectas = ch.data.datasets.filter(d => (d.type || 'bar') === 'line').map(d => ({ label: d.label, valor: d.data[0], color: d.borderColor }));
  }
  return info;
};
true;
`;

const MEDIDAS = `(() => {
  const W = window.innerWidth;
  const mc = mainContent;
  const r1 = window.__r1;
  const canv = [...mc.querySelectorAll('canvas')].map((cv, i) => Object.assign({ i,
    sim: (cv.closest('[data-simulador]') || {dataset:{}}).dataset.simulador || (cv.closest('.quiz') ? 'quiz' : null) }, window.__medirGrafico(cv)));
  const katex = [...mc.querySelectorAll('.katex-display')].map((d, i) => {
    const k = d.querySelector('.katex');
    const cont = d.closest('.formula, .definition, .note, .warning, .exercise, .simulador') || d.parentElement;
    return { i, sw: k ? k.scrollWidth : 0, cw: d.clientWidth, dentro: String(cont.className).split(' ')[0],
      pista: getComputedStyle(cont).backgroundImage !== 'none' || getComputedStyle(d).backgroundImage !== 'none',
      txt: d.textContent.replace(/\\s+/g, ' ').slice(0, 60) };
  }).filter(x => x.sw > x.cw + 1);
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
      txt: (el.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 50) });
  });
  const tablas = [...mc.querySelectorAll('table')].map((t, i) => {
    const r = t.getBoundingClientRect();
    return { i, sw: t.scrollWidth, cw: t.clientWidth, display: getComputedStyle(t).display, ox: getComputedStyle(t).overflowX,
      fuera: r1(r.right - mR), pista: getComputedStyle(t).backgroundImage !== 'none',
      cab: [...t.querySelectorAll('th')].slice(0, 6).map(th => th.textContent.trim().slice(0, 18)).join(' | ') };
  });
  const sims = [...mc.querySelectorAll('[data-simulador]')].map(s => {
    const lect = s.querySelector('.simulador-lectura');
    const cont = s.querySelector('.simulador-controles');
    return { sim: s.dataset.simulador, w: r1(s.getBoundingClientRect().width),
      columnas: cont ? getComputedStyle(cont).gridTemplateColumns : null,
      controles: cont ? [...cont.children].map(k => ({ w: r1(k.getBoundingClientRect().width), h: r1(k.getBoundingClientRect().height),
        txt: k.textContent.replace(/\\s+/g, ' ').trim().slice(0, 40) })) : [],
      lectura: lect ? { ariaLive: lect.getAttribute('aria-live'), txt: lect.textContent.replace(/\\s+/g, ' ').trim().slice(0, 300) } : null };
  });
  return { modulo: currentModuleId, innerWidth: W, docSw: document.documentElement.scrollWidth,
    areaW: mc.clientWidth, recortados, canv, katex, tablas, sims };
})()`;

// Estados de los simuladores del capítulo 2 (los mismos que revisó el diagnóstico)
const ESTADOS_CAP2 = {
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
    await espera(100);
  }
  await espera(200);
}

async function capturar(c, sel, archivo, { padre = null, indice = 0 } = {}) {
  if (SIN_CAPTURAS) return null;
  const rect = await c.evalua(`(() => {
    let el = document.querySelectorAll(${JSON.stringify(sel)})[${indice}];
    if (!el) return null;
    ${padre ? `el = el.closest(${JSON.stringify(padre)}) || el;` : ''}
    el.scrollIntoView({ behavior: 'instant', block: 'start' });
    let e = mainContent; while (e) { e.scrollLeft = 0; e = e.parentElement; }
    const r = el.getBoundingClientRect();
    return { x: r.left + window.scrollX, y: r.top + window.scrollY, w: r.width, h: r.height };
  })()`);
  if (!rect || !rect.w || !rect.h) return null;
  await espera(150);
  const pad = 6;
  const r = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
    clip: { x: Math.max(0, rect.x - pad), y: Math.max(0, rect.y - pad), width: rect.w + 2 * pad, height: Math.min(rect.h + 2 * pad, 6000), scale: 1 } });
  fs.writeFileSync(path.join(OUT, archivo), Buffer.from(r.data, 'base64'));
  return archivo;
}

async function cargarModulo(c, n) {
  await c.evalua(`loadModule(${n}), 'ok'`);
  await espera(900);
  await c.evalua(`(() => { let e = mainContent; while (e) { e.scrollLeft = 0; e = e.parentElement; } window.scrollTo({top:0, behavior:'instant'}); return 1; })()`);
  await espera(150);
}

const QUITAR_FIJOS = `(() => { if (!document.getElementById('quitar-fijos')) { const st = document.createElement('style'); st.id = 'quitar-fijos';
  st.textContent = 'header.usta-header{position:static!important} #sidebarToggle,#scrollToTopBtn{visibility:hidden!important}'; document.head.appendChild(st); } return 1; })()`;

const ESTADO_SIM = sim => `(() => {
  const raiz = document.querySelector('[data-simulador="${sim}"]');
  const p = raiz.querySelector('.simulador-lectura');
  return { lectura: p ? p.textContent.replace(/\\s+/g, ' ').trim() : null,
    graficos: [...raiz.querySelectorAll('canvas')].map(cv => window.__medirGrafico(cv)) };
})()`;

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const c = await Chrome.lanzar(PUERTO);
  const salida = { etiqueta: ETIQUETA, fecha: new Date().toISOString(), caps: {} };
  try {
    await c.enviar('Page.enable');
    await c.enviar('Runtime.enable');
    await c.enviar('Log.enable');
    const modos = ANCHOS.map(w => w === 375
      ? { nombre: '375', width: 375, height: 812, dsf: 2, mobile: true }
      : { nombre: String(w), width: w, height: 1000, dsf: 1, mobile: false });
    for (const cap of CAPS) {
      const sal = salida.caps[cap] = { medidas: {}, estados: {}, eventos: [] };
      for (const modo of modos) {
        c.contexto = `cap${cap} carga ${modo.nombre}`;
        await c.enviar('Emulation.setDeviceMetricsOverride', { width: modo.width, height: modo.height,
          deviceScaleFactor: modo.dsf, mobile: modo.mobile });
        await c.enviar('Page.navigate', { url: 'about:blank' });
        await espera(200);
        await c.enviar('Page.navigate', { url: SERVIDOR + ARCHIVO[cap] + '?r2=' + Date.now() + '#modulo-1' });
        await espera(600);
        await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined' && typeof renderMathInElement === 'function' && document.querySelector('#content-area > *')", 30000);
        await c.evalua('document.fonts.ready.then(() => 1)');
        await c.evalua(AYUDANTES);
        await espera(300);
        const nMod = await c.evalua('courseData.modules.length');
        sal.medidas[modo.nombre] = {};
        sal.estados[modo.nombre] = {};
        for (let n = 1; n <= nMod; n++) {
          c.contexto = `cap${cap} M${n} ${modo.nombre}`;
          await cargarModulo(c, n);
          const med = await c.evalua(MEDIDAS);
          sal.medidas[modo.nombre][n] = med;
          await c.evalua(QUITAR_FIJOS);
          await espera(100);
          for (const s of med.sims) {
            const sim = s.sim;
            const tieneLienzo = med.canv.some(k => k.sim === sim);
            if (!tieneLienzo) continue;
            await capturar(c, `[data-simulador="${sim}"]`, `cap${cap}-m${n}-${sim}-${modo.nombre}.png`);
            if (cap === 2 && ESTADOS_CAP2[sim]) {
              sal.estados[modo.nombre][`${sim}:inicial`] = await c.evalua(ESTADO_SIM(sim));
              for (const [estado, acciones] of ESTADOS_CAP2[sim]) {
                c.contexto = `cap${cap} M${n} ${modo.nombre} ${sim}:${estado}`;
                await aplicar(c, sim, acciones);
                await capturar(c, `[data-simulador="${sim}"]`, `cap${cap}-m${n}-${sim}-${estado}-${modo.nombre}.png`);
                sal.estados[modo.nombre][`${sim}:${estado}`] = await c.evalua(ESTADO_SIM(sim));
              }
              await cargarModulo(c, n); await c.evalua(QUITAR_FIJOS);
            }
          }
          const nq = await c.evalua(`document.querySelectorAll('.quiz-grafico').length`);
          for (let q = 0; q < nq; q++) {
            await capturar(c, '.quiz-grafico', `cap${cap}-m${n}-quiz-grafico${q + 1}-${modo.nombre}.png`, { indice: q, padre: '.quiz-pregunta' });
          }
          // Lienzos sueltos (fuera de simulador y de quiz), si los hay
          const sueltos = med.canv.filter(k => !k.sim);
          for (const k of sueltos) {
            await capturar(c, '#content-area canvas', `cap${cap}-m${n}-lienzo${k.i}-${modo.nombre}.png`, { indice: k.i, padre: '.grafico-wrapper' });
          }
          if (cap === 2) {
            for (const k of med.katex) {
              await capturar(c, '#content-area .katex-display', `cap${cap}-m${n}-formula${k.i}-${modo.nombre}.png`, { indice: k.i, padre: '.definition, .note, .warning, .formula' });
            }
            const nPartes = await c.evalua(`document.querySelectorAll('#content-area .formula-partes').length`);
            for (let q = 0; q < nPartes; q++) {
              await capturar(c, '#content-area .formula-partes', `cap${cap}-m${n}-formula-partes${q}-${modo.nombre}.png`, { indice: q, padre: '.definition, .note, .warning, .formula' });
            }
            for (const t of med.tablas) {
              await capturar(c, '#content-area table', `cap${cap}-m${n}-tabla${t.i}-${modo.nombre}.png`, { indice: t.i });
            }
          }
          console.log(`  cap${cap} ${modo.nombre} M${n}: ${med.canv.length} lienzos, docSw ${med.docSw}/${med.innerWidth}, recortados ${med.recortados.length}`);
        }
      }
      sal.eventos = c.eventos.filter(e => !/favicon/.test(e.txt));
      c.eventos = [];
    }
  } finally {
    await c.cerrar();
  }
  fs.writeFileSync(path.join(R2, `medidas-${ETIQUETA}.json`), JSON.stringify(salida, null, 1));
  const ev = Object.entries(salida.caps).map(([k, v]) => `cap${k}: ${v.eventos.length}`).join(' · ');
  console.log('listo; eventos de consola (sin favicon): ' + ev);
}
main().then(() => process.exit(0)).catch(e => { console.error('✗ ' + e.stack); process.exit(1); });
