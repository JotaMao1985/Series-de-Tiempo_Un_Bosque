const fs=require('fs');const src=fs.readFileSync(process.argv[2],'utf8');
const SIMULACROS={}; eval(src);
const v=SIMULACROS['cap5-simulacro'].versiones[0];
for (const n of [8,9]) { const p=v.preguntas.find(q=>q.n===n); fs.writeFileSync(process.argv[3]+'/p'+n+'.svg.txt', p.enunciado); }
