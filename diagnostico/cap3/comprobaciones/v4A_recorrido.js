#!/usr/bin/env node
// Verificador A · R4 cap. 3 · módulos 1-6 por HTTP con Chrome sin ventana (CDP), a 1200 y 375 px.
// Comprueba por módulo: cada <cite class="cita"> compuesto como «(Autor[es], año, loc)» con el loc de
// data-loc; su enlace apunta a un <li> que existe y está en la lista «Fuentes citadas en este módulo»
// de ESE módulo; la lista del módulo tiene exactamente las obras citadas; lista del capítulo y pie;
// errores de KaTeX, «$» sin componer; consola/excepciones; desborde horizontal medido contra el ancho
// FIJADO (no innerWidth, que crece con el desborde en modo móvil); cita seguida de espacio + puntuación.
// Uso: node v4A_recorrido.js <BASE_URL> <puerto_cdp>
const fs = require('fs'); const path = require('path');
const { Chrome, espera } = require('../diag/chrome');
const [BASE, P] = process.argv.slice(2);
const ARCH = 'capitulo-3-modelos-ar-ma-arma.html';
const MODOS = { 1200: { width: 1200, height: 1000, deviceScaleFactor: 1, mobile: false },
                375: { width: 375, height: 812, deviceScaleFactor: 2, mobile: true } };
const MIDE = ancho => `(() => {
  const main = document.getElementById('main-content') || document.querySelector('main');
  const citas = [...main.querySelectorAll('cite.cita')];
  const aside = main.querySelector('aside.fuentes-modulo');
  const lis = aside ? [...aside.querySelectorAll('li')] : [];
  const idsAside = new Set(lis.map(l => l.id));
  const malCompuestas = [], sinDestino = [], fueraLista = [], espacioPunt = [];
  const refsCitadas = new Set();
  for (const c of citas) {
    const t = c.textContent.replace(/\\s+/g, ' ').trim();
    const loc = c.dataset.loc; refsCitadas.add(c.dataset.ref);
    if (!/^\\(.+, \\d{4}[a-z]?, .+\\)$/.test(t) || !t.endsWith(', ' + loc + ')')) malCompuestas.push(t + ' [' + loc + ']');
    const a = c.querySelector('a[href^="#"]');
    const id = a ? a.getAttribute('href').slice(1) : '';
    const dest = id && document.getElementById(id);
    if (!dest) sinDestino.push(t);
    else if (!idsAside.has(id)) fueraLista.push(t + ' -> ' + id);
    const s = c.nextSibling;
    if (s && s.nodeType === 3 && /^\\s+[.,;:)]/.test(s.nodeValue)) espacioPunt.push(t + ' «' + s.nodeValue.slice(0, 8) + '»');
  }
  const textoLis = lis.map(l => l.textContent.replace(/\\s+/g, ' ').trim().slice(0, 40));
  const katexErr = main.querySelectorAll('.katex-error').length;
  let dolares = 0; const w = document.createTreeWalker(main, NodeFilter.SHOW_TEXT);
  while (w.nextNode()) { const n = w.currentNode;
    if (n.parentElement.closest('pre, code, script, style, .katex, textarea')) continue;
    if (/\\$/.test(n.nodeValue)) dolares++; }
  const sw = document.documentElement.scrollWidth;
  const anchos = [...main.querySelectorAll('*')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.right > ${ancho} + 1 && !e.closest('.overflow-x-auto, pre, .katex-display, table'); })
    .slice(0, 5).map(e => e.tagName + '.' + (e.className || '').toString().slice(0, 30));
  const capitulo = document.querySelectorAll('ul.lista-fuentes').length;
  const pie = [...document.querySelectorAll('footer li')].map(l => l.textContent.replace(/\\s+/g,' ').trim().slice(0, 30));
  return { h2: (main.querySelector('h2') || {}).textContent, nCitas: citas.length, refs: [...refsCitadas].sort(), lis: textoLis,
    nLis: lis.length, malCompuestas, sinDestino, fueraLista, espacioPunt, katexErr, dolares, sw, anchos, capitulo, pie,
    afirmaciones: main.querySelectorAll('[data-afirma]').length };
})()`;
(async () => {
  const c = await Chrome.lanzar(Number(P || 9353));
  const out = []; const datos = {};
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable'); await c.enviar('Log.enable');
    for (const ancho of [1200, 375]) {
      c.contexto = ancho + ' carga';
      await c.enviar('Emulation.setDeviceMetricsOverride', MODOS[ancho]);
      await c.enviar('Page.navigate', { url: `${BASE}/${ARCH}` });
      await espera(800);
      await c.esperaHasta("typeof loadModule === 'function' && typeof renderMathInElement === 'function' && typeof Chart !== 'undefined'", 30000);
      await c.evalua('document.fonts.ready.then(() => 1)');
      for (let n = 1; n <= 6; n++) {
        c.contexto = `${ancho} M${n}`;
        await c.evalua(`(() => { loadModule(${n}); return 1; })()`);
        await espera(1500);
        const m = await c.evalua(MIDE(ancho)); datos[`${ancho}-${n}`] = m;
        out.push(`${ancho}px M${n} «${(m.h2 || '').trim()}»: ${m.afirmaciones} afirmaciones, ${m.nCitas} citas de ${m.refs.length} obras [${m.refs.join(', ')}]; ` +
          `lista del módulo ${m.nLis} [${m.lis.join(' | ')}]; mal compuestas ${m.malCompuestas.length}, sin destino ${m.sinDestino.length}, ` +
          `destino fuera de la lista del módulo ${m.fueraLista.length}, espacio antes de puntuación ${m.espacioPunt.length}; KaTeX-err ${m.katexErr}, «$» ${m.dolares}; ` +
          `scrollWidth ${m.sw}/${ancho}${m.sw > ancho + 1 ? ' DESBORDA ' + m.anchos.join(',') : ''}; listas .lista-fuentes en la página ${m.capitulo}; pie ${m.pie.length}`);
        for (const k of ['malCompuestas', 'sinDestino', 'fueraLista', 'espacioPunt']) m[k].forEach(x => out.push('    ' + k + ': ' + x));
        if (m.refs.length !== m.nLis) out.push(`    !!! obras citadas ${m.refs.length} != entradas de la lista ${m.nLis}`);
      }
      out.push(`${ancho}px pie: ${JSON.stringify(datos[ancho + '-1'].pie)}`);
    }
  } finally { await c.cerrar(); }
  out.push(`eventos de consola/excepción: ${c.eventos.length}`); c.eventos.forEach(e => out.push('  ' + e.cuando + ' · ' + e.txt.slice(0, 200)));
  fs.writeFileSync(path.join(__dirname, 'v4A_recorrido.json'), JSON.stringify(datos, null, 1));
  fs.writeFileSync(path.join(__dirname, 'v4A_recorrido.out'), out.join('\n') + '\n');
  console.log(out.join('\n'));
  process.exit(0);
})().catch(e => { console.error(e.stack); process.exit(1); });
