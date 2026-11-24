#!/usr/bin/env node
// R2 del cap. 5 (correcciones tras el verificador, V2 y V3) · el mapa estacional sin cifras, con teclado, botón y toque.
// Para cada mapa y ancho: modo inicial; Tab desde el elemento enfocable anterior (¿llega a la rejilla?); flechas, Inicio
// y Fin (¿cambia la celda señalada y la línea del valor?); Tab al botón «Ver las cifras», Intro (¿aria-pressed, cifras,
// desplazamiento, señal del borde derecho?), desplazar hasta el final (¿se va la señal?), flechas en el modo con cifras,
// Espacio (¿vuelve?); un toque emulado sobre una celda. Contraste de cada cifra visible en el modo con cifras.
// Uso: BASE=http://127.0.0.1:8768 node r2_mapa_teclado.js > r2_mapa_teclado.out
const fs = require('fs');
const path = require('path');
const { Chrome, espera } = require('../diag/chrome');
const BASE = process.env.BASE || 'http://127.0.0.1:8768';
const OUT = path.resolve(__dirname, '..', 'capturas', 'r2');
const CASOS = [
  ['cap5', 'Htmls_Series/capitulo-5-sarima.html', 1, 'firma'],
  ['cap5', 'Htmls_Series/capitulo-5-sarima.html', 3, 'tienda'],
  ['cap1', 'Htmls_Series/capitulo-1-componentes-descomposicion.html', 3, 'cap1-airpassengers'],
  ['plantilla', 'plantilla/plantilla-capitulo.html', 3, 'demo-mapa'],
];
const ANCHOS = { 1200: { width: 1200, height: 1000, deviceScaleFactor: 1, mobile: false },
  800: { width: 800, height: 1000, deviceScaleFactor: 1, mobile: false },
  375: { width: 375, height: 812, deviceScaleFactor: 2, mobile: true } };

const ESTADO = id => `(() => {
  const raiz = document.querySelector('[data-mapa="${id}"]');
  const rej = raiz.querySelector('.mapa-estacional-rejilla');
  const marco = raiz.querySelector('.mapa-estacional-marco');
  const boton = raiz.querySelector('.mapa-estacional-boton');
  const mas = raiz.querySelector('.mapa-estacional-mas');
  const valor = raiz.querySelector('.mapa-estacional-valor');
  const lum = c => { const m = /rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)/.exec(c); const v = [1, 2, 3].map(i => Number(m[i]) / 255)
    .map(x => x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4)); return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]; };
  const k = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const spans = [...rej.querySelectorAll('.mapa-estacional-celda > span')].filter(s => getComputedStyle(s).visibility !== 'hidden');
  const ks = spans.map(s => k(getComputedStyle(s).color, getComputedStyle(s.parentNode).backgroundColor));
  const colores = [...new Set(spans.map(s => getComputedStyle(s).color))];
  const mr = marco.getBoundingClientRect();
  const cab = [...rej.querySelectorAll('[role=columnheader]')].filter(c => c.getAttribute('aria-label') !== 'Año');
  return {
    modo: raiz.classList.contains('mapa-estacional--sin-cifras') ? 'sin-cifras' : raiz.classList.contains('mapa-estacional--desplazable') ? 'desplazable' : 'cifras',
    tabindex: rej.getAttribute('tabindex'), foco: document.activeElement === rej ? 'rejilla' : document.activeElement === boton ? 'botón' : (document.activeElement.tagName + '.' + document.activeElement.className).slice(0, 50),
    boton: boton ? { visible: !boton.hidden && getComputedStyle(boton).display !== 'none', pressed: boton.getAttribute('aria-pressed'), texto: boton.textContent } : null,
    valor: valor ? { visible: getComputedStyle(valor).display !== 'none', txt: valor.textContent } : null,
    activa: (rej.querySelector('.mapa-estacional-activa') || {}).getAttribute ? rej.querySelector('.mapa-estacional-activa').getAttribute('aria-label') : null,
    desplaza: marco.scrollWidth > marco.clientWidth + 1, scrollLeft: Math.round(marco.scrollLeft), sw: marco.scrollWidth, cw: marco.clientWidth,
    senal: mas ? !mas.hidden && getComputedStyle(mas).display !== 'none' : null,
    mesesVisibles: cab.filter(c => { const r = c.getBoundingClientRect(); return r.left >= mr.left - 0.5 && r.right <= mr.right + 0.5; }).length,
    cifrasVisibles: spans.length, contrasteMin: ks.length ? Math.round(Math.min(...ks) * 100) / 100 : null, bajo45: ks.filter(x => x < 4.5).length,
    tonos: colores, focoVisible: document.activeElement === rej || document.activeElement === boton ? getComputedStyle(document.activeElement).outlineStyle + ' ' + getComputedStyle(document.activeElement).outlineColor : null
  };
})()`;

