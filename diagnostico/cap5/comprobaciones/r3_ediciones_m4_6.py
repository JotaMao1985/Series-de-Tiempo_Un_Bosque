"""R3 · Módulos 4, 5 y 6 (5.4 Identificar los órdenes, 5.5 El airline, 5.6 Estimar y comparar).

D6: la cuenta de etapas del ciclo frente al del Capítulo 4 (cuatro etapas allí, cinco aquí: no son
«dos etapas insertadas»); «rejilla» se glosa en su primer uso, dentro del ciclo; la introducción del
explorador del M6 dice el estado inicial y pregunta en vez de dar el resultado; cada módulo cierra
apuntando al siguiente. T3.2: la banda es ±1.96/√n, como en el resto del capítulo."""


def registra(c, mover, entre, despues, esc, T46, ENS, **_):
    # ------------------------------------------------------------ M4
    c("M4 · la banda, ±1.96/√n como en todo el capítulo", T46,
      r'''banda de $\pm 2/\sqrt{n}$— la distinción''',
      r'''banda de $\pm 1.96/\sqrt{n}$— la distinción''')
    c("M4 · el ciclo frente al del Capítulo 4: cuatro etapas allí, cinco aquí", T46,
      r'''      <p>Identificar un SARIMA es el ciclo de Box–Jenkins del Capítulo 4 con dos etapas insertadas. El orden importa,
        y el diagrama recoge también <strong>qué hallazgo te devuelve a una etapa anterior</strong>, que es la parte
        que ninguna lista numerada sabe dibujar.</p>''',
      r'''      <p>Identificar un SARIMA sigue el ciclo de Box–Jenkins del Capítulo 4, que tenía cuatro etapas:
        identificación, estimación, diagnóstico y uso. Aquí la identificación se abre en cuatro —transformar, elegir
        $D$, elegir $d$ y leer los cuatro órdenes—, la estimación y el diagnóstico van juntos en la quinta, y el uso,
        el pronóstico, queda para después del ciclo (Módulo 7). El orden importa, y el diagrama recoge también
        <strong>qué hallazgo te devuelve a una etapa anterior</strong>, que es la parte que ninguna lista numerada
        sabe dibujar.</p>''')
    c("M4 · ciclo, etapa 5: «rejilla» se glosa en su primer uso", ENS,
      '''            ("Qué haces", "<p>Estimas por máxima verosimilitud y compruebas los residuales. La "
                          "rejilla de candidatos solo se ordena por AICc si <strong>todos "
                          "comparten $d$ y $D$</strong>.</p>"),''',
      '''            ("Qué haces", "<p>Estimas por máxima verosimilitud y compruebas los residuales. La "
                          "rejilla de candidatos —los modelos vecinos que se ajustan para "
                          "compararlos; el Módulo 6 la recorre— solo se ordena por AICc si "
                          "<strong>todos comparten $d$ y $D$</strong>.</p>"),''')
    c("M4 · cierre que apunta al Módulo 5", T46,
      '''      </div>
    </div>
  </template>

  <template id="module-5">''',
      '''      </div>

      <p>En la serie del capítulo, el protocolo lleva a $d = D = 1$ y a un pico negativo aislado en el rezago $1$ y
        otro en el $12$: $q = Q = 1$. Ese modelo tiene nombre propio, <em>airline</em>, y el Módulo 5 lo estudia
        antes de que el Módulo 7 recorra el ciclo paso a paso.</p>
    </div>
  </template>

  <template id="module-5">''')

    # ------------------------------------------------------------ M5
    c("M5 · cierre que apunta al Módulo 6", T46,
      '''          parece más al de pronosticar el julio siguiente que al de pronosticar el mes que viene.</p>
      </div>
    </div>
  </template>''',
      '''          parece más al de pronosticar el julio siguiente que al de pronosticar el mes que viene.</p>
      </div>

      <p>Que el <em>airline</em> sea el punto de partida no lo hace el mejor modelo de cada serie. El Módulo 6 lo
        estima junto a otros $35$ candidatos y enseña los dos hábitos que cambian al compararlos cuando hay
        estacionalidad.</p>
    </div>
  </template>''')

    # ------------------------------------------------------------ M6
    c("M6 · intro del explorador: estado inicial y una pregunta, sin el resultado", T46,
      r'''        <p class="simulador-intro">Los cuatro selectores recorren los $36$ modelos SARIMA($p,1,q$)($P,1,Q$)$_{12}$
          ajustados de verdad en R sobre $\log(\text{AirPassengers})$. El gráfico muestra la ACF de los residuales del
          modelo elegido con la banda al $95\,\%$. Pon $P=Q=0$ para ver qué pasa sin parte estacional, y fíjate en que
          el mínimo de AICc y el de BIC coinciden aquí —cosa que no siempre ocurre—.</p>''',
      r'''        <p class="simulador-intro">Los cuatro selectores recorren los $36$ modelos SARIMA($p,1,q$)($P,1,Q$)$_{12}$
          ajustados de verdad en R sobre $\log(\text{AirPassengers})$; se abre en el ($0,1,1$)($0,1,1$)$_{12}$. El
          gráfico muestra la ACF de los residuales del modelo elegido con la banda al $95\,\%$. Pon $P=Q=0$ para ver
          qué pasa sin parte estacional, y busca qué modelos quedan a menos de $2$ puntos de AICc del mejor: ¿alguno
          mejora el diagnóstico?</p>''')
    c("M6 · cierre que apunta al Módulo 7", T46,
      '''          <code>simple_differencing=True</code> las dos salidas vuelven a coincidir hasta el cuarto decimal.</p>
      </div>''',
      r'''          <code>simple_differencing=True</code> las dos salidas vuelven a coincidir hasta el cuarto decimal.</p>
      </div>

      <p>Con el modelo elegido y diagnosticado, falta recorrer el ciclo entero sobre una serie, de la transformación
        al pronóstico. El Módulo 7 lo hace con la misma $\log(\text{AirPassengers})$ y cierra el problema que dejó
        abierto el Capítulo 4.</p>''')
