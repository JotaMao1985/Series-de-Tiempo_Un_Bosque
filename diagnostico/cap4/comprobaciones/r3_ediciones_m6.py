"""R3 · Módulo 6 (4.6 Estimar y comparar).

D5: la introducción del explorador deja de dar el resultado (cuántos modelos a menos de 2 puntos, cuántos
rechaza Ljung–Box, qué raíces tiene cada mejor): pide contarlos y mirarlos, y lo que se ve va a un
recuadro posterior a la actividad. Notación: el AICc cambia de T (Capítulo 3) a n y n*; se avisa."""


def registra(c, mover, entre, esc, T46, **_):
    c("M6 · el AICc con n y n*: se avisa que el Capítulo 3 escribía T", T46,
      r'''<p style="margin:0.6rem 0 0 0; font-size:0.9rem;">con $k = p + q + 1$ (los coeficientes ARMA más
          $\hat\sigma^2$; más uno si hay constante o deriva) y $n^{*} = n - d$ el <strong>número efectivo</strong> de
          observaciones.</p>''',
      r'''<p style="margin:0.6rem 0 0 0; font-size:0.9rem;">con $n$ el número de observaciones —lo que los
          Capítulos 2 y 3 llamaban $T$; aquí $T$ queda para el origen del pronóstico, el último dato, y vale
          $T = n$—, $k = p + q + 1$ (los coeficientes ARMA más $\hat\sigma^2$; más uno si hay constante o deriva) y
          $n^{*} = n - d$ el <strong>número efectivo</strong> de observaciones.</p>''')

    c("M6 · la introducción del explorador pide contar y mirar, no cuenta el resultado", T46,
      r'''Empieza en
          $d = 1$: cuatro modelos quedan a menos de 2 puntos del mejor, y con diferencias así el AICc apenas los
          distingue. Luego mira el correlograma de los residuales, cuyas barras se vuelven rojas cuando
          Ljung–Box(20) rechaza: descarta ocho modelos que se quedan cortos, pero todos los que quedan cerca del
          mejor pasan, así que filtra y no elige. Por último, mira las raíces de la
          lectura. El mejor de $d = 0$ tiene una raíz AR en $1.161$, cerca del círculo unitario, como si pidiera
          una diferencia; el mejor de $d = 1$, una raíz MA en $1.144$, como si quisiera deshacerla; y los buenos
          de $d = 2$ la tienen entre $1.000$ y $1.048$. Ningún $d$ sale limpio, y el Módulo 8 explica por
          qué.</p>''',
      r'''Empieza en
          $d = 1$ y cuenta cuántos modelos quedan a menos de 2 puntos del mejor. Luego mira el correlograma de los
          residuales, cuyas barras se vuelven rojas cuando Ljung–Box(20) rechaza, y busca qué modelos rechazan y si
          alguno de ellos está cerca del mejor. Por último, lee las raíces en la lectura, para el mejor de cada
          $d$: ¿alguna roza el círculo unitario?</p>''')

    c("M6 · recuadro tras el explorador: lo que enseña (antes iba en la introducción)", T46,
      r'''          <canvas aria-label="ΔAICc de los nueve modelos con el mismo orden de diferenciación" role="img"></canvas>
        </div>
      </div>

      <h3>Los mejores de cada $d$</h3>''',
      r'''          <canvas aria-label="ΔAICc de los nueve modelos con el mismo orden de diferenciación" role="img"></canvas>
        </div>
      </div>

      <div class="note">
        <p style="margin-bottom:0;"><strong>Lo que enseña el explorador.</strong> Con $d = 1$ cuatro modelos más
          quedan a menos de 2 puntos del mejor (el Módulo 7 contará siete, porque cuenta también las variantes con
          deriva), y con diferencias así el AICc apenas los distingue. Ljung–Box(20) rechaza en 8 de los 27 modelos,
          pero ninguno de los que quedan cerca del mejor de su $d$ está entre ellos, así que el correlograma filtra
          y no elige. Y las raíces: el mejor de $d = 0$ tiene una raíz AR en $1.161$, cerca del círculo unitario,
          como si pidiera una diferencia; el mejor de $d = 1$, una raíz MA en $1.144$, como si quisiera deshacerla;
          y los buenos de $d = 2$ la tienen entre $1.000$ y $1.048$. Ningún $d$ sale limpio, y el Módulo 8 explica
          por qué.</p>
      </div>

      <h3>Los mejores de cada $d$</h3>''')
