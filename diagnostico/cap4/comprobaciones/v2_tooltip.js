#!/usr/bin/env node
// Tooltip de las cruces de AICc = ∞ del M7 (y de la serie evaluada), en el árbol (8766) y en HEAD (8767).
const { Chrome, espera } = require('../diag/chrome');
async function main() {
  const c = await Chrome.lanzar(9287);
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable');
    await c.enviar('Emulation.setDeviceMetricsOverride', { width: 1200, height: 1000, deviceScaleFactor: 1, mobile: false });
    for (const [ver, pto] of [['nuevo', 8766], ['viejo', 8767]]) {
      await c.enviar('Page.navigate', { url: `http://127.0.0.1:${pto}/capitulo-4-modelos-arima.html#modulo-7` });
      await espera(700);
      await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined' && typeof renderMathInElement === 'function'", 30000);
      await c.evalua('document.fonts.ready.then(() => 1)');
      await c.evalua(`Chart.defaults.animation = false; loadModule(7), 1`); await espera(900);
      await c.evalua(`(() => { const r = document.querySelector('[data-simulador="traza-auto-arima"]'); const k = r.querySelector('input[type=checkbox]'); k.checked = true; k.dispatchEvent(new Event('change', {bubbles:true})); const i = r.querySelector('input[type=range]'); i.value = 42; i.dispatchEvent(new Event('input', {bubbles:true})); r.scrollIntoView({block:'center'}); return 1; })()`);
      await espera(500);
      const pts = await c.evalua(`(() => { const cv = document.querySelector('[data-simulador="traza-auto-arima"] canvas'); const ch = Chart.getChart(cv); const r = cv.getBoundingClientRect();
        const out = []; ch.data.datasets.forEach((d, k) => { const meta = ch.getDatasetMeta(k); meta.data.forEach((p, j) => { if (d.data[j] !== null && d.data[j] !== undefined && d.showLine === false) out.push({ ds: k, label: d.label, j, v: d.data[j], x: r.left + p.x, y: r.top + p.y }); }); });
        return out; })()`);
      const objetivos = [pts.find(p => p.label && p.label.startsWith('AICc = ∞')), pts.find(p => p.label && p.label.startsWith('AICc del')) , pts.find(p => p.label && /Modelo evaluado/.test(p.label)), pts.find(p => p.label && /Mejora/.test(p.label))].filter(Boolean);
      for (const o of objetivos) {
        await c.enviar('Input.dispatchMouseEvent', { type: 'mouseMoved', x: o.x, y: o.y });
        await espera(300);
        const t = await c.evalua(`(() => { const ch = Chart.getChart(document.querySelector('[data-simulador="traza-auto-arima"] canvas')); const tt = ch.tooltip; return { op: tt.opacity, titulo: tt.title, cuerpo: tt.body && tt.body.map(b => b.lines) }; })()`);
        console.log(ver, o.label, 'j=' + o.j, 'valor', o.v, '->', JSON.stringify(t));
      }
    }
  } finally { await c.cerrar(); }
}
main().then(() => process.exit(0)).catch(e => { console.error(e.stack); process.exit(1); });
