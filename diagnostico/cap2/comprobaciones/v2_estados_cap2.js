#!/usr/bin/env node
// Verificador independiente de la R2: estados de los simuladores del cap. 2.
// Para cada estado, compara lo que dice el aria-label de cada lienzo con lo que el lienzo
// tiene de verdad (barras fuera de la banda, r1, r10, CV de Guerrero...), guarda la lectura,
// y recorre φ del simulador del M5 de 0 a 1.05 para contrastar su intro y su nota.
// Uso: node v2_estados_cap2.js [BASE] [ancho=1200]
const fs = require('fs');
const path = require('path');
const { Chrome, espera } = require('../diag/chrome');

const BASE = process.argv[2] || 'http://127.0.0.1:8731';
const ANCHO = Number(process.argv[3] || 1200);
const OUT = path.resolve(__dirname, '..', 'capturas', 'r2v', 'estados');
const URL = `${BASE}/capitulo-2-estacionariedad-acf-pacf.html#modulo-1`;

const VERDAD = sim => `(() => {
  const raiz = document.querySelector('[data-simulador="${sim}"]');
  const lect = raiz.querySelector('.simulador-lectura');
  return { lectura: lect ? lect.textContent.replace(/\\s+/g, ' ').trim() : null, live: lect ? lect.getAttribute('aria-live') : null,
    lienzos: [...raiz.querySelectorAll('canvas')].map(cv => {
      const ch = Chart.getChart(cv);
      const o = { aria: cv.getAttribute('aria-label') };
      if (!ch) return o;
      o.leyenda = (ch.legend && ch.legend.legendItems || []).map(x => x.text);
      const xs = ch.scales.x;
      o.rotulosX = xs.getLabelItems(ch.chartArea).map(it => String(it.label)).filter(Boolean);
      o.rotulosY = ch.scales.y.getLabelItems(ch.chartArea).map(it => String(it.label));
      if (ch.config.type === 'bar') {
        const v = ch.data.datasets[0].data;
        const lineas = ch.data.datasets.filter(d => d.type === 'line');
        const b = lineas.length ? Math.abs(lineas[0].data[0]) : null;
        o.verdad = { n: v.length, fuera: b === null ? null : v.filter(r => Math.abs(r) > b).length, banda: b, r1: v[0], r10: v[9],
          r12: v[11], r24: v[23] };
        o.acf = v.map(x => Math.round(x * 1000) / 1000);
      } else {
        o.verdad = { series: ch.data.datasets.map(d => ({ label: d.label, n: d.data.length,
          puntos: d.data.map((y, i) => y === null ? null : [ch.data.labels[i], y]).filter(Boolean).slice(0, 3) })) };
      }
      return o;
    }) };
})()`;

async function poner(c, sim, tipo, idx, val) {
  await c.evalua(`(() => {
    const raiz = document.querySelector('[data-simulador="${sim}"]');
    if ('${tipo}' === 'range') { const i = raiz.querySelectorAll('input[type=range]')[${idx}]; i.value = ${JSON.stringify(val)}; i.dispatchEvent(new Event('input', { bubbles: true })); }
    if ('${tipo}' === 'select') { const s = raiz.querySelectorAll('select')[${idx}]; s.value = ${JSON.stringify(val)}; s.dispatchEvent(new Event('change', { bubbles: true })); }
    if ('${tipo}' === 'check') { const k = raiz.querySelectorAll('input[type=checkbox]')[${idx}]; if (k.checked !== ${JSON.stringify(val)}) { k.checked = ${JSON.stringify(val)}; k.dispatchEvent(new Event('change', { bubbles: true })); } }
    return 1; })()`);
  await espera(80);
}

