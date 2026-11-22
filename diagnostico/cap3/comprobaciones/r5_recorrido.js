#!/usr/bin/env node
// R5 del capítulo 3 · recorrido por HTTP con Chrome sin ventana (CDP), a 1200 y 375 px.
//   1. Módulos 1 a 10: errores de consola y de KaTeX, «$» sin componer, lienzos pintados, desborde
//      horizontal de la página; y en cada ejercicio (los ocho «Para practicar» y los tres del
//      Módulo 10): se abren la pista y la solución, se comprueba que los dos paneles quedan a la
//      vista, que el código sale coloreado y sin colapsar, y que ninguna fórmula se sale del ancho.
//   2. El quiz `cap3` entero, cuatro veces, pulsando botones y escribiendo en las casillas:
//        A  todo bien al primer intento;
//        B  fallo y acierto (se guarda la pista que sale en cada pregunta);
//        C  dos fallos (retro de fallo y, en las de varias respuestas, el desglose por opción);
//        D  las numéricas con valores de borde (redondeo pedido, coma decimal, tropiezos).
//
// Uso: node r5_recorrido.js <BASE_URL> <puerto_cdp>     Salida: r5_recorrido.json y r5_recorrido.out
const fs = require('fs');
const path = require('path');
const { Chrome, espera } = require('../diag/chrome');

const [BASE, PUERTO_S] = process.argv.slice(2);
const PUERTO = Number(PUERTO_S || 9285);
const ARCHIVO = 'capitulo-3-modelos-ar-ma-arma.html';
const MODOS = {
  1200: { width: 1200, height: 1000, deviceScaleFactor: 1, mobile: false },
  375: { width: 375, height: 812, deviceScaleFactor: 2, mobile: true },
};

const MODULO = `(() => {
  const main = document.getElementById('main-content') || document.querySelector('main');
  let dolares = 0;
  const w = document.createTreeWalker(main, NodeFilter.SHOW_TEXT);
  while (w.nextNode()) {
    const n = w.currentNode;
    if (n.parentElement.closest('pre, code, script, style, .katex, .quiz, .simulacro')) continue;
    if (n.nodeValue.includes('$')) dolares++;
  }
  const lienzos = [...main.querySelectorAll('canvas')].map(cv => !!Chart.getChart(cv));
  const ej = [...main.querySelectorAll('.ejercicio-guiado')].map(g => {
    const paneles = [...g.querySelectorAll('.ejercicio-panel')];
    const pres = [...g.querySelectorAll('pre')];
    const anchas = [...g.querySelectorAll('.katex')].filter(k => { const r = k.getBoundingClientRect(); return r.width > 0 && r.right > innerWidth + 1; }).length;
    return { titulo: (g.closest('.exercise')?.querySelector('h4')?.textContent || g.querySelector('.ejercicio-numero')?.textContent || '').trim(),
      entregables: g.querySelectorAll('ol > li').length,
      panelesVisibles: paneles.filter(p => !p.hidden && p.getBoundingClientRect().height > 20).length,
      botonesAbiertos: [...g.querySelectorAll('.ejercicio-boton')].filter(b => b.getAttribute('aria-expanded') === 'true').length,
      pres: pres.length, coloreados: pres.filter(p => p.querySelector('.token')).length,
      colapsados: pres.filter(p => p.classList.contains('collapsed')).length,
      lineasCodigo: pres.reduce((s, p) => s + p.textContent.split('\\n').length, 0),
      formulas: g.querySelectorAll('.katex').length, katexErr: g.querySelectorAll('.katex-error').length, formulasFuera: anchas,
      palabrasEnunciado: (g.querySelector('.ejercicio-enunciado')?.textContent || '').trim().split(/\\s+/).length };
  });
  return { h2: (main.querySelector('h2')?.textContent || '').replace(/\\s+/g, ' ').trim(), katexErr: main.querySelectorAll('.katex-error').length, dolares,
    lienzos: lienzos.length, sinPintar: lienzos.filter(x => !x).length, docSw: document.documentElement.scrollWidth, innerWidth, ej,
    cajasPractica: [...main.querySelectorAll('.exercise > h4')].filter(h => /Para practicar/.test(h.textContent)).length };
})()`;

