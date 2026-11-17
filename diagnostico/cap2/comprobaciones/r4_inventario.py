#!/usr/bin/env python3
"""
r4_inventario.py — rehace `bibliografia/contraste/cap2_inventario.tsv` contra el texto de hoy

El inventario del diagnóstico (136 filas, commit BASE) se hizo antes de las
rondas R1–R3. Este guion lo reescribe de modo que el `texto` de cada fila exista
literal en el capítulo actual (etiquetas fuera, blancos colapsados; de una
afirmación marcada se toma el tramo que va hasta su primera cita) y añade una columna, `r4`, que dice qué fue de ella:

  registrada: <veredicto>   tiene `data-afirma` y entrada en cap2.yml
  sin marcar: <por qué>     sigue en el capítulo y no se registró
Las filas del inventario viejo que ya no están se listan al final de la salida
(absorbidas por otra afirmación, o retiradas porque la frase ya no existe).

Uso:  python3 diagnostico/cap2/comprobaciones/r4_inventario.py
"""
import csv
import html
import io
import pathlib
import re
import subprocess
import sys

import yaml

RAIZ = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "precalculo"))
import audita_citas as A  # noqa: E402

BASE = "31bfbb6"
HTML = RAIZ / "Htmls_Series" / "capitulo-2-estacionariedad-acf-pacf.html"
TSV = RAIZ / "bibliografia" / "contraste" / "cap2_inventario.tsv"
REGISTRO = RAIZ / "bibliografia" / "contraste" / "cap2.yml"
JS = "vive en una cadena de JavaScript (la autoevaluación), donde el auditor no lee `data-afirma`"

# Filas viejas que salen del inventario: id → qué fue de ellas
FUERA = {
    "c2-m1-08": "absorbida en c2-m1-07", "c2-m2-04": "absorbida en c2-m2-03", "c2-m2-07": "absorbida en c2-m2-06",
    "c2-m3-02": "absorbida en c2-m3-01", "c2-m3-10": "absorbida en c2-m3-09", "c2-m3-11": "absorbida en c2-m3-09",
    "c2-m3-12": "absorbida en c2-m3-09", "c2-m3-14": "absorbida en c2-m3-13", "c2-m4-03": "absorbida en c2-m4-02",
    "c2-m5-02": "absorbida en c2-m5-01", "c2-m5-03": "absorbida en c2-m5-01",
    "c2-m5-06": "retirada: la frase ya no existe (R1)",
    "c2-m6-02": "absorbida en c2-m6-01; «las dos más usadas» se reescribió a «aquí se usan dos»",
    "c2-m6-03": "absorbida en c2-m6-01", "c2-m6-07": "absorbida en c2-m6-06",
    "c2-m6-08": "trasladada a c2-m4-14, donde ahora se presenta la TRM",
    "c2-m7-03": "absorbida en c2-m7-02", "c2-m7-04": "absorbida en c2-m7-02",
    "c2-m7-10": "absorbida en c2-m7-11 (la derivación del −0.5 es del capítulo)",
    "c2-m7-12": "absorbida en c2-m7-11", "c2-m8-06": "absorbida en c2-m8-05",
    "c2-m8-07": "retirada: la R1 quitó la tercera razón y la atribución a FPP3",
    "c2-m8-11": "retirada: la retroalimentación se reescribió en la R1",
    "c2-m9-07": "retirada: la varianza dejó de decidir (R1)",
    "c2-m9-09": "retirada: el umbral |λ| < 0.25 salió del pipeline (D6, R3)",
    "c2-m9-10": "retirada: el comentario se corrigió en la R1",
    "c2-m9-15": "retirada: la solución del ejercicio 1 se reescribió",
    "c2-m9-20": "retirada: «el ejemplo clásico» no tenía fuente; la pista remite ahora al Módulo 6",
    "c2-m9-21": "retirada: la frase ya no existe (R1 y R3)",
}

