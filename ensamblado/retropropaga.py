#!/usr/bin/env python3
"""
Retropropaga a los capítulos 1 y 2 lo que se añadió al construir el capítulo 3:

  1. el componente .derivacion (CSS + JS + llamada en loadModule),
  2. la opción `barrasExtra` de crearGraficoBarras,

y añade una caja de derivación real en cada capítulo, sobre álgebra que hasta
ahora se citaba sin desarrollar: Durbin-Levinson en el 2 y la fuerza F_T/F_S
en el 1.

Objetivo: que los cuatro archivos (plantilla + 3 capítulos) tengan exactamente
el mismo conjunto de reglas CSS y de funciones auxiliares.
"""
import pathlib
import re
import sys

BASE = pathlib.Path("/Users/javiermauriciosierra/Documents/Trabajo 2026/Bosque 2026/Series de tiempo")
SCRATCH = pathlib.Path("/private/tmp/claude-501/-Users-javiermauriciosierra-Documents-Trabajo-2026-Bosque-2026/831bcb00-26c3-43d4-8bd7-3dd033784b31/scratchpad")

CSS = (SCRATCH / "derivacion.css").read_text(encoding="utf-8").rstrip("\n")
JS = (SCRATCH / "derivacion.js").read_text(encoding="utf-8").rstrip("\n")

BARRAS_VIEJO = """      (opciones.lineas || []).forEach(linea => {
        datasets.push({
          type: 'line',"""

BARRAS_NUEVO = """      // Barras adicionales sobre el mismo eje (p. ej. la ACF muestral junto a
      // la teórica). Van antes que las rectas de referencia para que el orden
      // de los datasets sea estable: 0 = principal, 1..k = extra, luego líneas.
      (opciones.barrasExtra || []).forEach(extra => {
        datasets.push({
          type: 'bar',
          label: extra.etiqueta || '',
          data: extra.valores,
          backgroundColor: extra.color || COLORES_GRAFICO.secundario,
          borderWidth: 0,
          barPercentage: 0.4,
          categoryPercentage: 0.9,
          order: 2
        });
      });
      (opciones.lineas || []).forEach(linea => {
        datasets.push({
          type: 'line',"""

ANCLA_CSS = """    /* Enunciado de una pregunta con gráfico: mismo criterio de separación */
    .quiz-pregunta .quiz-enunciado + .quiz-grafico {
      margin-top: 0.9rem;
    }
  </style>"""

ANCLA_JS = """          if (!abierto) {
            if (typeof Prism !== 'undefined') Prism.highlightAllUnder(panel);
            katexEn(panel);
          }
        });
      });
    }
"""

# --- Derivación del capítulo 2: la recursión de Durbin-Levinson -------------
DER_CAP2 = r"""
      <div class="derivacion">
        <button type="button" class="derivacion-boton" aria-expanded="false" aria-controls="der-durbin-levinson">
          <i class="fas fa-square-root-variable" aria-hidden="true"></i>
          <span class="derivacion-texto">Ver el desarrollo paso a paso</span>
          <i class="fas fa-chevron-down" aria-hidden="true"></i>
        </button>
        <div class="derivacion-panel" id="der-durbin-levinson" hidden>
          <ol class="derivacion-pasos">
            <li>
              <p>Ajustar la regresión del rezago $k$ equivale a resolver el sistema de Yule–Walker de orden $k$, cuya
                matriz está formada por las propias autocorrelaciones:</p>
              $$\begin{pmatrix} 1 &amp; \rho_1 &amp; \cdots &amp; \rho_{k-1}\\ \rho_1 &amp; 1 &amp; \cdots &amp; \rho_{k-2}\\
                \vdots &amp; &amp; \ddots &amp; \vdots\\ \rho_{k-1} &amp; \rho_{k-2} &amp; \cdots &amp; 1\end{pmatrix}
                \begin{pmatrix}\phi_{k1}\\ \phi_{k2}\\ \vdots\\ \phi_{kk}\end{pmatrix}
                = \begin{pmatrix}\rho_1\\ \rho_2\\ \vdots\\ \rho_k\end{pmatrix}$$
              <p>Resolverlo por separado para cada $k$ costaría $O(k^3)$ operaciones… y hay que hacerlo para todos los
                rezagos del correlograma.</p>
            </li>
            <li>
              <p>La matriz no es una matriz cualquiera: es <strong>simétrica y de Toeplitz</strong> (constante a lo
                largo de cada diagonal). Eso permite pasar de la solución de orden $k-1$ a la de orden $k$ sin volver a
                empezar. El coeficiente nuevo es</p>
              $$\phi_{kk} = \frac{\rho_k - \sum_{j=1}^{k-1}\phi_{k-1,j}\,\rho_{k-j}}
                                  {1 - \sum_{j=1}^{k-1}\phi_{k-1,j}\,\rho_j}$$
            </li>
            <li>
              <p>Léelo como lo que es: en el numerador está la autocorrelación del rezago $k$ <strong>menos lo que ya
                  explican</strong> los rezagos anteriores. Justamente la parte "parcial" que buscábamos.</p>
            </li>
            <li>
              <p>Y los demás coeficientes se actualizan con una sola pasada:</p>
              $$\phi_{kj} = \phi_{k-1,j} - \phi_{kk}\,\phi_{k-1,k-j}, \qquad j = 1,\ldots,k-1$$
              <p>Arrancando en $\phi_{11} = \rho_1$, cada rezago cuesta $O(k)$ en vez de $O(k^3)$.</p>
            </li>
          </ol>
          <p class="derivacion-resultado">Esta es exactamente la recursión que implementan <code>pacf()</code> de R, el
            método <code>ywm</code> de statsmodels y la función <code>calcularPACF()</code> de los simuladores de esta
            página. Las tres coinciden hasta el redondeo con que se guardó el precálculo.</p>
        </div>
      </div>
"""

