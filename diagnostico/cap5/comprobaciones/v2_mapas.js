#!/usr/bin/env node
// Verificador independiente de la R2 del cap. 5 · componente .mapa-estacional.
// Mide por HTTP, con Chrome sin ventana (CDP, puerto 9281), el mapa del cap. 1 (M3), los del cap. 5 (M1
// `mapa-firma`, las 32 combinaciones; M3 `tienda-cuadricula`, los 8 casos) y el de la plantilla (M3), a 1200,
// 800 y 375 px (375 con mobile:true y dsf 2), en el árbol (ACTUAL) y en HEAD (ANTES, copia servida aparte).
// Por estado: contraste WCAG de cada cifra visible, si caben los doce meses sin desplazar, qué clase de ajuste
// tomó (cifras chicas / sin cifras), cuerpo de la cifra, guiones, filas ARIA y nombre accesible. Además, en
// los mapas sin cifra: ratón, toque y teclado sobre la línea del valor, y el árbol de accesibilidad de Chrome.
// Uso: ACTUAL=http://127.0.0.1:8769 PLANTILLA=http://127.0.0.1:8770 ANTES=http://127.0.0.1:8771 node v2_mapas.js
const fs = require('fs');
const path = require('path');
const { Chrome, espera } = require('../diag/chrome');

const ACTUAL = process.env.ACTUAL || 'http://127.0.0.1:8769';
const PLANTILLA = process.env.PLANTILLA || 'http://127.0.0.1:8770';
const ANTES = process.env.ANTES || 'http://127.0.0.1:8771';
const OUT = path.resolve(__dirname, '..', 'capturas', 'v2');
const PUERTO = 9281;

