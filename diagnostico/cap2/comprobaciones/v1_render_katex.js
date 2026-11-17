#!/usr/bin/env node
// Verificador independiente · R1 cap. 2 · render por HTTP en Chrome sin ventana:
// carga los nueve módulos y cuenta errores de KaTeX, excepciones y console.error.
// Uso: node v1_render_katex.js http://127.0.0.1:PUERTO/capitulo-2-estacionariedad-acf-pacf.html
const { spawn } = require('child_process'); const os = require('os'); const path = require('path'); const fs = require('fs');
const URL_ = process.argv[2]; const PUERTO = 9247;
const perfil = fs.mkdtempSync(path.join(os.tmpdir(), 'v1cdp-'));
const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  ['--headless=new', `--remote-debugging-port=${PUERTO}`, `--user-data-dir=${perfil}`, '--window-size=1280,900', 'about:blank'], { stdio: 'ignore' });
const espera = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  let obj; for (let i = 0; i < 50 && !obj; i++) { try { obj = (await (await fetch(`http://127.0.0.1:${PUERTO}/json/list`)).json()).find(t => t.type === 'page'); } catch (e) {} await espera(200); }
  const ws = new WebSocket(obj.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const pend = {}; const errores = [];
  ws.onmessage = ev => { const m = JSON.parse(ev.data); if (m.id && pend[m.id]) { pend[m.id](m); delete pend[m.id]; }
    if (m.method === 'Runtime.exceptionThrown') errores.push('EXC ' + JSON.stringify(m.params.exceptionDetails).slice(0, 300));
    if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') errores.push('console.error ' + JSON.stringify(m.params.args).slice(0, 300)); };
  const env = (method, params = {}) => new Promise(r => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async expr => (await env('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true })).result.result.value;
  await env('Runtime.enable'); await env('Page.enable');
  await env('Page.navigate', { url: URL_ }); await espera(4000);
  console.log('innerWidth', await ev('innerWidth'), '· katex cargado:', await ev('typeof katex'));
  for (let n = 1; n <= 9; n++) {
    await ev(`loadModule(${n})`); await espera(1500);
    const r = await ev(`(() => { const e = [...document.querySelectorAll('#main-content .katex-error, .katex-error')].map(x => x.title || x.textContent); const crudo = [...document.querySelectorAll('p, li, td')].filter(x => /\\$[^$]+\\$/.test(x.textContent) && !x.closest('pre')).map(x => x.textContent.trim().slice(0, 120)); return { katex: document.querySelectorAll('.katex').length, errores: e, sin_render: crudo }; })()`);
    console.log(`M${n}: ${r.katex} fórmulas, ${r.errores.length} errores KaTeX, ${r.sin_render.length} con $ sin renderizar`);
    r.errores.forEach(x => console.log('   ERR', x)); r.sin_render.forEach(x => console.log('   CRUDO', x));
  }
  console.log('excepciones / console.error:', errores.length); errores.forEach(x => console.log('  ', x));
  ws.close(); chrome.kill();
})().catch(e => { console.error(e); chrome.kill(); process.exit(1); });
