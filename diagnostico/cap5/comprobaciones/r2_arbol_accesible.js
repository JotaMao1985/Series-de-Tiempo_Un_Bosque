#!/usr/bin/env node
// R2 del cap. 5 · el mapa estacional en el árbol de accesibilidad de Chrome (CDP Accessibility): ¿las filas
// `role="row"` con `display: Contents` llegan como filas, con su cabecera y sus celdas? Mapa del M1 a 375 px.
// Uso: BASE=http://127.0.0.1:8768/Htmls_Series/capitulo-5-sarima.html node r2_arbol_accesible.js > r2_arbol_accesible.out
const { Chrome, espera } = require('../diag/chrome');
const BASE = process.env.BASE || 'http://127.0.0.1:8768/Htmls_Series/capitulo-5-sarima.html';
(async () => {
  const c = await Chrome.lanzar(9278);
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable'); await c.enviar('Accessibility.enable'); await c.enviar('DOM.enable');
    await c.enviar('Emulation.setDeviceMetricsOverride', { width: 375, height: 812, deviceScaleFactor: 2, mobile: true });
    await c.enviar('Page.navigate', { url: BASE + '#modulo-1' });
    await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined'", 30000);
    await c.evalua('loadModule(1), 1'); await espera(1500);
    const { root } = await c.enviar('DOM.getDocument', { depth: -1 });
    const { nodeId } = await c.enviar('DOM.querySelector', { nodeId: root.nodeId, selector: '[data-mapa="firma"] .mapa-estacional-rejilla' });
    const { nodes } = await c.enviar('Accessibility.getPartialAXTree', { nodeId, fetchRelatives: false });
    const raiz = nodes[0];
    const { nodes: todos } = await c.enviar('Accessibility.getFullAXTree');
    const porId = new Map(todos.map(n => [n.nodeId, n]));
    const r = porId.get(raiz.nodeId) || raiz;
    const hijos = (r.childIds || []).map(id => porId.get(id)).filter(Boolean);
    console.log('rejilla:', r.role?.value, '·', JSON.stringify(r.name?.value));
    console.log('hijos:', hijos.length, 'roles', [...new Set(hijos.map(h => h.role?.value))].join(', '));
    hijos.slice(0, 3).forEach((f, i) => {
      const cel = (f.childIds || []).map(id => porId.get(id)).filter(Boolean);
      console.log(`fila ${i + 1}: ${f.role?.value} con ${cel.length} hijos: ` + cel.slice(0, 4).map(x => `${x.role?.value} «${x.name?.value}»`).join(' · ') + ' …');
    });
  } finally { await c.cerrar(); }
})().then(() => process.exit(0)).catch(e => { console.error(e); process.exit(1); });
