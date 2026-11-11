#!/usr/bin/env node
// Arnés de revisión visual del cap. 1: capturas por elemento y medidas.
// Chrome sin ventana por CDP (WebSocket nativo), sin dependencias.
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawn } = require('child_process');

const DIAG = path.resolve(__dirname, '..');
const OUT = path.join(DIAG, 'capturas');
const BASE = process.env.BASE || 'http://localhost:8731/capitulo-1-componentes-descomposicion.html';
const PUERTO = 9257;
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const espera = ms => new Promise(r => setTimeout(r, ms));

class Chrome {
  constructor(ws) { this.ws = ws; this.id = 0; this.pend = new Map(); this.eventos = []; }
  static async abrir(puerto) {
    let obj = null;
    for (let i = 0; i < 80 && !obj; i++) {
      try {
        const l = await (await fetch(`http://127.0.0.1:${puerto}/json/list`)).json();
        obj = l.find(t => t.type === 'page' && t.webSocketDebuggerUrl);
      } catch (e) {}
      if (!obj) await espera(250);
    }
    if (!obj) throw new Error('sin pestaña CDP');
    const ws = new WebSocket(obj.webSocketDebuggerUrl);
    await new Promise((ok, mal) => { ws.onopen = ok; ws.onerror = () => mal(new Error('ws')); });
    const c = new Chrome(ws);
    ws.onmessage = ev => {
      const m = JSON.parse(ev.data);
      if (m.id && c.pend.has(m.id)) {
        const { ok, mal } = c.pend.get(m.id); c.pend.delete(m.id);
        m.error ? mal(new Error(m.error.message)) : ok(m.result);
      } else if (m.method) {
        if (m.method === 'Runtime.exceptionThrown') {
          c.eventos.push('EXCEPCION: ' + (m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text));
        } else if (m.method === 'Runtime.consoleAPICalled' && (m.params.type === 'error' || m.params.type === 'warning')) {
          c.eventos.push(m.params.type + ': ' + m.params.args.map(a => a.value ?? a.description).join(' '));
        }
      }
    };
    return c;
  }
  enviar(method, params = {}) {
    const id = ++this.id;
    return new Promise((ok, mal) => {
      this.pend.set(id, { ok, mal });
      this.ws.send(JSON.stringify({ id, method, params }));
      setTimeout(() => { if (this.pend.has(id)) { this.pend.delete(id); mal(new Error(method + ' sin respuesta')); } }, 60000);
    });
  }
  async evalua(expr) {
    const r = await this.enviar('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
    if (r.exceptionDetails) throw new Error('página: ' + (r.exceptionDetails.exception?.description || r.exceptionDetails.text));
    return r.result.value;
  }
  async esperaHasta(expr, ms) {
    const hasta = Date.now() + ms;
    for (;;) {
      try { if (await this.evalua(expr)) return true; } catch (e) {}
      if (Date.now() > hasta) throw new Error('timeout: ' + expr);
      await espera(200);
    }
  }
}

// ---------------------------------------------------------------- en página
const MEDIDAS = ancho => `(() => {
  const W = ${ancho};
  const mc = mainContent;
  const r2 = x => Math.round(x * 10) / 10;
  const canv = [...mc.querySelectorAll('canvas')].map((cv, i) => {
    const ch = Chart.getChart(cv);
    const r = cv.getBoundingClientRect();
    const sim = cv.closest('[data-simulador]')?.dataset.simulador || (cv.closest('.quiz') ? 'quiz' : null);
    const info = { i, sim, aria: cv.getAttribute('aria-label'), role: cv.getAttribute('role'),
      w: r2(r.width), h: r2(r.height), right: r2(r.right) };
    if (ch) {
      info.datasets = ch.data.datasets.map((d, k) => ({ label: d.label, color: d.borderColor, bg: d.backgroundColor,
        bw: d.borderWidth, dash: d.borderDash || null, visible: ch.isDatasetVisible(k), n: (d.data||[]).length }));
      const lg = ch.legend;
      info.legend = { display: ch.options.plugins.legend.display !== false,
        items: lg && lg.legendItems ? lg.legendItems.map(x => x.text) : [], h: lg ? r2(lg.height) : 0,
        font: ch.options.plugins.legend.labels?.font?.size };
      info.area = { w: r2(ch.chartArea.width), h: r2(ch.chartArea.height) };
      info.escalas = Object.values(ch.scales).map(s => ({ id: s.id, type: s.type,
        title: s.options.title?.display ? s.options.title.text : null,
        min: s.min, max: s.max, nTicks: s.ticks.length,
        ticks: s.ticks.map(t => t.label).filter(x => x !== '' && x != null).slice(0, 30),
        font: s.options.ticks?.font?.size, family: s.options.ticks?.font?.family }));
      info.tooltip = ch.options.plugins.tooltip?.enabled !== false;
      info.interaccion = ch.options.interaction?.mode;
    }
    return info;
  });
  const katex = [...mc.querySelectorAll('.katex-display')].map(d => {
    const k = d.querySelector('.katex');
    const f = d.closest('.formula');
    const cont = f || d.parentElement;
    return { sw: k ? k.scrollWidth : 0, cw: d.clientWidth, contCw: cont.clientWidth, contSw: cont.scrollWidth,
      ox: getComputedStyle(d).overflowX, oxCont: getComputedStyle(cont).overflowX,
      txt: d.textContent.replace(/\\s+/g, ' ').slice(0, 70) };
  }).filter(x => x.sw > x.cw + 1 || x.contSw > x.contCw + 1);
  const formulasTexto = [...mc.querySelectorAll('.formula')].filter(f => !f.querySelector('.katex-display'))
    .map(f => ({ sw: f.scrollWidth, cw: f.clientWidth, txt: f.textContent.replace(/\\s+/g,' ').trim().slice(0,70) }))
    .filter(x => x.sw > x.cw + 1);
  const tablas = [...mc.querySelectorAll('table')].map((t, i) => {
    const r = t.getBoundingClientRect();
    return { i, sw: t.scrollWidth, cw: t.clientWidth, parentCw: t.parentElement.clientWidth, right: r2(r.right),
      caption: (t.caption?.textContent || '').trim().slice(0, 60), ox: getComputedStyle(t).overflowX,
      display: getComputedStyle(t).display };
  });
  const desbordan = [];
  mc.querySelectorAll('*').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width && r.right > W + 1) {
      // sólo el más externo
      let p = el.parentElement, externo = true;
      while (p && p !== mc) { if (p.getBoundingClientRect().right > W + 1) { externo = false; break; } p = p.parentElement; }
      if (externo) desbordan.push({ tag: el.tagName, cls: String(el.className).slice(0, 50), right: r2(r.right),
        txt: (el.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 50) });
    }
  });
  const controles = [...mc.querySelectorAll('.control-slider')].map(c => {
    const l = c.querySelector('label'), o = c.querySelector('output'), inp = c.querySelector('input');
    return { sim: c.closest('[data-simulador]')?.dataset.simulador, label: l.childNodes[0].textContent,
      out: o.textContent, w: r2(c.getBoundingClientRect().width), labelSw: l.scrollWidth, labelCw: l.clientWidth,
      labelH: r2(l.getBoundingClientRect().height), min: inp.min, max: inp.max, step: inp.step, value: inp.value };
  });
  const lecturas = [...mc.querySelectorAll('.simulador-lectura')].map(p => ({
    sim: p.closest('[data-simulador]')?.dataset.simulador, txt: p.textContent.replace(/\\s+/g, ' ').trim() }));
  return { modulo: currentModuleId, ancho: W, innerWidth: window.innerWidth,
    docSw: document.documentElement.scrollWidth, mainW: Math.round(mc.getBoundingClientRect().width),
    canv, katex, formulasTexto, tablas, desbordan, controles, lecturas };
})()`;

const CAJAS = `(() => {
  const mc = mainContent;
  const lista = [];
  mc.querySelectorAll('[data-simulador]').forEach(el => lista.push({ sel: '[data-simulador="' + el.dataset.simulador + '"]', nombre: el.dataset.simulador }));
  mc.querySelectorAll('.mapa-estacional').forEach((el, i) => lista.push({ sel: '.mapa-estacional', nombre: 'mapa-estacional' }));
  mc.querySelectorAll('.ciclo').forEach((el, i) => lista.push({ sel: '.ciclo', nombre: 'ciclo' }));
  mc.querySelectorAll('.quiz-grafico').forEach((el, i) => lista.push({ sel: '.quiz-grafico', nombre: 'quiz-grafico', padre: true }));
  return lista;
})()`;

async function capturar(c, sel, archivo, opciones = {}) {
  const rect = await c.evalua(`(() => {
    let el = document.querySelector(${JSON.stringify(sel)});
    if (!el) return null;
    ${opciones.padre ? "el = el.closest('.quiz-bloque, .quiz-pregunta, li, .quiz') || el;" : ''}
    el.scrollIntoView({ behavior: 'instant', block: 'start' });
    const r = el.getBoundingClientRect();
    return { x: r.left + window.scrollX, y: r.top + window.scrollY, w: r.width, h: r.height };
  })()`);
  if (!rect) return null;
  await espera(250);
  const pad = 6;
  const r = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
    clip: { x: Math.max(0, rect.x - pad), y: Math.max(0, rect.y - pad), width: rect.w + 2 * pad, height: rect.h + 2 * pad, scale: 1 } });
  fs.writeFileSync(path.join(OUT, archivo), Buffer.from(r.data, 'base64'));
  return archivo;
}