// Utilidades que se inyectan en la página para manejar el quiz como lo haría una persona
const AYUDAS = `window.__q = {
  raiz: () => document.querySelector('.quiz[data-quiz="cap3"]'),
  bloques: () => [...window.__q.raiz().querySelectorAll('.quiz-pregunta')],
  datos: () => AUTOEVALUACIONES['cap3'],
  escribe: (i, v) => { const b = window.__q.bloques()[i]; const inp = b.querySelector('input'); inp.value = v; b.querySelector('.quiz-comprobar').click(); },
  pulsa: (i, j) => window.__q.bloques()[i].querySelectorAll('.quiz-opcion')[j].click(),
  marca: (i, js) => { const b = window.__q.bloques()[i]; const ops = b.querySelectorAll('.quiz-opcion');
    ops.forEach((o, j) => { const on = o.classList.contains('marcada'); if (on !== js.includes(j)) o.click(); }); b.querySelector('.quiz-comprobar').click(); },
  texto: (i, sel) => { const e = window.__q.bloques()[i].querySelector(sel); return e && !e.hidden ? e.textContent.replace(/\\s+/g, ' ').trim() : null; },
  estado: () => ({ marcador: window.__q.raiz().querySelector('.quiz-conteo').textContent.trim(),
    resumen: (() => { const r = window.__q.raiz().querySelector('.quiz-resumen'); return r && !r.hidden ? r.textContent.replace(/\\s+/g, ' ').trim() : null; })(),
    katexErr: window.__q.raiz().querySelectorAll('.katex-error').length,
    indefinidos: (window.__q.raiz().textContent.match(/undefined|NaN/g) || []).length,
    fuera: [...window.__q.raiz().querySelectorAll('.katex, .quiz-opcion')].filter(k => { const r = k.getBoundingClientRect(); return r.width > 0 && r.right > innerWidth + 1; }).length }),
  reinicia: () => window.__q.raiz().querySelector('.quiz-reiniciar').click(),
}; 1`;