const AYUDA = `
window.__lum = c => { const m = /rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)/.exec(c); if (!m) return null;
  const [r, g, b] = [1, 2, 3].map(i => Number(m[i]) / 255).map(v => v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4));
  return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
window.__k = (a, b) => { const x = window.__lum(a), y = window.__lum(b); if (x == null || y == null) return null;
  return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
window.__mapa = function (raiz) {
  const r1 = x => Math.round(x * 100) / 100;
  const marco = raiz.querySelector('.mapa-estacional-marco');
  const rej = raiz.querySelector('.mapa-estacional-rejilla');
  const mr = marco.getBoundingClientRect();
  const cab = [...rej.querySelectorAll('[role=columnheader]')].filter(c => c.textContent.trim() || c.querySelector('span'));
  const mesesSinDesplazar = cab.filter(c => { const r = c.getBoundingClientRect(); return r.left >= mr.left - 0.5 && r.right <= mr.right + 0.5; }).length;
  const celdas = [...rej.querySelectorAll('.mapa-estacional-celda')];
  const llenas = celdas.filter(c => !c.classList.contains('mapa-estacional-vacia'));
  // Cifra visible: el texto de la celda (span en el componente nuevo, nodo de texto en el viejo) con visibility visible.
  const cifras = llenas.map(c => {
    const s = c.querySelector('span') || c;
    const txt = s.textContent.trim();
    if (!txt) return null;
    const cs = getComputedStyle(s);
    const visible = cs.visibility === 'visible' && cs.display !== 'none';
    const bg = getComputedStyle(c).backgroundColor;
    // ancho del texto frente a la caja de la celda
    const rg = document.createRange(); rg.selectNodeContents(s); const tw = rg.getBoundingClientRect().width;
    return { t: txt, visible, k: window.__k(cs.color, bg), fs: parseFloat(cs.fontSize), tw: r1(tw), cw: c.clientWidth,
      cabe: tw <= c.clientWidth + 0.5, aria: c.getAttribute('aria-label'), bg, fg: cs.color };
  }).filter(Boolean);
  const vis = cifras.filter(x => x.visible);
  const ks = vis.map(x => x.k);
  const valor = raiz.querySelector('.mapa-estacional-valor');
  const ley = raiz.querySelector('.mapa-estacional-leyenda');
  const filas = [...rej.querySelectorAll('[role=row]')];
  const hijosNoFila = [...rej.children].filter(h => h.getAttribute('role') !== 'row').length;
  const guion = s => /(^|[^\\w])-\\d/.test(s || '');
  return {
    clases: raiz.className, marcoW: r1(mr.width), sw: marco.scrollWidth, cw: marco.clientWidth,
    desplaza: marco.scrollWidth > marco.clientWidth + 1, mesesSinDesplazar, cabecera: cab.map(c => c.textContent.trim()).join(' '),
    celdas: celdas.length, llenas: llenas.length, conCifra: cifras.length, cifrasVisibles: vis.length,
    contrasteMin: ks.length ? r1(Math.min(...ks)) : null, bajo45: ks.filter(k => k < 4.5).length,
    peores: vis.slice().sort((a, b) => a.k - b.k).slice(0, 2).map(x => ({ t: x.t, k: r1(x.k), bg: x.bg, fg: x.fg })),
    cuerpoMin: vis.length ? Math.min(...vis.map(x => x.fs)) : null, cuerpoMax: vis.length ? Math.max(...vis.map(x => x.fs)) : null,
    noCabenVisibles: vis.filter(x => !x.cabe).map(x => x.t + ' (' + x.tw + '/' + x.cw + ')').slice(0, 5),
    nNoCabenVisibles: vis.filter(x => !x.cabe).length,
    celda: llenas[0] ? { w: r1(llenas[0].getBoundingClientRect().width), h: r1(llenas[0].getBoundingClientRect().height) } : null,
    guionesCifra: cifras.filter(x => guion(x.t)).length, guionesAria: cifras.filter(x => guion(x.aria)).length,
    leyenda: ley ? ley.textContent.replace(/\\s+/g, ' ').trim() : null, guionLeyenda: ley ? guion(ley.textContent) : null,
    nota: (raiz.querySelector('.mapa-estacional-nota')?.textContent || '').replace(/\\s+/g, ' ').trim(),
    valor: valor ? { display: getComputedStyle(valor).display, txt: valor.textContent, ariaHidden: valor.getAttribute('aria-hidden') } : null,
    filas: filas.length, hijosNoFila, celdasPorFila: [...new Set(filas.map(f => f.children.length))],
    aria: rej.getAttribute('aria-label'), guionAria: guion(rej.getAttribute('aria-label')),
    enfocables: raiz.querySelectorAll('a[href], button, input, select, [tabindex]:not([tabindex="-1"])').length,
    primeras: llenas.slice(0, 3).map(c => c.getAttribute('aria-label'))
  };
};
true;`;

const MODOS = [
  { nombre: '1200', width: 1200, height: 1000, dsf: 1, mobile: false },
  { nombre: '800', width: 800, height: 1000, dsf: 1, mobile: false },
  { nombre: '375', width: 375, height: 812, dsf: 2, mobile: true },
];

const SERIES = ['airpassengers', 'usaccdeaths', 'co2', 'trm'];
const DIFS = ['ninguna', 'd1', 'D1', 'd1D1'];
const ESTADOS_FIRMA = [];
for (const se of SERIES) for (const lg of [true, false]) for (const df of DIFS) ESTADOS_FIRMA.push([se, lg, df]);
const ESTADOS_TIENDA = [];
for (const e of ['fijo', 'acelera']) for (const df of DIFS) ESTADOS_TIENDA.push([e, df]);
const CAPTURAS = new Set(['airpassengers-log-ninguna', 'airpassengers-log-d1D1', 'airpassengers-nolog-ninguna',
  'airpassengers-nolog-d1', 'co2-nolog-ninguna', 'trm-nolog-D1', 'usaccdeaths-nolog-d1D1', 'fijo-d1', 'acelera-d1D1', 'fijo-ninguna']);

