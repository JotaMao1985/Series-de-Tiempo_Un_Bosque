#!/usr/bin/env node
// Verificador B · R4 del capítulo 3 · módulos 7-11 por HTTP con Chrome sin ventana (CDP), a 1200 y 375 px.
// Por módulo: excepciones y errores de consola, .katex-error, «$» sin componer, citas compuestas,
// destino de cada enlace de cita (en la lista del módulo abierto), citas que caen fuera del ancho
// (y si están dentro de un contenedor con desplazamiento propio), desborde horizontal de la página.
// Abre todos los <details> antes de medir. Captura a 375 px las celdas de tabla con cita del M10.
// Uso: node v4B_recorrido.js <BASE_URL> <puerto_cdp>
const fs = require('fs');
const path = require('path');
const { Chrome, espera } = require('../diag/chrome');

const [BASE, PUERTO_S] = process.argv.slice(2);
const PUERTO = Number(PUERTO_S || 9261);
const URL = BASE.replace(/\/$/, '') + '/capitulo-3-modelos-ar-ma-arma.html';
const MODOS = {
  1200: { width: 1200, height: 1000, deviceScaleFactor: 1, mobile: false },
  375: { width: 375, height: 812, deviceScaleFactor: 2, mobile: true },
};

const MEDIDAS = (ancho) => `(() => {
  const main = document.getElementById('main-content') || document.querySelector('main');
  main.querySelectorAll('details').forEach(d => d.open = true);
  const citas = [...main.querySelectorAll('cite.cita')];
  const vacias = citas.filter(c => !c.textContent.replace(/[()\\s]/g, '')).length;
  const sinDestino = [];
  const fuera = [];
  for (const c of citas) {
    const a = c.querySelector('a[href^="#"]');
    const id = a ? a.getAttribute('href').slice(1) : null;
    const dest = id ? document.getElementById(id) : null;
    if (!dest || !main.contains(dest)) sinDestino.push((c.dataset.ref || '') + ' ' + (c.dataset.loc || '') + ' -> ' + id);
    const r = c.getBoundingClientRect();
    if (r.width && (r.right > ${ancho} + 0.5 || r.left < -0.5)) {
      let p = c.parentElement, cont = null;
      while (p && p !== main) { const s = getComputedStyle(p); if (/(auto|scroll)/.test(s.overflowX) && p.scrollWidth > p.clientWidth) { cont = p; break; } p = p.parentElement; }
      const afirma = c.closest('[data-afirma]');
      fuera.push({ cita: c.textContent.trim(), afirma: afirma ? afirma.dataset.afirma : null,
        right: Math.round(r.right), contenedor: cont ? (cont.tagName + '.' + cont.className).slice(0, 60) : null });
    }
  }
  const katexErr = main.querySelectorAll('.katex-error').length;
  let dolares = 0;
  const w = document.createTreeWalker(main, NodeFilter.SHOW_TEXT);
  while (w.nextNode()) {
    const n = w.currentNode;
    if (n.parentElement.closest('pre, code, script, style, .katex, .quiz, .simulacro, textarea')) continue;
    if (/\\$/.test(n.nodeValue)) dolares++;
  }
  const lista = [...main.querySelectorAll('li[id^="ref-"]')].map(li => li.id);
  return { titulo: (main.querySelector('h2') || {}).textContent?.replace(/\\s+/g, ' ').trim().slice(0, 50),
    citas: citas.length, vacias, sinDestino, fuera, katexErr, dolares, lista,
    scrollW: document.documentElement.scrollWidth, bodyW: document.body.scrollWidth };
})()`;

(async () => {
  const c = await Chrome.lanzar(PUERTO);
  await c.enviar('Runtime.enable'); await c.enviar('Log.enable'); await c.enviar('Page.enable');
  const salida = {};
  const lineas = [];
  for (const [ancho, m] of Object.entries(MODOS)) {
    await c.enviar('Emulation.setDeviceMetricsOverride', m);
    c.contexto = 'carga ' + ancho;
    await c.enviar('Page.navigate', { url: URL });
    await c.esperaHasta('typeof loadModule === "function" && document.readyState === "complete"', 30000);
    await espera(1500);
    for (const n of [7, 8, 9, 10, 11]) {
      c.contexto = `M${n} @${ancho}`;
      await c.evalua(`(async () => { if (window.Chart) Chart.defaults.animation = false; await loadModule(${n}); })()`);
      await espera(2500);
      const r = await c.evalua(MEDIDAS(Number(ancho)));
      r.eventos = c.eventos.filter(e => e.cuando === c.contexto).map(e => e.txt);
      salida[`M${n}@${ancho}`] = r;
      lineas.push(`M${n} @${ancho}px «${r.titulo}»: citas ${r.citas} (vacías ${r.vacias}), sin destino ${r.sinDestino.length}` +
        `, fuera del ancho ${r.fuera.length}, katex-error ${r.katexErr}, «$» sueltos ${r.dolares}, ` +
        `lista del módulo ${r.lista.length}, scrollWidth ${r.scrollW}/${r.bodyW}, eventos ${r.eventos.length}`);
      r.sinDestino.forEach(s => lineas.push('    SIN DESTINO: ' + s));
      r.fuera.forEach(f => lineas.push(`    FUERA: ${f.cita} [${f.afirma}] right=${f.right} contenedor=${f.contenedor}`));
      r.eventos.forEach(e => lineas.push('    EVENTO: ' + e));
      if (n === 10 && ancho === '375') {
        // captura de la tabla del M10 con las celdas citadas
        const rect = await c.evalua(`(() => { const t = [...document.querySelectorAll('#main-content table')].find(t => t.querySelector('cite.cita'));
          if (!t) return null; t.scrollIntoView({block: 'start', behavior: 'instant'}); const r = t.closest('div')?.getBoundingClientRect() || t.getBoundingClientRect();
          return { x: r.left + scrollX, y: r.top + scrollY, w: Math.min(r.width, 375), h: Math.min(r.height, 1600) }; })()`);
        if (rect) {
          const img = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
            clip: { x: Math.max(0, rect.x), y: rect.y, width: rect.w, height: rect.h, scale: 1 } });
          fs.writeFileSync(path.join(__dirname, 'v4B_m10_tabla_375.png'), Buffer.from(img.data, 'base64'));
          lineas.push('    captura: v4B_m10_tabla_375.png');
        }
      }
    }
  }
  const otros = c.eventos.filter(e => e.cuando && e.cuando.startsWith('carga')).map(e => e.cuando + ': ' + e.txt);
  otros.forEach(e => lineas.push('EVENTO de carga: ' + e));
  fs.writeFileSync(path.join(__dirname, 'v4B_recorrido.json'), JSON.stringify(salida, null, 1));
  fs.writeFileSync(path.join(__dirname, 'v4B_recorrido.out'), lineas.join('\n') + '\n');
  console.log(lineas.join('\n'));
  await c.cerrar();
})().catch(e => { console.error(e); process.exit(1); });
