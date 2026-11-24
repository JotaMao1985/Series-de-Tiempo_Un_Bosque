#!/usr/bin/env node
// Verificador B, R1 del cap. 5: revisión por HTTP con Chrome sin ventana (CDP, puerto 9279).
// Capítulo: M1, M3, M4, M5, M6, M7, M9, M10, M11 (ejercicios) y M12 a 1200 y 375 px, con los plegados abiertos:
// errores de consola, .katex-error, $ o \( sin renderizar, desbordamiento horizontal; y los tres simuladores
// tocados leyendo lo que dibujan. Deck: las diapositivas cambiadas a 1280×720.
// Uso: BASE=http://127.0.0.1:8767 node diagnostico/cap5/comprobaciones/v1b_revisa.js
const fs = require('fs');
const path = require('path');
const { Chrome, espera } = require('../diag/chrome');

const BASE = process.env.BASE || 'http://127.0.0.1:8767';
const PUERTO = 9279;
const OUT = path.resolve(__dirname, '..', 'capturas', 'v1b');
const MODULOS = [1, 3, 4, 5, 6, 7, 9, 10, 11, 12];
const DIAPOS = [25, 29, 36, 41, 43, 51, 61, 64, 69, 3, 7, 11, 4];

const MEDIR = `(() => {
  const vw = document.documentElement.clientWidth;
  const raiz = document.getElementById('mainContent') || document.querySelector('main') || document.body;
  // texto con $ o \\( fuera de código y de KaTeX
  const crudos = [];
  const tw = document.createTreeWalker(raiz, NodeFilter.SHOW_TEXT, { acceptNode: n => {
    const p = n.parentElement;
    if (!p || p.closest('code, pre, script, style, textarea, .katex, .katex-display, [hidden]')) return NodeFilter.FILTER_REJECT;
    return /\\$|\\\\\\(|\\\\\\[/.test(n.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT; } });
  while (tw.nextNode()) { const v = tw.currentNode.nodeValue; const i = v.search(/\\$|\\\\\\(|\\\\\\[/);
    crudos.push(v.slice(Math.max(0, i - 50), i + 50).replace(/\\s+/g, ' ')); }
  // desbordamiento: documento y elementos que salen del viewport sin un contenedor que desplace o recorte
  const recorta = el => { for (let e = el.parentElement; e && e !== document.body; e = e.parentElement) {
    const ox = getComputedStyle(e).overflowX; if (ox === 'auto' || ox === 'scroll' || ox === 'hidden') return true; } return false; };
  const fuera = [];
  raiz.querySelectorAll('*').forEach(el => { const r = el.getBoundingClientRect();
    if (r.width > 0 && r.right > vw + 1 && getComputedStyle(el).position !== 'fixed' && !recorta(el))
      fuera.push((el.tagName + '.' + (el.className && el.className.baseVal === undefined ? el.className : '')).slice(0, 60) + ' right=' + Math.round(r.right)); });
  return { vw, docSW: document.scrollingElement.scrollWidth, desborda: document.scrollingElement.scrollWidth > vw + 1,
    katexError: document.querySelectorAll('.katex-error').length,
    katexErrores: [...document.querySelectorAll('.katex-error')].slice(0, 5).map(e => e.getAttribute('title') || e.textContent.slice(0, 80)),
    crudos: crudos.slice(0, 12), nCrudos: crudos.length, fuera: [...new Set(fuera)].slice(0, 10), nFuera: fuera.length,
    plegadosCerrados: [...raiz.querySelectorAll('button[aria-expanded="false"]')].length,
    sims: [...raiz.querySelectorAll('[data-simulador]')].map(s => s.dataset.simulador) };
})()`;

const ABRIR_PLEGADOS = `(async () => { const raiz = document.getElementById('mainContent') || document.body; let n = 0;
  for (let vuelta = 0; vuelta < 3; vuelta++) {
    for (const b of [...raiz.querySelectorAll('button[aria-expanded="false"]')]) { b.click(); n++; await new Promise(r => setTimeout(r, 60)); }
  }
  return n; })()`;