async function preparar(c, modo, url, modulo) {
  await c.enviar('Emulation.setDeviceMetricsOverride', { width: modo.width, height: modo.height,
    deviceScaleFactor: modo.dsf, mobile: modo.mobile });
  await c.enviar('Emulation.setTouchEmulationEnabled', { enabled: modo.mobile, maxTouchPoints: modo.mobile ? 5 : 1 });
  await c.enviar('Page.navigate', { url: url + '#modulo-' + modulo });
  await espera(700);
  await c.esperaHasta("typeof loadModule === 'function' && typeof Chart !== 'undefined'", 30000);
  await c.evalua('document.fonts.ready.then(() => 1)');
  await c.evalua(`(() => { Chart.defaults.animation = false; return 1; })()`);
  await c.evalua(`loadModule(${modulo}), 1`);
  await espera(1200);
  await c.evalua(AYUDA);
  await c.evalua(`(() => { if (!document.getElementById('quitar-fijos')) { const st = document.createElement('style'); st.id = 'quitar-fijos';
    st.textContent = 'header.usta-header{position:static!important} #sidebarToggle,#scrollToTopBtn{visibility:hidden!important}'; document.head.appendChild(st); } return 1; })()`);
}

async function capturar(c, selector, indice, archivo) {
  const rect = await c.evalua(`(() => { const el = document.querySelectorAll(${JSON.stringify(selector)})[${indice}];
    if (!el) return null; el.scrollIntoView({ behavior: 'instant', block: 'start' });
    const r = el.getBoundingClientRect(); return { x: r.left + window.scrollX, y: r.top + window.scrollY, w: r.width, h: r.height }; })()`);
  if (!rect) return;
  await espera(150);
  const r = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
    clip: { x: Math.max(0, rect.x - 6), y: Math.max(0, rect.y - 6), width: rect.w + 12, height: rect.h + 12, scale: 1 } });
  fs.writeFileSync(path.join(OUT, archivo), Buffer.from(r.data, 'base64'));
}

// Árbol de accesibilidad de Chrome bajo la rejilla: cuántas filas, cabeceras y celdas expone.
async function arbol(c, selRaiz, indice) {
  const { root } = await c.enviar('DOM.getDocument', { depth: 0 });
  const { nodeIds } = await c.enviar('DOM.querySelectorAll', { nodeId: root.nodeId, selector: selRaiz + ' .mapa-estacional-rejilla' });
  if (!nodeIds[indice]) return null;
  const { node } = await c.enviar('DOM.describeNode', { nodeId: nodeIds[indice] });
  const out = {};
  for (const role of ['table', 'row', 'columnheader', 'rowheader', 'cell']) {
    try {
      const r = await c.enviar('Accessibility.queryAXTree', { backendNodeId: node.backendNodeId, role });
      out[role] = r.nodes.filter(n => !n.ignored).length;
      if (role === 'table') out.nombreTabla = r.nodes[0]?.name?.value || null;
      if (role === 'cell') out.nombreCelda = r.nodes[0]?.name?.value || null;
      if (role === 'columnheader') out.nombresCab = r.nodes.slice(0, 3).map(n => n.name?.value);
    } catch (e) { out[role] = 'error: ' + e.message; }
  }
  return out;
}

