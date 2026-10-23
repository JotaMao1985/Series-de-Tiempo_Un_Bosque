"""datos.py — Todo lo que la guía del proyecto de pronóstico AFIRMA con una cifra.

Fechas, pesos, rúbrica, tope, longitudes mínimas y las reglas de la opción
conjunta viven aquí y en ningún otro sitio. El ensamblador
(`precalculo/ensambla_proyecto.py`) los imprime y el auditor
(`proyecto/audita_proyecto.py`) los vuelve a calcular por su cuenta. Es la
lección 13 de los talleres: una cifra tecleada en dos sitios se despega en uno.

Las decisiones —D1 a D14 y P1 a P3— están en `PLAN_Proyecto_Pronostico.md`.
Portado de `Diseno de experimentos/proyecto/datos.py`, que es el modelo.
Cambiar una (una fecha, el peso, el canal) es tocar UNA línea de este archivo,
reensamblar y volver a auditar.
"""
from __future__ import annotations

from datetime import date, timedelta

# ---------------------------------------------------------------------------
# El calendario del curso (P1, Javier, 21 oct 2026)
# ---------------------------------------------------------------------------
# La última semana de clases, la 16, va del lunes 16 al sábado 21 de noviembre.
# Vale la numeración de los planes de Series y de Espacial —la semana 10 es la
# del 5 al 10 de octubre—, NO la de Diseño, que llama 9 a esa semana y pone su
# 16 del 23 al 28 de noviembre. Las demás se cuentan seguidas desde el ancla.
SEMANA_10_EMPIEZA = date(2026, 10, 5)

# Festivos de Colombia que caen dentro del tramo del proyecto. Ningún hito puede
# caer en uno (el auditor lo comprueba): el 16 de noviembre es la razón de que el
# informe se entregue el domingo 15.
FESTIVOS = (date(2026, 11, 2), date(2026, 11, 16))

# Series tiene clase los martes y los miércoles.
DIAS_DE_CLASE = (1, 2)          # weekday(): lunes = 0


def lunes_de_la_semana(n: int) -> date:
    return SEMANA_10_EMPIEZA + timedelta(weeks=n - 10)


def semana_del_curso(d: date) -> int:
    return 10 + (d - SEMANA_10_EMPIEZA).days // 7


DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]


def frase_fecha(d: date) -> str:
    """«martes 27 de octubre». El día de la semana SALE de la fecha."""
    return f"{DIAS[d.weekday()]} {d.day} de {MESES[d.month - 1]}"


def frase_semana(n: int) -> str:
    """«del lunes 16 al sábado 21 de noviembre», para una semana del curso."""
    ini, fin = lunes_de_la_semana(n), lunes_de_la_semana(n) + timedelta(days=5)
    if ini.month == fin.month:
        return f"del {DIAS[0]} {ini.day} al {DIAS[5]} {fin.day} de {MESES[fin.month - 1]}"
    return f"del {frase_fecha(ini)} al {frase_fecha(fin)}"


# ---------------------------------------------------------------------------
# D3 · Los hitos. D8 · todas las entregas cierran a la misma hora
# ---------------------------------------------------------------------------
HORA_ENTREGA = "11:00"

HITOS = [
    dict(id="ficha", n=1, nombre="Ficha de la serie", fecha=date(2026, 10, 27), semana=13,
         entrega="Una ficha de unas 150 palabras: la serie, su fuente, su frecuencia, su "
                 "longitud y la pregunta"),
    dict(id="preregistro", n=2, nombre="Preregistro", fecha=date(2026, 11, 3), semana=14,
         entrega="El protocolo de evaluación congelado, antes de tocar el tramo de prueba, y "
                 "la descarga cruda"),
    dict(id="avance", n=3, nombre="Avance", fecha=date(2026, 11, 10), semana=15,
         entrega="La exploración, la identificación y los candidatos sobre el tramo de "
                 "entrenamiento, con las desviaciones del plan"),
    dict(id="informe", n=4, nombre="Informe y código", fecha=date(2026, 11, 15), semana=15,
         entrega="El informe, el código que lo produce y los datos"),
]
HITO = {h["id"]: h for h in HITOS}

# D4 · La exposición: en clase, en la semana 16. El día exacto se acuerda en
# clase, entre los dos días de clase de esa semana.
SEMANA_EXPOSICION = 16
DIAS_EXPOSICION = (date(2026, 11, 17), date(2026, 11, 18))
DIA_EXPOSICION = "el día exacto se acuerda en clase"
MINUTOS_EXPOSICION = 10
MINUTOS_PREGUNTAS = 5

