const fs=require('fs');const src=fs.readFileSync(process.argv[2],'utf8');
const SIMULACROS={}; eval(src);
const s=SIMULACROS['cap5-simulacro'];
console.log('minutos',s.minutos,'titulo',s.titulo,'etapas',JSON.stringify(s.etapas));
for(const v of s.versiones){ console.log('=== VERSION',v.numero); console.log('CASO:',v.caso.replace(/<[^>]+>/g,' ').replace(/\s+/g,' '));
 for(const p of v.preguntas){ console.log('\n--- P'+p.n,'['+p.etapa+']',p.etiqueta,p.tipo);
  console.log('ENUNCIADO:',p.enunciado.replace(/<[^>]+>/g,' ').replace(/\s+/g,' '));
  if(p.tipo==='numero'){console.log('CLAVE:',JSON.stringify(p.clave)); console.log('CUENTA:',p.cuenta.replace(/<[^>]+>/g,' ').replace(/\s+/g,' ')); console.log('RUTAS:',JSON.stringify(p.rutas.map(r=>[r.valor,r.texto.replace(/<[^>]+>/g,'')])));}
  else {p.opciones.forEach((o,j)=>console.log((j===p.correcta?'*':' ')+'abcdef'[j]+') '+o.texto.replace(/<[^>]+>/g,' ').replace(/\s+/g,' ')+' || '+o.retro.replace(/<[^>]+>/g,' ').replace(/\s+/g,' ')));}
 }}