# Filas viejas que siguen sin marcar: id → (texto de hoy o None si no cambió, por qué)
SIN_MARCAR = {
    "c2-m0-01": ("Box, G. E. P., Jenkins, G. M., Reinsel, G. C., y Ljung, G. M. (2015).",
                 "ya no es texto tecleado: el pie lo escribe genera_referencias.py desde referencias.json"),
    "c2-m1-02": ("Si se observa una serie durante 1949–1954 y otra vez durante 1955–1960 y las dos ventanas se ven "
                 "estadísticamente iguales", "ilustración del capítulo de c2-m1-01"),
    "c2-m1-09": ("En este curso, «estacionaria» sin más quiere decir estacionaria en sentido débil.",
                 "convención del curso; es la misma de Hamilton p. 46 y Cryer y Chan p. 17"),
    "c2-m1-10": (None, "se sigue de la definición registrada en c2-m2-02"),
    "c2-m1-11": ("Caminata aleatoria No (2) y (3): la varianza crece con $t$", "la varianza está registrada en c2-m5-04"),
    "c2-m1-12": (None, "propia: lectura de la serie; la ficha de AirPassengers está en el registro del capítulo 1"),
    "c2-m1-14": (None, "observación del capítulo sobre las dos palabras (prioridad baja)"),
    "c2-m2-05": (None, "cubierta por c2-m2-06"),
    "c2-m3-03": ("Autocorrelación (autocorrelation function, ACF):",
                 "definición estándar en un recuadro de fórmulas; pasaje localizado (Cryer y Chan p. 16, ec. 2.3.1) "
                 "y sin registrar: segunda pasada"),
    "c2-m3-04": ("Con una muestra $y_1, \\ldots, y_T$ se estiman con",
                 "el estimador es la ec. 3.6.2 de Cryer y Chan p. 46, citada en c2-m3-05"),
    "c2-m3-08": (None, "valoración del capítulo (prioridad baja)"),
    "c2-m4-10": (None, "propia: valores de R sobre la caminata simulada"),
    "c2-m4-13": ("Con 24 rezagos, uno o dos picos fuera de la banda son lo normal por azar.",
                 "aritmética del capítulo (24 × 5 %)"),
    "c2-m5-08": ("deja una autocorrelación negativa en el rezago 1, que en teoría vale $-(1-\\phi)/2$",
                 "propia: la R1 la reescribió con la fórmula y las cifras del simulador"),
    "c2-m5-13": ("A ojo no se distinguen; las pruebas del Módulo 6 lo hacen con un número",
                 "remite al Módulo 6; el respaldo está en c2-m6-17"),
    "c2-m5-14": (None, JS + "; pasaje localizado: Cryer y Chan p. 57"),
    "c2-m6-12": ("Con series estacionales, ni el ADF ni el KPSS se aplican a la serie cruda",
                 "conclusión de los experimentos del módulo (c2-m6-11) y remisión a la regla del Módulo 7 (c2-m7-05)"),
    "c2-m6-13": ("La especificacion importa: para reproducir adf.test() de R hay que pedir",
                 "comentario de un bloque de código; propia, comprobada en la R1 (r1_python.py)"),
    "c2-m6-14": ("pero el P-VALOR no: R lo interpola en una tabla",
                 "comentario de código reescrito sin nombrar a Banerjee et al. ni a MacKinnon, que no se han leído; "
                 "lo dicen las ayudas de adf.test (tseries) y adfuller (statsmodels)"),
    "c2-m6-15": (None, JS),
    "c2-m7-13": (None, "propia: cifras del mismo párrafo; FPP3 §9.1 dice que tras la diferencia regular la "
                       "estacionalidad sigue"),
    "c2-m7-16": ("statsmodels no trae ndiffs/nsdiffs; estan en pmdarima",
                 "comentario de un bloque de código; sin pasaje: statsmodels no es obra de la biblioteca"),
    "c2-m7-17": ("Una tendencia sin quitar produce una ACF que decae lenta y casi linealmente desde",
                 JS + "; el respaldo es el de c2-m7-06"),
    "c2-m8-09": ("estima $\\lambda$ por máxima verosimilitud y da otro valor",
                 "software: lo dice el docstring de scipy, que no es obra de la biblioteca; comprobado en la R1"),
    "c2-m8-10": ("pero este capítulo recomienda usar el logaritmo", JS + "; ya no atribuye la recomendación a FPP3"),
    "c2-m8-12": ("Al contrario: necesita partir la serie en bloques estacionales, y aquí usa bloques de $m = 12$ meses.",
                 JS + "; depende de Guerrero (1993), como c2-m8-04"),
    "c2-m9-02": (None, "respaldo localizado en FPP3 §9.7 (primer paso del procedimiento), registrado en c2-m9-01"),
    "c2-m9-03": (None, "nombres de funciones (prioridad baja)"),
    "c2-m9-04": ("Si la dispersión crece con el nivel, transformar antes de diferenciar, y en la práctica con el "
                 "logaritmo (Módulo 8).", "resume c2-m8-01 y c2-m8-02 y la decisión D6 del curso"),
    "c2-m9-05": ("Si hay estacionalidad, aplicar $\\nabla_m$ antes que la diferencia regular: es la regla del orden "
                 "del Módulo 7.", "remite a c2-m7-05"),
    "c2-m9-06": ("Nunca sobre una serie estacional cruda: el ADF puede rechazar la raíz unitaria solo porque usa "
                 "menos rezagos que el periodo estacional (Módulo 6).", "propia: es c2-m6-11"),
    "c2-m9-08": (None, "consejo del capítulo (prioridad baja)"),
    "c2-m9-14": (None, "ficha de co2 en la ayuda de R, ya en la caché; sin registrar (prioridad baja)"),
    "c2-m9-16": ("Y ese $r_1 = -0.302$ no es sobrediferenciación", "propia: solución de un ejercicio, cifras de R"),
    "c2-m9-17": (None, "propia: resultado del Monte Carlo del ejercicio"),
    "c2-m9-18": ("La trampa: ndiffs sobre la serie CRUDA dice 0, porque la estacionalidad",
                 "comentario de un bloque de código; propia"),
    "c2-m9-19": ("menos rezagos fuera; Ljung–Box el único que no está pegado a cero",
                 "propia: cifras de R; la prueba se presenta en c2-m3-17"),
    "c2-m9-22": (None, "experiencia docente con asistentes de IA, sin fuente: decide Javier si se matiza"),
}