async function main() {
  const c = await Chrome.lanzar(PUERTO);
  const salida = { base: BASE, fecha: new Date().toISOString(), modulos: {}, quiz: {} };
  const R = [];
  const di = s => { console.log(s); R.push(s); };
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable'); await c.enviar('Log.enable');
    for (const ancho of [1200, 375]) {
      c.contexto = `${ancho} carga`;
      await c.enviar('Emulation.setDeviceMetricsOverride', MODOS[ancho]);
      await c.enviar('Page.navigate', { url: `${BASE}/${ARCHIVO}#modulo-1` });
      await espera(700);
      await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined' && typeof renderMathInElement === 'function'", 30000);
      await c.evalua('document.fonts.ready.then(() => 1)');
      await c.evalua(`(() => { Chart.defaults.animation = false; Chart.defaults.animations = {}; return 1; })()`);
      salida.modulos[ancho] = {};
      di(`\n===== ${ancho} px =====`);
      di('barra lateral: ' + (await c.evalua(`courseData.modules.map(m => m.id + ':' + m.duration).join(' · ')`)));
      for (let n = 1; n <= 10; n++) {
        c.contexto = `${ancho} M${n}`;
        await c.evalua(`(() => { loadModule(${n}); return 1; })()`);
        await espera(1200);
        // abre la pista y la solución de cada ejercicio, como haría el estudiante
        await c.evalua(`(() => { document.querySelectorAll('#main-content .ejercicio-boton').forEach(b => b.click()); return 1; })()`);
        await espera(500);
        const m = await c.evalua(MODULO);
        salida.modulos[ancho][n] = m;
        di(`M${n} «${m.h2.slice(0, 38)}»: KaTeX-err ${m.katexErr}, «$» ${m.dolares}, lienzos ${m.lienzos} (sin pintar ${m.sinPintar}), ` +
          `página ${m.docSw}/${m.innerWidth}${m.docSw > m.innerWidth + 1 ? ' DESBORDA' : ''}, «Para practicar» ${m.cajasPractica}, ejercicios ${m.ej.length}`);
        m.ej.forEach(e => di(`     · ${e.titulo}: ${e.entregables} entregables, enunciado ${e.palabrasEnunciado} palabras, paneles a la vista ${e.panelesVisibles}/2, ` +
          `código ${e.pres} bloque(s) (${e.lineasCodigo} líneas; coloreados ${e.coloreados}, colapsados ${e.colapsados}), ${e.formulas} fórmulas ` +
          `(KaTeX-err ${e.katexErr}, fuera del ancho ${e.formulasFuera})`));
      }

      // ------------------------------------------------------------ el quiz, a mano
      c.contexto = `${ancho} quiz`;
      await c.evalua(`(() => { loadModule(10); return 1; })()`);
      await espera(1200);
      await c.evalua(AYUDAS);
      const datos = await c.evalua(`window.__q.datos().map(p => ({ tipo: p.tipo, modulo: p.modulo, respuesta: p.respuesta, tolerancia: p.tolerancia,
        correctas: (p.opciones || []).map((o, j) => o.correcta ? j : -1).filter(j => j >= 0), n: (p.opciones || []).length }))`);
      const malo = { 1: '2.4', 3: '6.8', 6: '0.12' };            // un tropiezo típico en cada numérica (índices desde 0)
      const quiz = { A: null, B: [], C: [], D: [] };

      // A · todo bien al primer intento
      for (let i = 0; i < datos.length; i++) {
        const p = datos[i];
        if (p.tipo === 'numerica') await c.evalua(`window.__q.escribe(${i}, '${p.respuesta}')`);
        else if (p.tipo === 'multiple') await c.evalua(`window.__q.marca(${i}, ${JSON.stringify(p.correctas)})`);
        else await c.evalua(`window.__q.pulsa(${i}, ${p.correctas[0]})`);
        await espera(120);
      }
      quiz.A = await c.evalua('window.__q.estado()');
      di(`quiz A (todo bien): ${quiz.A.marcador} | ${quiz.A.resumen} | KaTeX-err ${quiz.A.katexErr}, «undefined/NaN» ${quiz.A.indefinidos}, fuera del ancho ${quiz.A.fuera}`);

      // B · fallo y acierto
      await c.evalua('window.__q.reinicia()'); await espera(400);
      for (let i = 0; i < datos.length; i++) {
        const p = datos[i];
        const noCorrecta = [...Array(p.n).keys()].find(j => !p.correctas.includes(j));
        if (p.tipo === 'numerica') await c.evalua(`window.__q.escribe(${i}, '${malo[i]}')`);
        else if (p.tipo === 'multiple') await c.evalua(`window.__q.marca(${i}, ${JSON.stringify([p.correctas[0], noCorrecta])})`);
        else await c.evalua(`window.__q.pulsa(${i}, ${noCorrecta})`);
        await espera(150);
        const pista = await c.evalua(`window.__q.texto(${i}, '.quiz-pista')`);
        if (p.tipo === 'numerica') await c.evalua(`window.__q.escribe(${i}, '${p.respuesta}')`);
        else if (p.tipo === 'multiple') await c.evalua(`window.__q.marca(${i}, ${JSON.stringify(p.correctas)})`);
        else await c.evalua(`window.__q.pulsa(${i}, ${p.correctas[0]})`);
        await espera(150);
        const retro = await c.evalua(`window.__q.texto(${i}, '.quiz-retro')`);
        quiz.B.push({ i: i + 1, pista, retro });
      }
      const eB = await c.evalua('window.__q.estado()');
      di(`quiz B (fallo y acierto): ${eB.marcador} | ${eB.resumen} | KaTeX-err ${eB.katexErr}, «undefined/NaN» ${eB.indefinidos}`);
      quiz.B.forEach(x => di(`     P${x.i} pista: ${(x.pista || 'SIN PISTA').slice(0, 150)}${x.pista && x.pista.length > 150 ? '…' : ''}`));

      // C · dos fallos
      await c.evalua('window.__q.reinicia()'); await espera(400);
      for (let i = 0; i < datos.length; i++) {
        const p = datos[i];
        const malas = [...Array(p.n).keys()].filter(j => !p.correctas.includes(j));
        for (let intento = 0; intento < 2; intento++) {
          if (p.tipo === 'numerica') await c.evalua(`window.__q.escribe(${i}, '${malo[i]}')`);
          else if (p.tipo === 'multiple') await c.evalua(`window.__q.marca(${i}, ${JSON.stringify([malas[0], p.correctas[0]])})`);
          else await c.evalua(`window.__q.pulsa(${i}, ${malas[intento]})`);
          await espera(150);
        }
        const retro = await c.evalua(`window.__q.texto(${i}, '.quiz-retro')`);
        const desglose = await c.evalua(`window.__q.bloques()[${i}].querySelectorAll('.quiz-retro li').length`);
        quiz.C.push({ i: i + 1, retro, desglose });
      }
      const eC = await c.evalua('window.__q.estado()');
      di(`quiz C (dos fallos): ${eC.marcador} | ${eC.resumen} | KaTeX-err ${eC.katexErr}, «undefined/NaN» ${eC.indefinidos}`);
      quiz.C.forEach(x => di(`     P${x.i}: retro de ${(x.retro || '').length} caracteres${datos[x.i - 1].tipo === 'multiple' ? `, desglose de ${x.desglose} opción(es) mal juzgadas` : ''}` +
        `${x.retro ? '' : ' · SIN RETRO'}`));

      // D · numéricas en el borde: cada valor se escribe en la casilla, en un quiz recién reiniciado
      const pruebas = { 1: ['1.68', '1,68', '1.675', '1.7', '1.69', '2.4', '0.42', '3.12', '0.29', '-1.2'],
        3: ['5.45', '5,45', '5.5', '5.4', '5.46', '1.09', '0.45', '6.8', '9.05', '6.5', '5.61'],
        6: ['7.13', '7,13', '7.132', '7.1317', '7.1', '7.14', '7.12', '7', '0.12', '13.93', '7.57'] };
      for (const i of Object.keys(pruebas)) {
        for (const v of pruebas[i]) {
          await c.evalua('window.__q.reinicia()'); await espera(120);
          await c.evalua(`window.__q.escribe(${i}, '${v}')`); await espera(80);
          const retro = await c.evalua(`window.__q.texto(${i}, '.quiz-retro')`);
          quiz.D.push({ i: Number(i) + 1, v, acierta: !!retro && /^Correcto/.test(retro) });
        }
        di(`quiz D · P${Number(i) + 1} (respuesta ${datos[i].respuesta}, tolerancia ${datos[i].tolerancia}): ` +
          quiz.D.filter(x => x.i === Number(i) + 1).map(x => `${x.v} ${x.acierta ? 'ACIERTA' : 'falla'}`).join(' · '));
      }
      salida.quiz[ancho] = quiz;
    }
    salida.eventos = c.eventos;
  } finally {
    await c.cerrar();
  }
  const ev = salida.eventos || [];
  di(`\neventos de consola o excepciones: ${ev.length}`);
  ev.forEach(e => di('  ' + e.cuando + ' · ' + e.txt.slice(0, 240)));
  fs.writeFileSync(path.join(__dirname, 'r5_recorrido.json'), JSON.stringify(salida, null, 1));
  fs.writeFileSync(path.join(__dirname, 'r5_recorrido.out'), R.join('\n') + '\n');
}
main().then(() => process.exit(0)).catch(e => { console.error('✗ ' + e.stack); process.exit(1); });