# --- Derivación del capítulo 1: de dónde sale la fuerza F_T -----------------
DER_CAP1 = r"""
      <div class="derivacion">
        <button type="button" class="derivacion-boton" aria-expanded="false" aria-controls="der-fuerza-ft">
          <i class="fas fa-square-root-variable" aria-hidden="true"></i>
          <span class="derivacion-texto">Ver el desarrollo paso a paso</span>
          <i class="fas fa-chevron-down" aria-hidden="true"></i>
        </button>
        <div class="derivacion-panel" id="der-fuerza-ft" hidden>
          <ol class="derivacion-pasos">
            <li>
              <p>Para medir cuánta tendencia hay, compara la serie <strong>sin estacionalidad</strong> con lo que queda
                si además le quitas la tendencia. Los dos objetos son</p>
              $$T_t + R_t \quad\text{(desestacionalizada)} \qquad\text{y}\qquad R_t \quad\text{(solo residuo)}$$
            </li>
            <li>
              <p>Si la tendencia fuera plana, quitarla no cambiaría nada y las dos varianzas coincidirían. Si fuera muy
                marcada, quitarla reduciría muchísimo la varianza. Esa razón es la medida natural:</p>
              $$\frac{\operatorname{Var}(R_t)}{\operatorname{Var}(T_t + R_t)}
                \;\in\; [0, 1] \;\;\text{aproximadamente}$$
            </li>
            <li>
              <p>Como interesa que <em>más tendencia</em> dé <em>número más alto</em>, se toma el complemento. Y como la
                razón puede pasar de 1 por el ruido de la estimación —las componentes STL no son exactamente
                incorreladas—, se trunca en cero:</p>
              $$F_T = \max\!\left(0,\; 1 - \frac{\operatorname{Var}(R_t)}{\operatorname{Var}(T_t + R_t)}\right)$$
            </li>
            <li>
              <p>$F_S$ es la misma construcción cambiando el papel de las componentes: se compara
                $\operatorname{Var}(S_t + R_t)$ con $\operatorname{Var}(R_t)$. Por eso las dos medidas se leen igual:
                $0$ es "esa componente no está" y valores cerca de $1$, "domina la serie".</p>
            </li>
          </ol>
          <p class="derivacion-resultado">La lectura práctica: $F_T$ y $F_S$ no son porcentajes de varianza explicada
            en sentido estricto, sino <strong>reducciones relativas de varianza</strong>. Sirven para comparar series
            entre sí —que es para lo que se usan como <em>features</em>— más que para interpretarse en términos
            absolutos.</p>
        </div>
      </div>
"""

TAREAS = [
    ("capitulo-1-componentes-descomposicion.html", DER_CAP1,
     "      <p>Ambas van de 0 (ausente) a 1 (muy marcada). Para <code>AirPassengers</code> resultan",
     "antes"),
    ("capitulo-2-estacionariedad-acf-pacf.html", DER_CAP2,
     "      <p>En la práctica no se corren $k$ regresiones: se obtiene la PACF a partir de la ACF con la "
     "<strong>recursión de\n          Durbin–Levinson</strong>, que es lo que hacen <code>pacf()</code> en R y "
     "el simulador de esta página.</p>\n",
     "despues"),
]

for nombre, derivacion, ancla, donde in TAREAS:
    ruta = BASE / "Htmls_Series" / nombre
    h = ruta.read_text(encoding="utf-8")
    n0 = len(h)

    def rep(viejo, nuevo, etq):
        global h
        if h.count(viejo) != 1:
            sys.exit(f"ABORTA [{nombre} / {etq}]: marcador aparece {h.count(viejo)} veces")
        h = h.replace(viejo, nuevo, 1)

    if ".derivacion-boton {" in h:
        print(f"{nombre}: ya tiene el componente, se omite")
        continue

    rep(ANCLA_CSS, ANCLA_CSS.replace("  </style>", "") + "\n" + CSS + "\n  </style>", "CSS")
    # crearGraficoBarras se introdujo en el capítulo 2: el 1 no la tiene porque
    # no dibuja ningún correlograma. Solo se extiende donde existe.
    tiene_barras = "function crearGraficoBarras" in h
    if tiene_barras:
        rep(BARRAS_VIEJO, BARRAS_NUEVO, "barrasExtra")
    rep("        iniciarEjerciciosGuiados();\n",
        "        iniciarEjerciciosGuiados();\n        iniciarDerivaciones();\n", "llamada")
    rep(ANCLA_JS, ANCLA_JS + "\n" + JS + "\n", "función iniciarDerivaciones")
    if donde == "antes":
        rep(ancla, derivacion.strip("\n") + "\n\n" + ancla, "caja de derivación")
    else:
        rep(ancla, ancla + derivacion.rstrip("\n") + "\n", "caja de derivación")

    # Comprobaciones
    obligatorios = [".derivacion-boton {", ".derivacion-pasos > li::before {",
                    "function iniciarDerivaciones()", "iniciarDerivaciones();",
                    'class="derivacion-boton"']
    if tiene_barras:
        obligatorios.append("barrasExtra")
    fallos = [m for m in obligatorios if m not in h]
    if fallos:
        sys.exit(f"ABORTA [{nombre}]: faltan {fallos}")

    ruta.write_text(h, encoding="utf-8")
    print(f"{nombre}: OK  ({n0:,} -> {len(h):,} bytes, +{len(h)-n0:,})")

print("\nRetropropagación terminada.")
