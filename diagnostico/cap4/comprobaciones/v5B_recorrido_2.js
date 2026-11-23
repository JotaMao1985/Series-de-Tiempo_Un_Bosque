#!/usr/bin/env node
// Verificador B · R5 del capítulo 4 · por HTTP (servidor 8774, Chrome sin ventana en el CDP 9284) · segunda lectura.
// M10: los ejercicios 1-3 con sus paneles abiertos y el quiz AUTOEVALUACIONES['cap4'] hecho en el navegador,
// a 1200 y 375 px: KaTeX, «$» sin componer, desbordamiento, consola; cuatro pasadas del quiz y valores límite
// de la numérica. Capturas en diagnostico/cap4/capturas/r5/v5B/.
// Uso: node diagnostico/cap4/comprobaciones/v5B_recorrido.js > diagnostico/cap4/comprobaciones/v5B_recorrido.out
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const { Chrome, espera } = require('../diag/chrome');

const RAIZ = path.resolve(__dirname, '..', '..', '..');
const OUT = path.resolve(__dirname, '..', 'capturas', 'r5', 'v5B_2');
const PUERTO_HTTP = 8774, PUERTO_CDP = 9284;
const BASE = `http://127.0.0.1:${PUERTO_HTTP}/capitulo-4-modelos-arima.html`;
// clave: índice 0-based de la correcta (lista en la múltiple; cadena con el número en la numérica)
const CLAVE = [1, '5.02', 2, [0, 2, 3], 1, 3, 2, 0];
const MAL = [0, '5.04', 0, [1, 4], 0, 0, 0, 2];         // primer fallo de cada pregunta
const MAL2 = [2, '5.00', 1, [0, 1], 2, 1, 1, 1];        // segundo fallo

const MEDIR = sel => `(() => {
  const zonas = [...document.querySelectorAll(${JSON.stringify(sel)})];
  let katexError = 0, katex = 0; const sueltos = [], seSalen = [];
  for (const z of zonas) {
    katexError += z.querySelectorAll('.katex-error').length; katex += z.querySelectorAll('.katex').length;
    const w = document.createTreeWalker(z, NodeFilter.SHOW_TEXT);
    for (let n = w.nextNode(); n; n = w.nextNode()) {
      const p = n.parentElement; if (!p || p.closest('pre, code, script, style, .katex, textarea')) continue;
      if (/\\$[^$]/.test(n.textContent) || /\\\\(frac|phi|theta|rho|sqrt|sum|hat|nabla|psi|sigma)/.test(n.textContent)) sueltos.push(n.textContent.trim().slice(0, 80));
    }
    for (const e of z.querySelectorAll('.katex-display, ol, p, li, .quiz-opcion, canvas')) {
      const r = e.getBoundingClientRect(); if (e.offsetParent !== null && r.right > innerWidth + 1 && !e.closest('pre')
        && ![...(function*(){ let a = e.parentElement; while (a) { yield a; a = a.parentElement; } })()].some(a => /auto|scroll|hidden/.test(getComputedStyle(a).overflowX))) seSalen.push(e.tagName + ' ' + e.textContent.slice(0, 40));
    }
  }
  return { zonas: zonas.length, katex, katexError, sueltos, seSalen, pagina: document.documentElement.scrollWidth, ventana: innerWidth };
})()`;

