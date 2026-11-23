#!/usr/bin/env node
// Verificador A, R5 cap. 4: los «Para practicar» c4m1..c4m9 por HTTP (servidor 8771, CDP 9281), a 1200 y 375 px.
// Mide en cada ejercicio: KaTeX con error, «$» sin renderizar, KaTeX dentro de <pre>, desbordamiento, que los
// botones Pista/Solución abran su panel al pulsarlos, y captura el ejercicio con los paneles abiertos
// en diagnostico/cap4/capturas/r5/v5A/. Uso: node v5A_revisa.js > v5A_revisa.out
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const { Chrome, espera } = require('../diag/chrome');
const RAIZ = path.resolve(__dirname, '..', '..', '..');
const OUT = path.resolve(__dirname, '..', 'capturas', 'r5', 'v5A2');
const BASE = 'http://127.0.0.1:8773/capitulo-4-modelos-arima.html';
const MIDE = (id) => `(() => {
  const sol = document.getElementById('${id}-sol'); if (!sol) return null;
  const ej = sol.closest('.exercise');
  const bP = ej.querySelector('[aria-controls="${id}-pista"]'), bS = ej.querySelector('[aria-controls="${id}-sol"]');
  bP.click(); bS.click();
  const abiertos = !document.getElementById('${id}-pista').hidden && !sol.hidden;
  const sueltos = []; const w = document.createTreeWalker(ej, NodeFilter.SHOW_TEXT);
  for (let n = w.nextNode(); n; n = w.nextNode()) { const p = n.parentElement;
    if (!p || p.closest('pre, code, .katex')) continue;
    if (/\\$[^$]|\\\\(frac|phi|theta|hat|nabla|sigma|psi)/.test(n.textContent)) sueltos.push(n.textContent.trim().slice(0, 60)); }
  const r = ej.getBoundingClientRect();
  const desborda = [...ej.querySelectorAll('*')].filter(e => { const q = e.getBoundingClientRect();
    return q.right > innerWidth + 1 && !e.closest('pre') && !e.closest('.katex-display') ; }).map(e => e.tagName + '.' + String(e.className).slice(0, 20)).slice(0, 5);
  const pres = [...ej.querySelectorAll('pre')].map(p => [p.scrollWidth > p.clientWidth, getComputedStyle(p).overflowX]);
  return { abiertos, katex: ej.querySelectorAll('.katex').length, katexError: ej.querySelectorAll('.katex-error').length,
    katexEnPre: ej.querySelectorAll('pre .katex').length, sueltos, desborda, pagina: document.documentElement.scrollWidth,
    ventana: innerWidth, preConScroll: pres, prism: ej.querySelectorAll('pre code .token').length > 0,
    ancho: Math.round(r.width) };
})()`;
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const srv = spawn('python3', ['-m', 'http.server', '8773', '--bind', '127.0.0.1', '--directory', path.join(RAIZ, 'Htmls_Series')], { stdio: 'ignore' });
  await espera(1200);
  const c = await Chrome.lanzar(9283); let fallos = 0;
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable'); await c.enviar('Log.enable');
    for (const modo of [{ n: '1200', width: 1200, height: 1000, dsf: 1, mobile: false }, { n: '375', width: 375, height: 812, dsf: 2, mobile: true }]) {
      await c.enviar('Emulation.setDeviceMetricsOverride', { width: modo.width, height: modo.height, deviceScaleFactor: modo.dsf, mobile: modo.mobile });
      c.contexto = 'carga ' + modo.n;
      await c.enviar('Page.navigate', { url: BASE });
      await c.esperaHasta(`typeof loadModule === 'function' && typeof Chart !== 'undefined'`, 20000);
      await espera(1500);
      console.log(`\n===== ${modo.n} px =====`);
      for (const k of [1, 2, 3, 4, 6, 7, 8, 9]) {
        c.contexto = `M${k} @${modo.n}`;
        await c.evalua(`loadModule(${k}), 'ok'`); await espera(1300);
        const m = await c.evalua(MIDE('c4m' + k)); await espera(500);
        if (!m) { console.log(`M${k}: SIN EJERCICIO c4m${k}`); fallos++; continue; }
        const mal = !m.abiertos || m.katexError || m.katexEnPre || m.sueltos.length || m.desborda.length || m.pagina > m.ventana + 1 || !m.prism;
        if (mal) fallos++;
        console.log(`M${k} c4m${k}: paneles abren ${m.abiertos} · katex ${m.katex} · error ${m.katexError} · en <pre> ${m.katexEnPre} · «$» sueltos ${m.sueltos.length}` +
          ` · página ${m.pagina}/${m.ventana} · se salen ${m.desborda.length} · <pre> con scroll ${JSON.stringify(m.preConScroll)} · prism ${m.prism}${mal ? '  <-- REVISAR ' + JSON.stringify(m) : ''}`);
        const rect = await c.evalua(`(() => { const e = document.getElementById('c4m${k}-sol').closest('.exercise'); e.scrollIntoView({block:'start'});
          const r = e.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height }; })()`);
        await espera(700);
        const r = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
          clip: { x: Math.max(0, rect.x - 6), y: Math.max(0, rect.y - 6), width: rect.w + 12, height: Math.min(rect.h + 12, 9000), scale: 1 } });
        fs.writeFileSync(path.join(OUT, `c4m${k}-${modo.n}.png`), Buffer.from(r.data, 'base64'));
        if (k === 8) {
          const info = await c.evalua(`(() => { const p = [...document.querySelectorAll('#content-area pre')].find(e => e.textContent.includes('ly <- log(lynx)') && !e.closest('.exercise'));
            if (!p) return null; p.scrollIntoView({block:'start'}); const r = p.getBoundingClientRect(); const cont = p.parentElement;
            return { padre: cont.className, barra: cont.querySelectorAll('button').length, scroll: p.scrollWidth > p.clientWidth, overflow: getComputedStyle(p).overflowX,
              prism: p.querySelectorAll('.token').length > 0, derecha: Math.round(r.right), x: r.left + scrollX, y: r.top + scrollY - 60, w: r.width, h: r.height + 70,
              hermanos: [...cont.children].indexOf(p) }; })()`);
          console.log('   <pre> suelto del lince en el M8: ' + JSON.stringify(info));
          if (info) { await espera(600); const q = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
            clip: { x: Math.max(0, info.x - 6), y: Math.max(0, info.y), width: info.w + 12, height: info.h, scale: 1 } });
            fs.writeFileSync(path.join(OUT, `m8-pre-lince-${modo.n}.png`), Buffer.from(q.data, 'base64')); }
        }
      }
    }
    console.log('\n===== consola =====');
    const ev = c.eventos.filter(e => !/favicon/.test(e.txt));
    console.log(ev.length ? ev.map(e => `[${e.cuando}] ${e.txt}`).join('\n') : 'sin errores ni avisos de consola');
    if (ev.length) fallos++;
    console.log(`\n${fallos ? 'HAY ' + fallos + ' COSAS QUE REVISAR' : 'TODO EN ORDEN'}`);
  } finally { await c.cerrar(); srv.kill(); }
  process.exit(fallos ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
