#!/usr/bin/env python3
"""R5 · tareas para r3bis_elemento.js: el quiz de principio a fin, los tres
ejercicios abiertos y el bloque del Módulo 2, a 1200 y 375 px.

Uso:
  python3 diagnostico/cap1/herramientas/r5_tareas.py > /tmp/r5_tareas.json
  OUT=diagnostico/cap1/capturas/r5 node diagnostico/cap1/herramientas/r3bis_elemento.js /tmp/r5_tareas.json
"""
import json

URL = "http://localhost:8731/capitulo-1-componentes-descomposicion.html"

QUIZ = r"""
(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const Q = () => [...mainContent.querySelectorAll('.quiz-pregunta')];
  const txt = el => el && !el.hidden ? el.innerText.replace(/\s+/g, ' ').trim().slice(0, 90) : null;
  const log = [];
  const snap = (i, tag) => { const b = Q()[i]; log.push([i + 1, tag, txt(b.querySelector('.quiz-pista')), b.querySelector('.quiz-retro').className, txt(b.querySelector('.quiz-retro'))]); };
  const op = (i, j) => Q()[i].querySelectorAll('.quiz-opcion')[j].click();
  op(0, 0); snap(0, 'falla a'); op(0, 1); snap(0, 'acierta b');
  op(1, 0); snap(1, 'falla a'); op(1, 1); snap(1, 'falla b');
  const b3 = Q()[2], inp = b3.querySelector('input'), btn = b3.querySelector('.quiz-comprobar');
  inp.value = '0.25'; btn.click(); snap(2, '0.25'); inp.value = '0.13'; btn.click(); snap(2, '0.13');
  op(3, 3); snap(3, 'falla d'); op(3, 0); snap(3, 'acierta a');
  const b5 = Q()[4], o5 = b5.querySelectorAll('.quiz-opcion'), c5 = b5.querySelector('.quiz-comprobar');
  o5[0].click(); o5[1].click(); o5[2].click(); c5.click(); snap(4, 'marca 1,2,3');
  o5[2].click(); o5[3].click(); c5.click(); snap(4, 'marca 1,2,4');
  op(5, 2); snap(5, 'acierta c');
  op(6, 3); snap(6, 'falla d'); op(6, 2); snap(6, 'acierta c');
  op(7, 1); snap(7, 'acierta b');
  await wait(400);
  return { log, marcador: mainContent.querySelector('.quiz-conteo').textContent,
           resumen: mainContent.querySelector('.quiz-resumen').innerText.replace(/\s+/g, ' ').trim(),
           katexErr: mainContent.querySelectorAll('.katex-error').length };
})()
"""

# Segunda pasada: se reinicia, se falla SOLO la pregunta 2 y se comprueba que el
# resumen manda al Módulo 4 (antes mandaba al 6).
SOLO_Q2 = r"""
(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  mainContent.querySelector('.quiz-reiniciar').click(); await wait(500);
  const Q = () => [...mainContent.querySelectorAll('.quiz-pregunta')];
  const op = (i, j) => Q()[i].querySelectorAll('.quiz-opcion')[j].click();
  op(0, 1); op(1, 0); op(1, 2);
  const b3 = Q()[2]; b3.querySelector('input').value = '1/8'; b3.querySelector('.quiz-comprobar').click();
  op(3, 0);
  const o5 = Q()[4].querySelectorAll('.quiz-opcion'); o5[1].click(); o5[2].click(); o5[4].click(); Q()[4].querySelector('.quiz-comprobar').click();
  op(5, 2); op(6, 2); op(7, 1);
  await wait(400);
  return { marcador: mainContent.querySelector('.quiz-conteo').textContent,
           resumen: mainContent.querySelector('.quiz-resumen').innerText.replace(/\s+/g, ' ').trim(),
           retroQ5: Q()[4].querySelector('.quiz-retro').innerText.replace(/\s+/g, ' ').trim().slice(0, 160) };
})()
"""

TODO_BIEN = r"""
(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  mainContent.querySelector('.quiz-reiniciar').click(); await wait(500);
  const Q = () => [...mainContent.querySelectorAll('.quiz-pregunta')];
  const op = (i, j) => Q()[i].querySelectorAll('.quiz-opcion')[j].click();
  op(0, 1); op(1, 3);
  const b3 = Q()[2]; b3.querySelector('input').value = '0.13'; b3.querySelector('.quiz-comprobar').click();
  op(3, 0);
  const o5 = Q()[4].querySelectorAll('.quiz-opcion'); o5[1].click(); o5[2].click(); o5[4].click(); Q()[4].querySelector('.quiz-comprobar').click();
  op(5, 2); op(6, 2); op(7, 1);
  await wait(400);
  return { marcador: mainContent.querySelector('.quiz-conteo').textContent,
           resumen: mainContent.querySelector('.quiz-resumen').innerText.replace(/\s+/g, ' ').trim() };
})()
"""