async function captura(c, sim, nombre) {
  const rect = await c.evalua(`(() => { const el = document.querySelector('[data-simulador="${sim}"]'); el.scrollIntoView({behavior:'instant', block:'start'});
    const r = el.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height }; })()`);
  await espera(120);
  const r = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
    clip: { x: rect.x - 4, y: rect.y - 4, width: rect.w + 8, height: rect.h + 8, scale: 1 } });
  fs.writeFileSync(path.join(OUT, `${nombre}-${ANCHO}.png`), Buffer.from(r.data, 'base64'));
}

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const c = await Chrome.lanzar(9291 + (ANCHO === 375 ? 1 : 0));
  const res = { base: BASE, ancho: ANCHO, estados: {}, phi: [], quiz: null };
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable');
    await c.enviar('Emulation.setDeviceMetricsOverride', ANCHO === 375
      ? { width: 375, height: 812, deviceScaleFactor: 2, mobile: true } : { width: ANCHO, height: 1000, deviceScaleFactor: 1, mobile: false });
    await c.enviar('Page.navigate', { url: URL });
    await espera(700);
    await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined'", 30000);
    await c.evalua('document.fonts.ready.then(() => 1)');
    await c.evalua(`(() => { Chart.defaults.animation = false; Chart.defaults.animations = {}; return 1; })()`);
    const st = `(() => { const s = document.createElement('style'); s.textContent = 'header.usta-header{position:static!important} #sidebarToggle,#scrollToTopBtn{visibility:hidden!important}'; document.head.appendChild(s); return 1; })()`;
    await c.evalua(st);
    const carga = async n => { await c.evalua(`loadModule(${n}), 1`); await espera(1200); };

    // M4 explorador
    await carga(4);
    for (const s of ['ruido_blanco', 'caminata', 'log_airpassengers', 'd_log_airpassengers', 'dd_log_airpassengers', 'trm', 'd_trm']) {
      await poner(c, 'explorador-acf-pacf', 'select', 0, s);
      res.estados[`explorador:${s}`] = await c.evalua(VERDAD('explorador-acf-pacf'));
      await captura(c, 'explorador-acf-pacf', `explorador-${s}`);
    }
    // M5 AR(1): rejilla de φ con y sin diferencia
    await carga(5);
    for (const dif of [false, true]) {
      await poner(c, 'ar1-phi', 'check', 0, dif);
      for (let k = 0; k <= 105; k += 5) {
        const phi = k / 100;
        await poner(c, 'ar1-phi', 'range', 0, phi);
        const v = await c.evalua(VERDAD('ar1-phi'));
        res.phi.push({ dif, phi, lectura: v.lectura, aria: v.lienzos.map(l => l.aria), acf: v.lienzos[1].acf, verdad: v.lienzos[1].verdad,
          leyenda: v.lienzos[0].leyenda, rotulosX: v.lienzos[1].rotulosX, rotulosYserie: v.lienzos[0].rotulosY });
        if ([0, 0.5, 0.95, 1, 1.05].includes(phi)) await captura(c, 'ar1-phi', `ar1-phi${k}${dif ? '-dif' : ''}`);
      }
    }
    for (const phi of [0.97, 0.98, 0.99]) {
      await poner(c, 'ar1-phi', 'check', 0, false);
      await poner(c, 'ar1-phi', 'range', 0, phi);
      const v = await c.evalua(VERDAD('ar1-phi'));
      res.phi.push({ dif: false, phi, lectura: v.lectura, acf: v.lienzos[1].acf, verdad: v.lienzos[1].verdad });
    }
    // M7 diferenciación
    await carga(7);
    for (const s of ['trm', 'log_airpassengers', 'caminata']) {
      await poner(c, 'diferenciacion', 'select', 0, s);
      for (const d of [0, 1, 2, 3]) {
        await poner(c, 'diferenciacion', 'range', 0, d);
        res.estados[`diferenciacion:${s}:d${d}`] = await c.evalua(VERDAD('diferenciacion'));
        await captura(c, 'diferenciacion', `dif-${s}-d${d}`);
      }
    }
    // M8 Box-Cox
    await carga(8);
    for (const L of [-1, -0.3, 0, 0.5, 1, 2]) {
      await poner(c, 'box-cox', 'range', 0, L);
      res.estados[`boxcox:${L}`] = await c.evalua(VERDAD('box-cox'));
      await captura(c, 'box-cox', `boxcox-${String(L).replace('.', '')}`);
    }
    // M6 Montecarlo y M2/M3 (estáticos)
    for (const [n, sim] of [[2, 'ruido-blanco'], [3, 'correlogramas-comparados'], [6, 'montecarlo-adf'], [1, 'panel-estacionariedad']]) {
      await carga(n);
      res.estados[`${sim}`] = await c.evalua(VERDAD(sim));
    }
    // M9: gráficos del quiz
    await carga(9);
    res.quiz = await c.evalua(`[...document.querySelectorAll('.quiz-grafico')].map(g => { const cv = g.querySelector('canvas'); const ch = Chart.getChart(cv);
      const pr = g.closest('.quiz-pregunta, .autoevaluacion-pregunta, li, div');
      return { aria: cv.getAttribute('aria-label'), role: cv.getAttribute('role'), acf: ch ? ch.data.datasets[0].data.map(x => Math.round(x*100)/100) : null,
        rotulosX: ch ? ch.scales.x.getLabelItems(ch.chartArea).map(it => String(it.label)) : null,
        rotulosY: ch ? ch.scales.y.getLabelItems(ch.chartArea).map(it => String(it.label)) : null,
        banda: ch ? ch.data.datasets.filter(d => d.type === 'line').map(d => d.data[0]) : null }; })`);
  } finally {
    await c.cerrar();
  }
  fs.writeFileSync(path.join(__dirname, `v2_estados_cap2_${ANCHO}.json`), JSON.stringify(res, null, 1));
  console.log('listo', Object.keys(res.estados).length, 'estados,', res.phi.length, 'valores de φ; eventos', c.eventos.length, c.eventos.slice(0, 5));
}
main().then(() => process.exit(0)).catch(e => { console.error('✗ ' + e.stack); process.exit(1); });
