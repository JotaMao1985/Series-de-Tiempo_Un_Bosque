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


async function capturar(c, sel, archivo, idx=0) {
  const rect = await c.evalua(`(() => {
    const el = document.querySelectorAll(${JSON.stringify(sel)})[${idx}];
    if (!el) return null;
    el.scrollIntoView({ behavior: 'instant', block: 'start' });
    const r = el.getBoundingClientRect();
    return { x: r.left + window.scrollX, y: r.top + window.scrollY, w: r.width, h: r.height };
  })()`);
  if (!rect) return null;
  await espera(250);
  const r = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
    clip: { x: Math.max(0, rect.x - 6), y: Math.max(0, rect.y - 6), width: rect.w + 12, height: rect.h + 12, scale: 1 } });
  fs.writeFileSync(path.join(OUT, archivo), Buffer.from(r.data, 'base64'));
  console.log('  ' + archivo);
}
async function main() {
  const perfil = fs.mkdtempSync(path.join(os.tmpdir(), 'cap1x-'));
  const proc = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PUERTO}`, `--user-data-dir=${perfil}`,
    '--window-size=1200,1000', '--no-first-run', '--hide-scrollbars', 'about:blank'], { stdio: 'ignore' });
  const res = {};
  try {
    const c = await Chrome.abrir(PUERTO);
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable');
    const fijos = `(() => { const st = document.createElement('style'); st.textContent = 'header.usta-header{position:static!important} #sidebarToggle,.back-to-top,#backToTop{visibility:hidden!important}'; document.head.appendChild(st); return 1; })()`;
    for (const modo of [{n:'800', w:800, h:1000, dsf:1, mob:false}, {n:'movil', w:375, h:812, dsf:2, mob:true}]) {
      await c.enviar('Emulation.setDeviceMetricsOverride', { width: modo.w, height: modo.h, deviceScaleFactor: modo.dsf, mobile: modo.mob });
      await c.enviar('Page.navigate', { url: BASE + '#modulo-4' });
      await espera(500);
      await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined' && typeof renderMathInElement === 'function'", 30000);
      await c.evalua('document.fonts.ready.then(() => 1)');
      await c.evalua(`loadModule(4), 1`); await espera(1200);
      if (modo.n === '800') {
        // vista real a 800 px, sin quitar nada
        await c.evalua(`document.querySelector('[data-simulador="comparador-escala"] .grafico-par').scrollIntoView({behavior:'instant', block:'center'}), 1`);
        await espera(300);
        const v = await c.enviar('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync(path.join(OUT, 'm4-vista-800.png'), Buffer.from(v.data, 'base64'));
        await c.evalua(fijos);
        await capturar(c, '[data-simulador="comparador-escala"]', 'm4-comparador-escala-800.png');
        await capturar(c, '[data-simulador="serie-vs-log"]', 'm4-serie-vs-log-800.png');
        res.anchos800 = await c.evalua(`(() => ({ main: mainContent.getBoundingClientRect().width, aside: document.getElementById('sidebar').getBoundingClientRect().width,
          par: [...document.querySelectorAll('.grafico-par')].map(p => ({ cw: p.clientWidth, sw: p.scrollWidth, cols: getComputedStyle(p).gridTemplateColumns })) }))()`);
        await c.evalua(`loadModule(6), 1`); await espera(1200);
        await capturar(c, '[data-simulador="descomp-clasica"]', 'm6-descomp-clasica-800.png');
        await c.evalua(`loadModule(3), 1`); await espera(1200);
        await capturar(c, '.mapa-estacional', 'm3-mapa-estacional-800.png');
      } else {
        await c.evalua(fijos);
        // cuadrícula: ¿por qué el par desborda?
        res.parMovil = await c.evalua(`(() => [...document.querySelectorAll('.grafico-par')].map(p => ({ cw: p.clientWidth, sw: p.scrollWidth, cols: getComputedStyle(p).gridTemplateColumns,
           hijos: [...p.children].map(h => Math.round(h.getBoundingClientRect().width)), simW: p.closest('.simulador').clientWidth })))()`);
        await c.evalua(`loadModule(3), 1`); await espera(1200);
        res.mapaMovil = await c.evalua(`(() => { const m = document.querySelector('.mapa-estacional-marco'); return { cw: m.clientWidth, sw: m.scrollWidth, ox: getComputedStyle(m).overflowX }; })()`);
        res.h4 = await c.evalua(`(() => [...document.querySelectorAll('.simulador h4')].map(h => ({ txt: h.textContent.trim(), disp: getComputedStyle(h).display, h: Math.round(h.getBoundingClientRect().height) })))()`);
        await c.evalua(`loadModule(9), 1`); await espera(1200);
        await capturar(c, '.quiz-grafico', 'm9-quiz-grafico-solo-movil.png');
        // botón flotante
        res.flotantes = await c.evalua(`(() => [...document.querySelectorAll('body *')].filter(e => getComputedStyle(e).position === 'fixed').map(e => ({ id: e.id, cls: String(e.className).slice(0,60), r: e.getBoundingClientRect().toJSON(), vis: getComputedStyle(e).visibility, disp: getComputedStyle(e).display })))()`);
      }
    }
    res.eventos = c.eventos;
  } finally { proc.kill(); await espera(500); try { fs.rmSync(perfil, { recursive: true, force: true }); } catch (e) {} }
  fs.writeFileSync(path.join(DIAG, 'medidas-extra.json'), JSON.stringify(res, null, 1));
  console.log(JSON.stringify(res, null, 1));
}
main().catch(e => { console.error(e.stack); process.exit(1); });