async function tecla(c, key, code, keyCode, texto) {
  await c.enviar('Input.dispatchKeyEvent', { type: 'keyDown', key, code, windowsVirtualKeyCode: keyCode, nativeVirtualKeyCode: keyCode, text: texto });
  await c.enviar('Input.dispatchKeyEvent', { type: 'keyUp', key, code, windowsVirtualKeyCode: keyCode, nativeVirtualKeyCode: keyCode });
  await espera(150);
}

async function captura(c, id, archivo) {
  const r = await c.evalua(`(() => { const e = document.querySelector('[data-mapa="${id}"]'); const r = e.getBoundingClientRect();
    return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height }; })()`);
  const s = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
    clip: { x: Math.max(0, r.x - 6), y: Math.max(0, r.y - 6), width: r.w + 12, height: r.h + 12, scale: 1 } });
  fs.writeFileSync(path.join(OUT, archivo), Buffer.from(s.data, 'base64'));
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const c = await Chrome.lanzar(9278);
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable'); await c.enviar('Log.enable');
    for (const [pag, url, mod, id] of CASOS) {
      for (const ancho of [1200, 800, 375]) {
        c.contexto = `${pag} ${id} ${ancho}`;
        await c.enviar('Emulation.setDeviceMetricsOverride', ANCHOS[ancho]);
        if (ancho === 375) await c.enviar('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
        else await c.enviar('Emulation.setTouchEmulationEnabled', { enabled: false });
        await c.enviar('Page.navigate', { url: `${BASE}/${url}#modulo-${mod}` });
        await espera(700);
        await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined'", 30000);
        await c.evalua('document.fonts.ready.then(() => 1)');
        await c.evalua(`loadModule(${mod}), 1`); await espera(1300);
        const pasos = [];
        const anota = async nombre => pasos.push([nombre, await c.evalua(ESTADO(id))]);
        await c.evalua(`(() => { const e = document.querySelector('[data-mapa="${id}"]'); e.scrollIntoView({ block: 'center' }); return 1; })()`);
        await anota('inicial');
        // Foco en el elemento enfocable anterior a la rejilla, y Tab
        await c.evalua(`(() => {
          const rej = document.querySelector('[data-mapa="${id}"] .mapa-estacional-rejilla');
          const todos = [...document.querySelectorAll('a[href], button, input, select, textarea, [tabindex]')]
            .filter(e => !e.disabled && e.offsetParent !== null && e.tabIndex >= 0 && !rej.contains(e));
          const previos = todos.filter(e => e.compareDocumentPosition(rej) & Node.DOCUMENT_POSITION_FOLLOWING);
          previos[previos.length - 1].focus(); return previos[previos.length - 1].tagName; })()`);
        await tecla(c, 'Tab', 'Tab', 9);
        await anota('Tab');
        if (pasos[pasos.length - 1][1].foco === 'rejilla') {
          await tecla(c, 'ArrowRight', 'ArrowRight', 39); await tecla(c, 'ArrowRight', 'ArrowRight', 39);
          await tecla(c, 'ArrowDown', 'ArrowDown', 40);
          await anota('→ → ↓');
          await tecla(c, 'End', 'End', 35);
          await anota('Fin');
          await captura(c, id, `teclado-${pag}-${id}-sin-cifras-${ancho}.png`);
          await tecla(c, 'Tab', 'Tab', 9);
          await anota('Tab (al botón)');
          await tecla(c, 'Enter', 'Enter', 13, '\r');
          await espera(300);
          await anota('Intro');
          await captura(c, id, `teclado-${pag}-${id}-con-cifras-${ancho}.png`);
          // Flechas en el modo con cifras: la celda señalada se desplaza a la vista
          await c.evalua(`document.querySelector('[data-mapa="${id}"] .mapa-estacional-rejilla').focus(), 1`);
          await tecla(c, 'End', 'End', 35);
          await anota('rejilla con cifras: Fin');
          await c.evalua(`(() => { const m = document.querySelector('[data-mapa="${id}"] .mapa-estacional-marco'); m.scrollLeft = m.scrollWidth; return 1; })()`);
          await espera(200);
          await anota('desplazado al final');
          await c.evalua(`document.querySelector('[data-mapa="${id}"] .mapa-estacional-boton').focus(), 1`);
          await tecla(c, ' ', 'Space', 32, ' ');
          await espera(300);
          await anota('Espacio');
        }
        // Toque (o clic) sobre la celda del medio de la tercera fila
        await c.evalua(`(() => { const f = document.querySelectorAll('[data-mapa="${id}"] .mapa-estacional-fila')[3] ||
          document.querySelectorAll('[data-mapa="${id}"] .mapa-estacional-fila')[1];
          const cel = f.querySelectorAll('.mapa-estacional-celda')[6]; cel.scrollIntoView({ block: 'center', behavior: 'instant' });
          return 1; })()`);
        await espera(400);   // la página desplaza con suavidad: se mide después
        const p = await c.evalua(`(() => { const f = document.querySelectorAll('[data-mapa="${id}"] .mapa-estacional-fila')[3] ||
          document.querySelectorAll('[data-mapa="${id}"] .mapa-estacional-fila')[1];
          const cel = f.querySelectorAll('.mapa-estacional-celda')[6];
          const r = cel.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2, esperado: cel.getAttribute('aria-label') }; })()`);
        if (ancho === 375) {
          await c.enviar('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: p.x, y: p.y }] });
          await c.enviar('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
        } else {
          await c.enviar('Input.dispatchMouseEvent', { type: 'mousePressed', x: p.x, y: p.y, button: 'left', clickCount: 1 });
          await c.enviar('Input.dispatchMouseEvent', { type: 'mouseReleased', x: p.x, y: p.y, button: 'left', clickCount: 1 });
        }
        await espera(300);
        await anota(`${ancho === 375 ? 'toque' : 'clic'} (esperado «${p.esperado}»)`);
        console.log(`\n=== ${pag} · ${id} · ${ancho} px`);
        for (const [nombre, e] of pasos) {
          console.log(`  ${nombre.padEnd(48)} modo ${e.modo.padEnd(11)} foco ${String(e.foco).padEnd(8)} tabindex ${e.tabindex} · botón ${e.boton ? (e.boton.visible ? 'visible aria-pressed=' + e.boton.pressed : 'oculto') : '—'}` +
            ` · valor ${e.valor && e.valor.visible ? '«' + e.valor.txt.slice(0, 60) + '»' : '(oculto)'} · señalada ${e.activa || '—'}` +
            ` · meses ${e.mesesVisibles}/12${e.desplaza ? ' DESPLAZA (' + e.scrollLeft + '/' + (e.sw - e.cw) + ')' : ''} · señal ${e.senal}` +
            ` · cifras ${e.cifrasVisibles} contraste mín ${e.contrasteMin} (<4.5: ${e.bajo45}) tonos ${e.tonos.length}${e.focoVisible ? ' · foco ' + e.focoVisible : ''}`);
        }
      }
    }
    console.log('\nconsola:', JSON.stringify(c.eventos.filter(e => !/favicon/.test(e.txt))));
  } finally { await c.cerrar(); }
})().then(() => process.exit(0)).catch(e => { console.error(e); process.exit(1); });
