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
  const perfil = fs.mkdtempSync(path.join(os.tmpdir(), 'cap1t-'));
  const proc = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PUERTO}`, `--user-data-dir=${perfil}`,
    '--window-size=1200,1000', '--no-first-run', '--hide-scrollbars', 'about:blank'], { stdio: 'ignore' });
  const res = {};
  try {
    const c = await Chrome.abrir(PUERTO);
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable');
    const fijos = `(() => { const st = document.createElement('style'); st.textContent = 'header.usta-header{position:static!important} #sidebarToggle,#scrollToTopBtn{visibility:hidden!important}'; document.head.appendChild(st); return 1; })()`;
    await c.enviar('Emulation.setDeviceMetricsOverride', { width: 375, height: 812, deviceScaleFactor: 2, mobile: true });
    await c.enviar('Page.navigate', { url: BASE + '#modulo-2' });
    await espera(500);
    await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined' && typeof renderMathInElement === 'function'", 30000);
    await c.evalua('document.fonts.ready.then(() => 1)');
    await c.evalua(fijos);
    for (const [n, idx, nombre] of [[2,0,'m2-tabla-conceptos-movil.png'],[4,0,'m4-tabla-amplitud-movil.png'],[9,0,'m9-tabla-0-movil.png'],[9,1,'m9-tabla-1-movil.png']]) {
      await c.evalua(`loadModule(${n}), 1`); await espera(1000);
      await capturar(c, 'table', nombre, idx);
    }
    await c.evalua(`loadModule(9), 1`); await espera(1000);
    res.m9 = await c.evalua(`(() => [...mainContent.querySelectorAll('table')].map(t => ({ sw: t.scrollWidth, cw: t.clientWidth, cap: (t.caption?.textContent||'').trim().slice(0,60) })))()`);
    await c.enviar('Emulation.setDeviceMetricsOverride', { width: 800, height: 1000, deviceScaleFactor: 1, mobile: false });
    await c.evalua(`loadModule(9), 1`); await espera(1000);
    res.m9_800 = await c.evalua(`(() => { const out=[]; mainContent.querySelectorAll('*').forEach(el => { const r = el.getBoundingClientRect(); if (r.right > 801 && el.tagName==='math') { const t = el.closest('table, .formula, p, li, td'); out.push({ cont: t ? t.tagName + '.' + t.className : null, txt: el.textContent.slice(0,60), right: r.right }); } }); return out; })()`);
    await capturar(c, 'table', 'm9-tabla-1-800.png', 1);
  } finally { proc.kill(); await espera(500); try { fs.rmSync(perfil, { recursive: true, force: true }); } catch (e) {} }
  console.log(JSON.stringify(res, null, 1));
}
main().catch(e => { console.error(e.stack); process.exit(1); });
