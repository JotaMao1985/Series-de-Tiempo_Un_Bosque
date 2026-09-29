# Diapositivas · Capítulo 4

`capitulo-4-modelos-arima.html` es la presentación (un HTML autocontenido). Teclas: `→` siguiente, `P` presentador,
`N` notas, `M` índice, `F` pantalla completa. Necesita internet al abrirla (fuentes, Prism y MathJax vienen de CDN).

Se genera con la skill `diapositivas-clase` (`skills_docencia`) a partir de `fuentes/capitulo_4.md`:

```bash
python3 <skill>/scripts/construir.py Htmls_Series/diapositivas/fuentes/capitulo_4.md
```

Cada cifra de la presentación se contrasta con su fuente (JSON de R, reejecución en R, statsmodels, documentación de R):

```bash
Rscript  Htmls_Series/diapositivas/fuentes/verificacion/verifica_directo_cap4.R
python3  Htmls_Series/diapositivas/fuentes/verificacion/verifica_python_cap4.py      # necesita statsmodels
python3  Htmls_Series/diapositivas/fuentes/verificacion/verifica_cifras_cap4.py      # necesita scipy; escribe verificacion_cifras.md
```

El detalle, cifra por cifra, está en `fuentes/verificacion/verificacion_cifras.md`. Si se edita una cifra en la fuente,
el guion falla hasta que el claim correspondiente se actualice.