// Movimientos de controles por simulador: [estado, [[índice del range, valor]...], extra JS]
const MOVIMIENTOS = {
  'construye-tu-serie': [
    ['beta2-A30-sigma0', [[0, 2], [1, 30], [2, 0]], `(() => { const ch = Chart.getChart(document.querySelector('[data-simulador="construye-tu-serie"] canvas')); ch.setDatasetVisibility(2, true); ch.update('none'); return 1; })()`],
    ['beta-neg-sigma20', [[0, -1], [1, 5], [2, 20]], null],
  ],
  'comparador-escala': [
    ['beta4-A40', [[0, 4], [1, 40]], null],
    ['beta0', [[0, 0], [1, 20]], null],
  ],
  'media-movil': [
    ['m5', [[0, 5]], null],
    ['m24', [[0, 24]], null],
  ],
  'loess-local': [
    ['foco1', [[0, 1]], null],
    ['foco144', [[0, 144]], null],
    ['grado0-planos', [[0, 72], [2, 0], [3, 0]], null],
    ['span61', [[0, 72], [1, 61], [2, 1], [3, 1]], null],
  ],
};

async function mover(c, sim, pasos, extra) {
  for (const [idx, val] of pasos) {
    await c.evalua(`(() => {
      const inp = document.querySelectorAll('[data-simulador="${sim}"] input[type=range]')[${idx}];
      inp.value = ${val}; inp.dispatchEvent(new Event('input', { bubbles: true })); return inp.value; })()`);
    await espera(120);
  }
  if (extra) await c.evalua(extra);
  await espera(300);
}

