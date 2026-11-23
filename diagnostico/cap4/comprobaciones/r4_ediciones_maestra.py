#!/usr/bin/env python3
"""
r4_ediciones_maestra.py — R4 del cap. 4 · correcciones de la sesión maestra tras la
verificación independiente (`diagnostico/cap4/R4_verificacion_A.md` y `_B.md`)

Edita las dos tablas de la ronda, no el capítulo:
  · `r4_marcas.json` (en git): cambios de prosa y marcas;
  · `bibliografia/_local/herramientas/cap4/r4_entradas.json` (fuera de git): tipo,
    afirmación, veredicto, nota y orden o retirada de fuentes. Ningún literal nuevo:
    solo se reordenan o retiran fuentes que ya estaban comprobadas.
Orden de la cadena: r4_reune.py → ESTE → r4_marca.py → ensambla_cap4/5/6 → r4_registro.py.
Es reejecutable: cada cambio comprueba si ya está hecho. Un cambio de prosa se añade
a la entrada cuyo cambio previo dejó el texto que se reescribe (o a la propia, si el
texto es el de la base), para que se aplique en el orden correcto.

Uso:  python3 diagnostico/cap4/comprobaciones/r4_ediciones_maestra.py [--comprobar]
"""
import json
import pathlib
import re
import sys

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
MARCAS = AQUI / "r4_marcas.json"
ENTRADAS = RAIZ / "bibliografia" / "_local" / "herramientas" / "cap4" / "r4_entradas.json"
SE = "sesión maestra (verificación R4)"

# (id, texto viejo, texto nuevo, motivo) — prosa; y la marca de ese id, vieja → nueva
PROSA = [
    ("c4-m1-29", "los modelos ARMA solo describen series",
     "los modelos ARMA se plantean para series",
     "Verificador A (Medio): Cryer y Chan (p. 55) no dicen «solo», y el mismo módulo (c4-m1-08, Cryer y Chan "
     "p. 202) habla de un ARMA(p+d, q) no estacionario. La frase ya empieza por «El Capítulo 3 terminó…»: no "
     "se repite."),
    ("c4-m6-08", "porque cuenta también las variantes con deriva)",
     "porque incluye al propio ganador y dos variantes con deriva)",
     "Verificador A (Bajo): la cuenta del Módulo 7 es 1 ganador + 4 + 2 con deriva = 7; «cuenta también las "
     "variantes con deriva» no explica el siete."),
    ("c4-m2-62", "y mientras no se haga el ajuste puede <em>absorberlos</em>",
     "y si se dejan fuera del modelo, el ajuste puede <em>absorberlos</em>",
     "Verificador A (Bajo): «mientras no se haga el ajuste puede absorberlos» se leía mal."),
    ("c4-m2-11", "si es del MA, la serie se diferenció de más y hay que <strong>bajar</strong> $d$",
     "si es del MA, lo más probable es que la serie se haya diferenciado de más y convenga "
     "<strong>bajar</strong> $d$",
     "Verificador A (Bajo): los Módulos 1 y 3 lo tratan como indicio; las fuentes (Cryer y Chan pp. 126–127) "
     "van de la sobrediferenciación a la raíz, no al revés."),
    ("c4-m7-05", "El de menor AICc es el <em>modelo actual</em>.",
     "El de menor AICc es el <em>modelo actual</em>; el artículo original elegía por AIC.",
     "Verificador B (Medio): la cita a Hyndman y Khandakar (2008, p. 11) iba pegada a «AICc», y el artículo "
     "elige por AIC (como c3-m9-20 en el cap. 3). La cita del AICc pasa a FPP3 §9.7."),
    ("c4-m7-10", "su menor raíz AR tiene módulo $1.001$",
     "su menor raíz AR tiene módulo $1.0009$, por debajo de los dos umbrales",
     "Verificador B (Medio): redondeada a 1.001 coincidía con el umbral del artículo y se leía como que el "
     "artículo no lo rechazaría. El bloque de código imprime 1.0009 (min|raiz AR| = 1.0009)."),
    ("c4-m7-11", "la búsqueda usa además una verosimilitud aproximada (CSS)",
     "la búsqueda usa una verosimilitud aproximada (CSS) en lugar de la exacta",
     "Verificador B (Bajo): según la ayuda de auto.arima (§Arguments), con approximation = TRUE la estimación es "
     "por suma de cuadrados condicional, no además de la exacta."),
    ("c4-m8-10", "y aun así $d = 1$ sobra, como coinciden en señalar ADF, KPSS y Phillips–Perron",
     "y aun así $d = 1$ sobra: una serie con ciclos de longitud no fija, como la del lince, es estacionaria, "
     "y ADF, KPSS y Phillips–Perron coinciden en no diferenciar",
     "Verificador B (Medio): la cita de FPP3 §9.1 iba pegada a lo que dicen las pruebas, y FPP3 no corre "
     "ninguna; §9.1 dice que el lince es estacionario porque sus ciclos son aperiódicos."),
    ("c4-m10-15", "Es ruido blanco.", "Es compatible con ruido blanco.",
     "Verificador B (Bajo): una ACF muestral no demuestra ruido blanco; FPP3 §9.1 lee el caso análogo como "
     "idéntico al de un ruido blanco."),
    ("c4-m10-123", "<strong>Comprobar las raíces no es opcional.</strong>",
     "<strong>Comprobar las raíces no es opcional</strong>.",
     "Verificador B (Bajo): la cita quedaba detrás del punto."),
]