# D1 · Equipos
MAX_INTEGRANTES = 2

# Topes de extensión de cada entrega
PALABRAS_FICHA = 150
PAGINAS_PREREGISTRO = 2
PAGINAS_INFORME = 10

# D8 · El canal: un repositorio PRIVADO de GitHub por equipo, con el docente
# como colaborador; cada hito es una release con su etiqueta. Cuenta la hora en
# que GitHub la publica, que el estudiante no controla, y la release congela lo
# entregado (el protocolo del preregistro, sobre todo).
CANAL_ENTREGA = "como una release del repositorio del proyecto en GitHub"
USUARIO_DOCENTE = "JotaMao1985"
NOMBRE_REPO = "proyecto-st-apellido1-apellido2"
ETIQUETA = {h["id"]: h["id"] for h in HITOS}     # la etiqueta de cada release

# D9 · Entrega tardía: por cada sesión de retraso se descuenta el 15 % de la
# nota ORIGINAL —no de lo que va quedando—. La primera sesión cuenta desde el
# cierre; cada clase que empiece sin la release suma otra.
DESCUENTO_POR_SESION = 15
EJEMPLO_RETRASO = 4.0
SESIONES_EJEMPLO = (0, 1, 2, 3)
TUTORIAS = (("martes y viernes", "11:00", "13:00"), ("jueves", "14:00", "16:00"))
DUDAS_EN = "en clase o en las horas de tutoría"

# ---------------------------------------------------------------------------
# D2 · Qué serie vale
# ---------------------------------------------------------------------------
# La longitud mínima sale del origen móvil: hacen falta T0 observaciones para
# el primer ajuste, h para el primer pronóstico y, con origenes_min(h) orígenes,
# origenes_min(h) − 1 más. T0 pide cuatro ciclos estacionales y nunca menos de 30.
CICLOS_ENTRENAMIENTO = 4
T0_MINIMO = 30

# Los orígenes crecen con h (Javier, 2026-10-23): el Diebold–Mariano a horizonte h
# necesita bastantes más orígenes que h. Con menos de h, `dm.test` ni corre, y el
# factor de Harvey–Leybourne–Newbold vale 0 con h − 1 o h orígenes y es pequeño
# cerca de ahí. Antes eran 10 fijos, y con h = 12 el informe no se podía renderizar.
ORIGENES_PISO = 10
ORIGENES_POR_H = 3


def origenes_min(h: int) -> int:
    return max(ORIGENES_PISO, ORIGENES_POR_H * h)


def t0_minimo(m: int) -> int:
    return max(CICLOS_ENTRENAMIENTO * m, T0_MINIMO)


def n_minimo(m: int, h: int) -> int:
    """n ≥ T0 + h + (origenes_min(h) − 1): con n así, `tsCV` da origenes_min(h) orígenes completos."""
    return t0_minimo(m) + h + origenes_min(h) - 1


# Los casos que la guía tabula: (frecuencia, m, h de ejemplo).
FRECUENCIAS = [
    ("Mensual", 12, 12),
    ("Trimestral", 4, 4),
    ("Semanal", 52, 13),
    ("Diaria, con estación semanal", 7, 14),
    ("Anual, sin estación", 1, 5),
]

# Las series que ya trabaja el material: el auditor comprueba que cada una
# aparece de verdad en algún documento de Htmls_Series/ (frente F).
SERIES_DEL_MATERIAL = ["AirPassengers", "USAccDeaths", "co2", "Nile", "lynx", "sunspot.year",
                       "BJsales", "TRM"]

# ---------------------------------------------------------------------------
# D11 · La opción conjunta con Estadística Espacial (P3, Javier, 21 oct 2026)
# ---------------------------------------------------------------------------
NOMBRE_REPO_CONJUNTO = "proyecto-st-ee-apellido1-apellido2"
PAGINAS_INFORME_CONJUNTO = 15
MINUTOS_EXPOSICION_CONJUNTA = 15
MINUTOS_PREGUNTAS_CONJUNTA = 10
PREGUNTAS_POR_MATERIA = 3            # al menos tantas de cada materia en la defensa
AREAS_MINIMAS = 25                   # propuesta de Series; la cifra final la fija Espacial
# Hasta cuándo se puede pasar de la conjunta al proyecto simple.
CAMBIO_HASTA = "preregistro"
# La pregunta (c), kriging del pronóstico, se retiró con P3: el kriging se ve en
# la semana 15 y el informe se entrega el domingo de esa semana.
PREGUNTAS_CONJUNTAS = ("a", "b")

