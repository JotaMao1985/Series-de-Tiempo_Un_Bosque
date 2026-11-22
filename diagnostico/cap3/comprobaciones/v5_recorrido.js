#!/usr/bin/env node
// Verificador R5 cap. 3 · recorrido por HTTP con Chrome sin ventana (CDP) a 1200 y 375 px.
// M1-M9: abre pista y solucion de cada «Para practicar» y mide KaTeX, «$» sin componer, desborde de
// la pagina y de las formulas. M10: abre los tres ejercicios y hace el quiz 'cap3' tres veces:
// (A) todo bien al primer intento; (B) un fallo y luego bien; (C) dos fallos; mas valores limite.
// Uso: node v5_recorrido.js <BASE_URL> <puerto_cdp>
const fs = require('fs'); const path = require('path');
const { Chrome, espera } = require('../diag/chrome');
const [BASE, PS] = process.argv.slice(2); const PUERTO = Number(PS || 9297);
const ARCHIVO = 'capitulo-3-modelos-ar-ma-arma.html';
const MODOS = { 1200: { width: 1200, height: 1000, deviceScaleFactor: 1, mobile: false },
  375: { width: 375, height: 812, deviceScaleFactor: 2, mobile: true } };
const MIDE = sel => `(() => { const m = document.getElementById('main-content') || document.querySelector('main');
  const zonas = [...m.querySelectorAll(${JSON.stringify(sel)})];
  let dol = 0, err = 0, desb = 0, vis = 0, kx = 0;
  zonas.forEach(z => { err += z.querySelectorAll('.katex-error').length; kx += z.querySelectorAll('.katex').length;
    if (z.offsetHeight > 0) vis++;
    desb += [...z.querySelectorAll('.katex-display')].filter(e => e.scrollWidth > e.clientWidth + 2).length;
    const w = document.createTreeWalker(z, NodeFilter.SHOW_TEXT);
    while (w.nextNode()) { const n = w.currentNode; if (n.parentElement.closest('pre, code, .katex')) continue; if (n.nodeValue.includes('$')) dol++; } });
  const anchos = zonas.map(z => [...z.querySelectorAll('p, li')].filter(e => e.getBoundingClientRect().right > innerWidth + 1).length).reduce((a, b) => a + b, 0);
  return { zonas: zonas.length, visibles: vis, katex: kx, katexErr: err, dolares: dol, desbordaFormula: desb, parrafosFuera: anchos,
    pagina: document.documentElement.scrollWidth, ancho: innerWidth }; })()`;
const ABRE = `(() => { const m = document.querySelector('main') || document; let n = 0;
  m.querySelectorAll('.ejercicio-boton[aria-expanded="false"]').forEach(b => { b.click(); n++; }); return n; })()`;

// Respuestas por pregunta (indice 0-9): correcta y erronea(s)
const PLAN = [
  { t: 'op', ok: 3, mal: [0, 1] }, { t: 'num', ok: '1.68', mal: ['1,7', '2.40'], borde: ['1.6849', '1.687', '1,68'] },
  { t: 'op', ok: 1, mal: [0, 2] }, { t: 'num', ok: '5.45', mal: ['5.5', '1.09'], borde: ['5.4549', '5.457'] },
  { t: 'mu', ok: [1, 3], mal: [[1], [0, 1, 3]] }, { t: 'op', ok: 3, mal: [0, 1] },
  { t: 'num', ok: '7.13', mal: ['7.1', '7.06'], borde: ['7.132', '7.1359', '7.137', '7.11'] },
  { t: 'op', ok: 2, mal: [1, 0] }, { t: 'op', ok: 0, mal: [1, 2] },
  { t: 'mu', ok: [0, 2, 4], mal: [[0, 2], [0, 1, 2, 4]] }];