MARCA = {
    "c4-m1-29": ("[[c4-m1-29]]los modelos ARMA solo describen series",
                 "[[c4-m1-29]]los modelos ARMA se plantean para series"),
    "c4-m6-08": ("porque cuenta también las variantes con deriva)",
                 "porque incluye al propio ganador y dos variantes con deriva)"),
    "c4-m2-62": ("[[c4-m2-62]]mientras no se haga el ajuste puede",
                 "[[c4-m2-62]]si se dejan fuera del modelo, el ajuste puede"),
    "c4-m2-11": ("si es del MA, la serie\n              se diferenció de más y hay que <strong>bajar</strong> $d$",
                 "si es del MA, lo más probable es que la serie se haya diferenciado de más y convenga "
                 "<strong>bajar</strong> $d$"),
    "c4-m7-05": ("[[c4-m7-05]]El de menor AICc es el <em>modelo actual</em>{{K|p. 11}}[[/]]",
                 "[[c4-m7-05]]El de menor AICc es el <em>modelo actual</em>{{F|§9.7}}; el artículo original "
                 "elegía por AIC{{K|p. 11}}[[/]]"),
    "c4-m7-10": ("su menor raíz AR tiene módulo $1.001$[[/]]",
                 "su menor raíz AR tiene módulo $1.0009$, por debajo de los dos umbrales[[/]]"),
    "c4-m7-11": ("la búsqueda usa además una verosimilitud aproximada (CSS)",
                 "la búsqueda usa una verosimilitud aproximada (CSS) en lugar de la exacta"),
    "c4-m8-10": ("[[c4-m8-10]]aun así $d = 1$ sobra, como coinciden en señalar ADF, KPSS y Phillips–Perron{{F|§9.1}}[[/]]",
                 "[[c4-m8-10]]aun así $d = 1$ sobra: una serie con ciclos de longitud no fija, como la del lince, "
                 "es estacionaria{{F|§9.1}}, y ADF, KPSS y Phillips–Perron coinciden en no diferenciar[[/]]"),
    "c4-m10-15": ("Es ruido blanco. La tabla", "Es compatible con ruido blanco. La tabla"),
    "c4-m10-123": ("[[c4-m10-123]]<strong>Comprobar las raíces no es opcional.</strong>{{F|§9.7}}[[/]]",
                   "[[c4-m10-123]]<strong>Comprobar las raíces no es opcional</strong>{{F|§9.7}}[[/]]"),
}


