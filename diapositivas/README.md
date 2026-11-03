# Diapositivas · Capítulos 4 y 5

`capitulo-4-modelos-arima.html` es la presentación (un HTML autocontenido). Teclas: `→` siguiente, `P` presentador,
`N` notas, `M` índice, `F` pantalla completa. Necesita internet al abrirla (fuentes, Prism y MathJax vienen de CDN).

Se genera con la skill `diapositivas-clase` (`skills_docencia`) a partir de `fuentes/capitulo_4.md`:

```bash
python3 <skill>/scripts/construir.py Htmls_Series/diapositivas/fuentes/capitulo_4.md
```

Cada cifra de la presentación se contrasta con su fuente (JSON de R, reejecución en R, statsmodels, documentación de R):

```bash
Rscript  Htmls_Series/diapositivas/fuentes/verificacion/verifica_directo_r46_cap4.R   # cifras exactas con el R de quien lo ejecute (R 4.6.0 al escribir esto)
python3  Htmls_Series/diapositivas/fuentes/verificacion/verifica_python_cap4.py      # necesita statsmodels
python3  Htmls_Series/diapositivas/fuentes/verificacion/verifica_cifras_cap4.py      # necesita scipy; escribe verificacion_cifras.md
```

`verifica_directo_cap4.R` (la reejecución en R 4.3.3 que dio `directo_cap4.json`) **no** se vuelve a lanzar con otro R: sus claims comprueban versiones y textos de ayuda de 4.3.3 y fallarían. Las cifras que se añadieron después salen del script `r46`, que guarda el entorno en su JSON. Las comprobaciones manuales contra libros (etiqueta `MAN`) van aparte en el informe.

El detalle, cifra por cifra, está en `fuentes/verificacion/verificacion_cifras.md`. Si se edita una cifra en la fuente,
el guion falla hasta que el claim correspondiente se actualice.

## Capítulo 5

`capitulo-5-sarima.html` (82 diapositivas, un divisor por módulo) cubre el capítulo en **dos clases**: la 1 va de los módulos 1 a 5 y termina en «Para la próxima clase»; la 2 empieza en el divisor «Clase 2 · Módulo 6». Misma convención que el 4: etiqueta en cada afirmación, fuente en cada cifra y `[SIN VERIFICAR]` donde no hubo con qué contrastar. Lleva tres gráficos animados (diferencias, satélites y pesos ψ), que salen del JSON del precálculo.

```bash
python3 Htmls_Series/diapositivas/fuentes/verificacion/genera_animados_cap5.py      # los tres .json animados, desde cap5_sarima.json
python3 Htmls_Series/diapositivas/fuentes/verificacion/recaptura_cap5.py           # vuelve a fotografiar m1-1, m6-1 y m7-1 con sus ajustes de lectura
python3 <skill>/scripts/construir.py Htmls_Series/diapositivas/fuentes/capitulo_5.md
python3 Htmls_Series/diapositivas/fuentes/verificacion/verifica_cifras_cap5.py      # escribe verificacion_cifras_cap5.md; ejecuta los bloques de R
```

Las fuentes del verificador se regeneran con `verifica_directo_cap5.R` (R; tarda unos minutos por el origen móvil), `verifica_python_cap5.py` (statsmodels) y `verifica_docs_cap5.R` (ayuda de R de las series, de `ets`, `nsdiffs` y `snaive`, y NEWS de forecast), todos desde la raíz del repositorio. Si se edita una cifra en la fuente, el verificador falla hasta que su claim se actualice; si un valor del JSON cae en un empate de redondeo, exige la fuente exacta.