# ---------------------------------------------------------------------------
# D6 · Pesos (P2, Javier, 21 oct 2026)
# ---------------------------------------------------------------------------
PROYECTO_DEL_CORTE = 50      # % del Corte III (el sílabo decía 20)
QUICES_DEL_CORTE = 50        # el resto: quices en clase; sin examen final ni Talleres 4 y 5
CORTE_III_DEL_CURSO = 40     # % del curso, como dice el sílabo
PROYECTO_DEL_CURSO = PROYECTO_DEL_CORTE * CORTE_III_DEL_CURSO / 100

NIVELES = [("insuficiente", 1.0), ("aceptable", 3.5), ("sólido", 5.0)]
VALOR_NIVEL = dict(NIVELES)

# La rúbrica. Cada criterio: id, nombre, puntos sobre 100, la exigencia del
# Módulo 12 del capítulo 6 que lo origina (D13; el frente G del auditor
# comprueba que las seis están) y un descriptor por nivel. `individual` marca
# lo que se califica persona por persona.
RUBRICA = [
    dict(hito="preregistro", titulo="Preregistro", criterios=[
        dict(id="P1", nombre="La serie y su fuente", puntos=4, exigencia="fuente",
             insuficiente="No se sabe de dónde sale la serie, o falta la fecha de descarga; no "
                          "cumple la longitud mínima, es una serie del material o no coincide con "
                          "la que se vuelve a descargar de la fuente citada.",
             aceptable="Fuente y fecha de descarga, pero sin la frecuencia, la unidad o lo que se "
                       "hará con los huecos y los cambios de metodología.",
             solido="Fuente citable con enlace, fecha de descarga, frecuencia, unidad, longitud "
                    "frente al mínimo y un plan para los huecos, escrito antes de usarlos."),
        dict(id="P2", nombre="El protocolo de evaluación", puntos=7, exigencia="protocolo",
             insuficiente="Falta el horizonte, la métrica o el método de referencia, o la "
                          "evaluación es una sola partición.",
             aceptable="Horizonte, métrica, referencia y origen móvil declarados, pero la métrica "
                       "no se justifica por el problema o no se dice la ventana.",
             solido="Horizonte, métrica justificada por el costo del error, T₀, número de "
                    "orígenes, ventana creciente o deslizante y referencia, todo decidido antes "
                    "de tocar el tramo de prueba."),
        dict(id="P3", nombre="Los candidatos y el plan de diagnóstico", puntos=4,
             exigencia="diagnostico",
             insuficiente="No hay candidatos, o el plan es «probar auto.arima».",
             aceptable="Dos o tres candidatos razonables, pero sin decir qué se mirará en los "
                       "residuos ni qué se hará si el diagnóstico falla.",
             solido="Candidatos justificados por lo que se espera de la serie, el diagnóstico "
                    "previsto con sus rezagos y un plan para cuando falle."),
    ]),
    dict(hito="avance", titulo="Avance", criterios=[
        dict(id="A1", nombre="La exploración", puntos=5, exigencia=None,
             insuficiente="Un gráfico de la serie sin lectura, o la exploración usa el tramo de "
                          "prueba.",
             aceptable="Descomposición, estacionariedad y transformación sobre el entrenamiento, "
                       "pero sin justificar el número de diferencias o la transformación.",
             solido="Descomposición leída, transformación y diferencias justificadas con "
                    "evidencia, y todo sobre el tramo de entrenamiento."),
        dict(id="A2", nombre="La identificación y las desviaciones", puntos=5, exigencia=None,
             insuficiente="No hay candidatos ajustados, o se esconden los cambios respecto al "
                          "preregistro.",
             aceptable="Candidatos ajustados con su ACF y su PACF, pero las desviaciones se "
                       "declaran sin su consecuencia.",
             solido="Candidatos identificados y ajustados sobre el entrenamiento, y cada "
                    "desviación del preregistro con su razón y su consecuencia."),
    ]),
    dict(hito="informe", titulo="Informe y código", criterios=[
        dict(id="I1", nombre="El modelo final y su justificación", puntos=6, exigencia=None,
             insuficiente="El modelo final no se justifica, o se eligió con el tramo de prueba.",
             aceptable="El modelo se justifica por un criterio de información, pero sin "
                       "comparar con los otros candidatos en el mismo terreno.",
             solido="El modelo se elige con lo preregistrado, y se dice qué tiene que los otros "
                    "candidatos no tienen."),
        dict(id="I2", nombre="Corrección técnica en R", puntos=8, exigencia="diagnostico",
             # Las raíces son las de φ(B) y θ(B), como en todo el curso: el caso
             # malo es dentro del círculo o sobre él (autoplot() dibuja las inversas).
             insuficiente="Errores que cambian el resultado: diferencias de más, un AICc "
                          "comparado entre órdenes de diferenciación distintos, raíces "
                          "dentro del círculo unitario, o sobre él, sin decirlo.",
             aceptable="El ajuste es correcto, con errores menores en la lectura de los "
                       "coeficientes o de las raíces.",
             solido="Estimación, órdenes, raíces y transformación correctos, y bien leídos."),
        dict(id="I3", nombre="El diagnóstico de los residuales", puntos=6, exigencia="diagnostico",
             insuficiente="No hay diagnóstico, o el Ljung–Box tiene los grados de libertad mal "
                          "puestos.",
             aceptable="Ljung–Box con sus grados de libertad y los gráficos, pero sin decir qué "
                       "se hizo con lo que se vio.",
             solido="Ljung–Box con sus grados de libertad, normalidad y raíces, con lo que se vio "
                    "interpretado y su consecuencia para los intervalos."),
        dict(id="I4", nombre="La evaluación por origen móvil", puntos=8, exigencia="origen",
             insuficiente="Una sola partición, o el modelo no se compara con la referencia.",
             aceptable="Origen móvil con la referencia y la métrica preregistradas, pero sin "
                       "contrastar la diferencia.",
             solido="Origen móvil como se preregistró, frente a la referencia, con Diebold–Mariano "
                    "y la lectura de lo que dice y lo que no dice."),
        dict(id="I5", nombre="Los intervalos y su cobertura", puntos=5, exigencia="cobertura",
             insuficiente="No se evalúan los intervalos, o solo a un nivel.",
             aceptable="Cobertura al 80 % y al 95 % por origen móvil, pero sin leer si falla ni "
                       "por qué.",
             solido="Cobertura a los dos niveles y Winkler, con la lectura de si el intervalo es "
                    "demasiado estrecho o demasiado ancho y qué lo explica."),
        dict(id="I6", nombre="Interpretación y conclusión", puntos=5, exigencia="referencia",
             insuficiente="La conclusión repite números, o esconde que el modelo no le gana a la "
                          "referencia.",
             aceptable="La conclusión responde la pregunta, pero sin decir para qué sirve el "
                       "pronóstico ni sus límites.",
             solido="La conclusión responde la pregunta en el lenguaje del problema, dice si el "
                    "modelo le gana a la referencia y qué no permite afirmar."),
        dict(id="I7", nombre="Fidelidad al preregistro y reproducibilidad", puntos=4,
             exigencia="fuente",
             insuficiente="El informe no se reproduce desde el repositorio, el protocolo cambió "
                          "sin decirlo o la descarga cruda no coincide con la que se vuelve a "
                          "descargar de la fuente citada.",
             aceptable="El informe se reproduce, pero el README no dice cómo, la serie cruda se "
                       "editó a mano o lo exploratorio va mezclado.",
             solido="Se clona, se sigue el README y el informe sale entero; la descarga cruda "
                    "está intacta y cada cambio al protocolo está declarado."),
        dict(id="I8", nombre="Declaración de uso de IA", puntos=3, exigencia="ia",
             insuficiente="No hay declaración, o dice «se usó IA» sin más.",
             aceptable="Dice qué herramienta y para qué, pero no qué se verificó.",
             solido="Dice qué herramienta, para qué, qué produjo y qué se verificó, con un "
                    "ejemplo que se puede comprobar en el repositorio."),
    ]),
    dict(hito="exposicion", titulo="Exposición", criterios=[
        dict(id="E1", nombre="La exposición", puntos=12, exigencia=None,
             insuficiente="Se pasa del tiempo, o no se entiende qué se pronosticó ni con qué "
                          "resultado.",
             aceptable="Cuenta el proyecto en el tiempo, pero sin decir qué salió distinto de lo "
                       "preregistrado.",
             solido="Cuenta en el tiempo la serie, el protocolo, lo que salió distinto, el "
                    "resultado frente a la referencia y sus límites."),
        dict(id="E2", nombre="Las preguntas", puntos=18, individual=True, exigencia=None,
             insuficiente="No sabe explicar una decisión de su propio proyecto.",
             aceptable="Explica lo que hizo, pero no por qué ni qué habría pasado de otra "
                       "manera.",
             solido="Explica lo que hizo, por qué, y qué habría cambiado con otra decisión."),
    ]),
]