def entradas_edits(e: dict) -> None:
    """Cambios del registro, por id. Cada uno deja la entrada igual si ya estaba hecho."""
    i = e["id"]
    if i == "c4-m1-29":
        e["nota"] = ("Cryer y Chan presentan los modelos ARMA en el capítulo de los modelos para series "
                     "estacionarias (como en c2-m1-15), y FPP3 §9.3 dice que normalmente se restringen los "
                     "autorregresivos a datos estacionarios: ninguna de las dos dice «solo», y la prosa ya no lo "
                     "dice (corrección de la sesión maestra tras la verificación). La segunda frase del párrafo "
                     "(el Capítulo 2 presentó la diferenciación como preprocesamiento) es una afirmación sobre el "
                     "propio material y queda fuera de la marca.")
    elif i == "c4-m6-08":
        e["afirmacion"] = ("Con d = 1 cuatro modelos más quedan a menos de 2 puntos de AICc del mejor; con "
                           "diferencias de ese tamaño el AICc apenas los distingue (el umbral de 2 puntos es una "
                           "convención del capítulo). El Módulo 7 cuenta siete porque incluye al ganador y dos "
                           "variantes con deriva.")
    elif i == "c4-m2-62":
        e["afirmacion"] = ("Si una intervención o un atípico se deja fuera del modelo, el ajuste de un ARIMA puede "
                           "absorberlo, por ejemplo subiendo d o inflando σ̂².")
    elif i == "c4-m2-11":
        e["afirmacion"] = ("Una raíz sobre el círculo unitario, o muy cerca, devuelve a la identificación, y si es "
                           "del MA lo más probable es que la serie se haya diferenciado de más y convenga bajar d.")
        e["nota"] = ("FPP3 §9.7 respalda que las raíces cerca del círculo unitario son un problema (inestabilidad "
                     "numérica, mal modelo para pronosticar). Cryer y Chan (pp. 126–127): sobrediferenciar deja una "
                     "raíz del MA en B = 1 y un modelo no invertible, con problemas de estimación; el capítulo usa la "
                     "implicación al revés (una raíz del MA en 1 indica que probablemente se diferenció de más), que "
                     "es una inferencia, y por eso la prosa la da como lo más probable y no como regla.")
    elif i == "c4-m7-05":
        e["afirmacion"] = ("De los modelos iniciales, el de menor AICc es el «modelo actual»; el artículo original "
                           "elegía por AIC.")
        e["veredicto"] = "respaldada"
        orden = {"hyndman2021forecasting": 0, "hyndman2008automatic": 1, "hyndman2026forecast": 2}
        e["fuentes"].sort(key=lambda f: orden[f["clave"]])
        e["nota"] = ("FPP3 §9.7 da el AICc como criterio de la búsqueda de ARIMA() (fable) y la ayuda de "
                     "auto.arima lo da como valor por defecto (ic = 'aicc', §Usage; comprobado con "
                     "formals(auto.arima)$ic); el artículo de 2008 (p. 11) elegía por AIC, y la prosa lo dice "
                     "(corrección de la sesión maestra tras la verificación: antes la cita al artículo iba pegada "
                     "a «AICc»).")
    elif i == "c4-m7-10":
        e["afirmacion"] = ("Con el ajuste que usa auto.arima (CSS-ML de Arima()), la menor raíz AR del "
                           "ARIMA(2,1,2) del Nilo tiene módulo 1.0009, por debajo de los dos umbrales (1.001 del "
                           "artículo y 1.01 del código).")
    elif i == "c4-m7-11":
        e["afirmacion"] = ("Si n > 150 o la frecuencia es mayor que 12, la opción approximation de auto.arima "
                           "vale TRUE: la búsqueda usa una verosimilitud aproximada (suma de cuadrados condicional) "
                           "en lugar de la exacta y reajusta al final el modelo ganador por máxima verosimilitud.")
    elif i == "c4-m8-10":
        e["afirmacion"] = ("Una serie con ciclos de longitud no fija, como la del lince, es estacionaria; sobre "
                           "log(lynx), las pruebas ADF, KPSS y Phillips–Perron coinciden en indicar cero "
                           "diferencias, aunque diferenciar reduzca la varianza.")
        e["fuentes"] = [f for f in e["fuentes"] if f["clave"] != "hamilton1994time"]
        nota = e.get("nota") or ""
        k = nota.find("Las tres pruebas")
        resto = nota[k:] if k >= 0 else ""
        resto = re.sub(r"\s*Hamilton \(p\. 506\).*$", "", resto, flags=re.S)
        e["nota"] = ("FPP3 §9.1 dice de la serie del lince que, aunque muestra ciclos fuertes, es estacionaria "
                     "porque los ciclos son aperiódicos; el capítulo usa log(lynx), de modo que la cita respalda "
                     "lo cualitativo y no la serie exacta. La cita va ahora pegada a esa parte y no a lo que dicen "
                     "las pruebas, que FPP3 no corre (corrección de la sesión maestra; se retiró la fuente de "
                     "Hamilton, que no respaldaba la frase). " + resto).strip()
    elif i == "c4-m10-15":
        e["afirmacion"] = ("Una ACF de la serie diferenciada con una sola barra aislada fuera de la banda es "
                           "compatible con ruido blanco, y entonces el modelo para la serie es una caminata "
                           "aleatoria: p = q = 0.")
        e["veredicto"] = "respaldada"
        e["nota"] = ("FPP3 §9.1 lee la serie diferenciada del precio de Google, con una sola autocorrelación fuera "
                     "de los límites y Ljung–Box que no rechaza, como parecida a la de un ruido blanco y concluye la "
                     "caminata aleatoria; la prosa dice ahora «compatible con ruido blanco» (antes «es ruido "
                     "blanco»). La fila de ruido blanco de la tabla de identificación es del propio Capítulo 3 "
                     "(c3-m5-11). Las cifras (ρ̂1 = 0.088, ρ̂8 = −0.190, banda 0.167) son de R y se reprodujeron.")
    elif i == "c4-m8-17":
        e["tipo"] = "resultado"
    elif i == "c4-m8-65":
        e["nota"] = re.sub(r"Repite lo que dicen c4-m3-11, c4-m10-01 y c4-m10-56 sobre KPSS y auto\.arima\.",
                           "Repite lo que dicen c4-m3-11 y c4-m10-01 sobre KPSS y auto.arima.", e.get("nota") or "")
    elif i == "c4-m10-21":
        e["nota"] = re.sub(r"\s*La frase principal del Módulo 7 \(c4-m7-09, a cargo del lector C\) debería decir "
                           r"lo mismo\.", " La frase principal del Módulo 7 (c4-m7-09) dice lo mismo.",
                           e.get("nota") or "")