const LECTURA = sim => `(() => {
  const raiz = document.querySelector('[data-simulador="${sim}"]');
  const p = raiz.querySelector('.simulador-lectura');
  const gr = [...raiz.querySelectorAll('canvas')].map(cv => { const ch = Chart.getChart(cv); if (!ch) return null;
    const ys = ch.scales.y || Object.values(ch.scales).find(s => !s.isHorizontal());
    return { datasets: ch.data.datasets.map(d => ({ label: d.label, n: (d.data || []).length,
      primeros: (d.data || []).slice(0, 40).map(v => v == null ? null : Math.round((typeof v === 'object' ? v.y : v) * 1e4) / 1e4) })),
      yMin: ys ? ys.min : null, yMax: ys ? ys.max : null }; });
  return { lectura: p ? p.textContent.replace(/\\s+/g, ' ').trim() : null, graficos: gr,
    controles: [...raiz.querySelectorAll('input')].map(i => ({ tipo: i.type, valor: i.type === 'checkbox' ? i.checked : i.value, min: i.min, max: i.max })) };
})()`;

async function aplicar(c, sim, acciones) {
  for (const [tipo, idx, val] of acciones) {
    const cuerpo = {
      range: `const i = raiz.querySelectorAll('input[type=range]')[${idx}]; i.value = ${JSON.stringify(val)}; i.dispatchEvent(new Event('input', { bubbles: true }));`,
      check: `const k = raiz.querySelectorAll('input[type=checkbox]')[${idx}]; if (k.checked !== ${val}) { k.checked = ${val}; k.dispatchEvent(new Event('change', { bubbles: true })); }`,
    }[tipo];
    await c.evalua(`(() => { const raiz = document.querySelector('[data-simulador="${sim}"]'); ${cuerpo} return 1; })()`);
    await espera(150);
  }
  await espera(300);
}

async function capturar(c, sel, archivo) {
  const rect = await c.evalua(`(() => { const el = document.querySelector(${JSON.stringify(sel)}); if (!el) return null;
    el.scrollIntoView({ behavior: 'instant', block: 'start' }); const r = el.getBoundingClientRect();
    return { x: r.left + window.scrollX, y: r.top + window.scrollY, w: r.width, h: r.height }; })()`);
  if (!rect) return null;
  await espera(200);
  const r = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
    clip: { x: Math.max(0, rect.x - 4), y: Math.max(0, rect.y - 4), width: rect.w + 8, height: rect.h + 8, scale: 1 } });
  fs.writeFileSync(path.join(OUT, archivo), Buffer.from(r.data, 'base64'));
  return archivo;
}