# Las seis exigencias del Módulo 12 del capítulo 6, con el texto con que las
# nombra el capítulo. El frente G del auditor exige que cada una tenga al menos
# un criterio y que su texto siga en el capítulo publicado.
EXIGENCIAS_M12 = {
    "fuente": "Fuente y fecha de corte",
    "referencia": "Al menos un método de referencia",
    "protocolo": "La métrica elegida y por qué",
    "origen": "Evaluación por origen móvil",
    "cobertura": "Cobertura del intervalo",
    "diagnostico": "Diagnóstico del modelo final",
    "ia": "Sobre el uso de asistentes de IA",
}

# Lo que el tope multiplica: lo escrito (preregistro, avance e informe).
HITOS_ESCRITOS = ("preregistro", "avance", "informe")

# ---------------------------------------------------------------------------
# D7 · El tope: las preguntas acotan lo escrito
# ---------------------------------------------------------------------------
UMBRAL_TOPE = 3.0


def puntos_de(hito: str) -> int:
    return sum(c["puntos"] for b in RUBRICA if b["hito"] == hito for c in b["criterios"])


def factor_tope(preguntas: float) -> float:
    return min(1.0, preguntas / UMBRAL_TOPE)


def nota_proyecto(escrito: float, exposicion: float, preguntas: float,
                  con_tope: bool = True) -> float:
    """Nota del proyecto en la escala de 5, con lo escrito evaluado en bloque.

    `escrito` es la nota media de preregistro, avance e informe; `exposicion`,
    la de E1; `preguntas`, la de E2 de ESA persona. Redondeada a dos decimales
    aquí, para que lo impreso y lo calculado sean el mismo carácter."""
    f = factor_tope(preguntas) if con_tope else 1.0
    p_esc = sum(puntos_de(h) for h in HITOS_ESCRITOS)
    p_e1 = next(c["puntos"] for b in RUBRICA for c in b["criterios"] if c["id"] == "E1")
    p_e2 = next(c["puntos"] for b in RUBRICA for c in b["criterios"] if c["id"] == "E2")
    return round((p_esc * escrito * f + p_e1 * exposicion + p_e2 * preguntas) / 100, 2)


