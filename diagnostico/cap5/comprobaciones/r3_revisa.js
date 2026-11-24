#!/usr/bin/env node
// R3 del capítulo 5 · revisión por HTTP, a 1200 y 375 px (adaptado de r1_revisa.js).
// Levanta su propio servidor (8765) y su Chrome sin ventana (CDP 9278), recorre los doce módulos con los
// paneles plegados abiertos y mide: errores de consola, .katex-error, «$» sin renderizar, KaTeX dentro de
// <pre>, desbordamiento horizontal y lienzos sin gráfico. Comprueba además lo que la ronda tocó: el orden
// de los h3 del M2 y del M11, los cierres de M2 a M10, las intros nuevas frente al estado inicial, la tabla
// ordenable del M11 (columnas, filas, descripción y pie), la lectura nueva de su simulador (sin selector de
// métrica) y las pestañas R/Python del bloque nuevo. Capturas en diagnostico/cap5/capturas/r3/.
// Uso: node diagnostico/cap5/comprobaciones/r3_revisa.js > diagnostico/cap5/comprobaciones/r3_revisa.out
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const { Chrome, espera } = require('../diag/chrome');

const RAIZ = path.resolve(__dirname, '..', '..', '..');
const OUT = path.resolve(__dirname, '..', 'capturas', 'r3');
const PUERTO_HTTP = 8765, PUERTO_CDP = 9278;
const BASE = `http://127.0.0.1:${PUERTO_HTTP}/capitulo-5-sarima.html`;

async function capturar(c, sel, archivo, indice = 0) {
  const rect = await c.evalua(`(() => { const el = document.querySelectorAll(${JSON.stringify(sel)})[${indice}];
    if (!el) return null; el.scrollIntoView({ behavior: 'instant', block: 'start' });
    const r = el.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height }; })()`);
  if (!rect) { console.log('   (sin elemento para ' + archivo + ')'); return; }
  await espera(900);
  const r = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
    clip: { x: Math.max(0, rect.x - 6), y: Math.max(0, rect.y - 6), width: rect.w + 12, height: Math.min(rect.h + 12, 4000), scale: 1 } });
  fs.writeFileSync(path.join(OUT, archivo), Buffer.from(r.data, 'base64'));
}
const indice = (c, sel, aguja) => c.evalua(`[...document.querySelectorAll(${JSON.stringify(sel)})].findIndex(e => e.textContent.includes(${JSON.stringify(aguja)}))`);

const MEDIR = `(() => {
  const m = document.getElementById('content-area') || document.querySelector('main');
  const sueltos = [];
  const w = document.createTreeWalker(m, NodeFilter.SHOW_TEXT);
  for (let n = w.nextNode(); n; n = w.nextNode()) {
    const p = n.parentElement; if (!p || p.closest('pre, code, script, style, .katex, textarea')) continue;
    if (/\\$[^$]/.test(n.textContent) || /\\\\(frac|phi|theta|rho|sqrt|sum|hat|nabla|eta)/.test(n.textContent)) sueltos.push(n.textContent.trim().slice(0, 80));
  }
  const anchos = [...m.querySelectorAll('table, pre, .katex-display, .formula, canvas, .note, .warning, .definition, .diagram, .tabla-ranking')]
    .filter(e => e.offsetParent !== null)
    .filter(e => { const r = e.getBoundingClientRect(); return r.right > innerWidth + 1 && !e.closest('pre') && getComputedStyle(e).overflowX === 'visible'
      && ![...(function*(){ let a = e.parentElement; while (a && a !== m) { yield a; a = a.parentElement; } })()].some(a => /auto|scroll|hidden/.test(getComputedStyle(a).overflowX)); })
    .map(e => e.tagName + '.' + e.className.toString().slice(0, 30));
  const h3 = [...m.querySelectorAll('h3')].map(h => h.textContent.trim()).filter(t => t !== 'Objetivo');
  const ultimo = [...m.querySelector('.animate-fade-in').children].pop();
  return { katexError: m.querySelectorAll('.katex-error').length, katex: m.querySelectorAll('.katex').length,
    katexEnPre: m.querySelectorAll('pre .katex').length, sueltos, pagina: document.documentElement.scrollWidth, ventana: innerWidth,
    seSalen: anchos, bloques: m.querySelectorAll('pre code').length, simuladores: m.querySelectorAll('[data-simulador]').length,
    graficos: [...m.querySelectorAll('canvas')].filter(cv => Chart.getChart(cv)).length, lienzos: m.querySelectorAll('canvas').length,
    h3, cierre: ultimo ? ultimo.tagName + ': ' + ultimo.textContent.replace(/\\s+/g, ' ').trim().slice(0, 140) : '' };
})()`;