async function cargarModulo(c, n) {
  await c.evalua(`loadModule(${n}), 'ok'`);
  await espera(1100);
  await c.evalua(`window.scrollTo({top:0, behavior:'instant'}), 1`);
  await espera(200);
}

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const perfil = fs.mkdtempSync(path.join(os.tmpdir(), 'cap1-chrome-'));
  const proc = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PUERTO}`, `--user-data-dir=${perfil}`,
    '--window-size=1200,1000', '--no-first-run', '--no-default-browser-check', '--hide-scrollbars', 'about:blank'],
    { stdio: 'ignore' });
  const medidas = {};
  const lecturasMov = {};
  let c;
  try {
    c = await Chrome.abrir(PUERTO);
    await c.enviar('Page.enable');
    await c.enviar('Runtime.enable');
    const modos = [
      { nombre: 'escritorio', width: 1200, height: 1000, dsf: 1, mobile: false, capturas: true },
      { nombre: 'movil', width: 375, height: 812, dsf: 2, mobile: true, capturas: true },
      { nombre: 'ancho800', width: 800, height: 1000, dsf: 1, mobile: false, capturas: false },
    ];
    for (const modo of modos) {
      await c.enviar('Emulation.setDeviceMetricsOverride', { width: modo.width, height: modo.height,
        deviceScaleFactor: modo.dsf, mobile: modo.mobile });
      await c.enviar('Page.navigate', { url: BASE + '#modulo-1' });
      await espera(500);
      await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined' && typeof renderMathInElement === 'function'", 30000);
      await c.evalua('document.fonts.ready.then(() => 1)');
      await c.evalua(`(() => { Chart.defaults.animation = false; Chart.defaults.animations = {}; return 1; })()`);
      await espera(500);
      medidas[modo.nombre] = {};
      for (let n = 1; n <= 9; n++) {
        await cargarModulo(c, n);
        medidas[modo.nombre][n] = await c.evalua(MEDIDAS(modo.width));
        if (!modo.capturas) {
          if (n === 8) {
            await capturar(c, '.formula:has(.katex-display)', `m8-formula-FT-FS-800.png`);
          }
          continue;
        }
        const cajas = await c.evalua(CAJAS);
        // Vista real del teléfono (cabecera fija y botón flotante incluidos) sobre el primer gráfico
        if (modo.mobile && cajas.length) {
          await c.evalua(`(() => { document.getElementById('quitar-fijos')?.remove(); const el = document.querySelector('${cajas[0].sel.replace(/'/g, "\\'")} canvas') || document.querySelector('${cajas[0].sel.replace(/'/g, "\\'")}'); el.scrollIntoView({behavior:'instant', block:'center'}); return 1; })()`);
          await espera(300);
          const v = await c.enviar('Page.captureScreenshot', { format: 'png' });
          fs.writeFileSync(path.join(OUT, `m${n}-vista-${modo.nombre}.png`), Buffer.from(v.data, 'base64'));
        }
        await c.evalua(`(() => { if (!document.getElementById('quitar-fijos')) { const st = document.createElement('style'); st.id = 'quitar-fijos'; st.textContent = 'header.usta-header{position:static!important} #sidebarToggle{visibility:hidden!important}'; document.head.appendChild(st); } return 1; })()`);
        await espera(150);
        for (const caja of cajas) {
          const f = `m${n}-${caja.nombre}-${modo.nombre}.png`;
          await capturar(c, caja.sel, f, { padre: caja.padre });
          console.log('  ' + f);
          if (MOVIMIENTOS[caja.nombre]) {
            for (const [estado, pasos, extra] of MOVIMIENTOS[caja.nombre]) {
              await mover(c, caja.nombre, pasos, extra);
              const f2 = `m${n}-${caja.nombre}-${estado}-${modo.nombre}.png`;
              await capturar(c, caja.sel, f2);
              const lect = await c.evalua(`(() => { const p = document.querySelector('[data-simulador="${caja.nombre}"] .simulador-lectura'); return p ? p.textContent.replace(/\\s+/g,' ').trim() : null; })()`);
              const outs = await c.evalua(`[...document.querySelectorAll('[data-simulador="${caja.nombre}"] output')].map(o => o.textContent)`);
              const leg = await c.evalua(`Chart.getChart(document.querySelector('[data-simulador="${caja.nombre}"] canvas')).legend.legendItems.map(x=>x.text)`);
              (lecturasMov[modo.nombre] ||= {})[`${caja.nombre}:${estado}`] = { lect, outs, leg };
              console.log('  ' + f2);
            }
            // recargar el módulo para dejar el estado inicial a los siguientes
            await cargarModulo(c, n);
          }
          if (caja.nombre === 'ciclo') {
            await c.evalua(`document.querySelectorAll('.ciclo-boton')[3].click(), 1`);
            await espera(300);
            await capturar(c, '.ciclo', `m${n}-ciclo-paso4-${modo.nombre}.png`);
          }
        }
        if (n === 8) {
          await capturar(c, '.formula:has(.katex-display)', `m8-formula-FT-FS-${modo.nombre}.png`);
        }
        if (n === 6 && modo.nombre === 'movil') {
          await capturar(c, 'table:has(th[scope=row])', `m6-tabla-pasos-movil.png`);
        }
      }
    }
    // pruebas de fuente en el lienzo
    medidas.eventos = c.eventos;
  } finally {
    proc.kill();
    await espera(500);
    try { fs.rmSync(perfil, { recursive: true, force: true }); } catch (e) {}
  }
  fs.writeFileSync(path.join(DIAG, 'medidas.json'), JSON.stringify({ medidas, lecturasMov }, null, 1));
  console.log('listo');
}
main().catch(e => { console.error('✗ ' + e.stack); process.exit(1); });
