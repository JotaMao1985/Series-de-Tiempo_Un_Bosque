#!/usr/bin/env python3
"""
audita_preparcial.py — que cada cifra del preparcial enseñe lo que su ítem afirma

Material de Series de Tiempo 2026-II (20948).

`genera_preparcial.R` produce cifras correctas. Eso no basta: una cifra correcta
puede ilustrar **lo contrario** de lo que el ítem promete, y entonces el
preparcial enseña el error justo antes del parcial. Este auditor comprueba la
afirmación pedagógica, no la aritmética.

Ejemplo de por qué existe: el ítem 25 prometía que `ndiffs()` y `kpss.test()`
discrepan. Sobre la serie original discrepaban en el truncamiento pero llegaban
a la MISMA conclusión — el ítem no enseñaba nada. Se cambió la serie por una
donde de verdad se contradicen. Sin este guion, eso se publica.

Uso:  python3 precalculo/audita_preparcial.py
      (desde la carpeta `Series de tiempo/` o desde `precalculo/`)

Devuelve 1 si alguna afirmación no se sostiene.
"""
from __future__ import annotations

import json
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
DATOS = AQUI / "salidas" / "preparcial_datos.json"

fallos: list[str] = []

MESES = ["ene", "feb", "mar", "abr", "may", "jun",
         "jul", "ago", "sep", "oct", "nov", "dic"]


def check(cond: bool, msg: str, extra: str = "") -> None:
    print(("  OK   " if cond else "  FALLA") + f"  {msg}" + (f"   [{extra}]" if extra else ""))
    if not cond:
        fallos.append(msg)


