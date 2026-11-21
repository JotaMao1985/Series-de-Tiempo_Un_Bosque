#!/usr/bin/env node
// R2 del cap. 3 · marcasLegibles() de HEAD frente a la del árbol de trabajo, sobre ejes sintéticos de
// rezagos u horizontes (1..n) a muchos anchos, con y sin tope de marcas (maxMarcas 12 es el de los
// gráficos de líneas; sin tope, los de barras). Exige: (a) si HEAD no tocaba el eje, ahora tampoco;
// (b) ninguna marca menos que en HEAD; (c) los múltiplos de 12 de HEAD siguen; (d) nunca más marcas que
// el tope; (e) el 1 rotulado siempre que el eje se toque.
// Uso (desde la raíz): node diagnostico/cap3/comprobaciones/r2_marcas.js
const fs = require('fs');
const { execSync } = require('child_process');
const ARCH = 'Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html';
function extrae(html) {
  const i = html.indexOf('    const ES_FECHA_MENSUAL');
  const j = html.indexOf('    // Rótulo de una marca del eje de categorías');
  return new Function(html.slice(i, j) + '\nreturn marcasLegibles;')();
}
const vieja = extrae(execSync(`git show HEAD:${ARCH}`, { maxBuffer: 1e8 }).toString());
const nueva = extrae(fs.readFileSync(ARCH, 'utf8'));
function eje(n, ancho, fuente) {
  const et = Array.from({ length: n }, (_, k) => String(k + 1));
  return { type: 'category', isHorizontal: () => true, width: ancho, min: 0, max: n - 1,
    getLabels: () => et, options: { ticks: { font: { size: fuente } } }, ticks: null };
}
let casos = 0, fallos = 0, con1 = 0, tocados = 0;
const ejemplos = {};
for (const [nombre, op, fuente] of [['barras', { barras: true, aire: 0.9 }, 10], ['líneas, tope 12', { maxMarcas: 12 }, 11]]) {
  for (const n of [5, 8, 10, 12, 16, 20, 24, 30, 36, 48, 60]) {
    if (op.maxMarcas && n > 60) continue;
    for (let ancho = 30; ancho <= 900; ancho += 5) {
      const a = eje(n, ancho, fuente), d = eje(n, ancho, fuente);
      const ra = vieja(a, op), rd = nueva(d, op);
      const ma = ra ? a.ticks.map(t => t.value + 1) : null, md = rd ? d.ticks.map(t => t.value + 1) : null;
      casos++;
      const mal = [];
      if (!ma !== !md) mal.push('a: uno toca el eje y el otro no');
      if (ma && md) {
        tocados++;
        if (md.length < ma.length) mal.push('b: menos marcas');
        if (ma.filter(v => v % 12 === 0).some(v => !md.includes(v))) mal.push('c: pierde un múltiplo de 12');
        if (op.maxMarcas && md.length > op.maxMarcas) mal.push('d: pasa del tope');
        if (!md.includes(1)) mal.push('e: sin el 1'); else con1++;
        if ([60, 160, 200, 240, 600].includes(ancho) && [16, 20, 24, 36].includes(n))
          ejemplos[`${nombre} · 1..${n} · ${ancho} px`] = `${ma.join(' ')}  ->  ${md.join(' ')}`;
      } else if ([60].includes(ancho) && [20, 36].includes(n)) {
        ejemplos[`${nombre} · 1..${n} · ${ancho} px`] = 'no se toca (ni antes ni ahora)';
      }
      if (mal.length) { fallos++; if (fallos <= 15) console.log('FALLA', nombre, `1..${n}`, ancho + ' px', mal.join('; '), '|', ma && ma.join(' '), '->', md && md.join(' ')); }
    }
  }
}
for (const [k, v] of Object.entries(ejemplos)) console.log(k.padEnd(34), v);
console.log(`${casos} ejes probados, ${tocados} rotulados por marcasLegibles, ${con1} con el 1; fallos: ${fallos}`);
process.exit(fallos ? 1 : 0);
