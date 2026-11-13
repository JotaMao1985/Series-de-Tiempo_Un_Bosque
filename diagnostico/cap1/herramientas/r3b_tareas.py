#!/usr/bin/env python3
"""R3b · genera las tareas de captura para r3_elemento.js (segunda mitad de la ronda R3).
Uso: python3 r3b_tareas.py > r3b_capturas.json ; node r3_elemento.js r3b_capturas.json"""
import json, sys
U = 'http://localhost:8731/capitulo-1-componentes-descomposicion.html'
SUF = {1200: 'escritorio', 800: '800', 375: 'movil'}
MED = ("(() => { const W = document.documentElement.clientWidth; const fuera = [...mainContent.querySelectorAll("
       "'.simulador, .simulador > *, .simulador canvas, fieldset, .grafico-pila, .grafico-par > *, ol.pasos-metodo, .derivacion')]"
       ".filter(el => { const r = el.getBoundingClientRect(); return r.width && r.right > W + 1; })"
       ".map(el => el.tagName + '.' + String(el.className).slice(0, 30));"
       " return { ancho: W, docSw: document.documentElement.scrollWidth, fuera: fuera.slice(0, 6),"
       " katexError: document.querySelectorAll('.katex-error').length }; })()")

def radio(sim, i):
    return {'js': "(() => { const r = document.querySelector('[data-simulador=\"%s\"]'); r.querySelectorAll('input[type=radio]')[%d].click();"
                  " return r.querySelector('.simulador-lectura').textContent.replace(/\\s+/g, ' ').trim(); })()" % (sim, i)}

def abre(panel):
    return {'js': "(() => { const b = document.querySelector('[aria-controls=\"%s\"]'); if (b.getAttribute('aria-expanded') !== 'true') b.click(); return b.getAttribute('aria-expanded'); })()" % panel,
            'espera': 500}

def tareas(anchos):
    t = []
    for a in anchos:
        s = SUF[a]
        stl = '[data-simulador="descomp-stl"]'
        t.append({'url': U, 'ancho': a, 'modulo': 6, 'pasos': [
            {'js': MED},
            {'sel': '.ciclo', 'archivo': f'm6-pasos-{s}.png'},
            {'sel': '[data-simulador="descomp-clasica"]', 'archivo': f'm6-descomp-clasica-{s}.png'},
            {'sel': '[data-simulador="escala-aditiva"]', 'archivo': f'm6-escala-aditiva-{s}.png'},
            {'sel': '.warning', 'archivo': f'm6-aviso-{s}.png'},
            {'sel': '#content-area', 'archivo': f'm6-pagina-{s}.png'},
        ]})
        t.append({'url': U, 'ancho': a, 'modulo': 7, 'pasos': [
            {'js': MED},
            {'sel': 'ol.pasos-metodo', 'archivo': f'm7-pasos-{s}.png'},
            {'sel': stl, 'archivo': f'm7-stl-partida-{s}.png'},
            radio('descomp-stl', 1), {'sel': stl, 'archivo': f'm7-stl-s11-{s}.png'},
            radio('descomp-stl', 0), radio('descomp-stl', 3), {'sel': stl, 'archivo': f'm7-stl-atipico-norob-{s}.png'},
            radio('descomp-stl', 5), {'sel': stl, 'archivo': f'm7-stl-atipico-rob-{s}.png'},
            radio('descomp-stl', 1), radio('descomp-stl', 4), {'sel': stl, 'archivo': f'm7-stl-s11-atipico-norob-{s}.png'},
            radio('descomp-stl', 2), radio('descomp-stl', 5), {'sel': stl, 'archivo': f'm7-stl-s11-orig-rob-{s}.png'},
            radio('descomp-stl', 0), radio('descomp-stl', 4),
            abre('der-robustez'), {'sel': '#der-robustez', 'archivo': f'm7-der-robustez-{s}.png'},
            abre('der-loess-ajuste'), {'sel': '#der-loess-ajuste', 'archivo': f'm7-der-loess-{s}.png'},
            {'js': MED},
            {'sel': '#content-area', 'archivo': f'm7-pagina-{s}.png'},
        ]})
        t.append({'url': U, 'ancho': a, 'modulo': 8, 'pasos': [
            {'js': MED},
            {'sel': '[data-simulador="desestacionalizada"]', 'archivo': f'm8-desestacionalizada-{s}.png'},
            {'sel': '#content-area table', 'archivo': f'm8-tabla-fuerzas-{s}.png'},
            {'sel': '#content-area', 'archivo': f'm8-pagina-{s}.png'},
        ]})
        t.append({'url': U, 'ancho': a, 'modulo': 9, 'pasos': [
            {'js': MED},
            {'sel': '#content-area', 'archivo': f'm9-pagina-{s}.png'},
        ]})
        for mod in (2, 4, 5):
            t.append({'url': U, 'ancho': a, 'modulo': mod, 'pasos': [{'js': MED}, {'sel': '#content-area', 'archivo': f'm{mod}-pagina-{s}.png'}]})
    # En el teléfono (escala 2) una página entera de 15 000 px no cabe en una captura: se corta.
    for tarea in t:
        if tarea['ancho'] < 500:
            for paso in tarea['pasos']:
                if paso.get('sel') == '#content-area':
                    paso['maxAlto'] = 7500
    return t

if __name__ == '__main__':
    anchos = [int(x) for x in sys.argv[1:]] or [1200, 800, 375]
    json.dump(tareas(anchos), sys.stdout, ensure_ascii=False, indent=1)
