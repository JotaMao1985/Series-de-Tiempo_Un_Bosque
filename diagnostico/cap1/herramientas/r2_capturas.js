#!/usr/bin/env node
// Arnés de la ronda R2 del cap. 1: vuelve a capturar cada gráfico a 1200, 800 y 375 px
// (capturas/r2/) y mide desbordes, ejes y alineación. Uso: node r2_capturas.js [módulos, p. ej. 4,6]
// Chrome sin ventana por CDP (WebSocket nativo), sin dependencias.
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawn } = require('child_process');

const DIAG = process.env.DIAG || path.resolve(__dirname, '..');
const OUT = path.join(DIAG, 'capturas', 'r2');
const BASE = process.env.BASE || 'http://localhost:8731/capitulo-1-componentes-descomposicion.html';
const PUERTO = Number(process.env.PUERTO || 9258);
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


const MEDIDAS = ancho => `(() => {
  const W = ${ancho};
  const mc = mainContent;
  const r2 = x => Math.round(x * 10) / 10;
  const canv = [...mc.querySelectorAll('canvas')].map((cv, i) => {
    const ch = Chart.getChart(cv);
    const r = cv.getBoundingClientRect();
    const sim = cv.closest('[data-simulador]')?.dataset.simulador || (cv.closest('.quiz') ? 'quiz' : null);
    const caja = cv.closest('.simulador') ? cv.closest('.simulador').getBoundingClientRect() : null;
    const info = { i, sim, aria: cv.getAttribute('aria-label'), w: r2(r.width), h: r2(r.height), left: r2(r.left), right: r2(r.right),
      fueraDeCaja: caja ? r2(Math.max(0, r.right - caja.right)) : 0 };
    if (ch) {
      info.datasets = ch.data.datasets.map((d, k) => ({ label: d.label, color: d.borderColor, bw: d.borderWidth, dash: d.borderDash || null, visible: ch.isDatasetVisible(k) }));
      const lg = ch.legend;
      info.legend = { display: ch.options.plugins.legend.display !== false, items: lg && lg.legendItems ? lg.legendItems.map(x => x.text) : [], h: lg ? r2(lg.height) : 0 };
      info.area = { w: r2(ch.chartArea.width), h: r2(ch.chartArea.height), left: r2(r.left + ch.chartArea.left), right: r2(r.left + ch.chartArea.right) };
      info.escalas = Object.values(ch.scales).map(s => {
        const et = s.ticks.map(t => Array.isArray(t.label) ? t.label.join(' ') : t.label).filter(x => x !== '' && x != null);
        // ¿se pisan las etiquetas del eje x?
        let pisan = null;
        if (s.isHorizontal() && s._labelItems) {
          const ctx = ch.ctx; ctx.save(); ctx.font = (s.options.ticks.font.size || 11) + 'px ' + (s.options.ticks.font.family || 'sans-serif');
          let prev = -1e9; pisan = 0;
          s.ticks.forEach((t, k) => { if (!t.label) return; const cx = s.getPixelForTick(k); const w = ctx.measureText(String(t.label)).width; if (cx - w / 2 < prev + 2) pisan++; prev = cx + w / 2; });
          ctx.restore();
        }
        return { id: s.id, title: s.options.title?.display ? s.options.title.text : null, min: s.min, max: s.max, w: r2(s.width), ticks: et.slice(0, 20), pisan,
          x0: s.isHorizontal() ? r2(r.left + s.getPixelForValue(s.min)) : null, x1: s.isHorizontal() ? r2(r.left + s.getPixelForValue(s.max)) : null };
      });
    }
    return info;
  });
  const katex = [...mc.querySelectorAll('.katex-display')].map(d => {
    const k = d.querySelector('.katex');
    const cont = d.closest('.formula') || d.parentElement;
    return { sw: k ? k.scrollWidth : 0, cw: d.clientWidth, contCw: cont.clientWidth, contSw: cont.scrollWidth, txt: d.textContent.replace(/\\s+/g, ' ').slice(0, 50) };
  }).filter(x => x.sw > x.cw + 1 || x.contSw > x.contCw + 1);
  const desbordan = [];
  mc.querySelectorAll('*').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width && r.right > W + 1) {
      let p = el.parentElement, externo = true;
      while (p && p !== mc) { if (p.getBoundingClientRect().right > W + 1) { externo = false; break; } p = p.parentElement; }
      if (externo) desbordan.push({ tag: el.tagName, cls: String(el.className).slice(0, 50), right: r2(r.right), txt: (el.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 50) });
    }
  });
  const mapa = [...mc.querySelectorAll('.mapa-estacional-marco')].map(m => ({ cw: m.clientWidth, sw: m.scrollWidth }));
  const h4 = [...mc.querySelectorAll('.simulador h4')].map(h => ({ txt: h.textContent.replace(/\\s+/g, ' ').trim().slice(0, 60), disp: getComputedStyle(h).display, h: Math.round(h.getBoundingClientRect().height) }));
  const par = [...mc.querySelectorAll('.grafico-par')].map(p => ({ cw: p.clientWidth, sw: p.scrollWidth, cols: getComputedStyle(p).gridTemplateColumns }));
  const lecturas = [...mc.querySelectorAll('.simulador-lectura')].map(p => ({ sim: p.closest('[data-simulador]')?.dataset.simulador, live: p.getAttribute('aria-live'), txt: p.textContent.replace(/\\s+/g, ' ').trim() }));
  return { modulo: currentModuleId, ancho: W, docSw: document.documentElement.scrollWidth, mainW: Math.round(mc.getBoundingClientRect().width), canv, katex, desbordan, mapa, h4, par, lecturas };
})()`;

