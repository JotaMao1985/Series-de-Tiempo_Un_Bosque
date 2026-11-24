// Verificador B: escala (--k) y pie de las 84 diapositivas, deck de 7686d33 (puerto 8768, copia fuera del repo)
// frente al del árbol (8767), a 1280×720, por HTTP. Uso: node diagnostico/cap5/comprobaciones/v1b_escalas_deck.js
const fs = require('fs'); const path = require('path');
const { Chrome, espera } = require('../diag/chrome');
(async () => {
  const c = await Chrome.lanzar(9279);
  const out = {};
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable');
    await c.enviar('Emulation.setDeviceMetricsOverride', { width: 1280, height: 720, deviceScaleFactor: 1, mobile: false });
    for (const [nombre, base] of [['7686d33', 'http://127.0.0.1:8768'], ['arbol', 'http://127.0.0.1:8767']]) {
      await c.enviar('Page.navigate', { url: `${base}/diapositivas/capitulo-5-sarima.html?revisar=1` });
      await espera(6000);
      await c.esperaHasta("!!document.getElementById('informe-revision')", 30000).catch(() => {});
      out[nombre] = await c.evalua(`(() => [...document.querySelectorAll('.diapo')].map((d, i) => {
        const pie = d.querySelector('.pie'); const f = d.querySelector('.pie .fuente');
        const sm = d.querySelector('.cuerpo small');
        return { n: i + 1, k: d.dataset.escala || d.style.getPropertyValue('--k') || null, conFuente: !!f,
          piePx: f ? getComputedStyle(f).fontSize : null, smallPx: sm ? getComputedStyle(sm).fontSize : null,
          smallTxt: sm ? sm.textContent.slice(0, 40) : null }; }))()`);
      out[nombre + '_informe'] = await c.evalua(`(document.getElementById('informe-revision') || {}).textContent || null`);
    }
  } finally { fs.writeFileSync(path.join(__dirname, 'v1b_escalas_deck.json'), JSON.stringify(out, null, 1)); await c.cerrar(); }
})().catch(e => { console.error(e); process.exit(1); });