# Corrección tras la verificación: la pregunta 3 fallada dos veces (12.5 y
# 0.042), para ver el `retroFallo`; y los rótulos y los datos de las preguntas.
FALLA_Q3 = r"""
(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  mainContent.querySelector('.quiz-reiniciar').click(); await wait(500);
  const Q = () => [...mainContent.querySelectorAll('.quiz-pregunta')];
  const b3 = Q()[2], inp = b3.querySelector('input'), btn = b3.querySelector('.quiz-comprobar');
  inp.value = '12.5'; btn.click(); const tras1 = b3.querySelector('.quiz-retro').hidden;
  inp.value = '0.042'; btn.click(); await wait(300);
  return { tras1, clase: b3.querySelector('.quiz-retro').className,
           retro: b3.querySelector('.quiz-retro').innerText.replace(/\s+/g, ' ').trim().slice(-230),
           rotulos: [...mainContent.querySelectorAll('.quiz-tipo')].map(e => e.textContent),
           entradilla: mainContent.querySelector('.quiz > p').innerText.replace(/\s+/g, ' ').trim().slice(0, 200),
           datosQ6: [...Q()[5].querySelectorAll('.quiz-datos li')].map(li => li.innerText.replace(/\s+/g, ' ').trim().slice(0, 22)),
           opcionesQ6: [...Q()[5].querySelectorAll('.quiz-opcion')].map(b => b.innerText.replace(/\s+/g, ' ').trim()),
           opcionQ2a: Q()[1].querySelectorAll('.quiz-opcion')[0].innerText.replace(/\s+/g, ' ').trim() };
})()
"""

ABRE = r"""
(async () => {
  mainContent.querySelectorAll('.ejercicio-boton').forEach(b => { if (b.getAttribute('aria-expanded') !== 'true') b.click(); });
  await new Promise(r => setTimeout(r, 900));
  return { paneles: [...mainContent.querySelectorAll('.ejercicio-panel')].map(p => [p.id, p.hidden]),
           katexErr: mainContent.querySelectorAll('.katex-error').length,
           sinRender: [...mainContent.querySelectorAll('.exercise, .quiz')].map(e => (e.innerText.match(/\$[^$]{1,40}\$/g) || []).length) };
})()
"""


def desborde(ancho):
    return (r"(() => { const W = %d; const mc = mainContent; const fuera = [...mc.querySelectorAll('.quiz *, .exercise *')].filter(el => { const r = el.getBoundingClientRect(); if (!r.width || r.right <= W + 1) return false; if (el.closest('.katex')) return false; let p = el.parentElement; while (p && p !== mc) { const o = getComputedStyle(p).overflowX; if (o === 'auto' || o === 'scroll' || o === 'hidden') return false; p = p.parentElement; } return true; }).map(el => el.tagName + '.' + String(el.className).slice(0, 30)); "
            r"const tablas = [...mc.querySelectorAll('.quiz table, .exercise table')].map(t => { const c = t.closest('.tabla-desplazable') || t; return [c.scrollWidth, c.clientWidth]; }); "
            r"const pres = [...mc.querySelectorAll('.exercise pre')].map(p => [p.scrollWidth, p.clientWidth]); "
            r"return { docSw: document.documentElement.scrollWidth, W, fuera: fuera.slice(0, 12), nFuera: fuera.length, tablas, pres }; })()") % ancho


def tarea(ancho):
    s = f"-{ancho}.png"
    return {
        "url": URL + "#modulo-9", "ancho": ancho,
        "pasos": [
            {"js": "new Promise(r => setTimeout(() => r([currentModuleId, location.hash, mainContent.querySelectorAll('.quiz-pregunta').length, mainContent.querySelectorAll('.quiz-datos table').length]), 1500))"},
            {"sel": ".quiz", "archivo": "quiz-inicial" + s},
            {"js": QUIZ, "espera": 500},
            {"sel": ".quiz", "archivo": "quiz-recorrido" + s},
            {"js": desborde(ancho)},
            {"js": SOLO_Q2, "espera": 400},
            {"sel": ".quiz-resumen", "archivo": "quiz-resumen-solo-q2" + s},
            {"js": TODO_BIEN, "espera": 400},
            {"sel": ".quiz-resumen", "archivo": "quiz-resumen-impecable" + s},
            {"js": FALLA_Q3, "espera": 400},
            {"sel": ".quiz-pregunta", "idx": 2, "archivo": "q3-fallada" + s},
            {"sel": ".quiz-pregunta", "idx": 5, "archivo": "q6-nueva" + s},
            {"sel": ".quiz-pregunta", "idx": 1, "archivo": "q2-nueva" + s},
            {"sel": ".exercise", "archivo": "ejercicios-cerrados" + s},
            {"js": ABRE, "espera": 600},
            {"js": desborde(ancho)},
            {"sel": ".ejercicio-guiado", "idx": 0, "archivo": "ejercicio1-abierto" + s},
            {"sel": ".ejercicio-guiado", "idx": 1, "archivo": "ejercicio2-abierto" + s},
            {"sel": ".ejercicio-guiado", "idx": 2, "archivo": "ejercicio3-abierto" + s},
            {"js": "loadModule(2), new Promise(r => setTimeout(() => r(1), 1300))"},
            {"js": "(() => { const pre = mainContent.querySelector('.code-tab-panel[data-lang=\"r\"] pre'); pre.classList.remove('collapsed'); pre.classList.add('expanded'); return [pre.innerText.split('\\n').slice(-9), pre.scrollWidth, pre.clientWidth]; })()"},
            {"sel": ".code-tabs", "archivo": "m2-bloque" + s},
            {"js": "loadModule(7), new Promise(r => setTimeout(() => r(1), 1300))"},
            {"js": "[...mainContent.querySelectorAll('p')].filter(p => p.textContent.includes('Ejercicio 3')).map(p => p.textContent.replace(/\\s+/g, ' ').trim().slice(-170))"},
        ],
    }


print(json.dumps([tarea(1200), tarea(375)], ensure_ascii=False, indent=1))
