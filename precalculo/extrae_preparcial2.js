#!/usr/bin/env node
// extrae_preparcial2.js — los ítems del preparcial del Corte II, ya interpolados
//
//   node precalculo/extrae_preparcial2.js [ruta del HTML]   → JSON por la salida estándar
//
// Ejecuta el <script> de la página contra un DOM de mentira (un Proxy que se
// devuelve a sí mismo para cualquier propiedad o llamada) y vuelca lo que el
// estudiante lee: enunciados, opciones, retroalimentación, claves, objetivos,
// módulos y los datos incrustados. Así `verifica_preparcial2.py` trabaja sobre
// el texto que de verdad se pinta —con cada cifra ya sustituida desde
// PREPARCIAL_DATOS— y no sobre una transcripción.
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ruta = process.argv[2] ||
  path.resolve(__dirname, '..', 'Htmls_Series', 'preparcial-corte-2.html');
const html = fs.readFileSync(ruta, 'utf8');
const ini = html.lastIndexOf('<script>');
const fin = html.lastIndexOf('</script>');
const codigo = html.slice(ini + '<script>'.length, fin);

const nada = new Proxy(function () {}, {
  get: (t, k) => (k === Symbol.toPrimitive ? () => 0 : k === 'length' ? 0 : nada),
  apply: () => nada,
  construct: () => nada,
  set: () => true
});
const contexto = {
  document: nada, window: nada, navigator: nada, localStorage: nada, location: nada,
  history: nada, Chart: nada, renderMathInElement: () => {}, Prism: nada,
  setTimeout: () => 0, clearTimeout: () => {}, setInterval: () => 0, clearInterval: () => {},
  requestAnimationFrame: () => 0, console, Math, JSON, Number, String, Array, Object, Set, Map,
  Date, RegExp, Error, Infinity, NaN, isFinite, parseFloat, parseInt, Symbol, Promise
};
vm.createContext(contexto);
// Las declaraciones `const` del script no cuelgan del contexto: se exponen al final.
vm.runInContext(codigo + `
;globalThis.__salida = {
  bloques: Object.fromEntries(['bloque-a', 'bloque-b', 'bloque-c', 'bloque-d']
    .map(b => [b, AUTOEVALUACIONES[b]])),
  simulacro: SIMULACRO, objetivos: OBJETIVOS, modulos: MODULOS_DEL_CORTE,
  datos: PREPARCIAL_DATOS, cursos: courseData };`, contexto);
process.stdout.write(JSON.stringify(contexto.__salida));