# Afirmaciones de hoy que el inventario viejo no tenía y que no se registraron
NUEVAS = [
    ("c2-m1-16", 1, "resultado", "alta",
     "Si la serie no lo es, los coeficientes estimados no significan lo que parecen, los errores estándar están mal "
     "y los pronósticos heredan el problema.",
     "sin pasaje leído que lo diga así; Hamilton trata las consecuencias en los caps. 15–18: segunda pasada"),
    ("c2-m3-18", 3, "resultado", "media",
     "Son demasiadas para el azar, incluso contando con que la media móvil con que se calcula ese residuo ya le "
     "deja algo de autocorrelación propia.",
     "el recuento es de R; que la media móvil induce autocorrelación en el residuo no tiene pasaje leído"),
    ("c2-m7-20", 7, "regla", "media",
     "Ese es el indicio: una autocorrelación negativa en el rezago 1 que se acerca a $-0.5$.",
     "propia: lo deduce el párrafo siguiente; se le quitó «más frecuente», que no tenía fuente"),
]


CORTE = "\x00"


class ConCortes(A.Lector):
    """El lector del auditor, que además deja una marca donde había una cita."""

    def handle_starttag(self, etiqueta, atributos):
        super().handle_starttag(etiqueta, atributos)
        if etiqueta == "cite" and "cita" in (dict(atributos).get("class") or "").split():
            actual = self._afirma_actual()
            if actual:
                self.afirmaciones[actual].texto += CORTE