const CAJAS = `(() => {
  const mc = mainContent;
  const lista = [];
  mc.querySelectorAll('[data-simulador]').forEach(el => lista.push({ sel: '[data-simulador="' + el.dataset.simulador + '"]', nombre: el.dataset.simulador }));
  mc.querySelectorAll('.mapa-estacional').forEach(() => lista.push({ sel: '.mapa-estacional', nombre: 'mapa-estacional' }));
  mc.querySelectorAll('.ciclo').forEach(() => lista.push({ sel: '.ciclo', nombre: 'ciclo' }));
  mc.querySelectorAll('.quiz-grafico').forEach(() => lista.push({ sel: '.quiz-grafico', nombre: 'quiz-grafico', padre: true }));
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

const MOVIMIENTOS = {
  'construye-tu-serie': [
    ['beta2-A30-sigma0', [[0, 2], [1, 30], [2, 0]], null],
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
  const soloModulos = process.argv[2] ? process.argv[2].split(',').map(Number) : [1, 2, 3, 4, 5, 6, 7, 8, 9];
  const perfil = fs.mkdtempSync(path.join(os.tmpdir(), 'cap1-r2-'));
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
    await c.enviar('Network.enable');
    await c.enviar('Network.setCacheDisabled', { cacheDisabled: true });
    const modos = [
      { nombre: 'escritorio', width: 1200, height: 1000, dsf: 1, mobile: false },
      { nombre: '800', width: 800, height: 1000, dsf: 1, mobile: false },
      { nombre: 'movil', width: 375, height: 812, dsf: 2, mobile: true },
    ];
    for (const modo of modos) {
      await c.enviar('Emulation.setDeviceMetricsOverride', { width: modo.width, height: modo.height,
        deviceScaleFactor: modo.dsf, mobile: modo.mobile });
      await c.enviar('Page.navigate', { url: BASE + '?v=' + Date.now() + '#modulo-1' });
      await espera(500);
      await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined' && typeof renderMathInElement === 'function'", 30000);
      await c.evalua('document.fonts.ready.then(() => 1)');
      await c.evalua(`(() => { Chart.defaults.animation = false; Chart.defaults.animations = {}; return 1; })()`);
      await espera(500);
      medidas[modo.nombre] = {};
      for (const n of soloModulos) {
        await cargarModulo(c, n);
        medidas[modo.nombre][n] = await c.evalua(MEDIDAS(modo.width));
        const cajas = await c.evalua(CAJAS);
        // Vista real de la pantalla (cabecera fija incluida) sobre el primer gráfico
        if (cajas.length && (modo.mobile || modo.nombre === '800')) {
          await c.evalua(`(() => { document.getElementById('quitar-fijos')?.remove(); const el = document.querySelector('${cajas[0].sel.replace(/'/g, "\\'")} canvas') || document.querySelector('${cajas[0].sel.replace(/'/g, "\\'")}'); el.scrollIntoView({behavior:'instant', block:'center'}); return 1; })()`);
          await espera(300);
          const v = await c.enviar('Page.captureScreenshot', { format: 'png' });
          fs.writeFileSync(path.join(OUT, `m${n}-vista-${modo.nombre}.png`), Buffer.from(v.data, 'base64'));
        }
        await c.evalua(`(() => { if (!document.getElementById('quitar-fijos')) { const st = document.createElement('style'); st.id = 'quitar-fijos'; st.textContent = 'header.usta-header{position:static!important} #sidebarToggle,#backToTop,.back-to-top{visibility:hidden!important}'; document.head.appendChild(st); } return 1; })()`);
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
              const arias = await c.evalua(`[...document.querySelectorAll('[data-simulador="${caja.nombre}"] canvas')].map(o => o.getAttribute('aria-label'))`);
              const ejes = await c.evalua(`[...document.querySelectorAll('[data-simulador="${caja.nombre}"] canvas')].map(cv => { const ch = Chart.getChart(cv); return Object.values(ch.scales).map(s => s.id + ': ' + s.ticks.map(t => t.label).filter(x => x !== '' && x != null).join(' | ')); })`);
              (lecturasMov[modo.nombre] ||= {})[`${caja.nombre}:${estado}`] = { lect, arias, ejes };
              console.log('  ' + f2);
            }
            await cargarModulo(c, n);
          }
          if (caja.nombre === 'ciclo') {
            await c.evalua(`document.querySelectorAll('.ciclo-boton')[3].click(), 1`);
            await espera(300);
            await capturar(c, '.ciclo', `m${n}-ciclo-paso4-${modo.nombre}.png`);
          }
        }
        if (n === 8) await capturar(c, '.formula:has(.katex-display)', `m8-formula-FT-FS-${modo.nombre}.png`);
        if (n === 6 && modo.nombre === 'movil') await capturar(c, 'table:has(th[scope=row])', `m6-tabla-pasos-movil.png`);
      }
    }
    medidas.eventos = c.eventos;
  } finally {
    proc.kill();
    await espera(500);
    try { fs.rmSync(perfil, { recursive: true, force: true }); } catch (e) {}
  }
  const destino = path.join(OUT, 'medidas-r2' + (process.argv[2] ? '-m' + process.argv[2].replace(/,/g, '_') : '') + '.json');
  fs.writeFileSync(destino, JSON.stringify({ medidas, lecturasMov }, null, 1));
  console.log('eventos:', JSON.stringify(medidas.eventos));
  console.log('listo');
}
main().catch(e => { console.error('✗ ' + e.stack); process.exit(1); });
