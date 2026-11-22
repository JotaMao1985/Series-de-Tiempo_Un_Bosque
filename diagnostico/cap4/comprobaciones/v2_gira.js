#!/usr/bin/env node
// Girar / cambiar el ancho con el módulo abierto (no lo cubrió la revisión por cargas nuevas): ΔAICc del M6 y leyendas del M3 y el M7.
const { Chrome, espera } = require('../diag/chrome');
async function main() {
  const c = await Chrome.lanzar(9289);
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable'); await c.enviar('Log.enable');
    await c.enviar('Emulation.setDeviceMetricsOverride', { width: 1200, height: 1000, deviceScaleFactor: 1, mobile: false });
    await c.enviar('Page.navigate', { url: 'http://127.0.0.1:8766/capitulo-4-modelos-arima.html#modulo-6' });
    await espera(700);
    await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined' && typeof renderMathInElement === 'function'", 30000);
    await c.evalua('document.fonts.ready.then(() => 1)');
    const medir = mod => c.evalua(`(() => { const sim = [...mainContent.querySelectorAll('[data-simulador]')].find(s => s.querySelector('canvas'));
      return [...sim.querySelectorAll('canvas')].map(cv => { const ch = Chart.getChart(cv); if (!ch) return null;
        const items = ch.legend.legendItems.map(x => x.text);
        return { w: Math.round(cv.getBoundingClientRect().width), eje: ch.options.indexAxis || 'x', area: [Math.round(ch.chartArea.width), Math.round(ch.chartArea.height)], leyenda: ch.legend.lineWidths.length, items,
          ticks: Object.values(ch.scales).map(s => s.id + ':' + s.ticks.length), pointStyleWidth: ch.options.plugins.legend.labels.pointStyleWidth, boxWidth: ch.options.plugins.legend.labels.boxWidth }; }); })()`);
    await c.evalua(`loadModule(6), 1`); await espera(900);
    await c.evalua(`(() => { const r = document.querySelector('[data-simulador="explorador-modelos"]'); const i = r.querySelectorAll('input[type=range]')[1]; i.value = 2; i.dispatchEvent(new Event('input', {bubbles:true})); return 1; })()`);
    await espera(400);
    console.log('1200      ', JSON.stringify((await medir())[1]));
    for (const w of [375, 560, 800, 1200]) {
      await c.enviar('Emulation.setDeviceMetricsOverride', { width: w, height: 900, deviceScaleFactor: 1, mobile: w < 500 });
      await espera(900);
      console.log(String(w).padEnd(10), JSON.stringify((await medir())[1]));
    }
    // M3: los rótulos cortos del teléfono se fijan al crear: ¿qué pasa al ensanchar después?
    await c.enviar('Emulation.setDeviceMetricsOverride', { width: 375, height: 900, deviceScaleFactor: 1, mobile: true });
    await c.evalua(`loadModule(3), 1`); await espera(900);
    console.log('M3 a 375  ', JSON.stringify((await medir())[1]));
    await c.enviar('Emulation.setDeviceMetricsOverride', { width: 1200, height: 900, deviceScaleFactor: 1, mobile: false });
    await espera(900);
    console.log('M3 -> 1200', JSON.stringify((await medir())[1]));
    // M7: legend click
    await c.evalua(`loadModule(7), 1`); await espera(900);
    await c.evalua(`(() => { const ch = Chart.getChart(document.querySelector('[data-simulador="traza-auto-arima"] canvas')); const it = ch.legend.legendItems[1]; ch.legend.options.onClick.call(ch.legend, {}, it, ch.legend); return 1; })()`);
    await espera(300);
    console.log('M7 tras pulsar la 2ª entrada:', JSON.stringify(await c.evalua(`(() => { const ch = Chart.getChart(document.querySelector('[data-simulador="traza-auto-arima"] canvas')); return ch.legend.legendItems.map(x => x.text + (x.hidden ? ' [oculto]' : '')); })()`)));
    console.log('eventos', JSON.stringify(c.eventos.filter(e => !/favicon/.test(e.txt))));
  } finally { await c.cerrar(); }
}
main().then(() => process.exit(0)).catch(e => { console.error(e.stack); process.exit(1); });