const QUIZ = (modo) => `(async () => {
  const raiz = document.querySelector('[data-quiz="cap3"]'); const r = raiz.querySelector('.quiz-reiniciar'); if (r) r.click();
  await new Promise(z => setTimeout(z, 300));
  const plan = ${JSON.stringify(PLAN)}; const out = [];
  const bloques = [...raiz.querySelectorAll('.quiz-pregunta')];
  const txt = e => e ? e.textContent.replace(/\\s+/g, ' ').trim() : '';
  for (let i = 0; i < bloques.length; i++) {
    const b = bloques[i], p = plan[i]; const intentos = [];
    const ops = [...b.querySelectorAll('.quiz-opcion')]; const inp = b.querySelector('.quiz-numerica input'); const com = b.querySelector('.quiz-comprobar');
    const estado = () => ({ pista: !b.querySelector('.quiz-pista').hidden, pistaTxt: txt(b.querySelector('.quiz-pista')).slice(0, 90),
      retro: !b.querySelector('.quiz-retro').hidden, retroTxt: txt(b.querySelector('.quiz-retro')).slice(0, 90),
      cerrada: com ? com.disabled : ops.every(o => o.disabled), correctaMarcada: ops.findIndex(o => o.classList.contains('correcta')),
      katexErr: b.querySelectorAll('.katex-error').length });
    const num = v => { inp.value = v; com.click(); intentos.push({ v, ...estado() }); };
    const mu = arr => { ops.forEach((o, j) => { if (o.classList.contains('marcada') !== arr.includes(j)) o.click(); }); com.click(); intentos.push({ v: arr, ...estado() }); };
    const op = j => { ops[j].click(); intentos.push({ v: j, ...estado() }); };
    const hacer = v => p.t === 'num' ? num(v) : p.t === 'mu' ? mu(v) : op(v);
    if ('${modo}' === 'A') hacer(p.ok);
    else if ('${modo}' === 'B') { hacer(p.mal[0]); hacer(p.ok); }
    else if ('${modo}' === 'C') { hacer(p.mal[0]); hacer(p.mal[1]); }
    else if ('${modo}'.startsWith('borde') && p.borde) { const k = Number('${modo}'.slice(5)); if (p.borde[k] !== undefined) hacer(p.borde[k]); }
    out.push({ i: i + 1, tipo: p.t, intentos });
  }
  await new Promise(z => setTimeout(z, 200));
  return { preguntas: out, marcador: txt(raiz.querySelector('.quiz-marcador, .quiz-puntuacion, .quiz-resumen')).slice(0, 300) };
})()`;

async function main() {
  const c = await Chrome.lanzar(PUERTO); const sal = { base: BASE, fecha: new Date().toISOString(), r: {} }; const res = [];
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable'); await c.enviar('Log.enable');
    for (const ancho of [1200, 375]) {
      sal.r[ancho] = {}; c.contexto = `${ancho} carga`;
      await c.enviar('Emulation.setDeviceMetricsOverride', MODOS[ancho]);
      await c.enviar('Page.navigate', { url: `${BASE}/${ARCHIVO}#modulo-1` }); await espera(800);
      await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined' && typeof renderMathInElement === 'function'", 30000);
      for (let n = 1; n <= 10; n++) {
        c.contexto = `${ancho} M${n}`;
        await c.evalua(`(() => { loadModule(${n}); return 1; })()`); await espera(1200);
        const abiertos = await c.evalua(ABRE); await espera(500);
        const med = await c.evalua(MIDE('.exercise .ejercicio-guiado, .ejercicio-guiado'));
        sal.r[ancho]['M' + n] = { abiertos, ...med };
        const l = `${ancho}px M${n}: paneles abiertos ${abiertos}; zonas ${med.zonas} (visibles ${med.visibles}), fórmulas ${med.katex}, KaTeX-err ${med.katexErr}, «$» ${med.dolares}, fórmulas que desbordan ${med.desbordaFormula}, párrafos fuera ${med.parrafosFuera}, página ${med.pagina}/${med.ancho}` + (med.pagina > med.ancho + 1 ? ' DESBORDA' : '');
        console.log(l); res.push(l);
        if (n === 10) {
          for (const modo of ['A', 'B', 'C', 'borde0', 'borde1', 'borde2', 'borde3']) {
            c.contexto = `${ancho} quiz ${modo}`;
            const q = await c.evalua(QUIZ(modo)); sal.r[ancho]['quiz_' + modo] = q;
            res.push(`${ancho}px quiz ${modo}: marcador «${q.marcador}»`);
            q.preguntas.forEach(p => p.intentos.forEach((t, k) => res.push(`   P${p.i} ${p.tipo} intento ${k + 1} [${JSON.stringify(t.v)}]: cerrada=${t.cerrada} pista=${t.pista} retro=${t.retro} correcta_marcada=${t.correctaMarcada} katexErr=${t.katexErr} · retro «${t.retroTxt}» · pista «${t.pistaTxt}»`)));
          }
        }
      }
    }
    sal.eventos = c.eventos;
  } finally { await c.cerrar(); }
  fs.writeFileSync(path.join(__dirname, 'v5_recorrido.json'), JSON.stringify(sal, null, 1));
  const ev = sal.eventos || []; res.push(`eventos de consola/excepción: ${ev.length}`); ev.forEach(e => res.push('  ' + e.cuando + ' · ' + e.txt.slice(0, 220)));
  fs.writeFileSync(path.join(__dirname, 'v5_recorrido.out'), res.join('\n') + '\n'); console.log('listo; eventos:', ev.length);
}
main().then(() => process.exit(0)).catch(e => { console.error('✗ ' + e.stack); process.exit(1); });