async function captura(c, sel, idx, archivo) {
  await c.evalua(`(() => { document.querySelectorAll(${JSON.stringify(sel)})[${idx}].scrollIntoView({ behavior: 'instant', block: 'start' }); return 1; })()`);
  await espera(900);
  const r = await c.enviar('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(OUT, archivo), Buffer.from(r.data, 'base64'));
}

const Q = `document.querySelector('.quiz[data-quiz="cap4"]')`;
const estadoQ = i => `(() => { const b = ${Q}.querySelectorAll('.quiz-pregunta')[${i}];
  const t = s => { const e = b.querySelector(s); return e && !e.hidden ? e.textContent.replace(/\\s+/g, ' ').trim() : null; };
  return { pista: t('.quiz-pista'), retro: t('.quiz-retro'), clase: b.querySelector('.quiz-retro').className,
           katexError: b.querySelectorAll('.katex-error').length }; })()`;
async function responder(c, i, valor) {
  if (typeof valor === 'string') {
    return c.evalua(`(() => { const b = ${Q}.querySelectorAll('.quiz-pregunta')[${i}]; const inp = b.querySelector('input');
      inp.value = ${JSON.stringify(valor)}; b.querySelector('.quiz-comprobar').click(); return 1; })()`);
  }
  if (Array.isArray(valor)) {
    return c.evalua(`(() => { const b = ${Q}.querySelectorAll('.quiz-pregunta')[${i}]; const ops = b.querySelectorAll('.quiz-opcion');
      ops.forEach(o => { if (o.classList.contains('marcada')) o.click(); });
      ${JSON.stringify(valor)}.forEach(j => ops[j].click()); b.querySelector('.quiz-comprobar').click(); return 1; })()`);
  }
  return c.evalua(`(() => { ${Q}.querySelectorAll('.quiz-pregunta')[${i}].querySelectorAll('.quiz-opcion')[${valor}].click(); return 1; })()`);
}
const reiniciar = c => c.evalua(`(() => { ${Q}.querySelector('.quiz-reiniciar').click(); return 1; })()`);
const conteo = c => c.evalua(`(() => { const r = ${Q}.querySelector('.quiz-resumen'); return ${Q}.querySelector('.quiz-conteo').textContent + ' || ' + (r && !r.hidden ? r.textContent.replace(/\\s+/g, ' ').trim() : '(sin resumen)'); })()`);

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const srv = spawn('python3', ['-m', 'http.server', String(PUERTO_HTTP), '--bind', '127.0.0.1', '--directory', path.join(RAIZ, 'Htmls_Series')], { stdio: 'ignore' });
  await espera(1200);
  const c = await Chrome.lanzar(PUERTO_CDP);
  let fallos = 0;
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable'); await c.enviar('Log.enable');
    for (const modo of [{ nombre: '1200', width: 1200, height: 1000, dsf: 1, mobile: false }, { nombre: '375', width: 375, height: 812, dsf: 2, mobile: true }]) {
      await c.enviar('Emulation.setDeviceMetricsOverride', { width: modo.width, height: modo.height, deviceScaleFactor: modo.dsf, mobile: modo.mobile });
      c.contexto = 'carga ' + modo.nombre;
      await c.enviar('Page.navigate', { url: BASE });
      await c.esperaHasta(`typeof loadModule === 'function' && typeof Chart !== 'undefined' && typeof DATOS_CAP4 !== 'undefined'`, 20000);
      await espera(1200);
      c.contexto = 'M8 @' + modo.nombre;
      await c.evalua(`loadModule(8), 'ok'`); await espera(1300);
      const m8 = await c.evalua(`(() => { const pres = [...document.querySelectorAll('#content-area pre')].filter(p => /log\\(lynx\\)/.test(p.textContent));
        return { bloquesLince: pres.length, coloreado: pres.map(p => p.querySelectorAll('span.token').length), ancho: document.documentElement.scrollWidth, ventana: innerWidth,
          desborda: pres.map(p => p.scrollWidth > p.clientWidth + 1 && getComputedStyle(p).overflowX === 'visible') }; })()`);
      console.log('M8, bloque del lince:', JSON.stringify(m8));
      const mm = await c.evalua(MEDIR('#content-area'));
      console.log('M8 completo:', JSON.stringify({ katex: mm.katex, katexError: mm.katexError, sueltos: mm.sueltos, seSalen: mm.seSalen, pagina: mm.pagina }));
      if (mm.katexError || mm.sueltos.length || mm.seSalen.length || mm.pagina > mm.ventana + 1) fallos++;
      await captura(c, '#content-area pre', await c.evalua(`[...document.querySelectorAll('#content-area pre')].findIndex(p => /log\\(lynx\\)/.test(p.textContent))`), `m8-bloque-lince-${modo.nombre}.png`);
      c.contexto = 'M10 @' + modo.nombre;
      await c.evalua(`loadModule(10), 'ok'`); await espera(1500);
      console.log(`\n===== ${modo.nombre} px =====`);
      // abrir pista y solución de E1-E3 con sus botones (no a mano), y comprobar aria-expanded
      const ab = await c.evalua(`(() => { const r = [];
        for (const id of ['c4e1', 'c4e2', 'c4e3']) for (const s of ['pista', 'sol']) {
          const b = document.querySelector('[aria-controls="' + id + '-' + s + '"]'); b.click();
          r.push(id + '-' + s + ':' + b.getAttribute('aria-expanded') + '/' + (!document.getElementById(id + '-' + s).hidden)); }
        return r.join(' '); })()`);
      console.log('botones de E1-E3 (aria-expanded/visible):', ab);
      await espera(800);
      const m = await c.evalua(MEDIR('#content-area .ejercicio-guiado'));
      const ejs = await c.evalua(`[...document.querySelectorAll('#content-area .ejercicio-guiado')].map(e => (e.querySelector('.ejercicio-numero')||{}).textContent || '?').join(' ')`);
      console.log('ejercicios guiados del M10:', ejs);
      console.log('E2, parrafo del lince:', await c.evalua(`[...document.querySelectorAll('#c4e2-sol p')].pop().textContent.replace(/\\s+/g, ' ').slice(0, 900)`));
      console.log('E3, apartados de la solucion:', await c.evalua(`[...document.querySelectorAll('#c4e3-sol p strong')].map(s => s.textContent).join(' | ')`));
      console.log('U+00 en la pagina:', await c.evalua(`document.body.innerText.includes('U+00')`));
      console.log('E1-E3 abiertos:', JSON.stringify(m));
      if (m.katexError || m.sueltos.length || m.seSalen.length || m.pagina > m.ventana + 1) fallos++;
      const idxE = await c.evalua(`[...document.querySelectorAll('#content-area .ejercicio-guiado')].findIndex(e => /BJsales/.test(e.textContent) && /1\\./.test((e.querySelector('.ejercicio-numero')||{}).textContent||''))`);
      for (let k = 0; k < 3; k++) await captura(c, '#content-area .ejercicio-guiado', idxE + k, `m10-e${k + 1}-${modo.nombre}.png`);

      // ---------------- quiz
      const n = await c.evalua(`${Q}.querySelectorAll('.quiz-pregunta').length`);
      console.log('preguntas del quiz:', n);
      // Pasada A: todo bien al primer intento
      c.contexto = 'quiz A @' + modo.nombre;
      for (let i = 0; i < n; i++) await responder(c, i, CLAVE[i]);
      await espera(400);
      console.log('A (todo bien):', await conteo(c));
      for (let i = 0; i < n; i++) { const e = await c.evalua(estadoQ(i)); if (e.katexError) { fallos++; console.log('  katex-error en P' + (i + 1)); }
        if (modo.nombre === '1200') console.log(`  P${i + 1} retro: ${(e.retro || '').slice(0, 160)}`); }
      const mq = await c.evalua(MEDIR('.quiz[data-quiz="cap4"]'));
      console.log('  quiz con retros abiertas:', JSON.stringify(mq));
      if (mq.katexError || mq.sueltos.length || mq.seSalen.length) fallos++;
      for (const k of [0, 1, 5]) await captura(c, '.quiz[data-quiz="cap4"] .quiz-pregunta', k, `m10-quiz-p${k + 1}-${modo.nombre}.png`);
      // Pasada B: un fallo y luego bien (la numérica, con coma)
      await reiniciar(c); await espera(500); c.contexto = 'quiz B @' + modo.nombre;
      for (let i = 0; i < n; i++) {
        await responder(c, i, MAL[i]); await espera(150);
        const e1 = await c.evalua(estadoQ(i));
        await responder(c, i, i === 1 ? '5,02' : CLAVE[i]); await espera(150);
        const e2 = await c.evalua(estadoQ(i));
        if (modo.nombre === '1200') console.log(`  B P${i + 1}: tras el fallo, pista=${e1.pista ? '«' + e1.pista.slice(0, 150) + '»' : 'NO'}; luego ${e2.clase}`);
        if (e1.katexError || e2.katexError) fallos++;
      }
      console.log('B (un fallo y bien):', await conteo(c));
      // Pasada C: dos fallos
      await reiniciar(c); await espera(500); c.contexto = 'quiz C @' + modo.nombre;
      for (let i = 0; i < n; i++) {
        await responder(c, i, MAL[i]); await espera(100); await responder(c, i, MAL2[i]); await espera(150);
        const e = await c.evalua(estadoQ(i));
        if (modo.nombre === '1200') console.log(`  C P${i + 1}: ${e.clase} · ${(e.retro || '').slice(0, 220)}`);
        if (e.katexError) fallos++;
      }
      console.log('C (dos fallos):', await conteo(c));
      if (modo.nombre === '1200') await captura(c, '.quiz[data-quiz="cap4"] .quiz-pregunta', 3, `m10-quiz-p4-desglose-${modo.nombre}.png`);
      // Pasada D: valores límite de la numérica (P2), cada uno en un quiz recién reiniciado, primer intento
      if (modo.nombre === '1200') {
        for (const v of ['5.02', '5,02', '5.01', '5.009', '5.0089', '5.026', '5.03', '5.031', '5.032', '5.04', '5.00', '4.99', '5']) {
          await reiniciar(c); await espera(250);
          await responder(c, 1, v); await espera(120);
          const e = await c.evalua(estadoQ(1));
          console.log(`  D P2 «${v}»: ${e.retro ? 'ACEPTADO' : (e.pista ? 'rechazado (pista)' : '?')}`);
        }
      }
    }
    console.log('\n===== consola =====');
    const ev = c.eventos.filter(e => !/favicon/.test(e.txt));
    console.log(ev.length ? ev.map(e => `[${e.cuando}] ${e.txt}`).join('\n') : 'sin errores ni avisos de consola (salvo el favicon)');
    if (ev.length) fallos++;
    console.log(`\n${fallos ? 'HAY ' + fallos + ' COSAS QUE REVISAR' : 'TODO EN ORDEN'}`);
  } finally {
    await c.cerrar(); srv.kill();
  }
  process.exit(fallos ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
