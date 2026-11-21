// v3 · verificador independiente de la R3: recorre los 11 modulos del cap. 3 por HTTP con Chrome sin
// ventana (CDP), a 1200 y 375 px. Uso: node v3_recorrido.js <puerto_http> <puerto_cdp>
// Requiere un servidor estatico sobre Htmls_Series en <puerto_http>.
const { Chrome, espera } = require('../diag/chrome.js');
const [PH, PC] = [process.argv[2] || '8761', process.argv[3] || '9361'];
const URL = `http://127.0.0.1:${PH}/capitulo-3-modelos-ar-ma-arma.html`;
const SONDA = `(() => {
  const cont = document.getElementById('content-area');
  const vw = document.documentElement.clientWidth;
  const katexErr = cont.querySelectorAll('.katex-error').length;
  // texto con $ sin componer fuera de code/pre/script
  const w = document.createTreeWalker(cont, NodeFilter.SHOW_TEXT);
  const dolares = []; let n;
  while ((n = w.nextNode())) {
    if (n.parentElement.closest('code,pre,script,style,.katex')) continue;
    if (/\\$|\\\\[a-z]+\\{|\\\\(phi|theta|psi|pi|sqrt|frac)\\b/.test(n.textContent)) dolares.push(n.textContent.trim().slice(0, 80));
  }
  // desbordes: elementos cuyo borde derecho pasa el viewport sin un contenedor con scroll horizontal
  const desb = [];
  for (const el of cont.querySelectorAll('*')) {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.right <= vw + 1) continue;
    let p = el.parentElement, scroll = false;
    while (p && p !== document.body) { const s = getComputedStyle(p).overflowX; if (s === 'auto' || s === 'scroll' || s === 'hidden') { scroll = true; break; } p = p.parentElement; }
    if (!scroll) desb.push(el.tagName + '.' + (el.className || '').toString().slice(0, 30) + ' ' + Math.round(r.right));
  }
  const h2 = (cont.querySelector('h2') || {}).textContent || '';
  const h3 = [...cont.querySelectorAll('h3')].map(h => h.textContent.trim());
  const canv = [...cont.querySelectorAll('canvas')];
  return { h2: h2.replace(/\\s+/g, ' ').trim(), h3, katexErr, dolares: dolares.slice(0, 5), nDolares: dolares.length,
    pagina: document.documentElement.scrollWidth > vw + 1 ? document.documentElement.scrollWidth : 0,
    desb: desb.slice(0, 6), nDesb: desb.length, canvas: canv.length, canvasVacios: canv.filter(c => c.width === 0 || c.height === 0).length,
    sidebar: [...document.querySelectorAll('.nav-item')].map(a => a.textContent.replace(/\\s+/g, ' ').trim()) };
})()`;
(async () => {
  const c = await Chrome.lanzar(PC);
  await c.enviar('Runtime.enable'); await c.enviar('Log.enable'); await c.enviar('Page.enable');
  const salida = {};
  for (const ancho of [1200, 375]) {
    await c.enviar('Emulation.setDeviceMetricsOverride', { width: ancho, height: 900, deviceScaleFactor: 1, mobile: ancho < 768 });
    c.contexto = `${ancho}px carga`;
    await c.enviar('Page.navigate', { url: URL });
    await c.esperaHasta("typeof loadModule === 'function' && typeof renderMathInElement === 'function' && document.readyState === 'complete'", 30000);
    await espera(1500);
    for (let m = 1; m <= 11; m++) {
      c.contexto = `${ancho}px M${m}`;
      await c.evalua(`loadModule(${m})`);
      await espera(2200);
      // abrir los desarrollos plegados para comprobar tambien su KaTeX
      await c.evalua(`document.querySelectorAll('.derivacion-boton[aria-expanded="false"]').forEach(b => b.click()), true`);
      await espera(600);
      salida[`${ancho}-M${m}`] = await c.evalua(SONDA);
    }
  }
  salida.eventos = c.eventos;
  console.log(JSON.stringify(salida, null, 1));
  await c.cerrar();
})().catch(e => { console.error(e); process.exit(1); });
