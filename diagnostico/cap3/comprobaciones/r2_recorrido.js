#!/usr/bin/env node
// Verificador independiente de la R2 del cap. 2: recorre los capítulos 2 a 6, módulo a módulo,
// a 1200, 1024, 800 y 375 px, y mide lo que dibujan los lienzos (rótulos del eje x realmente
// pintados, solapes, rótulos fuera del lienzo, leyenda, eje y, el 0, aria-label), las tablas
// (recortadas por <main>, si llenan su caja), las fórmulas que desbordan, los títulos de los
// simuladores, las columnas de controles y la consola. Sirve para HEAD y para el árbol de trabajo.
//
// Uso: node v2_recorrido.js <BASE_URL> <etiqueta> <puerto_cdp> [capitulos=2,3,4,5,6] [anchos=1200,1024,800,375] [capturas=1]
// Salida: diagnostico/cap2/comprobaciones/v2_recorrido_<etiqueta>.json y capturas en
// diagnostico/cap2/capturas/r2v/<etiqueta>/
const fs = require('fs');
const path = require('path');
const { Chrome, espera } = require('../diag/chrome');

const [BASE, ETIQ, PUERTO_S, CAPS_S, ANCHOS_S, CAPT_S] = process.argv.slice(2);
const PUERTO = Number(PUERTO_S || 9271);
const CAPS = (CAPS_S || '2,3,4,5,6').split(',').map(Number);
const ANCHOS = (ANCHOS_S || '1200,1024,800,375').split(',').map(Number);
const CAPTURAS = CAPT_S === undefined ? true : CAPT_S === '1';
const ARCH = {
  2: 'capitulo-2-estacionariedad-acf-pacf.html', 3: 'capitulo-3-modelos-ar-ma-arma.html',
  4: 'capitulo-4-modelos-arima.html', 5: 'capitulo-5-sarima.html', 6: 'capitulo-6-pronostico-evaluacion.html'
};
const OUT = path.resolve(__dirname, '..', 'capturas', 'r2', 'recorrido-' + ETIQ);
const MODOS = {
  1200: { width: 1200, height: 1000, deviceScaleFactor: 1, mobile: false },
  1024: { width: 1024, height: 900, deviceScaleFactor: 1, mobile: false },
  800: { width: 800, height: 1000, deviceScaleFactor: 1, mobile: false },
  375: { width: 375, height: 812, deviceScaleFactor: 2, mobile: true },
};

const AYUDANTES = `
window.__r1 = x => Math.round(x * 10) / 10;
window.__medir = function (cv) {
  const r1 = window.__r1;
  const ch = Chart.getChart(cv);
  const r = cv.getBoundingClientRect();
  const o = { aria: cv.getAttribute('aria-label'), w: r1(r.width), h: r1(r.height) };
  if (!ch) return o;
  o.tipo = ch.config.type;
  o.datasets = ch.data.datasets.map(d => ({ label: d.label, type: d.type || ch.config.type,
    color: typeof d.borderColor === 'string' ? d.borderColor : null,
    bg: typeof d.backgroundColor === 'string' ? d.backgroundColor : null, n: (d.data || []).length }));
  const lg = ch.legend;
  if (lg && ch.options.plugins.legend.display !== false && lg.legendHitBoxes) {
    o.leyenda = { h: r1(lg.height), items: (lg.legendItems || []).map(x => x.text),
      fuera: lg.legendHitBoxes.filter(b => b.left < -0.5 || b.left + b.width > ch.width + 0.5).length,
      estilos: (lg.legendItems || []).map(x => x.pointStyle || 'box') };
  }
  o.area = { w: r1(ch.chartArea.width), h: r1(ch.chartArea.height) };
  const ctx = ch.ctx;
  o.escalas = Object.values(ch.scales).map(s => {
    const e = { id: s.id, type: s.type, horiz: s.isHorizontal(), titulo: s.options.title && s.options.title.display ? s.options.title.text : null,
      min: s.min, max: s.max };
    const items = s.getLabelItems ? s.getLabelItems(ch.chartArea) : [];
    const cajas = items.map(it => {
      ctx.save(); ctx.font = it.font.string;
      const lab = Array.isArray(it.label) ? it.label.join(' ') : String(it.label);
      const w = ctx.measureText(lab).width; ctx.restore();
      const x = it.options.translation[0], y = it.options.translation[1];
      const al = it.options.textAlign;
      const left = al === 'left' ? x : al === 'right' ? x - w : x - w / 2;
      return { lab, left: r1(left), right: r1(left + w), y: r1(y) };
    }).filter(c => c.lab !== '');
    e.rotulos = cajas.map(c => c.lab);
    if (s.isHorizontal()) {
      cajas.sort((a, b) => a.left - b.left);
      let min = Infinity; const sol = [];
      for (let i = 1; i < cajas.length; i++) {
        const g = cajas[i].left - cajas[i - 1].right; min = Math.min(min, g);
        if (g < 2) sol.push(cajas[i - 1].lab + '|' + cajas[i].lab + ' (' + r1(g) + ')');
      }
      e.minGap = cajas.length > 1 ? r1(min) : null; e.solapes = sol;
      e.fuera = cajas.filter(c => c.left < -0.5 || c.right > ch.width + 0.5).map(c => c.lab);
      if (s.type === 'category') e.etiquetas = s.getLabels().map(String);
    } else {
      cajas.sort((a, b) => a.y - b.y);
      const sol = [];
      for (let i = 1; i < cajas.length; i++) if (cajas[i].y - cajas[i - 1].y < 11) sol.push(cajas[i - 1].lab + '|' + cajas[i].lab);
      e.solapes = sol;
      e.tieneCero = (s.min < 0 && s.max > 0) ? cajas.some(c => /^[−-]?0(\\.0+)?$/.test(c.lab)) : null;
    }
    return e;
  });
  return o;
};
true;`;

