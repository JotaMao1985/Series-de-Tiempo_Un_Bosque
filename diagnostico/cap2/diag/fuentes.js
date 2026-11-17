#!/usr/bin/env node
// ¿El módulo de arranque pinta los ejes con Montserrat/Fira Code o con la letra de respaldo?
// Compara el lienzo tal como quedó al cargar con el mismo lienzo repintado cuando ya están las
// fuentes (toDataURL, sin depender del desplazamiento). Dos escenarios: red normal y fuentes de
// Google retrasadas 8 s (más que el tope de 3 s de fuentesDeLosLienzos()).
const fs = require('fs');
const path = require('path');
const { Chrome, espera } = require('./chrome');

const DIAG = __dirname;
const OUT = path.resolve(DIAG, '..', 'capturas');
const BASE = process.env.BASE || 'http://localhost:8731/capitulo-2-estacionariedad-acf-pacf.html';
const PUERTO = 9265;

async function capturaLienzo(c, idx, archivo) {
  await c.evalua(`(() => { if (!document.getElementById('quitar-fijos')) { const st = document.createElement('style'); st.id = 'quitar-fijos';
    st.textContent = 'header.usta-header{position:static!important} #sidebarToggle,#scrollToTopBtn{visibility:hidden!important}'; document.head.appendChild(st); } return 1; })()`);
  const rect = await c.evalua(`(() => { const el = document.querySelectorAll('[data-simulador] .grafico-wrapper')[${idx}];
    el.scrollIntoView({ behavior: 'instant', block: 'center' }); const r = el.getBoundingClientRect();
    return { x: r.left + window.scrollX, y: r.top + window.scrollY, w: r.width, h: r.height }; })()`);
  await espera(300);
  const r = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
    clip: { x: rect.x - 4, y: rect.y - 4, width: rect.w + 8, height: rect.h + 8, scale: 1 } });
  fs.writeFileSync(path.join(OUT, archivo), Buffer.from(r.data, 'base64'));
}

async function escenario(c, ancho, lentas) {
  const et = lentas ? 'fuentes-lentas' : 'fuentes-normales';
  c.contexto = `${et} ${ancho}`;
  await c.enviar('Emulation.setDeviceMetricsOverride', { width: ancho, height: 900, deviceScaleFactor: 1, mobile: ancho < 768 });
  await c.enviar('Network.setCacheDisabled', { cacheDisabled: true });
  let oyente = null;
  if (lentas) {
    await c.enviar('Fetch.enable', { patterns: [{ urlPattern: '*fonts.gstatic.com*' }] });
    oyente = m => { if (m.method === 'Fetch.requestPaused') setTimeout(() => c.enviar('Fetch.continueRequest', { requestId: m.params.requestId }).catch(() => {}), 4500); };
    c.oyentes.push(oyente);
  }
  await c.enviar('Page.navigate', { url: 'about:blank' });
  await c.esperaHasta(`location.href === 'about:blank'`, 10000, 30);
  await c.enviar('Page.navigate', { url: BASE + '#modulo-1' });
  const t0 = Date.now();
  await c.esperaHasta(`typeof Chart !== 'undefined' && !!Chart.getChart(document.querySelector('[data-simulador] canvas'))`, 20000, 30);
  const ms = Date.now() - t0;
  const alCrear = await c.evalua(`({ estado: document.fonts.status, montserrat: document.fonts.check('400 11px Montserrat'),
    fira: document.fonts.check("400 11px 'Fira Code'"),
    urls: [...document.querySelectorAll('[data-simulador] canvas')].map(cv => cv.toDataURL().length) })`);
  await espera(1200);
  const estable = await c.evalua(`({ estado: document.fonts.status, montserrat: document.fonts.check('400 11px Montserrat') })`);
  await c.evalua(`(window.__antes = [...document.querySelectorAll('[data-simulador] canvas')].map(cv => cv.toDataURL()), 1)`);
  await capturaLienzo(c, 0, `m1-fuente-${et}-inicial-${ancho}.png`);
  await c.evalua('document.fonts.ready.then(() => 1)');
  await espera(lentas ? 8000 : 1000);
  const despues = await c.evalua(`({ estado: document.fonts.status, montserrat: document.fonts.check('400 11px Montserrat'), fira: document.fonts.check("400 11px 'Fira Code'") })`);
  const sinRepintar = await c.evalua(`[...document.querySelectorAll('[data-simulador] canvas')].map((cv, i) => cv.toDataURL() !== window.__antes[i])`);
  const cambia = await c.evalua(`(() => { const cvs = [...document.querySelectorAll('[data-simulador] canvas')];
    cvs.forEach(cv => Chart.getChart(cv).update('none'));
    return cvs.map((cv, i) => cv.toDataURL() !== window.__antes[i]); })()`);
  await capturaLienzo(c, 0, `m1-fuente-${et}-repintado-${ancho}.png`);
  if (lentas) { c.oyentes = c.oyentes.filter(f => f !== oyente); await c.enviar('Fetch.disable'); }
  await c.enviar('Network.setCacheDisabled', { cacheDisabled: false });
  return { escenario: et, ancho, msHastaPrimerGrafico: ms, alCrear, a1200ms: estable, despues, cambiaSinRepintar: sinRepintar, lienzoCambiaAlRepintar: cambia };
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const c = await Chrome.lanzar(PUERTO);
  const res = [];
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable'); await c.enviar('Network.enable');
    for (const [ancho, lentas] of [[1200, false], [375, false], [1200, true], [375, true]]) res.push(await escenario(c, ancho, lentas));
    res.push({ eventos: c.eventos });
  } finally { await c.cerrar(); }
  fs.writeFileSync(path.join(DIAG, 'fuentes.json'), JSON.stringify(res, null, 1));
  console.log(JSON.stringify(res, null, 1));
  process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
