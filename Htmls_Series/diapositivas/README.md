# Diapositivas · Capítulo 4

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