const MEDIDAS = `(() => {
  const r1 = window.__r1;
  const mc = mainContent;
  const main = document.getElementById('main-content') || mc.parentElement;
  const mR = main.getBoundingClientRect().right;
  const canv = [...mc.querySelectorAll('canvas')].map((cv, i) => Object.assign({ i,
    sim: cv.closest('[data-simulador]') ? cv.closest('[data-simulador]').dataset.simulador : (cv.closest('.quiz-grafico') ? 'quiz' : (cv.closest('[id]') ? '#' + cv.closest('[id]').id : null)) },
    window.__medir(cv)));
  const tablas = [...mc.querySelectorAll('table')].map((t, i) => {
    const tr = t.querySelector('tr');
    const r = t.getBoundingClientRect();
    const trW = tr ? tr.getBoundingClientRect().width : 0;
    const cs = getComputedStyle(t);
    return { i, display: cs.display, cw: t.clientWidth, sw: t.scrollWidth, w: r1(r.width), trW: r1(trW),
      vacio: r1(t.clientWidth - trW), right: r1(r.right), cabecera: (t.querySelector('th') ? t.querySelector('th').textContent.trim().slice(0, 30) : ''),
      enRanking: !!t.closest('.tabla-ranking') };
  });
  const recortados = [];
  mc.querySelectorAll('*').forEach(el => {
    const r = el.getBoundingClientRect();
    if (!r.width || r.right <= mR + 1) return;
    let p = el.parentElement, recogido = false, externo = true;
    while (p && p !== main) {
      const ox = getComputedStyle(p).overflowX;
      if (p.getBoundingClientRect().right > mR + 1) { externo = false; break; }
      if (ox === 'auto' || ox === 'scroll' || ox === 'hidden') { recogido = true; break; }
      p = p.parentElement;
    }
    if (externo && !recogido) recortados.push({ tag: el.tagName, cls: String(el.className).slice(0, 40), sobra: r1(r.right - mR),
      txt: (el.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 50) });
  });
  const desplazables = [...mc.querySelectorAll('.formula, .definition, .note, .warning, .exercise, .katex-display')]
    .filter(e => e.scrollWidth > e.clientWidth + 1)
    .map(e => ({ cls: String(e.className).split(' ')[0], sw: e.scrollWidth, cw: e.clientWidth,
      txt: e.textContent.replace(/\\s+/g, ' ').trim().slice(0, 50) }));
  const partes = [...mc.querySelectorAll('.formula-partes')].map(p => {
    const hijos = [...p.querySelectorAll(':scope > .katex, :scope > span.katex')];
    const tops = [...new Set(hijos.map(h => Math.round(h.getBoundingClientRect().top)))];
    return { renglones: tops.length, partes: hijos.length, sw: p.scrollWidth, cw: p.clientWidth,
      desborda: hijos.some(h => h.getBoundingClientRect().right > p.getBoundingClientRect().right + 1),
      txt: p.textContent.replace(/\\s+/g, ' ').trim().slice(0, 40) };
  });
  const sims = [...mc.querySelectorAll('[data-simulador]')].map(s => {
    const h4 = s.querySelector('h4');
    const ctl = s.querySelector('.simulador-controles');
    const lect = s.querySelector('.simulador-lectura');
    return { sim: s.dataset.simulador, w: r1(s.getBoundingClientRect().width),
      h4: h4 ? { h: r1(h4.getBoundingClientRect().height), txt: h4.textContent.trim().slice(0, 60), display: getComputedStyle(h4).display } : null,
      columnas: ctl ? getComputedStyle(ctl).gridTemplateColumns.split(' ').filter(Boolean).length : null,
      controles: ctl ? [...ctl.children].map(k => r1(k.getBoundingClientRect().width)) : [],
      lectura: lect ? { live: lect.getAttribute('aria-live'), txt: lect.textContent.replace(/\\s+/g, ' ').trim().slice(0, 600) } : null };
  });
  return { innerWidth, docSw: document.documentElement.scrollWidth, mainW: r1(mc.getBoundingClientRect().width),
    canv, tablas, recortados, desplazables, partes, sims };
})()`;

