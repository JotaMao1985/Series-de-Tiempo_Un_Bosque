"""R3 · Módulo 8 (4.8 Diagnóstico y errores comunes).

D5: el escalón se llama por su nombre, el «modelo de dos medias» del Módulo 3; RMSE, MAE y naïve se
glosan donde la tabla fuera de muestra los usa por primera vez. Notación: «abanico» queda para la banda
del pronóstico que se abre con el horizonte; el intervalo de valores de la tabla es el «rango»."""


def registra(c, mover, entre, esc, T79, **_):
    c("M8 · el escalón es el modelo de dos medias del Módulo 3", T79,
      r'''La alternativa a la raíz unitaria es un escalón: un modelo con
        $d = 0$ y un solo regresor, que vale $1$ desde 1899,''',
      r'''La alternativa a la raíz unitaria es un escalón: el modelo de dos
        medias del Módulo 3, con $d = 0$ y un solo regresor, que vale $1$ desde 1899,''')
    c("M8 · RMSE, MAE y naïve, glosados donde se usan por primera vez", T79,
      r'''La comparación válida es fuera de muestra. Entrenando hasta 1950 y pronosticando los 20 años siguientes:</p>''',
      r'''La comparación válida es fuera de muestra. Se entrena hasta 1950, se pronostican los 20 años siguientes y se
          miden la raíz del error cuadrático medio (RMSE) y el error absoluto medio (MAE) de esos 20 pronósticos. El
          <em>naïve</em> repite siempre el último valor observado: es la caminata aleatoria.</p>''')
    c("M8 · «rango», no «abanico», para el intervalo de valores de la tabla", T79,
      r'''el abanico completo va de $123$ a $133$''',
      r'''el rango completo va de $123$ a $133$''')
