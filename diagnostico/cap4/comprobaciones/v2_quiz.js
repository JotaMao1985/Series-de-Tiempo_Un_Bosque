#!/usr/bin/env node
// Compara AUTOEVALUACIONES['cap4'] y SIMULACROS['cap4-simulacro'] entre HEAD (8767) y el árbol (8766): todo salvo
// `dibujar` (función) debe ser idéntico, y de `alto` y `descripcionGrafico` solo cambian los de las dos preguntas con gráfico.
const fs = require('fs'); const path = require('path');
const { Chrome, espera } = require('../diag/chrome');
async function volcar(c, pto) {
  await c.enviar('Page.navigate', { url: `http://127.0.0.1:${pto}/capitulo-4-modelos-arima.html#modulo-1` });
  await espera(600);
  await c.esperaHasta("typeof courseData !== 'undefined' && typeof AUTOEVALUACIONES !== 'undefined'", 30000);
  return c.evalua(`JSON.stringify({ quiz: AUTOEVALUACIONES['cap4'].map(p => Object.assign({}, p, { dibujar: typeof p.dibujar })),
    simulacro: (typeof SIMULACROS !== 'undefined' && SIMULACROS['cap4-simulacro']) || null,
    claves: Object.keys(AUTOEVALUACIONES), claves_sim: typeof SIMULACROS !== 'undefined' ? Object.keys(SIMULACROS) : null,
    cursoMods: courseData.modules ? courseData.modules.map(m => m.title || m.id) : Object.keys(courseData) })`);
}
async function main() {
  const c = await Chrome.lanzar(9285);
  try {
    await c.enviar('Page.enable'); await c.enviar('Runtime.enable');
    const nuevo = JSON.parse(await volcar(c, 8766)); const viejo = JSON.parse(await volcar(c, 8767));
    fs.writeFileSync(path.join(__dirname, 'v2_quiz_nuevo.json'), JSON.stringify(nuevo, null, 1));
    fs.writeFileSync(path.join(__dirname, 'v2_quiz_viejo.json'), JSON.stringify(viejo, null, 1));
    console.log('preguntas', viejo.quiz.length, nuevo.quiz.length, 'claves', JSON.stringify(nuevo.claves), JSON.stringify(nuevo.claves_sim));
    console.log('simulacro idéntico:', JSON.stringify(viejo.simulacro) === JSON.stringify(nuevo.simulacro), 'tamaño', JSON.stringify(nuevo.simulacro).length);
    console.log('módulos idénticos:', JSON.stringify(viejo.cursoMods) === JSON.stringify(nuevo.cursoMods), nuevo.cursoMods.length);
    viejo.quiz.forEach((p, i) => {
      const q = nuevo.quiz[i];
      const ks = new Set([...Object.keys(p), ...Object.keys(q)]);
      const difs = [...ks].filter(k => JSON.stringify(p[k]) !== JSON.stringify(q[k]));
      if (difs.length) console.log(`  pregunta ${i + 1} (${p.tipo}, M${p.modulo}): cambia`, difs.join(', '), '\n     antes:', JSON.stringify(difs.map(k => p[k])).slice(0, 300), '\n     ahora:', JSON.stringify(difs.map(k => q[k])).slice(0, 700));
    });
  } finally { await c.cerrar(); }
}
main().then(() => process.exit(0)).catch(e => { console.error(e.stack); process.exit(1); });
