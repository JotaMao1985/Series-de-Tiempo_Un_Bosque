// Diagnóstico cap. 5 · vuelca a JSON el quiz AUTOEVALUACIONES['cap5'] y el
// simulacro SIMULACROS['cap5-simulacro'], con el texto visible de cada opción,
// su marca de correcta, su retro, la pista, la clave numérica, la tolerancia
// y las «rutas» (errores frecuentes) del simulacro. No se toca el HTML.
//   node diagnostico/cap5/diag/ejercicios_vuelca.js > diagnostico/cap5/diag/ejercicios_vuelca.json
// Adaptado de diagnostico/cap4/diag/ejercicios_vuelca.js.
const fs = require('fs');
const path = require('path');
const raiz = path.resolve(__dirname, '../../..');
const cap5 = fs.readFileSync(path.join(raiz, 'Htmls_Series/capitulo-5-sarima.html'), 'utf8');

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
  .replace(/<sub>(.*?)<\/sub>/g, '$1').replace(/<sup>(.*?)<\/sup>/g, '^$1')
  .replace(/<[^>]+>/g, ' ')
  .replace(/&nbsp;/g, ' ').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&').replace(/&quot;/g, '"')
  .replace(/\\\(|\\\)/g, '')
  .replace(/\\(nabla|theta|Theta|lambda|phi|Phi|varepsilon|mu|approx|sigma|pi|rho|psi|ge|le|lt|gt|infty|gamma|beta|alpha|delta|ell|times|hat)/g, 'x')
  .replace(/\\[a-zA-Z]+/g, '')
  .replace(/[${}_^\\]/g, '')
  .replace(/\s+/g, ' ').replace(/\s+([.,;:])/g, '$1').trim();

const salida = {};
const q = trozo(cap5, "AUTOEVALUACIONES['cap5'] = [", '\n    ];');
const Q = evalua('const AUTOEVALUACIONES = {};' + q, "AUTOEVALUACIONES['cap5']");
salida.cap5 = Q.map((p, i) => ({
  instrumento: 'cap5', n: i + 1, linea_bloque: linea(cap5, "AUTOEVALUACIONES['cap5'] = ["),
  tipo: p.tipo || 'opcion', modulo: p.modulo ?? null,
  pregunta: visible(p.pregunta), pista: p.pista ? visible(p.pista) : null,
  respuesta: p.respuesta ?? null, tolerancia: p.tolerancia ?? null,
  retroAcierto: p.retroAcierto ? visible(p.retroAcierto) : null,
  retroFallo: p.retroFallo ? visible(p.retroFallo) : null,
  dibujar: p.dibujar ? String(p.dibujar) : null,
  opciones: (p.opciones || []).map(o => ({ texto: visible(o.texto), largo: visible(o.texto).length, correcta: !!o.correcta, retro: o.retro ? visible(o.retro) : null }))
}));
const s = trozo(cap5, "SIMULACROS['cap5-simulacro'] = {", '\n    };');
const S = evalua('const SIMULACROS = {};' + s, "SIMULACROS['cap5-simulacro']");
salida.simulacro_meta = { minutos: S.minutos, etapas: S.etapas, versiones: S.versiones.length, linea_bloque: linea(cap5, "SIMULACROS['cap5-simulacro'] = {"), caso: visible(S.versiones[0].caso) };
salida.simulacro = S.versiones[0].preguntas.map(p => ({
  instrumento: 'simulacro', n: p.n, id: p.id, etapa: p.etapa, etiqueta: visible(p.etiqueta), tipo: p.tipo,
  enunciado: visible(p.enunciado), enunciado_html: p.enunciado,
  clave: p.clave ?? null, cuenta: p.cuenta ? visible(p.cuenta) : null,
  rutas: (p.rutas || []).map(r => ({ valor: r.valor, cifra: r.cifra, texto: visible(r.texto) })),
  correcta: p.correcta ?? null,
  opciones: (p.opciones || []).map((o, j) => ({ texto: visible(o.texto), largo: visible(o.texto).length, correcta: p.correcta === j, retro: o.retro ? visible(o.retro) : null })),
  otros_campos: Object.keys(p).filter(k => !['n','id','etapa','etiqueta','tipo','enunciado','clave','cuenta','rutas','correcta','opciones'].includes(k))
}));
console.log(JSON.stringify(salida, null, 1));
