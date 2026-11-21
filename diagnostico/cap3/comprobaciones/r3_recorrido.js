#!/usr/bin/env node
// R3 del capítulo 3 · recorre los 11 módulos por HTTP con Chrome sin ventana (CDP) a 1200 y 375 px.
// Por módulo: excepciones y errores de consola, errores de KaTeX (.katex-error), «$» sin componer,
// fórmulas que desbordan, lienzos que se pintaron, titulares h3 en orden, el título del módulo en el
// encabezado y en la barra lateral, y que lo movido esté donde debe.
//
// Uso: node r3_recorrido.js <BASE_URL> <puerto_cdp>
// Salida: r3_recorrido.json y r3_recorrido.out (resumen) junto a este archivo.
const fs = require('fs');
const path = require('path');
const { Chrome, espera } = require('../diag/chrome');

const [BASE, PUERTO_S] = process.argv.slice(2);
const PUERTO = Number(PUERTO_S || 9283);
const ARCHIVO = 'capitulo-3-modelos-ar-ma-arma.html';
const MODOS = {
  1200: { width: 1200, height: 1000, deviceScaleFactor: 1, mobile: false },
  375: { width: 375, height: 812, deviceScaleFactor: 2, mobile: true },
};

const MEDIDAS = `(() => {
  const main = document.getElementById('main-content') || document.querySelector('main');
  const h2 = main.querySelector('h2');
  const h3 = [...main.querySelectorAll('h3')].filter(e => !e.closest('.simulador') && !e.closest('div.rounded-lg'))
    .map(e => e.textContent.replace(/\\s+/g, ' ').trim());
  const katexErr = main.querySelectorAll('.katex-error').length;
  // «$» que quedó como texto (fórmula sin componer): se busca en los nodos de texto fuera de código
  let dolares = 0;
  const w = document.createTreeWalker(main, NodeFilter.SHOW_TEXT);
  while (w.nextNode()) {
    const n = w.currentNode;
    if (n.parentElement.closest('pre, code, script, style, .katex, .quiz, .simulacro')) continue;
    if (n.nodeValue.includes('$')) dolares++;
  }
  const lienzos = [...main.querySelectorAll('canvas')].map(cv => {
    const ch = Chart.getChart(cv);
    return { pintado: !!ch, w: Math.round(cv.getBoundingClientRect().width) };
  });
  const katexDesborda = [...main.querySelectorAll('.katex-display')].filter(e => e.scrollWidth > e.clientWidth + 2).length;
  const lecturas = [...main.querySelectorAll('.simulador-lectura')].map(e => e.textContent.trim().length);
  const nTablas = main.querySelectorAll('table').length;
  const nCodigo = main.querySelectorAll('.code-tabs').length;
  return { h2: h2 ? h2.textContent.replace(/\\s+/g, ' ').trim() : null, h3, katexErr, dolares, lienzos,
    sinPintar: lienzos.filter(l => !l.pintado).length, katexDesborda, lecturasVacias: lecturas.filter(n => n === 0).length,
    nTablas, nCodigo, docSw: document.documentElement.scrollWidth, innerWidth,
    formulas: main.querySelectorAll('.katex').length };
})()`;

async function main() {
  const c = await Chrome.lanzar(PUERTO);
  const salida = { base: BASE, fecha: new Date().toISOString(), r: {} };
  const resumen = [];
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable'); await c.enviar('Log.enable');
    for (const ancho of [1200, 375]) {
      salida.r[ancho] = {};
      c.contexto = `${ancho} carga`;
      await c.enviar('Emulation.setDeviceMetricsOverride', MODOS[ancho]);
      await c.enviar('Page.navigate', { url: `${BASE}/${ARCHIVO}#modulo-1` });
      await espera(700);
      await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined' && typeof renderMathInElement === 'function'", 30000);
      await c.evalua('document.fonts.ready.then(() => 1)');
      await c.evalua(`(() => { Chart.defaults.animation = false; Chart.defaults.animations = {}; return 1; })()`);
      const titulos = await c.evalua(`courseData.modules.map(m => m.title + ' (' + m.duration + ')')`);
      salida.r[ancho].courseData = titulos;
      const lateral = await c.evalua(`[...document.querySelectorAll('#module-nav .nav-item')].map(e => e.textContent.replace(/\\s+/g,' ').trim()).filter(t => /Cierre/.test(t))`);
      salida.r[ancho].lateral = lateral;
      for (let n = 1; n <= 11; n++) {
        c.contexto = `${ancho} M${n}`;
        await c.evalua(`(() => { loadModule(${n}); return 1; })()`);
        await espera(1300);
        const med = await c.evalua(MEDIDAS);
        salida.r[ancho][n] = med;
        const linea = `${ancho}px M${n}: «${med.h2}» · ${med.formulas} fórmulas, KaTeX-err ${med.katexErr}, «$» ${med.dolares}, ` +
          `lienzos ${med.lienzos.length} (sin pintar ${med.sinPintar}), desbordan ${med.katexDesborda}, tablas ${med.nTablas}, código ${med.nCodigo}`;
        console.log(linea); resumen.push(linea);
      }
    }
    salida.eventos = c.eventos;
  } finally {
    await c.cerrar();
  }
  fs.writeFileSync(path.join(__dirname, 'r3_recorrido.json'), JSON.stringify(salida, null, 1));
  const ev = salida.eventos || [];
  resumen.push(`eventos de consola/excepción: ${ev.length}`);
  ev.forEach(e => resumen.push('  ' + e.cuando + ' · ' + e.txt.slice(0, 220)));
  fs.writeFileSync(path.join(__dirname, 'r3_recorrido.out'), resumen.join('\n') + '\n');
  console.log('listo; eventos:', ev.length);
}
main().then(() => process.exit(0)).catch(e => { console.error('✗ ' + e.stack); process.exit(1); });