// Cuenta las veces que una lectura que ya es región viva cambia al abrir el módulo (anuncio no pedido)
const ESPIA = `(() => {
  window.__anunciosCarga = 0;
  if (typeof actualizarLectura === 'function' && !window.__espiaPuesto) {
    const orig = actualizarLectura;
    window.actualizarLectura = function (el, campos) {
      if (window.__cargando && el && el.hasAttribute && el.hasAttribute('aria-live')) window.__anunciosCarga++;
      return orig.apply(this, arguments);
    };
    window.__espiaPuesto = true;
  }
  return typeof actualizarLectura;
})()`;

async function capturar(c, sel, indice, archivo) {
  const rect = await c.evalua(`(() => {
    const el = document.querySelectorAll(${JSON.stringify(sel)})[${indice}];
    if (!el) return null;
    el.scrollIntoView({ behavior: 'instant', block: 'start' });
    const r = el.getBoundingClientRect();
    return { x: r.left + window.scrollX, y: r.top + window.scrollY, w: r.width, h: r.height };
  })()`);
  if (!rect || !rect.w) return null;
  await espera(150);
  const r = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
    clip: { x: Math.max(0, rect.x - 4), y: Math.max(0, rect.y - 4), width: rect.w + 8, height: rect.h + 8, scale: 1 } });
  fs.writeFileSync(path.join(OUT, archivo), Buffer.from(r.data, 'base64'));
  return archivo;
}

const QUITAR_FIJOS = `(() => { if (!document.getElementById('quitar-fijos')) { const st = document.createElement('style'); st.id = 'quitar-fijos';
  st.textContent = 'header.usta-header{position:static!important} #sidebarToggle,#scrollToTopBtn{visibility:hidden!important}'; document.head.appendChild(st); } return 1; })()`;

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const c = await Chrome.lanzar(PUERTO);
  const salida = { base: BASE, etiqueta: ETIQ, fecha: new Date().toISOString(), r: {} };
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable'); await c.enviar('Log.enable');
    for (const cap of CAPS) {
      salida.r[cap] = {};
      for (const ancho of ANCHOS) {
        c.contexto = `cap${cap} ${ancho} carga`;
        await c.enviar('Emulation.setDeviceMetricsOverride', MODOS[ancho]);
        await c.enviar('Page.navigate', { url: `${BASE}/${ARCH[cap]}#modulo-1` });
        await espera(700);
        await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined' && typeof renderMathInElement === 'function'", 30000);
        await c.evalua('document.fonts.ready.then(() => 1)');
        await c.evalua(`(() => { Chart.defaults.animation = false; Chart.defaults.animations = {}; return 1; })()`);
        await c.evalua(AYUDANTES);
        const tipoLect = await c.evalua(ESPIA);
        const nMod = await c.evalua(`courseData.modules.length`);
        salida.r[cap][ancho] = { espia: tipoLect, modulos: {} };
        for (let n = 1; n <= nMod; n++) {
          c.contexto = `cap${cap} ${ancho} M${n}`;
          await c.evalua(`(() => { window.__cargando = true; window.__anunciosCarga = 0; document.getElementById('quitar-fijos')?.remove(); loadModule(${n}); return 1; })()`);
          await espera(1300);
          await c.evalua(`(() => { window.__cargando = false; let e = mainContent; while (e) { e.scrollLeft = 0; e = e.parentElement; } window.scrollTo({top:0, behavior:'instant'}); return 1; })()`);
          await espera(150);
          const med = await c.evalua(MEDIDAS);
          med.anunciosCarga = await c.evalua('window.__anunciosCarga');
          salida.r[cap][ancho].modulos[n] = med;
          if (CAPTURAS) {
            await c.evalua(QUITAR_FIJOS);
            const nSim = med.sims.length;
            for (let k = 0; k < nSim; k++) await capturar(c, '[data-simulador]', k, `c${cap}-m${n}-sim${k}-${med.sims[k].sim}-${ancho}.png`);
            const nq = await c.evalua(`document.querySelectorAll('.quiz-grafico').length`);
            for (let q = 0; q < nq; q++) await capturar(c, '.quiz-grafico', q, `c${cap}-m${n}-quiz${q}-${ancho}.png`);
            // lienzos fuera de simuladores y del quiz
            const sueltos = await c.evalua(`[...mainContent.querySelectorAll('canvas')].map((cv,i)=>(!cv.closest('[data-simulador]') && !cv.closest('.quiz-grafico')) ? i : -1).filter(i=>i>=0)`);
            for (const i of sueltos) await capturar(c, '#main-content canvas, main canvas', i, `c${cap}-m${n}-lienzo${i}-${ancho}.png`);
          }
          console.log(`${ETIQ} cap${cap} ${ancho} M${n}: ${med.canv.length} lienzos, ${med.tablas.length} tablas, ${med.recortados.length} recortados, anuncios ${med.anunciosCarga}`);
        }
      }
    }
    salida.eventos = c.eventos;
  } finally {
    await c.cerrar();
  }
  fs.writeFileSync(path.join(__dirname, `r2_recorrido_${ETIQ}.json`), JSON.stringify(salida));
  console.log('listo; eventos:', (salida.eventos || []).length);
}
main().then(() => process.exit(0)).catch(e => { console.error('✗ ' + e.stack); process.exit(1); });