const ESTADOS = {
  'sobrediferenciacion-estacional': [0, 1, 2].map(D => [`D${D}`, [['range', 0, D]]]),
  'airline-pesos': [['Theta0', [['range', 1, 0]]], ['Theta-0.95', [['range', 1, -0.95]]], ['Theta-0.56', [['range', 1, -0.56]]],
    ['theta0.5-Theta0.5', [['range', 0, 0.5], ['range', 1, 0.5]]]],
  'calendario-regresores': [[false, false], [true, false], [false, true], [true, true]].map(([a, b]) =>
    [`dias${+a}-pascua${+b}`, [['check', 0, a], ['check', 1, b]]]),
};

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const c = await Chrome.lanzar(PUERTO);
  const salida = { base: BASE, fecha: new Date().toISOString(), capitulo: {}, simuladores: {}, deck: {}, eventos: null };
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable'); await c.enviar('Log.enable');
    for (const modo of [{ n: '1200', width: 1200, height: 1000, dsf: 1, mobile: false }, { n: '375', width: 375, height: 812, dsf: 2, mobile: true }]) {
      c.contexto = `carga ${modo.n}`;
      await c.enviar('Emulation.setDeviceMetricsOverride', { width: modo.width, height: modo.height, deviceScaleFactor: modo.dsf, mobile: modo.mobile });
      await c.enviar('Page.navigate', { url: `${BASE}/capitulo-5-sarima.html#modulo-1` });
      await espera(800);
      await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined' && typeof renderMathInElement === 'function'", 30000);
      await c.evalua('document.fonts.ready.then(() => 1)');
      await c.evalua('(() => { Chart.defaults.animation = false; return 1; })()');
      salida.capitulo[modo.n] = {};
      for (const m of MODULOS) {
        c.contexto = `M${m} ${modo.n}`;
        await c.evalua(`loadModule(${m}), 1`);
        await espera(1200);
        const abiertos = await c.evalua(ABRIR_PLEGADOS);
        await espera(800);
        const med = await c.evalua(MEDIR);
        med.abiertos = abiertos;
        salida.capitulo[modo.n][m] = med;
        await c.evalua('window.scrollTo(0, 0), 1');
        const v = await c.enviar('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync(path.join(OUT, `cap-m${m}-${modo.n}.png`), Buffer.from(v.data, 'base64'));
        for (const sim of med.sims.filter(s => ESTADOS[s])) {
          const clave = `${sim}@${modo.n}`;
          salida.simuladores[clave] = { inicial: await c.evalua(LECTURA(sim)) };
          await capturar(c, `[data-simulador="${sim}"]`, `sim-${sim}-inicial-${modo.n}.png`);
          for (const [estado, acciones] of ESTADOS[sim]) {
            await aplicar(c, sim, acciones);
            salida.simuladores[clave][estado] = await c.evalua(LECTURA(sim));
            await capturar(c, `[data-simulador="${sim}"]`, `sim-${sim}-${estado}-${modo.n}.png`);
          }
          // intro del simulador
          salida.simuladores[clave].intro = await c.evalua(`(() => { const s = document.querySelector('[data-simulador="${sim}"]');
            const t = s.querySelector('.simulador-intro, p'); return t ? t.textContent.replace(/\\s+/g, ' ').trim().slice(0, 600) : null; })()`);
        }
      }
    }
    // Deck a 1280×720
    c.contexto = 'deck';
    await c.enviar('Emulation.setDeviceMetricsOverride', { width: 1280, height: 720, deviceScaleFactor: 1, mobile: false });
    for (const n of DIAPOS) {
      await c.enviar('Page.navigate', { url: `${BASE}/diapositivas/capitulo-5-sarima.html?todo=1#${n}` });
      await espera(2500);
      try { await c.esperaHasta("window.MathJax && MathJax.startup && MathJax.startup.promise ? MathJax.startup.promise.then(() => true) : true", 15000); } catch (e) {}
      await espera(800);
      salida.deck[n] = await c.evalua(`(() => { const d = document.querySelector('.diapo.activa'); if (!d) return null;
        const cuerpo = d.querySelector('.cuerpo'); const r = d.getBoundingClientRect();
        const fuera = [...d.querySelectorAll('*')].filter(e => { const q = e.getBoundingClientRect(); return q.width > 0 && (q.right > r.right + 1 || q.bottom > r.bottom + 1); }).length;
        return { titulo: (d.querySelector('h1, h2') || {}).textContent, escala: d.dataset.escala || getComputedStyle(d).getPropertyValue('--k'),
          mjxError: d.querySelectorAll('mjx-merror, [data-mjx-error]').length, crudo: /\\\\\\(|\\\\\\)/.test(d.innerText), fuera,
          pie: (d.querySelector('.pie') || {}).innerText }; })()`);
      const v = await c.enviar('Page.captureScreenshot', { format: 'png' });
      fs.writeFileSync(path.join(OUT, `deck-${String(n).padStart(2, '0')}.png`), Buffer.from(v.data, 'base64'));
    }
  } finally {
    salida.eventos = c.eventos;
    fs.writeFileSync(path.join(__dirname, 'v1b_revisa.json'), JSON.stringify(salida, null, 1));
    await c.cerrar();
  }
}
main().catch(e => { console.error(e); process.exit(1); });
