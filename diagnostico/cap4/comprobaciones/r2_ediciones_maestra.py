"""R2 del cap. 4 · correcciones de la sesión maestra tras la verificación independiente.

Se aplica DESPUÉS de r2_edita.py (el del redactor). Cada marcador debe aparecer una sola
vez; con --comprobar solo dice si el árbol ya las tiene. Atiende V1–V7 de
`diagnostico/cap4/R2_verificacion.md`. Después hay que reensamblar el cap. 4
(`python3 ensamblado/ensambla_cap4.py`); el armazón no cambia.
"""
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
JS = RAIZ / 'ensamblado/cap4/chapter.js'

SUST = [
    # V1 · las barras fuera de la banda, en el color de la serie; las de dentro, en gris.
    ("""    const UNIDAD_NILO = '10⁸ m³';
""",
     """    // Correlogramas de identificación (M4, M10): las barras que salen de la
    // banda van en el color de la serie y las de dentro en gris. Con el eje en
    // ±1, las barras de 0.21–0.24 del Nilo y el ρ̂₈ = −0.190 de la TRM quedan a
    // 1–3 px de la banda: el color dice cuáles salen sin medir píxeles, con el
    // mismo criterio que la cuenta de la lectura (|ρ̂| > banda).
    function resaltarFueraDeBanda(grafico, valores, b, color, nombre) {
      grafico.data.datasets[0].backgroundColor =
        valores.map(v => (Math.abs(v) > b ? color : COLORES_GRAFICO.gris));
      const etiquetas = grafico.options.plugins.legend.labels;
      const base = etiquetas.generateLabels;
      etiquetas.generateLabels = chart => base(chart).flatMap(item => (item.datasetIndex !== 0 ? [item] : [
        Object.assign({}, item, { text: `${nombre} fuera de la banda`, fillStyle: color, strokeStyle: color }),
        Object.assign({}, item, { text: 'Dentro', fillStyle: COLORES_GRAFICO.gris,
                                  strokeStyle: COLORES_GRAFICO.gris })
      ]));
      grafico.update('none');
      return grafico;
    }

    const UNIDAD_NILO = '10⁸ m³';
"""),
    ("""        gAcf = barrasCompactas(crearGraficoBarras(cAcf, REZAGOS, info.acf, {
          etiqueta: 'ACF muestral', color: COLORES_GRAFICO.primario,
          lineas: lineasBanda(info.n), tituloX: 'Rezago k'
        }), ALTOS_BARRAS);
        gPacf = barrasCompactas(crearGraficoBarras(cPacf, REZAGOS, info.pacf, {
          etiqueta: 'PACF muestral', color: COLORES_GRAFICO.terciario,
          lineas: lineasBanda(info.n), tituloX: 'Rezago k'
        }), ALTOS_BARRAS);
""",
     """        gAcf = resaltarFueraDeBanda(barrasCompactas(crearGraficoBarras(cAcf, REZAGOS, info.acf, {
          etiqueta: 'ACF muestral', color: COLORES_GRAFICO.primario,
          lineas: lineasBanda(info.n), tituloX: 'Rezago k'
        }), ALTOS_BARRAS), info.acf, info.banda, COLORES_GRAFICO.primario, 'ACF');
        gPacf = resaltarFueraDeBanda(barrasCompactas(crearGraficoBarras(cPacf, REZAGOS, info.pacf, {
          etiqueta: 'PACF muestral', color: COLORES_GRAFICO.terciario,
          lineas: lineasBanda(info.n), tituloX: 'Rezago k'
        }), ALTOS_BARRAS), info.pacf, info.banda, COLORES_GRAFICO.terciario, 'PACF');
"""),
    ("""        gAcf = barrasCompactas(crearGraficoBarras(cAcf, REZAGOS, info.acf, {
          etiqueta: 'ACF muestral', color: COLORES_GRAFICO.primario,
          lineas: lineasBanda(info.n), tituloX: 'Rezago k'
        }), ALTOS_ACF);
""",
     """        gAcf = resaltarFueraDeBanda(barrasCompactas(crearGraficoBarras(cAcf, REZAGOS, info.acf, {
          etiqueta: 'ACF muestral', color: COLORES_GRAFICO.primario,
          lineas: lineasBanda(info.n), tituloX: 'Rezago k'
        }), ALTOS_ACF), info.acf, info.banda, COLORES_GRAFICO.primario, 'ACF');
"""),
    # V5 · la banda del aria-label de la TRM, sin doble redondeo.
    ("""        ariaLienzo(cAcf, descripcionCorrelograma('ACF muestral', cual, info.acf, info.banda));

        const fuera = info.acf.filter(v => Math.abs(v) > info.banda).length;""",
     """        ariaLienzo(cAcf, descripcionCorrelograma('ACF muestral', cual, info.acf, banda(info.n)));

        const fuera = info.acf.filter(v => Math.abs(v) > info.banda).length;"""),
    # V2 · el ΔAICc se tumba hasta 460 px: entre 421 y ~455 los nueve rótulos se tocaban.
    ("""        const tumbado = gAicc.width < ESTRECHO;""",
     """        // Erguido, los nueve rótulos de siete caracteres necesitan ~460 px: entre
        // 421 y 455 se tocaban (hueco de −1 px a 421).
        const tumbado = gAicc.width < 460;"""),
    # V3 · el tooltip de una cruz no da un AICc inventado.
    ("""          ], { scales: escalas });
        lineaCompacta(grafico, ALTOS_TRAZA);
""",
     """          ], { scales: escalas });
        // La cruz se dibuja en TECHO, que no es un AICc: su tooltip dice solo «∞».
        const tt = grafico.options.plugins.tooltip;
        const etiquetaPorDefecto = Chart.defaults.plugins.tooltip.callbacks.label;
        tt.callbacks = Object.assign({}, tt.callbacks, {
          label(item) {
            return item.dataset.pointStyle === 'crossRot' ? 'AICc = ∞ (descartado)'
                                                          : etiquetaPorDefecto.call(this, item);
          }
        });
        lineaCompacta(grafico, ALTOS_TRAZA);
"""),
    # V4 · concordancia.
    ("""`${fmt(inter.psi[inter.psi.length - 1], 3)}; los ${h} primeros, en naranja, entran en σₕ`);""",
     """`${fmt(inter.psi[inter.psi.length - 1], 3)}; ` +
          (h === 1 ? 'el primero, en naranja, entra en σₕ' : `los ${h} primeros, en naranja, entran en σₕ`));"""),
    ("""        ariaLienzo(canvas, `Últimos ${VISIBLES} meses de la TRM y pronóstico de caminata aleatoria a ${H} meses: ` +""",
     """        ariaLienzo(canvas, `Últimos ${VISIBLES} meses de la TRM y pronóstico de caminata aleatoria a ${H} ` +
          `${H === 1 ? 'mes' : 'meses'}: ` +"""),
    ("""          { etiqueta: `σ a ${H} meses`, valor: `${fmt(sigma * Math.sqrt(H))} = σ̂·√${H}` },""",
     """          { etiqueta: `σ a ${H} ${H === 1 ? 'mes' : 'meses'}`, valor: `${fmt(sigma * Math.sqrt(H))} = σ̂·√${H}` },"""),
    # V6 · el año del escalón y el rango de β salen de los datos.
    ("""          b === 0 ? 'Sin escalón' : `Descenso de ${fmt(b, 0)} en 1899`,""",
     """          b === 0 ? 'Sin escalón' : `Descenso de ${fmt(b, 0)} en ${etiquetas[malla.posicion - 1]}`,"""),
    ("""          (b === 0 ? 'sin escalón' : `con un descenso de ${fmt(b, 0)} desde 1899`) +""",
     """          (b === 0 ? 'sin escalón' : `con un descenso de ${fmt(b, 0)} desde ${etiquetas[malla.posicion - 1]}`) +"""),
    ("""        ariaLienzo(cCurva, `Tasa de rechazo de KPSS al 5 % frente al tamaño del descenso, de 0 a 300: ` +""",
     """        ariaLienzo(cCurva, `Tasa de rechazo de KPSS al 5 % frente al tamaño del descenso, de ` +
          `${fmt(betas[0], 0)} a ${fmt(betas[betas.length - 1], 0)}: ` +"""),
    # V6 · el primer año de la realización simulada, del dato y no a mano.
    ("""      const etiquetas = aniosDesde(1871, malla.n, 0);""",
     """      const etiquetas = aniosDesde(SERIES_CAP4.nilo.inicio[0], malla.n, 0);"""),
    # V7 · σ está guardada a tres decimales: σ√h no puede darse a tres (778.013 frente a 778.015 de R).
    ("""          `y σ√h = ${fmt(inter.sigma * Math.sqrt(h), 3)}`);""",
     """          `y σ√h = ${fmt(inter.sigma * Math.sqrt(h), 1)}`);"""),
    ("""          { etiqueta: 'σ√h', valor: fmt(inter.sigma * Math.sqrt(h), 3) },""",
     """          // σ llega redondeada a tres decimales: σ√h, a uno (a h = 30, 778.0, como la prosa).
          { etiqueta: 'σ√h', valor: fmt(inter.sigma * Math.sqrt(h), 1) },"""),
]


def main():
    texto = JS.read_text(encoding='utf-8')
    comprobar = '--comprobar' in sys.argv
    faltan = 0
    for viejo, nuevo in SUST:
        n_viejo, n_nuevo = texto.count(viejo), texto.count(nuevo)
        if comprobar:
            if n_nuevo != 1:
                faltan += 1
                print('FALTA:', nuevo.strip().splitlines()[0][:90])
            continue
        if n_nuevo == 1 and n_viejo == 0:
            continue
        if n_viejo != 1:
            sys.exit(f'marcador no único ({n_viejo}): {viejo.strip().splitlines()[0][:90]}')
        texto = texto.replace(viejo, nuevo)
    if comprobar:
        print('OK' if not faltan else f'{faltan} sin aplicar')
        sys.exit(1 if faltan else 0)
    JS.write_text(texto, encoding='utf-8')
    print(f'{len(SUST)} sustituciones aplicadas')


if __name__ == '__main__':
    main()