def main() -> int:
    d = json.loads(DATOS.read_text(encoding="utf-8"))
    I = d["items"]

    print("— i01 · barajar destruye la autocorrelación, no la media ni la sd")
    check(abs(I["i01"]["media_igual"]) < 1e-9 and abs(I["i01"]["sd_igual"]) < 1e-9,
          "media y sd idénticas tras barajar")
    check(abs(I["i01"]["acf_original"]["acf"][0]) > 0.5
          and abs(I["i01"]["acf_barajada"]["acf"][0]) < I["i01"]["acf_barajada"]["banda"],
          "r1 alto en la serie, dentro de banda en la barajada",
          f"{I['i01']['acf_original']['acf'][0]} vs {I['i01']['acf_barajada']['acf'][0]}")

    print("— i04 · el gráfico de subseries enseña la tendencia DENTRO de cada mes")
    p = I["i04"]["pendiente_por_mes"]
    check(min(p) > 0, "los 12 meses tienen pendiente positiva", f"min={min(p)}")

    print("— i05 · el atípico lo absorbe el residuo, no la tendencia ni el estacional")
    r, t_, s = (abs(I["i05"][k]) for k in
                ("salto_en_residuo", "salto_en_tendencia", "salto_en_estacional"))
    check(r > 5 * max(t_, s), "el residuo domina", f"res={r} tend={t_} est={s}")

    print("— i07 · la 2×4 centrada pierde dos observaciones en cada extremo")
    check(I["i07"]["no_estimados_inicio"] == 2 and I["i07"]["no_estimados_final"] == 2,
          "pierde 2 y 2")

    print("— i08 · los índices estacionales clásicos suman cero")
    check(abs(I["i08"]["suman_cero"]) < 1e-9, "suman cero")

    print("— i09 · la malla de s.window discrimina de verdad")
    q = [(m["s_window"], m["acf_residuo_12"], m["queda_estacionalidad"]) for m in I["i09"]["malla"]]
    for sw, a, f in q:
        print(f"        s.window={str(sw):9} acf12={a:+.4f} deja estructura={f}")
    check(len({f for _, _, f in q}) == 2, "no todas las s.window dan el mismo veredicto")

    print("— i10 · sin robust, el atípico contamina el estacional de su mes")
    er = abs(I["i10"]["estacional_del_mes"]["robusto"])
    en = abs(I["i10"]["estacional_del_mes"]["no_robusto"])
    check(en > er, "no robusto contamina más", f"rob={er} no_rob={en}")

    print("— i11 · F_T casi igual, F_S muy distinta")
    check(I["i11"]["diferencia_FT"] < 0.03 and I["i11"]["diferencia_FS"] > 0.4,
          "el par cumple lo que el ítem promete",
          f"dFT={I['i11']['diferencia_FT']} dFS={I['i11']['diferencia_FS']}")

    print("— i15 · la PACF en el rezago 1 separa ruido blanco de AR(1)")
    check(abs(I["i15"]["pacf1_blanco"]) < 0.1 and I["i15"]["pacf1_ar"] > 0.15,
          "PACF1 separa", f"blanco={I['i15']['pacf1_blanco']} ar={I['i15']['pacf1_ar']}")

    print("— i16 · la caminata: varianza creciente y ADF que no rechaza")
    v = I["i16"]["varianza_por_tramo"]
    check(v[0] < v[1] < v[2], "la varianza crece tramo a tramo", str(v))
    check(I["i16"]["adf"]["p_valor"] > 0.10, "ADF no rechaza en niveles")
    check(I["i16"]["adf_diferenciada"]["p_valor"] < 0.05, "ADF rechaza tras diferenciar")

    print("— i18 · una ACF lenta NO prueba raíz unitaria")
    check(I["i18"]["acf_linea"][0] > 0.8 and I["i18"]["acf_caminata"][0] > 0.8,
          "las dos ACF decaen despacio")
    check(I["i18"]["linea_adf"]["p_valor"] < 0.05,
          "el ADF SÍ rechaza en la tendencia determinista")
    check(I["i18"]["caminata_adf"]["p_valor"] > 0.10, "el ADF NO rechaza en la caminata")

    print("— i19 · los picos del correlograma delatan el periodo 12")
    check(all(k in I["i19"]["picos"] for k in (12, 24)), "12 y 24 entre los picos",
          str(I["i19"]["picos"]))

    print("— i22 · r4 alto: la estacionalidad trimestral se ve en el rezago 4")
    check(I["i22"]["r4"] > 0.4 and I["i22"]["r4"] > I["i22"]["r1"], "r4 alto y mayor que r1",
          f"r1={I['i22']['r1']} r4={I['i22']['r4']}")

    print("— i23 · el KPSS de nivel caza lo que el ADF deja pasar")
    L = I["i23"]["linea"]
    check(L["adf"]["p_valor"] < 0.05 and L["kpss_nivel"]["p_valor"] < 0.05
          and L["kpss_tendencia"]["p_valor"] > 0.05,
          "ADF rechaza · KPSS nivel rechaza · KPSS tendencia no")

    print("— i24 · el ADF cambia de conclusión al crecer n (potencia)")
    check(I["i24"]["corto"]["adf"]["p_valor"] > 0.10
          and I["i24"]["largo"]["adf"]["p_valor"] < 0.05, "cambia de conclusión")

    print("— i25 · ndiffs() y kpss.test() se contradicen sobre el MISMO dato")
    check(bool(I["i25"]["se_contradicen"]), "se contradicen de verdad, no solo en el truncamiento",
          f"ndiffs={I['i25']['ndiffs']} kpss.test p={I['i25']['kpss_test_nivel']['p_valor']}")
    check(I["i25"]["truncamiento_urca"] != I["i25"]["truncamiento_kpss_test"],
          "y los truncamientos difieren",
          f"urca={I['i25']['truncamiento_urca']} kpss.test={I['i25']['truncamiento_kpss_test']}")

    print("— i26 · ur.df con tendencia rechaza, con deriva no")
    check(I["i26"]["rechaza_trend_5"] and not I["i26"]["rechaza_drift_5"],
          "elegir mal la especificación cambia la conclusión")

    print("— i27 · la varianza mínima señala d = 1")
    check(I["i27"]["minimo_en"] == I["i27"]["ndiffs"], "la tabla coincide con ndiffs()",
          f"tabla={I['i27']['minimo_en']} ndiffs={I['i27']['ndiffs']}")

    print("— i28 · las dos diferencias conmutan")
    check(bool(I["i28"]["conmutan"]) and I["i28"]["diferencia_maxima"] == 0,
          "diferencia máxima exactamente cero")

    print("— i29 · tras d = 1 queda estacionalidad en el rezago 12")
    check(abs(I["i29"]["acf12_despues"]) > I["i29"]["despues"]["banda"],
          "acf12 fuera de banda", f"acf12={I['i29']['acf12_despues']}")

    print("— i30 · el logaritmo estabiliza la varianza por tramos")
    vc, vl = I["i30"]["var_por_tramo_cruda"], I["i30"]["var_por_tramo_log"]
    check(max(vc) / min(vc) > 3 and max(vl) / min(vl) < 2, "la razón de varianzas cae",
          f"{max(vc)/min(vc):.1f}x -> {max(vl)/min(vl):.1f}x")

    print("— i31 · λ ≈ 0: la transformación es prácticamente el logaritmo")
    check(abs(I["i31"]["transformado"] - I["i31"]["log_del_valor"]) < 0.05,
          "coincide con log", f"λ={I['i31']['lambda']}")

    print("— i32 · tras diferenciar, el logaritmo falla en más de un tercio de los datos")
    check(I["i32"]["cuantos_NaN"] > 0.3 * len(I["i32"]["valores"]),
          "bastantes NaN", f"{I['i32']['cuantos_NaN']} NaN")

    print("\n— p-valores en el borde de la tabla (obligan a escribir «p < 0.01», no «p = 0.01»)")
    bordes = []

    def recorre(nodo, ruta=""):
        if isinstance(nodo, dict):
            if nodo.get("fuera_tabla") is True:
                bordes.append(f"{ruta} (p={nodo.get('p_valor')})")
            for k, v in nodo.items():
                recorre(v, f"{ruta}.{k}" if ruta else k)
        elif isinstance(nodo, list):
            for k, v in enumerate(nodo):
                recorre(v, f"{ruta}[{k}]")

    recorre(I)
    for b in bordes:
        print(f"        {b}")
    print(f"        -> {len(bordes)} p-valores fuera de tabla. P2 tiene que escribirlos con < o >.")


    # -----------------------------------------------------------------
    # Bloque E · lo que cada figura promete que se ve
    #
    # Estos ítems no están en el blueprint, así que las §3 y §4 de
    # `verifica_preparcial.R` —que recorren los 32— no los miran. Y son los
    # únicos del instrumento cuya respuesta correcta es una afirmación sobre
    # LO QUE LA FIGURA DEJA VER: si el dato cambia y deja de verse, el ítem
    # enseña lo contrario de lo que promete sin que nada falle. De ahí que se
    # comprueben aquí, una a una, las cuatro afirmaciones de cada uno.
    # -----------------------------------------------------------------
    S = d["series"]

    def por_ciclo(nombre):
        v, f = S[nombre]["valores"], S[nombre]["frecuencia"]
        return [v[a * f:(a + 1) * f] for a in range(len(v) // f)]

    print("— E02 · el gráfico de tiempo enseña tres cosas y esconde la cuarta")
    anios = por_ciclo("demanda")
    niveles = [sum(a) / len(a) for a in anios]
    amplitudes = [max(a) - min(a) for a in anios]
    check(niveles[-1] > niveles[0],
          "se ve: la serie crece a lo largo de la década",
          f"{niveles[0]:.1f} → {niveles[-1]:.1f}")
    check(sum(amplitudes[-3:]) / 3 > 1.3 * (sum(amplitudes[:3]) / 3),
          "se ve: los altibajos se ensanchan con el nivel",
          f"{sum(amplitudes[:3]) / 3:.1f} → {sum(amplitudes[-3:]) / 3:.1f}")
    picos = [a.index(max(a)) for a in anios]
    check(len(set(picos)) > 1,
          "NO se ve, y además es falso: el mes más alto no es el mismo todos los años",
          " ".join(f"{MESES[m]}×{picos.count(m)}" for m in sorted(set(picos))))

    print("— E03 · el atípico se encuentra por la forma, no por el nivel")
    ay = por_ciclo("demanda_atipico")
    plano = S["demanda_atipico"]["valores"]
    quiebres = [a[2] - (a[1] + a[3]) / 2 for a in ay]  # marzo menos sus vecinos
    raro = quiebres.index(max(quiebres))
    otros = [q for i, q in enumerate(quiebres) if i != raro]
    check(max(quiebres) > 2.5 * max(otros),
          "se ve: un solo año rompe la forma en marzo, y por goleada",
          f"{max(quiebres):.1f} frente a {max(otros):.1f} del siguiente")
    check(max(ay[raro]) < max(plano),
          "el atípico NO es el máximo de la serie: buscar el punto más alto falla",
          f"atípico {max(ay[raro]):.1f} · máximo {max(plano):.1f}")
    medias = [sum(a) / len(a) for a in ay]
    check(medias.index(max(medias)) != raro,
          "y tampoco es el año de media más alta: promediar también falla",
          f"media más alta en el año {medias.index(max(medias)) + 1}, atípico en el {raro + 1}")

    print("— E05 · la correlación alta que no significa relación lineal")
    B = d["bloque_e"]["dispersion"]
    check(B["correlacion"] > 0.75,
          "la correlación es alta de verdad: sin eso el ítem no engaña a nadie",
          f"r = {B['correlacion']}")
    lo, medio, hi = B["residuo_por_tercil"]
    check(lo > 0 and medio < 0 and hi > 0,
          "y la nube es una U alrededor de la recta: corta en los extremos, larga en el centro",
          f"residuo medio por tercil: {lo:+.2f} {medio:+.2f} {hi:+.2f}")
    check(min(lo, hi) > abs(medio) / 3,
          "el desvío de los extremos no es ruido: se ve al lado del central",
          f"extremos {lo:+.2f}/{hi:+.2f} contra centro {medio:+.2f}")

    print("— E06 · dos series sin relación que correlacionan por tener tendencia")
    P = d["bloque_e"]["espuria"]
    check(P["correlacion_niveles"] > 0.8,
          "los niveles correlacionan tanto que invitan a concluir algo",
          f"r = {P['correlacion_niveles']}")
    check(abs(P["correlacion_diferencias"]) < 0.15,
          "y las diferencias no correlacionan: no había nada detrás",
          f"r = {P['correlacion_diferencias']}")
    check(P["de_cada_cien"] > 50,
          "no es una casualidad rebuscada: pasa en más de la mitad de los pares",
          f"{P['pares_con_r_alto']} de {P['pares_probados']} pares independientes")

    # Las cifras que estos dos ítems IMPRIMEN tienen que ser las que R calculó.
    # Las §3 y §4 de `verifica_preparcial.R` hacen esto con los 32 del blueprint
    # y no miran el bloque E, así que aquí va su equivalente: si el generador
    # cambia un número y la prosa se queda con el viejo, esto lo dice.
    prosa_e = pathlib.Path(AQUI.parent / "Htmls_Series" / "preparcial-corte-1.html").read_text(
        encoding="utf-8")
    ini = prosa_e.index("AUTOEVALUACIONES['bloque-e']")
    prosa_e = prosa_e[ini:prosa_e.index("const SIMULACRO", ini)]
    citadas = {
        "la correlación de la dispersión": str(B["correlacion"]),
        # La prosa lo publica como porcentaje; el JSON lo guarda como fracción.
        "el R² de la recta, en porcentaje": f'{B["r2_lineal"] * 100:.1f}',
        "el residuo del tercil frío": f"{lo:+.2f}".lstrip("+"),
        "el residuo del tercil templado": f"{medio:.2f}",
        "el residuo del tercil caluroso": f"{hi:+.2f}".lstrip("+"),
        "la correlación espuria de niveles": str(P["correlacion_niveles"]),
        "la correlación espuria de diferencias": str(P["correlacion_diferencias"]),
        "los pares que pasan de 0.7": str(P["pares_con_r_alto"]),
        "los pares probados": str(P["pares_probados"]),
    }
    for que, valor in citadas.items():
        check(valor in prosa_e,
              f"la prosa del bloque E cita {que} tal como R lo calculó", valor)

    print()
    if fallos:
        print(f"AUDITORÍA: {len(fallos)} FALLOS")
        for f in fallos:
            print(f"  · {f}")
        return 1
    print("AUDITORÍA: todo en verde")
    return 0


if __name__ == "__main__":
    sys.exit(main())