# Las filas de la tabla del tope: (situación, escrito, exposición, preguntas).
# Solo valores alcanzables: la exposición es UN criterio (1,0 · 3,5 · 5,0), las
# preguntas son la media de las respondidas (con una o dos: 1,0 · 2,25 · 3,0 ·
# 3,5 · 4,25 · 5,0) y lo escrito es una media de niveles ponderada por los
# puntos de sus trece criterios. El auditor comprueba las tres cosas.
EJEMPLOS_TOPE = [
    ("Proyecto impecable que no sabe defender", 5.0, 5.0, 1.0),
    ("Una pregunta aceptable y otra insuficiente: justo por debajo del umbral", 4.25, 3.5, 2.25),
    ("Proyecto flojo, pero lo defiende bien", 3.0, 3.5, 5.0),
]


def filas_tope() -> list[dict]:
    return [dict(situacion=s, escrito=e, exposicion=x, preguntas=q,
                 factor=round(factor_tope(q), 2),
                 sin_tope=nota_proyecto(e, x, q, con_tope=False),
                 con_tope=nota_proyecto(e, x, q))
            for s, e, x, q in EJEMPLOS_TOPE]


def nota_con_retraso(original: float, sesiones: int) -> float:
    """D9: el 15 % de la nota ORIGINAL por sesión, sin bajar de 0."""
    return round(max(0.0, original * (1 - sesiones * DESCUENTO_POR_SESION / 100)), 2)


def filas_retraso() -> list[dict]:
    return [dict(sesiones=s, descuento=s * DESCUENTO_POR_SESION,
                 nota=nota_con_retraso(EJEMPLO_RETRASO, s)) for s in SESIONES_EJEMPLO]


# ---------------------------------------------------------------------------
# Formato de las cifras (las mismas grafías que los talleres)
# ---------------------------------------------------------------------------
def nota(x: float) -> str:
    """Escala de 5 con coma decimal y SIEMPRE con decimal: «3,0», «4,5», «2,56»."""
    s = f"{x:.2f}"
    if s.endswith("0"):
        s = s[:-1]
    return s.replace(".", ",")


def divisor(x: float) -> str:
    """El mismo número dentro de una fórmula, con punto y sin decimal sobrante."""
    return f"{x:.2f}".rstrip("0").rstrip(".")


def pct(x: float) -> str:
    return f"{x:.2f}".rstrip("0").rstrip(".")


def tutorias_en() -> str:
    return " y ".join(f"<strong>{d} de {i} a {f}</strong>" for d, i, f in TUTORIAS)
