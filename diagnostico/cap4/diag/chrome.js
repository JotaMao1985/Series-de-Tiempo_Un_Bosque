// Cliente CDP mínimo (WebSocket nativo de Node ≥ 22), copiado del arnés del cap. 1
// (diagnostico/cap1/herramientas/cdp.js); copia de diagnostico/cap3/diag/chrome.js para el cap. 4.
const os = require('os');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const espera = ms => new Promise(r => setTimeout(r, ms));

class Chrome {
  constructor(ws) { this.ws = ws; this.id = 0; this.pend = new Map(); this.eventos = []; this.oyentes = []; }
  static async lanzar(puerto) {
    const perfil = fs.mkdtempSync(path.join(os.tmpdir(), 'cap4-chrome-'));
    const proc = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${puerto}`, `--user-data-dir=${perfil}`,
      '--window-size=1200,1000', '--no-first-run', '--no-default-browser-check', '--hide-scrollbars', 'about:blank'],
      { stdio: 'ignore' });
    const c = await Chrome.abrir(puerto);
    c.cerrar = async () => { try { c.ws.close(); } catch (e) {} proc.kill(); await espera(500);
      try { fs.rmSync(perfil, { recursive: true, force: true }); } catch (e) {} };
    return c;
  }
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
          c.eventos.push({ cuando: c.contexto, txt: 'EXCEPCION: ' + (m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text) });
        } else if (m.method === 'Runtime.consoleAPICalled' && (m.params.type === 'error' || m.params.type === 'warning')) {
          c.eventos.push({ cuando: c.contexto, txt: m.params.type + ': ' + m.params.args.map(a => a.value ?? a.description).join(' ') });
        } else if (m.method === 'Log.entryAdded' && (m.params.entry.level === 'error' || m.params.entry.level === 'warning')) {
          c.eventos.push({ cuando: c.contexto, txt: 'log ' + m.params.entry.level + ': ' + m.params.entry.text + ' ' + (m.params.entry.url || '') });
        }
        c.oyentes.forEach(f => f(m));
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
  async esperaHasta(expr, ms, paso = 200) {
    const hasta = Date.now() + ms;
    for (;;) {
      try { if (await this.evalua(expr)) return true; } catch (e) {}
      if (Date.now() > hasta) throw new Error('timeout: ' + expr);
      await espera(paso);
    }
  }
}

module.exports = { Chrome, espera };
