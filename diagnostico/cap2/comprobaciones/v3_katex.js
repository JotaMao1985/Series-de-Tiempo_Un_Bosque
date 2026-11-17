// Errores de KaTeX, excepciones y $ sin componer en los nueve módulos del cap. 2 (375 y 1200 px).
const { Chrome, espera } = require('../diag/chrome');
(async () => {
  const c = await Chrome.lanzar(9293);
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable'); await c.enviar('Log.enable');
    for (const w of [1200, 375]) {
      await c.enviar('Emulation.setDeviceMetricsOverride', { width: w, height: 900, deviceScaleFactor: 1, mobile: w < 768 });
      await c.enviar('Page.navigate', { url: 'http://localhost:8731/capitulo-2-estacionariedad-acf-pacf.html?k=' + Date.now() });
      await c.esperaHasta("typeof courseData !== 'undefined' && typeof renderMathInElement === 'function' && document.querySelector('#content-area > *')", 30000);
      for (let m = 1; m <= 9; m++) {
        c.contexto = `${w} M${m}`;
        await c.evalua(`loadModule(${m}), 1`); await espera(700);
        const r = await c.evalua(`(() => { const a = document.getElementById('content-area');
          const err = a.querySelectorAll('.katex-error').length;
          const txt = [...a.querySelectorAll('p, li, td, th')].filter(e => !e.closest('pre')).map(e => e.innerText).join(' ');
          const dolares = (txt.match(/\\$[^$]{1,40}\\$/g) || []).slice(0, 3);
          return { err, dolares, katex: a.querySelectorAll('.katex').length }; })()`);
        console.log(w, 'M' + m, JSON.stringify(r));
      }
    }
    const ev = c.eventos.filter(e => !/favicon/.test(e.txt));
    console.log('eventos:', ev.length); ev.forEach(e => console.log('  ', e.cuando, e.txt.slice(0, 200)));
  } finally { await c.cerrar(); }
})().catch(e => { console.error(e); process.exit(1); });
