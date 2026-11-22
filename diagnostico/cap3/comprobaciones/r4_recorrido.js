#!/usr/bin/env node
// R4 del capítulo 3 · recorre los 11 módulos por HTTP con Chrome sin ventana (CDP) a 1200 y 375 px.
// Por módulo: excepciones y errores de consola, errores de KaTeX (.katex-error), «$» sin componer,
// fórmulas que desbordan, lienzos que se pintaron, titulares h3 en orden, el título del módulo en el
// encabezado, y lo de esta ronda: citas compuestas (ninguna vacía), enlaces de cita con destino en el
// módulo abierto, la lista de fuentes del módulo, la del capítulo, el pie, citas fuera del viewport,
// puntuación huérfana tras una cita y desborde horizontal de la página.
//
// Uso: node r4_recorrido.js <BASE_URL> <puerto_cdp>
// Salida: r4_recorrido.json y r4_recorrido.out (resumen) junto a este archivo.
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
  const citas = [...main.querySelectorAll('cite.cita')];
  const citasVacias = citas.filter(c => !c.textContent.trim()).length;
  const sinDestino = citas.filter(c => { const a = c.querySelector('a'); if (!a) return true;
    const id = (a.getAttribute('href') || '').slice(1); return !id || !document.getElementById(id); }).length;
  const fueraViewport = citas.filter(c => { const r = c.getBoundingClientRect(); return r.width > 0 && (r.right > innerWidth + 1 || r.left < -1); }).length;
  const sinAfirma = citas.filter(c => !c.closest('[data-afirma]')).length;
  const aside = main.querySelector('aside.fuentes-modulo');
  const fuentesModulo = aside ? aside.querySelectorAll('ul.lista-fuentes > li').length : 0;
  const asideEstilo = aside ? getComputedStyle(aside).borderTopStyle + '/' + getComputedStyle(aside).fontSize : null;
  const citaEstilo = citas.length ? getComputedStyle(citas[0]).fontStyle + '/' + getComputedStyle(citas[0].querySelector('a')).color : null;
  const refsCapitulo = [...main.querySelectorAll('ul.lista-fuentes')].filter(u => !u.closest('aside')).reduce((s, u) => s + u.children.length, 0);
  const pie = document.querySelectorAll('footer ul.lista-fuentes > li').length;
  // puntuación que quedó sola al principio de una línea tras una cita
  let huerfana = 0;
  citas.forEach(c => { const s = c.nextSibling; if (!s || s.nodeType !== 3 || !/^[.,;:)]/.test(s.nodeValue)) return;
    const r = document.createRange(); r.setStart(s, 0); r.setEnd(s, 1);
    const a = c.getClientRects(); const b = r.getBoundingClientRect();
    if (a.length && b.top > a[a.length - 1].bottom - 2) huerfana++; });
  const afirmaciones = main.querySelectorAll('[data-afirma]').length;
  const nTablas = main.querySelectorAll('table').length;
  const nCodigo = main.querySelectorAll('.code-tabs').length;
  return { h2: h2 ? h2.textContent.replace(/\\s+/g, ' ').trim() : null, h3, katexErr, dolares, lienzos,
    sinPintar: lienzos.filter(l => !l.pintado).length, katexDesborda, lecturasVacias: lecturas.filter(n => n === 0).length,
    nTablas, nCodigo, docSw: document.documentElement.scrollWidth, innerWidth,
    afirmaciones, nCitas: citas.length, citasVacias, sinDestino, fueraViewport, sinAfirma, fuentesModulo, asideEstilo, citaEstilo,
    refsCapitulo, pie, huerfana,
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
          `lienzos ${med.lienzos.length} (sin pintar ${med.sinPintar}), desbordan ${med.katexDesborda} · afirmaciones ${med.afirmaciones}, citas ${med.nCitas} ` +
          `(vacías ${med.citasVacias}, sin destino ${med.sinDestino}, fuera del viewport ${med.fueraViewport}, fuera de afirmación ${med.sinAfirma}, puntuación huérfana ${med.huerfana}), ` +
          `fuentes del módulo ${med.fuentesModulo}, lista del capítulo ${med.refsCapitulo}, pie ${med.pie}, página ${med.docSw}/${med.innerWidth}px` +
          (med.docSw > med.innerWidth + 1 ? ' DESBORDA' : '');
        console.log(linea); resumen.push(linea);
      }
    }
    salida.eventos = c.eventos;
  } finally {
    await c.cerrar();
  }
  fs.writeFileSync(path.join(__dirname, 'r4_recorrido.json'), JSON.stringify(salida, null, 1));
  const ev = salida.eventos || [];
  resumen.push(`eventos de consola/excepción: ${ev.length}`);
  ev.forEach(e => resumen.push('  ' + e.cuando + ' · ' + e.txt.slice(0, 220)));
  fs.writeFileSync(path.join(__dirname, 'r4_recorrido.out'), resumen.join('\n') + '\n');
  console.log('listo; eventos:', ev.length);
}
main().then(() => process.exit(0)).catch(e => { console.error('✗ ' + e.stack); process.exit(1); });