def main() -> int:
    marcas = json.loads(MARCAS.read_text("utf-8"))
    dato = json.loads(ENTRADAS.read_text("utf-8"))
    por_id = {e["id"]: e for e in marcas}
    antes_m, antes_e = json.dumps(marcas, ensure_ascii=False), json.dumps(dato, ensure_ascii=False)
    plano = lambda s: " ".join(s.split())

    for ident, viejo, nuevo, motivo in PROSA:
        ya = any(plano(p[0]) == plano(viejo) and plano(p[1]) == plano(nuevo) for e in marcas for p in e["prosa"])
        if ya:
            continue
        # el cambio va tras el que dejó ese texto, si lo hubo
        duenio = next((e for e in marcas for p in e["prosa"] if plano(viejo) in plano(p[1])), por_id[ident])
        duenio["prosa"].append([viejo, nuevo, motivo + f" [{SE}]"])
    for ident, (viejo, nuevo) in MARCA.items():
        lista = por_id[ident]["marcas"]
        hechos = [n for n, m in enumerate(lista) if plano(nuevo) in plano(m)]
        if hechos:
            continue
        cand = [n for n, m in enumerate(lista) if plano(viejo) in plano(m)]
        if len(cand) != 1:
            sys.exit(f"ABORTA: la marca de {ident} no tiene el texto viejo exactamente una vez")
        n = cand[0]
        patron = re.compile(r"\s+".join(map(re.escape, viejo.split())))
        lista[n], k = patron.subn(nuevo.replace("\\", "\\\\"), lista[n])
        if k != 1:
            sys.exit(f"ABORTA: la marca de {ident} no se pudo sustituir")
    for e in dato["entradas"]:
        entradas_edits(e)

    cambia_m = json.dumps(marcas, ensure_ascii=False) != antes_m
    cambia_e = json.dumps(dato, ensure_ascii=False) != antes_e
    if "--comprobar" in sys.argv:
        print("OK, ya aplicadas" if not (cambia_m or cambia_e) else "FALTAN correcciones por aplicar")
        return 1 if (cambia_m or cambia_e) else 0
    MARCAS.write_text(json.dumps(marcas, ensure_ascii=False, indent=1) + "\n", "utf-8")
    ENTRADAS.write_text(json.dumps(dato, ensure_ascii=False, indent=1) + "\n", "utf-8")
    print(f"OK  {len(PROSA)} cambios de prosa y {len(MARCA)} marcas de la sesión maestra; "
          f"r4_marcas.json {'cambió' if cambia_m else 'igual'}, r4_entradas.json {'cambió' if cambia_e else 'igual'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
