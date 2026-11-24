#!/usr/bin/env node
// Verificador independiente R2 cap. 5: regresiones en el navegador (CDP, puerto 9281).
//  1. Consola de los caps. 1–6 y de la guía del proyecto, módulo a módulo, a 1200 y 375 px; lienzos sin gráfico.
//  2. El icono del M11 (`fa-trophy`): su ::before y su ancho dibujado.
//  3. El quiz del cap. 5 en HEAD (8771) y en el árbol (8769): enunciados, opciones, clave, pistas y retros.
//  4. El mapa del M1 a 800 px: ¿se reajusta al cerrar la barra lateral y al cambiar el ancho de la ventana?
const fs = require('fs');
const path = require('path');
const { Chrome, espera } = require('../diag/chrome');
const ACTUAL = 'http://127.0.0.1:8769';
const ANTES = 'http://127.0.0.1:8771';
const PAGINAS = ['capitulo-1-componentes-descomposicion.html', 'capitulo-2-estacionariedad-acf-pacf.html',
  'capitulo-3-modelos-ar-ma-arma.html', 'capitulo-4-modelos-arima.html', 'capitulo-5-sarima.html',
  'capitulo-6-pronostico-evaluacion.html', 'proyecto-pronostico-corte-iii.html'];

async function abrir(c, url, w, h, dsf, mobile) {
  await c.enviar('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: dsf, mobile });
  await c.enviar('Page.navigate', { url });
  await espera(800);
  await c.esperaHasta("typeof loadModule === 'function'", 30000);
  await c.evalua('document.fonts.ready.then(() => 1)');
  await espera(300);
}

async function main() {
  const c = await Chrome.lanzar(9281);
  const out = { consola: [], lienzos: [], icono: null, quiz: null, resize: [] };
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable'); await c.enviar('Log.enable');
    for (const [w, h, dsf, mob] of [[1200, 1000, 1, false], [375, 812, 2, true]]) {
      for (const p of PAGINAS) {
        c.contexto = `${p} ${w}`;
        await abrir(c, `${ACTUAL}/${p}#modulo-1`, w, h, dsf, mob);
        const n = await c.evalua(`document.querySelectorAll('template[id^="module-"]').length`);
        for (let m = 1; m <= n; m++) {
          c.contexto = `${p} ${w} M${m}`;
          await c.evalua(`loadModule(${m}), 1`);
          await espera(900);
          const l = await c.evalua(`(() => [...mainContent.querySelectorAll('canvas')].map(cv => {
            const ch = typeof Chart !== 'undefined' ? Chart.getChart(cv) : null;
            const datos = ch ? ch.data.datasets.reduce((a, d) => a + (d.data || []).filter(v => v !== null && v !== undefined).length, 0) : 0;
            const r = cv.getBoundingClientRect();
            return { sim: cv.closest('[data-simulador]')?.dataset.simulador || (cv.closest('.quiz-pregunta, .quiz') ? 'quiz' : '?'),
              chart: !!ch, datos, w: Math.round(r.width), h: Math.round(r.height) };
          }))()`);
          const malos = l.filter(x => !x.chart || !x.datos || !x.w || !x.h);
          out.lienzos.push({ p, w, m, n: l.length, malos });
        }
        console.log(`  ${w} ${p}: ${n} módulos`);
      }
    }
    out.consola = c.eventos.filter(e => !/favicon\.ico/.test(e.txt));
    out.consolaTotal = c.eventos.length;

    // 2. Icono del M11
    await abrir(c, `${ACTUAL}/capitulo-5-sarima.html#modulo-11`, 1200, 1000, 1, false);
    await c.evalua('loadModule(11), 1'); await espera(1200);
    out.icono = await c.evalua(`(() => { const i = document.querySelector('[data-simulador="comparativa-particion"] h4 i');
      const cs = getComputedStyle(i, '::before'); const r = i.getBoundingClientRect();
      return { clase: i.className, content: cs.content, fuente: cs.fontFamily, ancho: Math.round(r.width * 10) / 10,
        fuenteCargada: document.fonts.check('900 16px "Font Awesome 6 Free"'),
        hojaFA: [...document.styleSheets].some(s => (s.href || '').includes('font-awesome/6.0.0')) }; })()`);
    // ¿Está fa-trophy en la hoja 6.0.0? (regla .fa-trophy:before)
    out.icono.reglaEnHoja = await c.evalua(`(() => { for (const s of document.styleSheets) { try { for (const r of s.cssRules) {
      if (r.selectorText && /\\.fa-trophy(:|::)before/.test(r.selectorText)) return r.cssText.slice(0, 80); } } catch (e) {} } return null; })()`);
    out.icono.reglaRankingStar = await c.evalua(`(() => { for (const s of document.styleSheets) { try { for (const r of s.cssRules) {
      if (r.selectorText && /\\.fa-ranking-star/.test(r.selectorText)) return r.cssText.slice(0, 80); } } catch (e) {} } return null; })()`);

    // 3. Quiz cap5: HEAD frente al árbol
    const VOLCAR = `JSON.stringify(AUTOEVALUACIONES['cap5'].map(q => { const o = {}; for (const k of Object.keys(q).sort()) {
      if (typeof q[k] === 'function') continue; o[k] = q[k]; } return o; }))`;
    await abrir(c, `${ANTES}/capitulo-5-sarima.html#modulo-1`, 1200, 1000, 1, false);
    const qa = JSON.parse(await c.evalua(VOLCAR));
    await abrir(c, `${ACTUAL}/capitulo-5-sarima.html#modulo-1`, 1200, 1000, 1, false);
    const qb = JSON.parse(await c.evalua(VOLCAR));
    const dif = [];
    qb.forEach((q, i) => { const a = qa[i] || {};
      for (const k of new Set([...Object.keys(a), ...Object.keys(q)])) {
        if (JSON.stringify(a[k]) !== JSON.stringify(q[k])) dif.push({ i, k, antes: a[k] === undefined ? '(no había)' : String(JSON.stringify(a[k])).slice(0, 80), ahora: String(JSON.stringify(q[k])).slice(0, 300) });
      } });
    out.quiz = { nAntes: qa.length, nAhora: qb.length, diferencias: dif };
    // El lienzo del quiz y su aria-label, ya dibujado
    await c.evalua('loadModule(11), 1'); await espera(1500);
    out.quiz.lienzo = await c.evalua(`[...document.querySelectorAll('.quiz canvas, [data-quiz] canvas')].map(cv => ({ aria: cv.getAttribute('aria-label'), h: Math.round(cv.getBoundingClientRect().height) }))`);

    // 4. Mapa del M1 y cambio de ancho
    await abrir(c, `${ACTUAL}/capitulo-5-sarima.html#modulo-1`, 800, 1000, 1, false);
    await c.evalua('loadModule(1), 1'); await espera(1200);
    const estado = async etiqueta => out.resize.push({ etiqueta, ...(await c.evalua(`(() => { const r = document.querySelector('[data-simulador="mapa-firma"] .mapa-estacional');
      return { clases: r.className, ancho: Math.round(r.getBoundingClientRect().width), celda: Math.round(r.querySelector('.mapa-estacional-celda').getBoundingClientRect().width * 10) / 10,
        valor: getComputedStyle(r.querySelector('.mapa-estacional-valor')).display, sidebar: document.body.className.slice(0, 60) }; })()`)) });
    await estado('800, al abrir');
    const hayBoton = await c.evalua(`!!document.getElementById('sidebarToggle')`);
    if (hayBoton) { await c.evalua(`document.getElementById('sidebarToggle').click(), 1`); await espera(900); await estado('800, tras pulsar el botón de la barra lateral'); }
    await c.enviar('Emulation.setDeviceMetricsOverride', { width: 1200, height: 1000, deviceScaleFactor: 1, mobile: false });
    await espera(900); await estado('ventana a 1200 sin recargar');
    await c.enviar('Emulation.setDeviceMetricsOverride', { width: 375, height: 812, deviceScaleFactor: 2, mobile: true });
    await espera(900); await estado('ventana a 375 sin recargar');
  } finally { await c.cerrar(); }
  fs.writeFileSync(path.join(__dirname, 'v2_consola.json'), JSON.stringify(out, null, 1));
  console.log(JSON.stringify({ consola: out.consola, consolaTotal: out.consolaTotal,
    lienzosMalos: out.lienzos.filter(x => x.malos.length), totalLienzos: out.lienzos.reduce((a, x) => a + x.n, 0),
    icono: out.icono, quiz: out.quiz, resize: out.resize }, null, 1));
}
main().then(() => process.exit(0)).catch(e => { console.error('✗ ' + e.stack); process.exit(1); });