const LECTURA = sim => `(() => { const r = document.querySelector('[data-simulador="${sim}"]');
  return r ? r.querySelector('.simulador-lectura').textContent.replace(/\\s+/g, ' ').trim() : null; })()`;
const INTRO = sim => `(() => { const r = document.querySelector('[data-simulador="${sim}"]');
  return r ? r.querySelector('.simulador-intro').textContent.replace(/\\s+/g, ' ').trim() : null; })()`;

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
      await c.esperaHasta(`typeof loadModule === 'function' && typeof Chart !== 'undefined' && typeof DATOS_CAP5 !== 'undefined'`, 20000);
      await espera(1500);
      console.log(`\n===== ${modo.nombre} px · typeof tailwind = ${await c.evalua('typeof tailwind')} =====`);
      const v = modo.nombre;
      for (let n = 1; n <= 12; n++) {
        c.contexto = `M${n} @${v}`;
        await c.evalua(`loadModule(${n}), 'ok'`);
        await espera(1300);
        const intros = {};
        for (const sim of await c.evalua(`[...document.querySelectorAll('#content-area [data-simulador]')].map(e => e.dataset.simulador).filter(s => !/simulacro/.test(s))`)) {
          intros[sim] = { intro: await c.evalua(INTRO(sim)), lectura: await c.evalua(LECTURA(sim)) };
        }
        await c.evalua(`(() => { document.querySelectorAll('#content-area .ejercicio-panel[hidden], #content-area .derivacion-panel[hidden]').forEach(e => e.hidden = false);
          document.querySelectorAll('#content-area details').forEach(d => d.open = true); return 1; })()`);
        await espera(400);
        const m = await c.evalua(MEDIR);
        const mal = m.katexError || m.katexEnPre || m.sueltos.length || m.pagina > m.ventana + 1 || m.seSalen.length || m.graficos !== m.lienzos;
        if (mal) fallos++;
        console.log(`M${String(n).padStart(2)}: katex ${m.katex} · katex-error ${m.katexError} · katex en <pre> ${m.katexEnPre} · «$» sueltos ${m.sueltos.length}` +
          ` · ancho de página ${m.pagina}/${m.ventana} · elementos que se salen ${m.seSalen.length} · bloques ${m.bloques} · simuladores ${m.simuladores}` +
          ` · gráficos ${m.graficos}/${m.lienzos}${mal ? '   <-- REVISAR ' + JSON.stringify({ s: m.sueltos, a: m.seSalen }) : ''}`);
        if (v === '1200') {
          console.log(`   h3: ${m.h3.join(' | ')}`);
          console.log(`   último elemento: ${m.cierre}`);
          for (const [sim, t] of Object.entries(intros)) console.log(`   [${sim}] intro: ${t.intro}\n   [${sim}] lectura inicial: ${t.lectura}`);
        }
        if (n === 1) await capturar(c, '#content-area p', `m1-apertura-${v}.png`, await indice(c, '#content-area p', 'fracaso deliberado'));
        if (n === 2) {
          await capturar(c, '#content-area p', `m2-como-se-escribe-${v}.png`, await indice(c, '#content-area p', 'Antes de los ejemplos'));
          await capturar(c, '#content-area p', `m2-satelite-${v}.png`, await indice(c, '#content-area p', 'lo único genuinamente nuevo'));
        }
        if (n === 3) await capturar(c, '[data-simulador="cuatro-combinaciones"] .simulador-intro', `m3-intro-cuatro-${v}.png`);
        if (n === 4) await capturar(c, '#content-area p', `m4-ciclo-${v}.png`, await indice(c, '#content-area p', 'que tenía cuatro etapas'));
        if (n === 7) await capturar(c, '#content-area .warning', `m7-biasadj-${v}.png`, await indice(c, '#content-area .warning', 'biasadj'));
        if (n === 8) await capturar(c, '#content-area p', `m8-evidencias-${v}.png`, await indice(c, '#content-area p', 'Cuatro comprobaciones'));
        if (n === 9) await capturar(c, '#content-area .warning', `m9-rmse-${v}.png`, await indice(c, '#content-area .warning', 'fuera de muestra'));
        if (n === 11) {
          const t = await c.evalua(`(() => { const r = document.querySelector('.tabla-ranking[data-ranking="comparativa"]');
            if (!r) return null; const tb = r.querySelector('table');
            return { titulo: r.querySelector('.tabla-ranking-titulo').textContent.trim(),
              caption: tb && tb.caption ? tb.caption.textContent.trim() : null,
              cabeceras: tb ? [...tb.tHead.rows[0].cells].map(x => x.textContent.trim()) : null,
              filas: tb ? [...tb.tBodies[0].rows].map(f => [...f.cells].map(x => x.textContent.trim()).join(' | ')) : null,
              pie: r.querySelector('.tabla-ranking-pie').textContent.trim(),
              marcoDesborda: r.querySelector('.tabla-ranking-marco').scrollWidth > r.querySelector('.tabla-ranking-marco').clientWidth,
              overflowMarco: getComputedStyle(r.querySelector('.tabla-ranking-marco')).overflowX }; })()`);
          console.log('   tabla ordenable:', JSON.stringify(t, null, 1).replace(/\n\s*/g, ' '));
          if (!t || t.filas.length !== 8 || t.cabeceras.length !== 7) { fallos++; console.log('   <-- REVISAR la tabla ordenable'); }
          // ordenar por MAE con el botón
          await c.evalua(`(() => { const b = [...document.querySelectorAll('.tabla-ranking[data-ranking="comparativa"] th button')].find(x => x.textContent.startsWith('MAE')); b.click(); return 1; })()`);
          await espera(300);
          console.log('   ordenada por MAE, primera fila:', await c.evalua(`document.querySelector('.tabla-ranking[data-ranking="comparativa"] tbody tr').textContent.replace(/\\s+/g, ' ').trim()`));
          console.log('   selectores en el simulador:', await c.evalua(`document.querySelectorAll('[data-simulador="comparativa-particion"] select').length`));
          await c.evalua(`(() => { document.querySelectorAll('[data-simulador="comparativa-particion"] input[type=checkbox]').forEach(i => { if (!i.checked) i.click(); }); return 1; })()`);
          await espera(500);
          console.log('   lectura con los ocho:', await c.evalua(LECTURA('comparativa-particion')));
          await capturar(c, '[data-simulador="comparativa-particion"]', `m11-simulador-ocho-${v}.png`);
          await c.evalua(`(() => { document.querySelectorAll('[data-simulador="comparativa-particion"] input[type=checkbox]').forEach(i => { if (i.checked) i.click(); }); return 1; })()`);
          await espera(500);
          console.log('   lectura sin ninguno:', await c.evalua(LECTURA('comparativa-particion')));
          await capturar(c, '.tabla-ranking[data-ranking="comparativa"]', `m11-tabla-${v}.png`);
          // las pestañas del bloque nuevo
          const tab = await c.evalua(`(() => { const ct = [...document.querySelectorAll('#content-area .code-tabs')].find(x => x.querySelector('[aria-label="La comparación desde muchos orígenes"]'));
            if (!ct) return null; const vis = () => [...ct.querySelectorAll('.code-tab-panel')].map(p => p.dataset.lang + ':' + (!p.hidden && p.offsetParent !== null));
            const antes = vis(); ct.querySelector('button[data-lang="python"]').click(); const py = vis();
            const lineasPy = ct.querySelector('.code-tab-panel[data-lang="python"] pre').textContent.split('\\n').length;
            ct.querySelector('button[data-lang="r"]').click(); const r = vis();
            const lineasR = ct.querySelector('.code-tab-panel[data-lang="r"] pre').textContent.split('\\n').length;
            return { antes, trasPython: py, trasR: r, lineasR, lineasPy, prism: !!ct.querySelector('pre code .token') }; })()`);
          console.log('   pestañas del bloque nuevo:', JSON.stringify(tab));
          if (!tab || tab.trasPython.join() !== 'r:false,python:true' || tab.trasR.join() !== 'r:true,python:false') { fallos++; console.log('   <-- REVISAR las pestañas'); }
          await capturar(c, '#content-area .code-tabs', `m11-bloque-nuevo-${v}.png`, await indice(c, '#content-area .code-tabs', 'mediana <- function'));
          await capturar(c, '#content-area .warning', `m11-aviso-61-${v}.png`, await indice(c, '#content-area .warning', 'Esa conclusión es falsa'));
        }
      }
    }
    console.log('\n===== consola =====');
    const ev = c.eventos.filter(e => !/favicon/.test(e.txt));
    console.log(ev.length ? ev.map(e => `[${e.cuando}] ${e.txt}`).join('\n') : 'sin errores ni avisos de consola');
    if (ev.length) fallos++;
    console.log(`\n${fallos ? 'HAY ' + fallos + ' COSAS QUE REVISAR' : 'TODO EN ORDEN'}`);
  } finally {
    await c.cerrar(); srv.kill();
  }
  process.exit(fallos ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
