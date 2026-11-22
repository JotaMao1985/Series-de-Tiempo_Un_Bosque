// Diagnóstico cap. 4 · vuelca a JSON los cuatro instrumentos de práctica, con
// el texto visible de cada opción, su marca de correcta, su retro, la pista y
// las numéricas (respuesta, tolerancia). No se toca el HTML.
//   node diagnostico/cap4/diag/ejercicios_vuelca.js > diagnostico/cap4/diag/ejercicios_vuelca.json
// Instrumentos: AUTOEVALUACIONES['cap4'] y SIMULACROS['cap4-simulacro'] del
// capítulo 4; AUTOEVALUACIONES['bloque-a'..'bloque-d'] y SIMULACRO del
// preparcial (Htmls_Series/preparcial-corte-2.html).
const fs = require('fs');
const path = require('path');
const raiz = path.resolve(__dirname, '../../..');
const cap4 = fs.readFileSync(path.join(raiz, 'Htmls_Series/capitulo-4-modelos-arima.html'), 'utf8');
const prep = fs.readFileSync(path.join(raiz, 'Htmls_Series/preparcial-corte-2.html'), 'utf8');

// Todo nombre desconocido se resuelve a un stub inocuo (los `dibujar` no se ejecutan).
const stub = new Proxy(function () { return stub; }, { get: (t, k) => k === Symbol.toPrimitive ? () => 0 : stub });
const entorno = new Proxy({}, {
  has: (t, k) => !(k in globalThis) || k === 'stub',
  get: (t, k) => (k === Symbol.unscopables ? undefined : k in t ? t[k] : stub),
  set: (t, k, v) => { t[k] = v; return true; }
});
const evalua = (codigo, devuelve) => new Function('__e', `with (__e) { ${codigo}; return ${devuelve}; }`)(entorno);

function trozo(txt, marca, cierre) {
  const i = txt.indexOf(marca);
  if (i < 0) throw new Error('no encuentro ' + marca);
  const f = txt.indexOf(cierre, i) + cierre.length;
  return txt.slice(i, f);
}
const linea = (txt, marca) => txt.slice(0, txt.indexOf(marca)).split('\n').length;

const visible = s => String(s ?? '')
  .replace(/<[^>]+>/g, '')
  .replace(/&nbsp;/g, ' ').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&').replace(/&quot;/g, '"')
  .replace(/\\\(|\\\)/g, '')
  .replace(/\\(nabla|theta|lambda|phi|varepsilon|mu|approx|sigma|pi|rho|psi|ge|le|lt|gt|infty|gamma|beta|alpha|delta|ell)/g, 'x')
  .replace(/\\[a-zA-Z]+/g, '')
  .replace(/[${}_^\\]/g, '')
  .replace(/\s+/g, ' ').trim();

function normaliza(nombre, linea0, Q) {
  return Q.map((p, i) => ({
    instrumento: nombre, n: i + 1, linea_bloque: linea0,
    tipo: p.tipo || 'opcion', modulo: p.modulo ?? p.clave ?? null, objetivo: p.objetivo ?? null,
    pregunta: visible(p.pregunta ?? p.enunciado),
    pista: p.pista ? visible(p.pista) : null,
    respuesta: p.respuesta ?? null, tolerancia: p.tolerancia ?? null,
    retroAcierto: p.retroAcierto ? visible(p.retroAcierto) : null,
    retroFallo: p.retroFallo ? visible(p.retroFallo) : null,
    opciones: (p.opciones || []).map(o => typeof o === 'string'
      ? { texto: visible(o), largo: visible(o).length, correcta: null, retro: null }
      : { texto: visible(o.texto), largo: visible(o.texto).length, correcta: !!o.correcta, retro: o.retro ? visible(o.retro) : null }),
    filas: p.filas ? p.filas.map(visible) : null,
    respuestas: p.respuestas ? p.respuestas.map(visible) : null,
    elementos: p.elementos ? p.elementos.map(visible) : null
  }));
}

const salida = {};
// --- capítulo 4: quiz ---
const qCap4 = trozo(cap4, "AUTOEVALUACIONES['cap4'] = [", '\n    ];');
salida.cap4 = normaliza('cap4', linea(cap4, "AUTOEVALUACIONES['cap4'] = ["),
  evalua('const SIMULACROS = {}, AUTOEVALUACIONES = {};' + qCap4, "AUTOEVALUACIONES['cap4']"));
// --- capítulo 4: simulacro (sin clave) ---
const sCap4 = trozo(cap4, "SIMULACROS['cap4-simulacro'] = {", '\n    };');
salida.simulacro = normaliza('simulacro', linea(cap4, "SIMULACROS['cap4-simulacro'] = {"),
  evalua('const SIMULACROS = {};' + sCap4, "SIMULACROS['cap4-simulacro'].preguntas"));
// --- preparcial ---
const ini = prep.indexOf('    const PREPARCIAL_DATOS = ');
const fin = prep.indexOf('    const SIM = { fase:');
const codigo = prep.slice(ini, fin)
  .replace(/^    const /gm, '    var ');           // `var` para que vivan en __e
const AUTO = evalua('var AUTOEVALUACIONES = {}; var CAP3 = "c3", CAP4 = "c4";' + codigo,
  '{ a: AUTOEVALUACIONES, s: SIMULACRO, d: PREPARCIAL_DATOS }');
for (const b of ['bloque-a', 'bloque-b', 'bloque-c', 'bloque-d'])
  salida[b] = normaliza(b, linea(prep, `AUTOEVALUACIONES['${b}'] = [`), AUTO.a[b]);
salida['prep-simulacro'] = normaliza('prep-simulacro', linea(prep, 'const SIMULACRO = {'), AUTO.s.items);
console.log(JSON.stringify(salida, null, 1));
