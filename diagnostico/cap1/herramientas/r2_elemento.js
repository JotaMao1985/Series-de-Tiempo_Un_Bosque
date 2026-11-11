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
const PUERTO = Number(process.env.PUERTO || 9259);
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



// uso: node sel.js '<json>'  con [{url, ancho, modulo, pasos:[{js}|{sel, idx, archivo, vista}]}]
async function main() {
  const tareas = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  fs.mkdirSync(OUT, { recursive: true });
  const perfil = fs.mkdtempSync(path.join(os.tmpdir(), 'cap1-sel-'));
  const proc = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PUERTO}`, `--user-data-dir=${perfil}`, '--window-size=1200,1000', '--no-first-run', '--hide-scrollbars', 'about:blank'], { stdio: 'ignore' });
  try {
    const c = await Chrome.abrir(PUERTO);
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable'); await c.enviar('Network.enable');
    await c.enviar('Network.setCacheDisabled', { cacheDisabled: true });
    for (const t of tareas) {
      const movil = t.ancho < 500;
      await c.enviar('Emulation.setDeviceMetricsOverride', { width: t.ancho, height: movil ? 812 : 1000, deviceScaleFactor: movil ? 2 : 1, mobile: movil });
      await c.enviar('Page.navigate', { url: t.url + (t.url.includes('?') ? '&' : '?') + 'v=' + Date.now() });
      await espera(600);
      await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined'", 30000);
      await c.evalua('document.fonts.ready.then(() => 1)');
      if (t.modulo) { await c.evalua(`loadModule(${t.modulo}), 1`); await espera(1300); }
      await c.evalua(`(() => { const st = document.createElement('style'); st.textContent = 'header.usta-header{position:static!important} #sidebarToggle,#backToTop,.back-to-top{visibility:hidden!important}'; document.head.appendChild(st); return 1; })()`);
      for (const p of t.pasos) {
        if (p.js) { console.log(JSON.stringify(await c.evalua(p.js))); await espera(p.espera || 300); continue; }
        const rect = await c.evalua(`(() => { const el = document.querySelectorAll(${JSON.stringify(p.sel)})[${p.idx || 0}]; if (!el) return null; el.scrollIntoView({behavior:'instant', block:'start'}); const r = el.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height }; })()`);
        if (!rect) { console.log('sin elemento', p.sel); continue; }
        await espera(250);
        const r = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: Math.max(0, rect.x - 6), y: Math.max(0, rect.y - 6), width: rect.w + 12, height: Math.min(rect.h, p.maxAlto || 1e5) + 12, scale: 1 } });
        fs.writeFileSync(path.join(p.dir || OUT, p.archivo), Buffer.from(r.data, 'base64'));
        console.log('  ' + p.archivo);
      }
    }
    console.log('eventos', JSON.stringify(c.eventos));
  } finally { proc.kill(); await espera(400); try { fs.rmSync(perfil, { recursive: true, force: true }); } catch (e) {} }
}
main().catch(e => { console.error(e.stack); process.exit(1); });