def plano(texto: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", texto))).strip()


def main() -> int:
    crudo = HTML.read_text("utf-8")
    hoy = plano(crudo)
    lineas = crudo.split("\n")
    registro = {x["id"]: x for x in yaml.safe_load(REGISTRO.read_text("utf-8"))["afirmaciones"]}
    viejo = subprocess.run(["git", "show", f"{BASE}:bibliografia/contraste/cap2_inventario.tsv"], cwd=RAIZ,
                           capture_output=True, check=True).stdout.decode("utf-8")
    filas_viejas = {f["id"]: f for f in csv.DictReader(io.StringIO(viejo), delimiter="\t")}
    lector = ConCortes()
    lector.feed(crudo)
    lector.close()

    def linea_de(texto: str) -> int:
        inicio = texto[:40]
        for n, l in enumerate(lineas, start=1):
            if plano(l) and plano(l)[:25] in inicio and inicio[:25] in plano(l) + " ":
                return n
        clave = texto.split(" ")
        for k in (4, 3, 2):
            for n, l in enumerate(lineas, start=1):
                if " ".join(clave[:k]) in plano(l):
                    return n
        return 0

    salida, problemas = [], []
    campos = ["id", "modulo", "linea", "tipo", "texto", "fuente_candidata", "donde_buscar", "hallado", "prioridad", "r4"]

    def comprueba(ident: str, texto: str) -> None:
        if plano(texto) not in hoy:
            problemas.append(f"{ident}: el texto no está literal en el capítulo: {texto[:70]}")

    for ident, x in registro.items():
        a = lector.afirmaciones[ident]
        # El tramo literal: la prosa marcada hasta su primera cita (o, si ese
        # tramo es muy corto, el más largo de los que quedan entre citas).
        tramos = [re.sub(r"\s+", " ", t).strip() for t in a.texto.split(CORTE)]
        texto = tramos[0] if len(tramos[0]) >= 40 else max(tramos, key=len)
        if len(texto) > 260:
            texto = texto[:260].rsplit(" ", 1)[0]
        vieja = filas_viejas.get(ident, {})
        fuentes = x.get("fuentes") or []
        claves = "; ".join(dict.fromkeys(f["clave"] for f in fuentes))
        locs = "; ".join(dict.fromkeys(f"{f['clave'].split('2')[0].split('1')[0]} {f['loc']}" for f in fuentes))
        fila = {"id": ident, "modulo": A.RE_ID.match(ident).group(2), "linea": a.linea,
                "tipo": x["tipo"], "texto": texto,
                "fuente_candidata": claves or vieja.get("fuente_candidata", ""),
                "donde_buscar": vieja.get("donde_buscar", "afirmación nueva de la R4: ver la nota de cap2.yml"),
                "hallado": locs or ("no" if x["veredicto"] == "pendiente" else "propia"),
                "prioridad": vieja.get("prioridad", "media"),
                "r4": f"registrada: {x['veredicto']}"}
        comprueba(ident, texto)
        salida.append(fila)

    for ident, vieja in filas_viejas.items():
        if ident in registro:
            continue
        if ident in FUERA:
            continue
        if ident not in SIN_MARCAR:
            problemas.append(f"{ident}: fila vieja sin destino")
            continue
        nuevo, porque = SIN_MARCAR[ident]
        texto = nuevo or vieja["texto"]
        comprueba(ident, texto)
        salida.append({**vieja, "texto": texto, "linea": linea_de(plano(texto)), "r4": f"sin marcar: {porque}"})

    for ident, modulo, tipo, prioridad, texto, porque in NUEVAS:
        comprueba(ident, texto)
        salida.append({"id": ident, "modulo": modulo, "linea": linea_de(plano(texto)), "tipo": tipo, "texto": texto,
                       "fuente_candidata": "", "donde_buscar": "afirmación que el inventario del diagnóstico no tenía",
                       "hallado": "no", "prioridad": prioridad, "r4": f"sin marcar: {porque}"})

    sobran = (set(FUERA) | set(SIN_MARCAR)) - set(filas_viejas)
    if sobran:
        problemas.append(f"ids que no estaban en el inventario viejo: {sorted(sobran)}")
    if problemas:
        print("\n".join(problemas))
        print(f"FALLA  {len(problemas)} problemas: no se escribe")
        return 1

    salida.sort(key=lambda f: tuple(int(n) for n in A.RE_ID.match(f["id"]).groups()[1:]))
    with TSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=campos, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(salida)
    reg = sum(1 for f in salida if f["r4"].startswith("registrada"))
    print(f"OK  {TSV.relative_to(RAIZ)}: {len(salida)} filas · {reg} registradas · {len(salida) - reg} sin marcar")
    print(f"    del inventario viejo ({len(filas_viejas)} filas): {len(FUERA)} salen")
    for ident, que in FUERA.items():
        print(f"      {ident}  {que}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