// En un mapa sin cifras: ratón sobre una celda, toque en otra, y Tab desde el control anterior.
async function interaccion(c, selRaiz, indice, modo) {
  const pos = await c.evalua(`(() => { const raiz = document.querySelectorAll(${JSON.stringify(selRaiz)})[${indice}];
    raiz.scrollIntoView({ block: 'center', behavior: 'instant' });
    const cs = [...raiz.querySelectorAll('.mapa-estacional-celda:not(.mapa-estacional-vacia)')];
    const a = cs[5].getBoundingClientRect(), b = cs[cs.length - 4].getBoundingClientRect();
    return { a: [a.x + a.width / 2, a.y + a.height / 2], b: [b.x + b.width / 2, b.y + b.height / 2],
      ariaA: cs[5].getAttribute('aria-label'), ariaB: cs[cs.length - 4].getAttribute('aria-label') }; })()`);
  await espera(150);
  const leer = () => c.evalua(`document.querySelectorAll(${JSON.stringify(selRaiz)})[${indice}].querySelector('.mapa-estacional-valor')?.textContent || null`);
  const res = { ariaA: pos.ariaA, ariaB: pos.ariaB, inicial: await leer() };
  if (!modo.mobile) {
    await c.enviar('Input.dispatchMouseEvent', { type: 'mouseMoved', x: pos.a[0], y: pos.a[1] });
    await espera(150);
    res.raton = await leer();
  } else {
    await c.enviar('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: pos.b[0], y: pos.b[1] }] });
    await c.enviar('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
    await espera(400);
    res.toque = await leer();
  }
  // Teclado: ¿alguna celda recibe el foco con Tab? Se parte del último control antes del mapa.
  res.teclado = await c.evalua(`(() => { const raiz = document.querySelectorAll(${JSON.stringify(selRaiz)})[${indice}];
    const celdasEnfocables = [...raiz.querySelectorAll('.mapa-estacional-celda')].filter(x => x.tabIndex >= 0).length;
    return { celdasEnfocables, focusin: false }; })()`);
  await c.evalua(`(() => { const raiz = document.querySelectorAll(${JSON.stringify(selRaiz)})[${indice}];
    const sim = raiz.closest('[data-simulador]') || raiz.parentElement;
    const ctl = [...sim.querySelectorAll('select, input, button')].pop(); if (ctl) ctl.focus(); return 1; })()`);
  const pasos = [];
  for (let i = 0; i < 4; i++) {
    await c.enviar('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 });
    await c.enviar('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 });
    await espera(80);
    pasos.push(await c.evalua(`(() => { const a = document.activeElement; return a ? (a.tagName + '.' + String(a.className).split(' ')[0] + (a.closest('.mapa-estacional') ? ' [en el mapa]' : '')) : null; })()`));
  }
  res.teclado.tab = pasos;
  res.teclado.valorTrasTab = await leer();
  return res;
}

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const c = await Chrome.lanzar(PUERTO);
  const salida = { fecha: new Date().toISOString(), estados: [], interacciones: [], arboles: [], eventos: null };
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable'); await c.enviar('Log.enable');
    await c.enviar('DOM.enable'); await c.enviar('Accessibility.enable');
    const PAGINAS = [
      { id: 'cap1', base: '/capitulo-1-componentes-descomposicion.html', modulo: 3, sel: '.mapa-estacional[data-mapa]' },
      { id: 'plantilla', base: '/plantilla-capitulo.html', modulo: 3, sel: '.mapa-estacional[data-mapa]', soloActual: false },
      { id: 'cap5', base: '/capitulo-5-sarima.html', modulo: 1, sel: '[data-simulador="mapa-firma"] .mapa-estacional', sim: 'mapa-firma' },
      { id: 'cap5', base: '/capitulo-5-sarima.html', modulo: 3, sel: '[data-simulador="tienda-cuadricula"] .mapa-estacional', sim: 'tienda-cuadricula' },
    ];
    for (const version of ['actual', 'antes']) {
      for (const modo of MODOS) {
        for (const pag of PAGINAS) {
          const host = pag.id === 'plantilla' ? (version === 'actual' ? PLANTILLA : ANTES) : (version === 'actual' ? ACTUAL : ANTES);
          c.contexto = `${version} ${pag.id} M${pag.modulo} ${modo.nombre}`;
          await preparar(c, modo, host + pag.base, pag.modulo);
          let estados = [[null]];
          if (pag.sim === 'mapa-firma') estados = ESTADOS_FIRMA;
          if (pag.sim === 'tienda-cuadricula') estados = ESTADOS_TIENDA;
          for (const est of estados) {
            let nombre = 'unico';
            if (pag.sim === 'mapa-firma') {
              const [se, lg, df] = est; nombre = `${se}-${lg ? 'log' : 'nolog'}-${df}`;
              await c.evalua(`(() => { const raiz = document.querySelector('[data-simulador="mapa-firma"]');
                const s = raiz.querySelectorAll('select'); s[0].value = '${se}'; s[0].dispatchEvent(new Event('change', { bubbles: true }));
                s[1].value = '${df}'; s[1].dispatchEvent(new Event('change', { bubbles: true }));
                const k = raiz.querySelector('input[type=checkbox]'); if (k.checked !== ${lg}) { k.checked = ${lg}; k.dispatchEvent(new Event('change', { bubbles: true })); }
                return 1; })()`);
            } else if (pag.sim === 'tienda-cuadricula') {
              const [e, df] = est; nombre = `${e}-${df}`;
              await c.evalua(`(() => { const raiz = document.querySelector('[data-simulador="tienda-cuadricula"]');
                const s = raiz.querySelectorAll('select'); s[0].value = '${e}'; s[0].dispatchEvent(new Event('change', { bubbles: true }));
                s[1].value = '${df}'; s[1].dispatchEvent(new Event('change', { bubbles: true })); return 1; })()`);
            }
            await espera(200);
            const m = await c.evalua(`window.__mapa(document.querySelector(${JSON.stringify(pag.sel)}))`);
            const lect = pag.sim ? await c.evalua(`document.querySelector('[data-simulador="${pag.sim}"] .simulador-lectura')?.textContent.replace(/\\s+/g, ' ').trim()`) : null;
            salida.estados.push({ version, ancho: modo.nombre, pagina: pag.id, sim: pag.sim || null, estado: nombre, mapa: m, lectura: lect });
            if (version === 'actual' && (CAPTURAS.has(nombre) || nombre === 'unico')) {
              await capturar(c, pag.sel, 0, `mapa-${pag.id}-${pag.sim || 'M' + pag.modulo}-${nombre}-${modo.nombre}.png`);
            }
            if (version === 'antes' && (nombre === 'airpassengers-log-ninguna' || nombre === 'fijo-d1' || nombre === 'unico') && modo.nombre !== '1200') {
              await capturar(c, pag.sel, 0, `antes-mapa-${pag.id}-${pag.sim || 'M' + pag.modulo}-${nombre}-${modo.nombre}.png`);
            }
          }
          if (version === 'actual') {
            salida.arboles.push({ ancho: modo.nombre, pagina: pag.id, sim: pag.sim || null, arbol: await arbol(c, pag.sel.replace(/ \.mapa-estacional$/, ''), 0) });
            const sinCifras = await c.evalua(`document.querySelector(${JSON.stringify(pag.sel)}).classList.contains('mapa-estacional--sin-cifras')`);
            if (sinCifras) {
              const r = await interaccion(c, pag.sel, 0, modo);
              salida.interacciones.push({ ancho: modo.nombre, pagina: pag.id, sim: pag.sim || null, ...r });
              await capturar(c, pag.sel, 0, `mapa-${pag.id}-${pag.sim || 'M' + pag.modulo}-tras-interaccion-${modo.nombre}.png`);
            }
          }
          console.log(`  ${version} ${modo.nombre} ${pag.id} ${pag.sim || ''}: ${estados.length} estados`);
        }
      }
    }
    salida.eventos = c.eventos;
  } finally {
    await c.cerrar();
  }
  fs.writeFileSync(path.join(__dirname, 'v2_mapas.json'), JSON.stringify(salida, null, 1));
  console.log('listo; eventos de consola:', salida.eventos ? salida.eventos.length : 'n/d');
}
main().then(() => process.exit(0)).catch(e => { console.error('✗ ' + e.stack); process.exit(1); });
