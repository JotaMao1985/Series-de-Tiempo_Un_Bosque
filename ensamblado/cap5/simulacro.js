    // ================================================================
    // Simulacro del quiz (Módulo 12)
    //
    // Un ensayo del quiz del capítulo 5, que se rinde en Brightspace en clase:
    // doce preguntas, cincuenta minutos y la misma forma, con otra serie y
    // otros contextos. SE CORRIGE AL ENTREGAR: cada cifra se compara con su
    // banda de tolerancia y, si cae en un error frecuente conocido, lo
    // nombra; cada opción trae su retroalimentación y la nota final cuenta
    // los aciertos por bloque. La clave viaja en la página a propósito: el
    // simulacro no es ninguna de las tres versiones del quiz.
    //
    // Es el motor del módulo 7.13 de Diseño de Experimentos, copiado sin
    // cambiar una línea de lógica: el del Módulo 11 del capítulo 4 no
    // corrige, y este ya corrige las dos formas que tiene el quiz (cifra y
    // selección única). Con una sola versión no muestra el selector, y la
    // nota final nombra los bloques como los da el registro (`etapas`).
    //
    // Lo respondido, el reloj y si ya se corrigió viven en ESTADO_SIMULACRO,
    // fuera del renderizado: salir a otro módulo a consultar algo y volver no
    // borra nada, y el reloj sigue corriendo, como el del salón.
    //
    // Se engancha al registro SIMULADORES, que loadModule() ya recorre. El CSS
    // es el del componente .simulacro (componentes/simulacro.css) más las
    // piezas de la corrección (componentes/simulacro_correccion.css); los
    // instala ensambla_cap5.py y ensambla_cap6.py los recorta.
    //
    // SIMULACROS['id'] = { minutos, titulo, etapas, versiones: [{ numero, caso,
    // preguntas: [{ n, etapa, etiqueta, tipo, enunciado, ... }] }] } lo escribe
    // exporta_simulacro.py, en la carpeta del quiz, fuera del repositorio. Una
    // pregunta 'numero' trae { clave: { valor, tol, texto }, cuenta, rutas:
    // [{ valor, cifra, texto }] }; una 'opcion', { opciones: [{ texto, retro }],
    // correcta }.
    // ================================================================
    const SIMULACROS = {};
    const ESTADO_SIMULACRO = {};

    SIMULADORES['cap5-simulacro'] = function (raiz) {
      const id = raiz.dataset.simulador;
      const prep = SIMULACROS[id];
      if (!prep) {
        console.warn(`Simulacro no registrado: ${id}`);
        return [];
      }
      if (!ESTADO_SIMULACRO[id]) {
        ESTADO_SIMULACRO[id] = {
          actual: 0,
          versiones: prep.versiones.map(v => estadoNuevoSimulacro(prep, v))
        };
      }
      return pintarSimulacro(raiz, prep, ESTADO_SIMULACRO[id]);
    };

    function estadoNuevoSimulacro(prep, version) {
      return {
        respuestas: version.preguntas.map(pr => pr.tipo === 'numero' ? '' : []),
        finAt: null,
        restante: prep.minutos * 60,
        corregido: false,
        usados: 0
      };
    }

    // Lo que teclea el estudiante: punto o coma decimal y signo «-» o «−». Un
    // espacio DENTRO de la cifra es un separador de miles, y en el parcial no
    // se acepta: aquí tampoco. Con punto Y coma a la vez no se adivina cuál es
    // el de miles. En los dos casos se devuelve NaN y la corrección lo dice.
    function leeCifraSimulacro(s) {
      let t = String(s).trim().replace(/^[−–]/, '-').replace(/^\+/, '');
      if (t === '') return null;
      if (t.includes('.') && t.includes(',')) return NaN;
      t = t.replace(',', '.');
      if (!/^-?(\d+(\.\d*)?|\.\d+)$/.test(t)) return NaN;
      return parseFloat(t);
    }

    function pintarSimulacro(raiz, prep, global) {
      const selector = raiz.querySelector('.simulacro-versiones');
      const caso = raiz.querySelector('.simulacro-caso');
      const contenedor = raiz.querySelector('.simulacro-preguntas');
      const conteo = raiz.querySelector('.simulacro-conteo');
      const resumen = raiz.querySelector('.simulacro-resumen');
      const nota = raiz.querySelector('.simulacro-nota');
      const reloj = raiz.querySelector('.simulacro-reloj');
      const empezar = raiz.querySelector('.simulacro-empezar');
      const entregar = raiz.querySelector('.simulacro-entregar');
      const borrar = raiz.querySelector('.simulacro-borrar');
      let listas = [];
      let casillas = [];
      let cajas = [];
      let tic = null;

      const vacia = r => (Array.isArray(r) ? r.length === 0 : r.trim() === '');
      const version = () => prep.versiones[global.actual];
      const estado = () => global.versiones[global.actual];

      // --- El selector de versión ---------------------------------------
      selector.innerHTML = '';
      selector.hidden = prep.versiones.length < 2;
      const botonesVersion = prep.versiones.map((v, k) => {
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'simulacro-version';
        b.textContent = `Versión ${v.numero}`;
        b.onclick = () => {
          if (k === global.actual) return;
          para();
          global.actual = k;
          pinta();
        };
        selector.appendChild(b);
        return b;
      });

      // --- Las preguntas ------------------------------------------------
      function pinta() {
        const v = version(), est = estado();
        botonesVersion.forEach((b, k) => {
          b.classList.toggle('activa', k === global.actual);
          b.setAttribute('aria-pressed', k === global.actual ? 'true' : 'false');
        });
        caso.innerHTML = v.caso;
        contenedor.innerHTML = '';
        listas = []; casillas = []; cajas = [];

        v.preguntas.forEach((pr, i) => {
          const caja = document.createElement('div');
          caja.className = 'simulacro-pregunta';
          caja.innerHTML = `<span class="simulacro-etiqueta">${pr.n}. ${pr.etiqueta}</span>` +
            `<div class="simulacro-enunciado">${pr.enunciado}</div>`;
          if (pr.tipo === 'numero') {
            const fila = document.createElement('label');
            fila.className = 'simulacro-respuesta';
            fila.innerHTML = '<span>Respuesta</span>';
            const casilla = document.createElement('input');
            casilla.type = 'text';
            casilla.inputMode = 'decimal';
            casilla.autocomplete = 'off';
            casilla.spellcheck = false;
            casilla.className = 'simulacro-numero';
            casilla.setAttribute('aria-label', `Respuesta de la pregunta ${pr.n}`);
            casilla.value = est.respuestas[i];
            casilla.oninput = () => {
              est.respuestas[i] = casilla.value;
              pintaConteo();
            };
            fila.appendChild(casilla);
            caja.appendChild(fila);
            casillas[i] = casilla;
          } else {
            const lista = document.createElement('div');
            lista.className = 'simulacro-opciones';
            lista.setAttribute('role', 'group');
            lista.setAttribute('aria-label', `Opciones de la pregunta ${pr.n}`);
            pr.opciones.forEach((op, j) => {
              const b = document.createElement('button');
              b.type = 'button';
              b.className = 'simulacro-opcion';
              b.innerHTML = `<span class="simulacro-letra">${LETRAS[j]})</span><span>${op.texto}</span>`;
              b.onclick = () => {
                if (est.corregido) return;
                est.respuestas[i] = est.respuestas[i].includes(j) ? [] : [j];
                pintaOpciones(i);
                pintaConteo();
              };
              lista.appendChild(b);
            });
            caja.appendChild(lista);
            listas[i] = lista;
          }
          contenedor.appendChild(caja);
          cajas[i] = caja;
          if (listas[i]) pintaOpciones(i);
        });

        if (est.corregido) corrige();
        else nota.textContent = '';
        if (est.finAt !== null) arranca();
        pintaReloj();
        pintaConteo();
      }

      function pintaOpciones(i) {
        const est = estado();
        listas[i].querySelectorAll('.simulacro-opcion').forEach((o, j) => {
          const marcada = est.respuestas[i].includes(j);
          o.classList.toggle('marcada', marcada);
          o.setAttribute('aria-pressed', marcada ? 'true' : 'false');
        });
      }

      // Lo tecleado entra en el resumen como TEXTO, nunca como HTML: es lo
      // único de la página que escribe el estudiante.
      function pintaConteo() {
        const v = version(), est = estado();
        const hechas = est.respuestas.filter(r => !vacia(r)).length;
        conteo.textContent = `${hechas} de ${v.preguntas.length} respondidas`;
        resumen.textContent = 'Tus respuestas: ';
        v.preguntas.forEach((pr, i) => {
          const r = est.respuestas[i];
          const b = document.createElement('b');
          b.textContent = `${pr.n}: ` + (vacia(r) ? '—'
            : Array.isArray(r) ? r.map(j => LETRAS[j]).join('') : r.trim());
          if (i) resumen.appendChild(document.createTextNode(' · '));
          resumen.appendChild(b);
        });
        resumen.appendChild(document.createTextNode('.'));
        entregar.disabled = est.corregido;
        entregar.textContent = est.corregido ? 'Corregido' : 'Entregar y corregir';
      }

      // --- La corrección -------------------------------------------------
      // Devuelve 'acierto', 'fallo' o 'vacia', y escribe la retroalimentación
      // debajo de la pregunta. Lo que tecleó el estudiante entra como texto.
      function veredicto(pr, r, caja) {
        const retro = document.createElement('div');
        retro.className = 'simulacro-retro';
        const cabeza = document.createElement('p');
        cabeza.className = 'simulacro-veredicto';
        retro.appendChild(cabeza);
        let resultado;

        if (pr.tipo === 'numero') {
          const x = leeCifraSimulacro(r);
          if (x === null) {
            resultado = 'vacia';
            cabeza.textContent = `Sin responder. La respuesta es ${pr.clave.texto}.`;
          } else if (Number.isNaN(x)) {
            resultado = 'fallo';
            const crudo = String(r).trim();
            const miles = /^[−–-]?\d{1,3}([.,\s  ]\d{3})+$/.test(crudo);
            const seguido = leeCifraSimulacro(crudo.replace(/[.,\s  ]/g, ''));
            cabeza.textContent = miles
              ? `«${crudo}» lleva separador de miles, y en el quiz no se acepta: escribe la cifra seguida. ` +
                (Math.abs(seguido - pr.clave.valor) <= pr.clave.tol ? 'Sin el separador, sería la correcta. ' : '') +
                `La respuesta es ${pr.clave.texto}.`
              : `«${crudo}» no se lee como una cifra. La respuesta es ${pr.clave.texto}.`;
          } else if (Math.abs(x - pr.clave.valor) <= pr.clave.tol) {
            resultado = 'acierto';
            cabeza.textContent = `Correcto: ${String(r).trim()}. La respuesta es ${pr.clave.texto}.`;
          } else {
            resultado = 'fallo';
            cabeza.textContent = `Tu respuesta, ${String(r).trim()}, no es la correcta. La respuesta es ${pr.clave.texto}.`;
            const ruta = pr.rutas.find(rt => Math.abs(x - rt.valor) <= pr.clave.tol);
            const miles = Math.abs(x * 1000 - pr.clave.valor) <= pr.clave.tol;
            if (ruta || miles) {
              // El texto de la ruta es del registro, no del estudiante: lleva
              // subíndices y entra como HTML.
              const aviso = document.createElement('p');
              aviso.className = 'simulacro-aviso';
              aviso.innerHTML = ruta
                ? `Tu cifra coincide con un error frecuente: ${ruta.texto}.`
                : 'Tu cifra es la clave dividida entre mil: parece que usaste un separador de miles.';
              retro.appendChild(aviso);
            }
          }
          const cuenta = document.createElement('p');
          cuenta.innerHTML = pr.cuenta;
          retro.appendChild(cuenta);
          if (pr.rutas.length) {
            const errores = document.createElement('p');
            errores.className = 'simulacro-errores';
            errores.innerHTML = 'Errores frecuentes: ' +
              pr.rutas.map(rt => `si obtuviste ${rt.cifra}, ${rt.texto}`).join('; ') + '.';
            retro.appendChild(errores);
          }
        } else {
          const elegida = r.length ? r[0] : null;
          if (elegida === null) {
            resultado = 'vacia';
            cabeza.textContent = `Sin responder. La correcta es la ${LETRAS[pr.correcta]}).`;
          } else if (elegida === pr.correcta) {
            resultado = 'acierto';
            cabeza.textContent = `Correcto: la ${LETRAS[pr.correcta]}).`;
          } else {
            resultado = 'fallo';
            cabeza.textContent = `Marcaste la ${LETRAS[elegida]}); la correcta es la ${LETRAS[pr.correcta]}).`;
            const suya = document.createElement('p');
            suya.innerHTML = `<b>${LETRAS[elegida]})</b> ${pr.opciones[elegida].retro}`;
            retro.appendChild(suya);
          }
          const buena = document.createElement('p');
          buena.innerHTML = `<b>${LETRAS[pr.correcta]})</b> ${pr.opciones[pr.correcta].retro}`;
          retro.appendChild(buena);
        }
        caja.appendChild(retro);
        return resultado;
      }

      function corrige() {
        const v = version(), est = estado();
        const cuenta = { acierto: 0, fallo: 0, vacia: 0 };
        const porEtapa = {};
        v.preguntas.forEach((pr, i) => {
          const caja = cajas[i];
          caja.querySelectorAll('.simulacro-retro').forEach(n => n.remove());
          const res = veredicto(pr, est.respuestas[i], caja);
          cuenta[res] += 1;
          caja.classList.remove('acierto', 'fallo', 'vacia');
          caja.classList.add(res);
          porEtapa[pr.etapa] = porEtapa[pr.etapa] || [0, 0];
          porEtapa[pr.etapa][1] += 1;
          if (res === 'acierto') porEtapa[pr.etapa][0] += 1;
          if (casillas[i]) casillas[i].disabled = true;
          if (listas[i]) {
            listas[i].querySelectorAll('.simulacro-opcion').forEach((o, j) => {
              o.disabled = true;
              o.classList.toggle('correcta', j === pr.correcta);
              o.classList.toggle('equivocada', est.respuestas[i].includes(j) && j !== pr.correcta);
            });
          }
        });
        const usados = est.usados;
        const nombreEtapa = e => (prep.etapas && prep.etapas[e]) || `etapa ${e}`;
        const etapas = Object.keys(porEtapa).sort()
          .map(e => `${nombreEtapa(e)}: ${porEtapa[e][0]} de ${porEtapa[e][1]}`).join(' · ');
        const quien = prep.versiones.length < 2 ? 'Simulacro' : `Versión ${v.numero}`;
        nota.textContent = `${quien}: ${cuenta.acierto} de ${v.preguntas.length} correctas ` +
          `(${etapas})` + (cuenta.vacia ? `, ${cuenta.vacia} sin responder` : '') +
          `. Tiempo usado: ${Math.floor(usados / 60)} min ${String(usados % 60).padStart(2, '0')} s.`;
      }

      entregar.onclick = () => {
        const est = estado();
        if (est.corregido) return;
        if (est.finAt !== null) {
          est.restante = segundos();
          est.finAt = null;
        }
        para();
        est.usados = prep.minutos * 60 - est.restante;
        est.corregido = true;
        corrige();
        pintaReloj();
        pintaConteo();
        nota.scrollIntoView({ block: 'nearest' });
      };

      // --- El reloj ------------------------------------------------------
      // `finAt` es la hora en que se acaba y manda mientras corre;
      // `restante` solo guarda los segundos cuando está pausado.
      function para() {
        if (tic !== null) { clearInterval(tic); tic = null; }
      }
      function segundos() {
        const est = estado();
        return est.finAt === null
          ? est.restante
          : Math.max(0, Math.round((est.finAt - Date.now()) / 1000));
      }
      function pintaReloj() {
        const est = estado();
        const s = segundos();
        reloj.textContent = `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
        reloj.classList.toggle('acabado', s === 0);
        empezar.disabled = est.corregido;
        empezar.textContent = est.corregido ? 'Reloj detenido'
          : est.finAt !== null ? 'Pausar'
          : (s === prep.minutos * 60 ? `Empezar los ${prep.minutos} minutos` : 'Seguir');
      }
      function arranca() {
        para();
        tic = setInterval(() => {
          const est = estado();
          if (segundos() === 0) {
            est.finAt = null;
            est.restante = 0;
            para();
          }
          pintaReloj();
        }, 250);
      }
      empezar.onclick = () => {
        const est = estado();
        if (est.corregido) return;
        if (est.finAt !== null) {          // corriendo: se pausa
          est.restante = segundos();
          est.finAt = null;
          para();
        } else {
          if (est.restante === 0) est.restante = prep.minutos * 60;
          est.finAt = Date.now() + est.restante * 1000;
          arranca();
        }
        pintaReloj();
      };
      borrar.onclick = () => {
        para();
        global.versiones[global.actual] = estadoNuevoSimulacro(prep, version());
        pinta();
      };

      pinta();
      // Lo que devuelve un simulador son los objetos que destruirSimuladores()
      // apaga al cambiar de módulo. Aquí no hay gráficos: lo que hay que
      // apagar es el intervalo del reloj.
      return [{ destroy: para }];
    }

    // [inicio · simulacro del quiz]
    // ================================================================
    // Simulacro del quiz (Módulo 12) · CON clave: se corrige al entregar
    //
    // NO SE EDITA A MANO: lo escribe exporta_simulacro.py, en la carpeta
    // del quiz (fuera del repositorio), desde el mismo generador que arma
    // los paquetes de Brightspace. La clave viaja aquí a propósito (D4 de
    // PLAN_Quiz_Cap5.md): no es ninguna de las tres versiones del quiz, y
    // ninguna de sus claves cae en la banda de las de ellas.
    // ================================================================
    SIMULACROS['cap5-simulacro'] = {
      "minutos": 50,
      "titulo": "Simulacro del quiz del capítulo 5",
      "etapas": {
        "1": "preguntas 1 a 9",
        "2": "preguntas 10 a 12"
      },
      "versiones": [
        {
          "numero": 0,
          "caso": "<h3>Vehículos en un peaje — simulacro</h3>\n<p>Una vía intermunicipal registra los <b>vehículos que pasan cada mes por un peaje, en miles de vehículos</b>, de enero de 2011 a diciembre de 2025: N = 180 meses.\nSe analiza su logaritmo natural, log y<sub>t</sub>, con el recorrido del capítulo: diferenciar, comparar candidatos,\ndiagnosticar y pronosticar.</p>\n<p>Las preguntas 1 a 7 siguen el análisis de esta serie, la 8 y la 9 miran otras dos series de la\nconcesión y las 10 a 12 son de otros contextos. Aquí están todas en la misma página; ninguna necesita la respuesta de\notra. Escriba cada cifra con los decimales que pida su pregunta, con punto o con coma como separador decimal y <b>sin\nseparar los miles</b>. En el quiz de Brightspace se ve una pregunta por página, no se puede volver a la anterior y cada\npregunta trae los datos que necesita.</p>",
          "preguntas": [
            {
              "n": 1,
              "id": "S1",
              "etapa": 1,
              "etiqueta": "cap. 5 · mód. 5.1, 5.3 y 5.7 · Las diferencias",
              "tipo": "opcion",
              "enunciado": "<p>La tabla resume cinco formas de diferenciar log y<sub>t</sub>: con d diferencias regulares y D estacionales, los n datos que quedan, su varianza y sus autocorrelaciones muestrales en los rezagos 1 y 12:</p><table style=\"border-collapse:collapse;margin:6px 0 12px 0;font-size:95%\"><thead><tr><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">d</th><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">D</th><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">n</th><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">Varianza</th><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">ρ̂<sub>1</sub></th><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">ρ̂<sub>12</sub></th></tr></thead><tbody><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">180</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0.067411</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0.6361</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0.7258</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">179</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0.047480</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">−0.2743</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0.8797</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">168</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0.014465</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0.8154</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0.1208</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">167</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0.005259</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">−0.2783</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">−0.4782</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">2</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">166</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0.013502</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">−0.6012</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">−0.4812</td></tr></tbody></table><p>¿Con qué diferencias se sigue el análisis?</p>",
              "opciones": [
                {
                  "texto": "d = 0 y D = 1",
                  "retro": "Con solo ∇<sub>12</sub> queda ρ̂<sub>1</sub> = 0.8154: la serie conserva su tendencia. Primero D y después d, sobre la serie ya diferenciada estacionalmente, y ahí hace falta d = 1 (módulos 5.3 y 5.8)."
                },
                {
                  "texto": "d = 1 y D = 0",
                  "retro": "Con solo ∇, ρ̂<sub>12</sub> = 0.8797 sigue alto: la diferencia regular no toca la estacionalidad, y la varianza (0.047480) apenas baja (módulo 5.3)."
                },
                {
                  "texto": "d = 1 y D = 1",
                  "retro": "Sin diferenciar, ρ̂<sub>12</sub> = 0.7258: la estación pide ∇<sub>12</sub>, y se decide primero. Tras ∇<sub>12</sub> queda ρ̂<sub>1</sub> = 0.8154, una tendencia sin resolver, así que hace falta además ∇. Con las dos, la varianza es la menor de la tabla (0.005259) y las barras de 1 y 12 quedan negativas, la huella de dos diferencias justas (módulos 5.3 y 5.7)."
                },
                {
                  "texto": "d = 2 y D = 1",
                  "retro": "Una diferencia regular de más sube la varianza de 0.005259 a 0.013502: es sobrediferenciar, y al estimar dejaría un θ̂ pegado a −1 (módulo 5.3)."
                }
              ],
              "correcta": 2
            },
            {
              "n": 2,
              "id": "N2",
              "etapa": 1,
              "etiqueta": "cap. 5 · mód. 5.3 · Una diferencia doble a mano",
              "tipo": "numero",
              "enunciado": "<p>Los vehículos de cuatro meses, en miles de vehículos, fueron:</p><table style=\"border-collapse:collapse;margin:6px 0 12px 0;font-size:95%\"><thead><tr><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">Mes</th><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">y<sub>t</sub> (miles de vehículos)</th></tr></thead><tbody><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">agosto de 2024</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">496.19</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">septiembre de 2024</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">445.82</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">agosto de 2025</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">506.77</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">septiembre de 2025</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">434.25</td></tr></tbody></table><p>Calcule ∇∇<sub>12</sub> log y<sub>t</sub> en septiembre de 2025, con el logaritmo natural y al menos cuatro decimales en cada logaritmo. Responda con cuatro decimales; si es negativo, con su signo.</p>",
              "clave": {
                "valor": -0.0474,
                "tol": 0.000379,
                "texto": "−0.0474"
              },
              "cuenta": "∇∇<sub>12</sub> log y<sub>t</sub> = log y<sub>t</sub> − log y<sub>t−1</sub> − log y<sub>t−12</sub> + log y<sub>t−13</sub> = 6.0736 − 6.2281 − 6.0999 + 6.2070 = −0.04739, que con cuatro decimales es −0.0474. Son las cuatro esquinas del cuadrado del Módulo 5.3: el mes y el anterior, este año y el pasado. Los operadores conmutan, así que da igual aplicar primero ∇ o ∇<sub>12</sub>.",
              "rutas": [
                {
                  "valor": -22.15,
                  "cifra": "−22.1500",
                  "texto": "no tomó logaritmos: diferenció las noches en miles"
                },
                {
                  "valor": -0.026295,
                  "cifra": "−0.0263",
                  "texto": "aplicó solo la diferencia estacional, ∇<sub>12</sub>"
                },
                {
                  "valor": -0.154437,
                  "cifra": "−0.1544",
                  "texto": "aplicó solo la diferencia regular, ∇"
                },
                {
                  "valor": -0.020583,
                  "cifra": "−0.0206",
                  "texto": "usó el logaritmo en base 10 y no el natural"
                }
              ]
            },
            {
              "n": 3,
              "id": "S3",
              "etapa": 1,
              "etiqueta": "cap. 5 · mód. 5.6 y 5.10 · La rejilla por AICc",
              "tipo": "opcion",
              "enunciado": "<p>Para log y<sub>t</sub> se ajustaron estos candidatos, donde n es el número de datos sobre el que se evalúa la verosimilitud y k el de coeficientes ARMA:</p><table style=\"border-collapse:collapse;margin:6px 0 12px 0;font-size:95%\"><thead><tr><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">Modelo</th><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">d</th><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">D</th><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">n</th><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">k</th><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">AICc</th></tr></thead><tbody><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">ARIMA(0,1,2)(0,1,1)<sub>12</sub></td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">167</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">3</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">−473.84</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">ARIMA(0,1,1)(1,0,1)<sub>12</sub></td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">179</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">3</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">−479.13</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">ARIMA(0,1,1)(0,1,1)<sub>12</sub></td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">167</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">2</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">−474.98</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">ARIMA(1,1,1)(0,1,1)<sub>12</sub></td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">167</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">3</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">−473.93</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">ARIMA(0,1,1)(1,1,1)<sub>12</sub></td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">167</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">3</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">−473.73</td></tr></tbody></table><p>Un compañero propone quedarse con el modelo de menor AICc de toda la tabla. ¿Qué se le responde?</p>",
              "opciones": [
                {
                  "texto": "No: ese modelo tiene otra d, y su AICc se calcula sobre otros datos.",
                  "retro": "El de menor AICc tiene d = 1, como los demás. Lo que cambia es su D, y por eso se evalúa sobre 179 datos y no sobre 167 (módulo 5.6)."
                },
                {
                  "texto": "No: ese modelo tiene otra D, y su AICc se calcula sobre otros datos.",
                  "retro": "El de menor AICc, el ARIMA(0,1,1)(1,0,1)<sub>12</sub>, usa D = 0: su verosimilitud se evalúa sobre n = 179 datos y la de los demás sobre 167. Doce datos más mueven el AICc más que cualquier parámetro, así que las cifras no viven en la misma escala. Entre los que comparten d = 1 y D = 1 gana el airline, con AICc = −474.98 (módulos 5.6 y 5.10)."
                },
                {
                  "texto": "Sí: todos comparten d y D, así que manda el menor AICc.",
                  "retro": "No todos comparten D: el de menor AICc tiene D = 0 y su verosimilitud se evalúa sobre 12 datos más. Su AICc no se compara con el de los demás (módulos 5.6 y 5.10)."
                },
                {
                  "texto": "No: el AICc solo compara modelos con el mismo número de coeficientes.",
                  "retro": "El AICc existe justamente para comparar modelos con distinto número de coeficientes: su penalización cobra cada uno. Lo que no puede cambiar es el conjunto de datos sobre el que se evalúa la verosimilitud, que es lo que fijan d y D (módulo 5.6)."
                }
              ],
              "correcta": 1
            },
            {
              "n": 4,
              "id": "N4",
              "etapa": 1,
              "etiqueta": "cap. 5 · mód. 5.2, 5.4 y 5.7 · El satélite del modelo ajustado",
              "tipo": "numero",
              "enunciado": "<p>Para log y<sub>t</sub> se eligió el airline, ARIMA(0,1,1)(0,1,1)<sub>12</sub>, que en la notación del capítulo es (1 − B)(1 − B<sup>12</sup>) log y<sub>t</sub> = (1 + θB)(1 + ΘB<sup>12</sup>) ε<sub>t</sub>, con θ̂ = −0.4012 y Θ̂ = −0.6514. Calcule la autocorrelación teórica en el rezago 13 de ∇∇<sub>12</sub> log y<sub>t</sub> que implica el modelo ajustado. Responda con cuatro decimales.</p>",
              "clave": {
                "valor": 0.158,
                "tol": 0.001264,
                "texto": "0.1580"
              },
              "cuenta": "En el airline, ρ<sub>13</sub> = θΘ / [(1 + θ²)(1 + Θ²)] = ρ<sub>1</sub>·ρ<sub>12</sub>: (−0.4012)·(−0.6514) / [(1 + 0.1610)(1 + 0.4243)] = 0.2613 / 1.6536 = 0.1580. El producto de dos coeficientes negativos da un satélite positivo, y ese satélite no pide un parámetro: lo produce la multiplicación de los dos polinomios.",
              "rutas": [
                {
                  "valor": 0.261342,
                  "cifra": "0.2613",
                  "texto": "dio el coeficiente θΘ del rezago 13 y no la autocorrelación"
                },
                {
                  "valor": -0.802916,
                  "cifra": "−0.8029",
                  "texto": "sumó ρ<sub>1</sub> y ρ<sub>12</sub> en vez de multiplicarlas"
                },
                {
                  "valor": -0.345576,
                  "cifra": "−0.3456",
                  "texto": "dio ρ<sub>1</sub> = θ/(1 + θ²), la autocorrelación del rezago 1"
                },
                {
                  "valor": -0.158046,
                  "cifra": "−0.1580",
                  "texto": "cambió el signo: el producto de dos negativos es positivo"
                }
              ]
            },
            {
              "n": 5,
              "id": "N5",
              "etapa": 1,
              "etiqueta": "cap. 5 · mód. 5.6 y 5.7 · Ljung–Box con 2m rezagos",
              "tipo": "numero",
              "enunciado": "<p>Los n = 167 residuales del airline ajustado a log y<sub>t</sub> tienen autocorrelaciones muestrales r<sub>12</sub> = −0.0801 y r<sub>24</sub> = 0.0180. Para los otros 22 rezagos entre 1 y 24, la suma de los términos de Ljung–Box es Σ r<sub>k</sub>²/(n − k) = 0.0006073. Calcule el estadístico Q(24) de Ljung–Box. Responda con dos decimales.</p>",
              "clave": {
                "valor": 18.37,
                "tol": 0.14696,
                "texto": "18.37"
              },
              "cuenta": "Q(24) = n(n + 2) Σ<sub>k=1</sub><sup>24</sup> r<sub>k</sub>²/(n − k) = 167·169·(0.0006073 + −0.0801²/155 + 0.0180²/143) = 28 223·0.0006510 = 18.37. Con 24 − 2 = 22 grados de libertad (se descuentan θ y Θ), el valor crítico al 5 % es 33.92, así que la prueba no rechaza. Se usan 2m = 24 rezagos para que las barras de 12 y 24 pesen en el estadístico.",
              "rutas": [
                {
                  "valor": 1.232198,
                  "cifra": "1.23",
                  "texto": "sumó solo los términos de los rezagos 12 y 24"
                },
                {
                  "valor": 207.36313,
                  "cifra": "207.36",
                  "texto": "no dividió entre n − k los términos de los rezagos 12 y 24"
                },
                {
                  "valor": 21.21431,
                  "cifra": "21.21",
                  "texto": "usó los N = 180 meses de la serie en vez de los n = 167 residuales"
                },
                {
                  "valor": 32.610759,
                  "cifra": "32.61",
                  "texto": "dividió entre k en vez de entre n − k"
                }
              ]
            },
            {
              "n": 6,
              "id": "N6",
              "etapa": 1,
              "etiqueta": "cap. 5 · mód. 5.5 · La desviación del pronóstico",
              "tipo": "numero",
              "enunciado": "<p>En el airline ajustado a log y<sub>t</sub>, θ̂ = −0.4012, Θ̂ = −0.6514 y σ̂² = 0.003152. Sus pesos ψ valen ψ<sub>0</sub> = 1, ψ<sub>j</sub> = 1 + θ para j = 1, …, 11 y, al cruzar el rezago estacional, ψ<sub>12</sub> = (1 + θ) + (1 + Θ). Calcule σ<sub>13</sub>, la desviación típica del error cuando se pronostica a h = 13 meses, en la escala de log y<sub>t</sub>. Responda con cuatro decimales.</p>",
              "clave": {
                "valor": 0.1357,
                "tol": 0.001086,
                "texto": "0.1357"
              },
              "cuenta": "σ<sub>h</sub>² = σ² Σ<sub>j=0</sub><sup>h−1</sup> ψ<sub>j</sub>², así que a h = 13 entran ψ<sub>0</sub> a ψ<sub>12</sub>: 1 + 11·(1 + θ)² + (2 + θ + Θ)² = 1 + 11·0.3586 + 0.8976 = 5.8417, y σ<sub>13</sub> = √(0.003152·5.8417) = 0.1357. El salto de ψ<sub>12</sub> es la huella de la estación: la incertidumbre crece a ritmo constante dentro del año y pega un escalón al cruzar el rezago 12.",
              "rutas": [
                {
                  "valor": 0.129284,
                  "cifra": "0.1293",
                  "texto": "no vio el escalón: tomó ψ<sub>12</sub> = 1 + θ"
                },
                {
                  "valor": 0.164012,
                  "cifra": "0.1640",
                  "texto": "sumó los pesos ψ<sub>j</sub> en vez de sus cuadrados"
                },
                {
                  "valor": 0.018413,
                  "cifra": "0.0184",
                  "texto": "dio la varianza: olvidó la raíz"
                },
                {
                  "valor": 0.143069,
                  "cifra": "0.1431",
                  "texto": "sumó trece pesos: añadió ψ<sub>13</sub>"
                }
              ]
            },
            {
              "n": 7,
              "id": "N7",
              "etapa": 1,
              "etiqueta": "cap. 5 · mód. 5.2 y 5.7 · El pronóstico de enero",
              "tipo": "numero",
              "enunciado": "<p>Para pronosticar enero de 2026 con el airline ajustado a log y<sub>t</sub>, (1 − B)(1 − B<sup>12</sup>) log y<sub>t</sub> = (1 + θB)(1 + ΘB<sup>12</sup>) ε<sub>t</sub> con θ̂ = −0.4012 y Θ̂ = −0.6514, se tienen el logaritmo de los vehículos y el residual de tres meses:</p><table style=\"border-collapse:collapse;margin:6px 0 12px 0;font-size:95%\"><thead><tr><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">Mes</th><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">log y<sub>t</sub></th><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">Residual</th></tr></thead><tbody><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">diciembre de 2024</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">6.3973</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0.0294</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">enero de 2025</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">6.3034</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0.0313</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">diciembre de 2025</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">6.4671</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0.0764</td></tr></tbody></table><p>Calcule el pronóstico puntual de enero de 2026 en la escala original, en miles de vehículos: el que da exp del pronóstico en logaritmos. Responda con dos decimales.</p>",
              "clave": {
                "valor": 561.07,
                "tol": 4.48856,
                "texto": "561.07"
              },
              "cuenta": "Despejado, el modelo dice log y<sub>t</sub> = log y<sub>t−1</sub> + log y<sub>t−12</sub> − log y<sub>t−13</sub> + ε<sub>t</sub> + θε<sub>t−1</sub> + Θε<sub>t−12</sub> + θΘε<sub>t−13</sub>. Para enero de 2026 el choque del mes se pronostica con 0 y los otros tres son los residuales: 6.4671 + 6.3034 − 6.3973 + (−0.4012)·0.0764 + (−0.6514)·0.0313 + 0.261342·0.0294 = 6.32984. De vuelta con exp, e<sup>6.32984</sup> = 561.07 miles de vehículos: la mediana del pronóstico, no su media.",
              "rutas": [
                {
                  "valor": 585.929808,
                  "cifra": "585.93",
                  "texto": "olvidó los términos MA: usó solo las dos diferencias"
                },
                {
                  "valor": 6.329843,
                  "cifra": "6.33",
                  "texto": "no deshizo el logaritmo"
                },
                {
                  "valor": 546.426606,
                  "cifra": "546.43",
                  "texto": "repitió enero de 2025 (el pronóstico ingenuo estacional)"
                },
                {
                  "valor": 202134312.018342,
                  "cifra": "202134312.02",
                  "texto": "sumó el log de diciembre de 2024 en vez de restarlo"
                }
              ]
            },
            {
              "n": 8,
              "id": "GI",
              "etapa": 1,
              "etiqueta": "cap. 5 · mód. 5.4 · Identificar por la ACF y la PACF",
              "tipo": "opcion",
              "enunciado": "<p>La misma concesión lleva la serie mensual de camiones que pasan por otro peaje de la vía. La figura muestra la ACF y la PACF muestrales de ∇∇<sub>12</sub> log y<sub>t</sub> de esa serie, con n = 179 datos tras las dos diferencias y la banda ±1.96/√n en trazos. ¿Qué modelo sugieren?</p><figure class='simulacro-figura'><div class='simulacro-figura-paneles'><svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 460 214' role='img' aria-label='Correlograma: ACF de ∇∇₁₂ log y' data-panel='acf' font-family='Montserrat, system-ui, sans-serif' font-size='12'><text x='230' y='17' text-anchor='middle' fill='#012820' font-size='13.5' font-weight='600'>ACF de ∇∇₁₂ log y</text><rect x='48' y='30' width='400' height='144' fill='none' stroke='#cbd5e1'/><g stroke='#e2e8f0'><line class='grid-y' data-v='-0.5' x1='48' x2='448' y1='147' y2='147'/><line class='grid-y' data-v='0' x1='48' x2='448' y1='102' y2='102'/><line class='grid-y' data-v='0.5' x1='48' x2='448' y1='57' y2='57'/></g><g fill='#475569' text-anchor='end'><text class='tick-y' data-v='-0.5' x='42' y='151'>−0.5</text><text class='tick-y' data-v='0' x='42' y='106'>0</text><text class='tick-y' data-v='0.5' x='42' y='61'>0.5</text></g><g stroke='#e2e8f0'><line class='grid-x' data-v='6' x1='112.9' x2='112.9' y1='30' y2='174'/><line class='grid-x' data-v='12' x1='177.7' x2='177.7' y1='30' y2='174'/><line class='grid-x' data-v='18' x1='242.6' x2='242.6' y1='30' y2='174'/><line class='grid-x' data-v='24' x1='307.5' x2='307.5' y1='30' y2='174'/><line class='grid-x' data-v='30' x1='372.3' x2='372.3' y1='30' y2='174'/><line class='grid-x' data-v='36' x1='437.2' x2='437.2' y1='30' y2='174'/></g><g fill='#475569' text-anchor='middle'><text class='tick-x' data-v='6' x='112.9' y='189'>6</text><text class='tick-x' data-v='12' x='177.7' y='189'>12</text><text class='tick-x' data-v='18' x='242.6' y='189'>18</text><text class='tick-x' data-v='24' x='307.5' y='189'>24</text><text class='tick-x' data-v='30' x='372.3' y='189'>30</text><text class='tick-x' data-v='36' x='437.2' y='189'>36</text></g><text x='248' y='206' text-anchor='middle' fill='#475569'>Rezago (meses)</text><line class='cero' x1='48' x2='448' y1='102' y2='102' stroke='#64748b' stroke-width='1'/><line class='banda' data-v='0.1465' x1='48' x2='448' y1='88.8' y2='88.8' stroke='#2563eb' stroke-width='1.3' stroke-dasharray='5 4'/><line class='banda' data-v='-0.1465' x1='48' x2='448' y1='115.2' y2='115.2' stroke='#2563eb' stroke-width='1.3' stroke-dasharray='5 4'/><g stroke='#012820' stroke-width='4' stroke-linecap='butt'><line class='barra' data-k='1' x1='58.8' x2='58.8' y1='102' y2='147'/><line class='barra' data-k='2' x1='69.6' x2='69.6' y1='102' y2='96.7'/><line class='barra' data-k='3' x1='80.4' x2='80.4' y1='102' y2='105'/><line class='barra' data-k='4' x1='91.2' x2='91.2' y1='102' y2='99.7'/><line class='barra' data-k='5' x1='102.1' x2='102.1' y1='102' y2='100.6'/><line class='barra' data-k='6' x1='112.9' x2='112.9' y1='102' y2='98.5'/><line class='barra' data-k='7' x1='123.7' x2='123.7' y1='102' y2='111.1'/><line class='barra' data-k='8' x1='134.5' x2='134.5' y1='102' y2='103.1'/><line class='barra' data-k='9' x1='145.3' x2='145.3' y1='102' y2='95.3'/><line class='barra' data-k='10' x1='156.1' x2='156.1' y1='102' y2='103.3'/><line class='barra' data-k='11' x1='166.9' x2='166.9' y1='102' y2='78.9'/><line class='barra' data-k='12' x1='177.7' x2='177.7' y1='102' y2='160.3'/><line class='barra' data-k='13' x1='188.5' x2='188.5' y1='102' y2='66'/><line class='barra' data-k='14' x1='199.4' x2='199.4' y1='102' y2='107.8'/><line class='barra' data-k='15' x1='210.2' x2='210.2' y1='102' y2='100.9'/><line class='barra' data-k='16' x1='221' x2='221' y1='102' y2='107.3'/><line class='barra' data-k='17' x1='231.8' x2='231.8' y1='102' y2='98.4'/><line class='barra' data-k='18' x1='242.6' x2='242.6' y1='102' y2='105.9'/><line class='barra' data-k='19' x1='253.4' x2='253.4' y1='102' y2='93.9'/><line class='barra' data-k='20' x1='264.2' x2='264.2' y1='102' y2='100.1'/><line class='barra' data-k='21' x1='275' x2='275' y1='102' y2='109.5'/><line class='barra' data-k='22' x1='285.8' x2='285.8' y1='102' y2='103.6'/><line class='barra' data-k='23' x1='296.6' x2='296.6' y1='102' y2='108'/><line class='barra' data-k='24' x1='307.5' x2='307.5' y1='102' y2='68'/><line class='barra' data-k='25' x1='318.3' x2='318.3' y1='102' y2='133.7'/><line class='barra' data-k='26' x1='329.1' x2='329.1' y1='102' y2='91.1'/><line class='barra' data-k='27' x1='339.9' x2='339.9' y1='102' y2='103.3'/><line class='barra' data-k='28' x1='350.7' x2='350.7' y1='102' y2='98.6'/><line class='barra' data-k='29' x1='361.5' x2='361.5' y1='102' y2='105.6'/><line class='barra' data-k='30' x1='372.3' x2='372.3' y1='102' y2='99.1'/><line class='barra' data-k='31' x1='383.1' x2='383.1' y1='102' y2='109.4'/><line class='barra' data-k='32' x1='393.9' x2='393.9' y1='102' y2='103.3'/><line class='barra' data-k='33' x1='404.8' x2='404.8' y1='102' y2='93.3'/><line class='barra' data-k='34' x1='415.6' x2='415.6' y1='102' y2='102.3'/><line class='barra' data-k='35' x1='426.4' x2='426.4' y1='102' y2='104'/><line class='barra' data-k='36' x1='437.2' x2='437.2' y1='102' y2='117'/></g></svg><svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 460 214' role='img' aria-label='Correlograma: PACF de ∇∇₁₂ log y' data-panel='pacf' font-family='Montserrat, system-ui, sans-serif' font-size='12'><text x='230' y='17' text-anchor='middle' fill='#012820' font-size='13.5' font-weight='600'>PACF de ∇∇₁₂ log y</text><rect x='48' y='30' width='400' height='144' fill='none' stroke='#cbd5e1'/><g stroke='#e2e8f0'><line class='grid-y' data-v='-0.5' x1='48' x2='448' y1='162' y2='162'/><line class='grid-y' data-v='0' x1='48' x2='448' y1='102' y2='102'/><line class='grid-y' data-v='0.5' x1='48' x2='448' y1='42' y2='42'/></g><g fill='#475569' text-anchor='end'><text class='tick-y' data-v='-0.5' x='42' y='166'>−0.5</text><text class='tick-y' data-v='0' x='42' y='106'>0</text><text class='tick-y' data-v='0.5' x='42' y='46'>0.5</text></g><g stroke='#e2e8f0'><line class='grid-x' data-v='6' x1='112.9' x2='112.9' y1='30' y2='174'/><line class='grid-x' data-v='12' x1='177.7' x2='177.7' y1='30' y2='174'/><line class='grid-x' data-v='18' x1='242.6' x2='242.6' y1='30' y2='174'/><line class='grid-x' data-v='24' x1='307.5' x2='307.5' y1='30' y2='174'/><line class='grid-x' data-v='30' x1='372.3' x2='372.3' y1='30' y2='174'/><line class='grid-x' data-v='36' x1='437.2' x2='437.2' y1='30' y2='174'/></g><g fill='#475569' text-anchor='middle'><text class='tick-x' data-v='6' x='112.9' y='189'>6</text><text class='tick-x' data-v='12' x='177.7' y='189'>12</text><text class='tick-x' data-v='18' x='242.6' y='189'>18</text><text class='tick-x' data-v='24' x='307.5' y='189'>24</text><text class='tick-x' data-v='30' x='372.3' y='189'>30</text><text class='tick-x' data-v='36' x='437.2' y='189'>36</text></g><text x='248' y='206' text-anchor='middle' fill='#475569'>Rezago (meses)</text><line class='cero' x1='48' x2='448' y1='102' y2='102' stroke='#64748b' stroke-width='1'/><line class='banda' data-v='0.1465' x1='48' x2='448' y1='84.4' y2='84.4' stroke='#2563eb' stroke-width='1.3' stroke-dasharray='5 4'/><line class='banda' data-v='-0.1465' x1='48' x2='448' y1='119.6' y2='119.6' stroke='#2563eb' stroke-width='1.3' stroke-dasharray='5 4'/><g stroke='#c2410c' stroke-width='4' stroke-linecap='butt'><line class='barra' data-k='1' x1='58.8' x2='58.8' y1='102' y2='162'/><line class='barra' data-k='2' x1='69.6' x2='69.6' y1='102' y2='132.6'/><line class='barra' data-k='3' x1='80.4' x2='80.4' y1='102' y2='123.3'/><line class='barra' data-k='4' x1='91.2' x2='91.2' y1='102' y2='113.4'/><line class='barra' data-k='5' x1='102.1' x2='102.1' y1='102' y2='104.4'/><line class='barra' data-k='6' x1='112.9' x2='112.9' y1='102' y2='93.5'/><line class='barra' data-k='7' x1='123.7' x2='123.7' y1='102' y2='107.7'/><line class='barra' data-k='8' x1='134.5' x2='134.5' y1='102' y2='117.5'/><line class='barra' data-k='9' x1='145.3' x2='145.3' y1='102' y2='105.8'/><line class='barra' data-k='10' x1='156.1' x2='156.1' y1='102' y2='101.6'/><line class='barra' data-k='11' x1='166.9' x2='166.9' y1='102' y2='53.4'/><line class='barra' data-k='12' x1='177.7' x2='177.7' y1='102' y2='161.1'/><line class='barra' data-k='13' x1='188.5' x2='188.5' y1='102' y2='131.6'/><line class='barra' data-k='14' x1='199.4' x2='199.4' y1='102' y2='112.7'/><line class='barra' data-k='15' x1='210.2' x2='210.2' y1='102' y2='106.8'/><line class='barra' data-k='16' x1='221' x2='221' y1='102' y2='114.4'/><line class='barra' data-k='17' x1='231.8' x2='231.8' y1='102' y2='107.5'/><line class='barra' data-k='18' x1='242.6' x2='242.6' y1='102' y2='96.6'/><line class='barra' data-k='19' x1='253.4' x2='253.4' y1='102' y2='107.5'/><line class='barra' data-k='20' x1='264.2' x2='264.2' y1='102' y2='102.6'/><line class='barra' data-k='21' x1='275' x2='275' y1='102' y2='97.7'/><line class='barra' data-k='22' x1='285.8' x2='285.8' y1='102' y2='104.5'/><line class='barra' data-k='23' x1='296.6' x2='296.6' y1='102' y2='95.3'/><line class='barra' data-k='24' x1='307.5' x2='307.5' y1='102' y2='97.3'/><line class='barra' data-k='25' x1='318.3' x2='318.3' y1='102' y2='112.4'/><line class='barra' data-k='26' x1='329.1' x2='329.1' y1='102' y2='103.6'/><line class='barra' data-k='27' x1='339.9' x2='339.9' y1='102' y2='98.6'/><line class='barra' data-k='28' x1='350.7' x2='350.7' y1='102' y2='105'/><line class='barra' data-k='29' x1='361.5' x2='361.5' y1='102' y2='106.9'/><line class='barra' data-k='30' x1='372.3' x2='372.3' y1='102' y2='104.4'/><line class='barra' data-k='31' x1='383.1' x2='383.1' y1='102' y2='104'/><line class='barra' data-k='32' x1='393.9' x2='393.9' y1='102' y2='110.8'/><line class='barra' data-k='33' x1='404.8' x2='404.8' y1='102' y2='101.9'/><line class='barra' data-k='34' x1='415.6' x2='415.6' y1='102' y2='100.5'/><line class='barra' data-k='35' x1='426.4' x2='426.4' y1='102' y2='105.2'/><line class='barra' data-k='36' x1='437.2' x2='437.2' y1='102' y2='96.6'/></g></svg></div><figcaption>Arriba, la ACF; abajo, la PACF, de los rezagos 1 a 36. La banda vale ±0.15.</figcaption></figure>",
              "opciones": [
                {
                  "texto": "ARIMA(0,1,1)(0,1,1)<sub>12</sub>",
                  "retro": "Esa lectura falla en la parte estacional no: en 12, 24 y 36 la ACF decae (r<sub>12</sub> = −0.65, r<sub>24</sub> = 0.38) y la PACF se corta tras el 12 (p<sub>12</sub> = −0.49, p<sub>24</sub> = 0.04): un AR(1) estacional (módulo 5.4)."
                },
                {
                  "texto": "ARIMA(1,1,0)(0,1,1)<sub>12</sub>",
                  "retro": "Esa lectura falla en la parte regular no: en los rezagos bajos la ACF se corta tras el 1 (r<sub>1</sub> = −0.50, y de 2 a 4 dentro de ±0.15) y la PACF decae (p<sub>1</sub> = −0.50, p<sub>2</sub> = −0.26): un MA(1) regular; en la estacional tampoco: en 12, 24 y 36 la ACF decae (r<sub>12</sub> = −0.65, r<sub>24</sub> = 0.38) y la PACF se corta tras el 12 (p<sub>12</sub> = −0.49, p<sub>24</sub> = 0.04): un AR(1) estacional (módulo 5.4)."
                },
                {
                  "texto": "ARIMA(1,1,0)(1,1,0)<sub>12</sub>",
                  "retro": "Esa lectura falla en la parte regular no: en los rezagos bajos la ACF se corta tras el 1 (r<sub>1</sub> = −0.50, y de 2 a 4 dentro de ±0.15) y la PACF decae (p<sub>1</sub> = −0.50, p<sub>2</sub> = −0.26): un MA(1) regular (módulo 5.4)."
                },
                {
                  "texto": "ARIMA(0,1,1)(1,1,0)<sub>12</sub>",
                  "retro": "La tabla del Módulo 5.4, leída dos veces: en los rezagos bajos la ACF se corta tras el 1 (r<sub>1</sub> = −0.50, y de 2 a 4 dentro de ±0.15) y la PACF decae (p<sub>1</sub> = −0.50, p<sub>2</sub> = −0.26): un MA(1) regular; y en 12, 24 y 36 la ACF decae (r<sub>12</sub> = −0.65, r<sub>24</sub> = 0.38) y la PACF se corta tras el 12 (p<sub>12</sub> = −0.49, p<sub>24</sub> = 0.04): un AR(1) estacional. Las barras de 11 y 13 son satélites del producto de los dos polinomios y no piden parámetros."
                }
              ],
              "correcta": 3
            },
            {
              "n": 9,
              "id": "GD",
              "etapa": 1,
              "etiqueta": "cap. 5 · mód. 5.6 y 5.7 · El diagnóstico de un primer intento",
              "tipo": "opcion",
              "enunciado": "<p>En la concesión, la serie de galones de combustible que vende cada mes una estación de servicio de la vía se modeló con un SARIMA de dos parámetros. La figura muestra sus 150 residuales estandarizados contra el tiempo y su ACF, con la banda ±1.96/√n en trazos. Ljung–Box con 24 rezagos da Q = 20.94, con 24 − 2 = 22 grados de libertad, y χ²<sub>0.95</sub>(22) = 33.92. ¿Qué indica el diagnóstico?</p><figure class='simulacro-figura'><div class='simulacro-figura-paneles'><svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 460 214' role='img' aria-label='Residuales en el tiempo: Residuales estandarizados' data-panel='tiempo' font-family='Montserrat, system-ui, sans-serif' font-size='12'><text x='230' y='17' text-anchor='middle' fill='#012820' font-size='13.5' font-weight='600'>Residuales estandarizados</text><rect x='48' y='30' width='400' height='144' fill='none' stroke='#cbd5e1'/><g stroke='#e2e8f0'><line class='grid-y' data-v='-4' x1='48' x2='448' y1='174' y2='174'/><line class='grid-y' data-v='-2' x1='48' x2='448' y1='138' y2='138'/><line class='grid-y' data-v='0' x1='48' x2='448' y1='102' y2='102'/><line class='grid-y' data-v='2' x1='48' x2='448' y1='66' y2='66'/><line class='grid-y' data-v='4' x1='48' x2='448' y1='30' y2='30'/></g><g fill='#475569' text-anchor='end'><text class='tick-y' data-v='-4' x='42' y='178'>−4</text><text class='tick-y' data-v='-2' x='42' y='142'>−2</text><text class='tick-y' data-v='0' x='42' y='106'>0</text><text class='tick-y' data-v='2' x='42' y='70'>2</text><text class='tick-y' data-v='4' x='42' y='34'>4</text></g><g stroke='#e2e8f0'><line class='grid-x' data-v='25' x1='114.2' x2='114.2' y1='30' y2='174'/><line class='grid-x' data-v='50' x1='180.5' x2='180.5' y1='30' y2='174'/><line class='grid-x' data-v='75' x1='246.7' x2='246.7' y1='30' y2='174'/><line class='grid-x' data-v='100' x1='312.9' x2='312.9' y1='30' y2='174'/><line class='grid-x' data-v='125' x1='379.1' x2='379.1' y1='30' y2='174'/><line class='grid-x' data-v='150' x1='445.4' x2='445.4' y1='30' y2='174'/></g><g fill='#475569' text-anchor='middle'><text class='tick-x' data-v='25' x='114.2' y='189'>25</text><text class='tick-x' data-v='50' x='180.5' y='189'>50</text><text class='tick-x' data-v='75' x='246.7' y='189'>75</text><text class='tick-x' data-v='100' x='312.9' y='189'>100</text><text class='tick-x' data-v='125' x='379.1' y='189'>125</text><text class='tick-x' data-v='150' x='445.4' y='189'>150</text></g><text x='248' y='206' text-anchor='middle' fill='#475569'>Mes</text><line class='cero' x1='48' x2='448' y1='102' y2='102' stroke='#64748b' stroke-width='1.2' stroke-dasharray='5 4'/><polyline points='50.6,109 53.3,114.1 55.9,102.5 58.6,107 61.2,109.8 63.9,109 66.5,98.9 69.2,89.8 71.8,99.3 74.5,93.3 77.1,91.6 79.8,101 82.4,106.1 85.1,93.7 87.7,106.7 90.4,97.5 93,90.4 95.7,102 98.3,109.8 101,104.1 103.6,98 106.3,100.3 108.9,111 111.6,89.9 114.2,88.3 116.9,101.3 119.5,89.3 122.2,92.5 124.8,110 127.5,108.5 130.1,113.9 132.8,89.8 135.4,102.3 138.1,91.2 140.7,84.5 143.4,101.4 146,90.5 148.7,105.9 151.3,101.7 154,85.6 156.6,135.5 159.3,79.3 161.9,101.2 164.6,93.5 167.2,96.9 169.9,104.3 172.5,76.6 175.2,93.8 177.8,89.3 180.5,117.3 183.1,101.1 185.7,92.4 188.4,117 191,109.6 193.7,106.7 196.3,86.9 199,90.6 201.6,78.5 204.3,114.8 206.9,110.1 209.6,100.1 212.2,119.4 214.9,100.9 217.5,106.9 220.2,83.5 222.8,104.8 225.5,105.5 228.1,120.7 230.8,119.8 233.4,91.1 236.1,86.6 238.7,107.2 241.4,112.4 244,117.4 246.7,87.7 249.3,108.3 252,104.6 254.6,114.9 257.3,91.6 259.9,115.8 262.6,96.6 265.2,100.7 267.9,101.7 270.5,84.4 273.2,130.7 275.8,108.3 278.5,121.4 281.1,90.9 283.8,125.7 286.4,102.5 289.1,98.6 291.7,116.8 294.4,111.2 297,111 299.7,116.9 302.3,114.9 305,81 307.6,111 310.3,83.4 312.9,94.3 315.5,98 318.2,105.4 320.8,107.8 323.5,75.7 326.1,93.8 328.8,97.7 331.4,82.3 334.1,135.1 336.7,102.2 339.4,106.2 342,112.3 344.7,115.4 347.3,68.2 350,68.5 352.6,96.6 355.3,135.1 357.9,86 360.6,103.5 363.2,78.1 365.9,77.2 368.5,137.1 371.2,99.6 373.8,62.7 376.5,65.9 379.1,108.7 381.8,151.6 384.4,113.2 387.1,132.5 389.7,138.4 392.4,160 395,149.8 397.7,132.7 400.3,139.9 403,79.6 405.6,83.5 408.3,112.9 410.9,107.3 413.6,115 416.2,111.4 418.9,127.9 421.5,106.6 424.2,61.5 426.8,120.5 429.5,93.1 432.1,111.9 434.8,55.2 437.4,147.2 440.1,85.5 442.7,69.2 445.4,114.4' fill='none' stroke='#94a3b8' stroke-width='0.8'/><g fill='#012820'><circle class='pt' data-t='1' cx='50.6' cy='109' r='2.2'/><circle class='pt' data-t='2' cx='53.3' cy='114.1' r='2.2'/><circle class='pt' data-t='3' cx='55.9' cy='102.5' r='2.2'/><circle class='pt' data-t='4' cx='58.6' cy='107' r='2.2'/><circle class='pt' data-t='5' cx='61.2' cy='109.8' r='2.2'/><circle class='pt' data-t='6' cx='63.9' cy='109' r='2.2'/><circle class='pt' data-t='7' cx='66.5' cy='98.9' r='2.2'/><circle class='pt' data-t='8' cx='69.2' cy='89.8' r='2.2'/><circle class='pt' data-t='9' cx='71.8' cy='99.3' r='2.2'/><circle class='pt' data-t='10' cx='74.5' cy='93.3' r='2.2'/><circle class='pt' data-t='11' cx='77.1' cy='91.6' r='2.2'/><circle class='pt' data-t='12' cx='79.8' cy='101' r='2.2'/><circle class='pt' data-t='13' cx='82.4' cy='106.1' r='2.2'/><circle class='pt' data-t='14' cx='85.1' cy='93.7' r='2.2'/><circle class='pt' data-t='15' cx='87.7' cy='106.7' r='2.2'/><circle class='pt' data-t='16' cx='90.4' cy='97.5' r='2.2'/><circle class='pt' data-t='17' cx='93' cy='90.4' r='2.2'/><circle class='pt' data-t='18' cx='95.7' cy='102' r='2.2'/><circle class='pt' data-t='19' cx='98.3' cy='109.8' r='2.2'/><circle class='pt' data-t='20' cx='101' cy='104.1' r='2.2'/><circle class='pt' data-t='21' cx='103.6' cy='98' r='2.2'/><circle class='pt' data-t='22' cx='106.3' cy='100.3' r='2.2'/><circle class='pt' data-t='23' cx='108.9' cy='111' r='2.2'/><circle class='pt' data-t='24' cx='111.6' cy='89.9' r='2.2'/><circle class='pt' data-t='25' cx='114.2' cy='88.3' r='2.2'/><circle class='pt' data-t='26' cx='116.9' cy='101.3' r='2.2'/><circle class='pt' data-t='27' cx='119.5' cy='89.3' r='2.2'/><circle class='pt' data-t='28' cx='122.2' cy='92.5' r='2.2'/><circle class='pt' data-t='29' cx='124.8' cy='110' r='2.2'/><circle class='pt' data-t='30' cx='127.5' cy='108.5' r='2.2'/><circle class='pt' data-t='31' cx='130.1' cy='113.9' r='2.2'/><circle class='pt' data-t='32' cx='132.8' cy='89.8' r='2.2'/><circle class='pt' data-t='33' cx='135.4' cy='102.3' r='2.2'/><circle class='pt' data-t='34' cx='138.1' cy='91.2' r='2.2'/><circle class='pt' data-t='35' cx='140.7' cy='84.5' r='2.2'/><circle class='pt' data-t='36' cx='143.4' cy='101.4' r='2.2'/><circle class='pt' data-t='37' cx='146' cy='90.5' r='2.2'/><circle class='pt' data-t='38' cx='148.7' cy='105.9' r='2.2'/><circle class='pt' data-t='39' cx='151.3' cy='101.7' r='2.2'/><circle class='pt' data-t='40' cx='154' cy='85.6' r='2.2'/><circle class='pt' data-t='41' cx='156.6' cy='135.5' r='2.2'/><circle class='pt' data-t='42' cx='159.3' cy='79.3' r='2.2'/><circle class='pt' data-t='43' cx='161.9' cy='101.2' r='2.2'/><circle class='pt' data-t='44' cx='164.6' cy='93.5' r='2.2'/><circle class='pt' data-t='45' cx='167.2' cy='96.9' r='2.2'/><circle class='pt' data-t='46' cx='169.9' cy='104.3' r='2.2'/><circle class='pt' data-t='47' cx='172.5' cy='76.6' r='2.2'/><circle class='pt' data-t='48' cx='175.2' cy='93.8' r='2.2'/><circle class='pt' data-t='49' cx='177.8' cy='89.3' r='2.2'/><circle class='pt' data-t='50' cx='180.5' cy='117.3' r='2.2'/><circle class='pt' data-t='51' cx='183.1' cy='101.1' r='2.2'/><circle class='pt' data-t='52' cx='185.7' cy='92.4' r='2.2'/><circle class='pt' data-t='53' cx='188.4' cy='117' r='2.2'/><circle class='pt' data-t='54' cx='191' cy='109.6' r='2.2'/><circle class='pt' data-t='55' cx='193.7' cy='106.7' r='2.2'/><circle class='pt' data-t='56' cx='196.3' cy='86.9' r='2.2'/><circle class='pt' data-t='57' cx='199' cy='90.6' r='2.2'/><circle class='pt' data-t='58' cx='201.6' cy='78.5' r='2.2'/><circle class='pt' data-t='59' cx='204.3' cy='114.8' r='2.2'/><circle class='pt' data-t='60' cx='206.9' cy='110.1' r='2.2'/><circle class='pt' data-t='61' cx='209.6' cy='100.1' r='2.2'/><circle class='pt' data-t='62' cx='212.2' cy='119.4' r='2.2'/><circle class='pt' data-t='63' cx='214.9' cy='100.9' r='2.2'/><circle class='pt' data-t='64' cx='217.5' cy='106.9' r='2.2'/><circle class='pt' data-t='65' cx='220.2' cy='83.5' r='2.2'/><circle class='pt' data-t='66' cx='222.8' cy='104.8' r='2.2'/><circle class='pt' data-t='67' cx='225.5' cy='105.5' r='2.2'/><circle class='pt' data-t='68' cx='228.1' cy='120.7' r='2.2'/><circle class='pt' data-t='69' cx='230.8' cy='119.8' r='2.2'/><circle class='pt' data-t='70' cx='233.4' cy='91.1' r='2.2'/><circle class='pt' data-t='71' cx='236.1' cy='86.6' r='2.2'/><circle class='pt' data-t='72' cx='238.7' cy='107.2' r='2.2'/><circle class='pt' data-t='73' cx='241.4' cy='112.4' r='2.2'/><circle class='pt' data-t='74' cx='244' cy='117.4' r='2.2'/><circle class='pt' data-t='75' cx='246.7' cy='87.7' r='2.2'/><circle class='pt' data-t='76' cx='249.3' cy='108.3' r='2.2'/><circle class='pt' data-t='77' cx='252' cy='104.6' r='2.2'/><circle class='pt' data-t='78' cx='254.6' cy='114.9' r='2.2'/><circle class='pt' data-t='79' cx='257.3' cy='91.6' r='2.2'/><circle class='pt' data-t='80' cx='259.9' cy='115.8' r='2.2'/><circle class='pt' data-t='81' cx='262.6' cy='96.6' r='2.2'/><circle class='pt' data-t='82' cx='265.2' cy='100.7' r='2.2'/><circle class='pt' data-t='83' cx='267.9' cy='101.7' r='2.2'/><circle class='pt' data-t='84' cx='270.5' cy='84.4' r='2.2'/><circle class='pt' data-t='85' cx='273.2' cy='130.7' r='2.2'/><circle class='pt' data-t='86' cx='275.8' cy='108.3' r='2.2'/><circle class='pt' data-t='87' cx='278.5' cy='121.4' r='2.2'/><circle class='pt' data-t='88' cx='281.1' cy='90.9' r='2.2'/><circle class='pt' data-t='89' cx='283.8' cy='125.7' r='2.2'/><circle class='pt' data-t='90' cx='286.4' cy='102.5' r='2.2'/><circle class='pt' data-t='91' cx='289.1' cy='98.6' r='2.2'/><circle class='pt' data-t='92' cx='291.7' cy='116.8' r='2.2'/><circle class='pt' data-t='93' cx='294.4' cy='111.2' r='2.2'/><circle class='pt' data-t='94' cx='297' cy='111' r='2.2'/><circle class='pt' data-t='95' cx='299.7' cy='116.9' r='2.2'/><circle class='pt' data-t='96' cx='302.3' cy='114.9' r='2.2'/><circle class='pt' data-t='97' cx='305' cy='81' r='2.2'/><circle class='pt' data-t='98' cx='307.6' cy='111' r='2.2'/><circle class='pt' data-t='99' cx='310.3' cy='83.4' r='2.2'/><circle class='pt' data-t='100' cx='312.9' cy='94.3' r='2.2'/><circle class='pt' data-t='101' cx='315.5' cy='98' r='2.2'/><circle class='pt' data-t='102' cx='318.2' cy='105.4' r='2.2'/><circle class='pt' data-t='103' cx='320.8' cy='107.8' r='2.2'/><circle class='pt' data-t='104' cx='323.5' cy='75.7' r='2.2'/><circle class='pt' data-t='105' cx='326.1' cy='93.8' r='2.2'/><circle class='pt' data-t='106' cx='328.8' cy='97.7' r='2.2'/><circle class='pt' data-t='107' cx='331.4' cy='82.3' r='2.2'/><circle class='pt' data-t='108' cx='334.1' cy='135.1' r='2.2'/><circle class='pt' data-t='109' cx='336.7' cy='102.2' r='2.2'/><circle class='pt' data-t='110' cx='339.4' cy='106.2' r='2.2'/><circle class='pt' data-t='111' cx='342' cy='112.3' r='2.2'/><circle class='pt' data-t='112' cx='344.7' cy='115.4' r='2.2'/><circle class='pt' data-t='113' cx='347.3' cy='68.2' r='2.2'/><circle class='pt' data-t='114' cx='350' cy='68.5' r='2.2'/><circle class='pt' data-t='115' cx='352.6' cy='96.6' r='2.2'/><circle class='pt' data-t='116' cx='355.3' cy='135.1' r='2.2'/><circle class='pt' data-t='117' cx='357.9' cy='86' r='2.2'/><circle class='pt' data-t='118' cx='360.6' cy='103.5' r='2.2'/><circle class='pt' data-t='119' cx='363.2' cy='78.1' r='2.2'/><circle class='pt' data-t='120' cx='365.9' cy='77.2' r='2.2'/><circle class='pt' data-t='121' cx='368.5' cy='137.1' r='2.2'/><circle class='pt' data-t='122' cx='371.2' cy='99.6' r='2.2'/><circle class='pt' data-t='123' cx='373.8' cy='62.7' r='2.2'/><circle class='pt' data-t='124' cx='376.5' cy='65.9' r='2.2'/><circle class='pt' data-t='125' cx='379.1' cy='108.7' r='2.2'/><circle class='pt' data-t='126' cx='381.8' cy='151.6' r='2.2'/><circle class='pt' data-t='127' cx='384.4' cy='113.2' r='2.2'/><circle class='pt' data-t='128' cx='387.1' cy='132.5' r='2.2'/><circle class='pt' data-t='129' cx='389.7' cy='138.4' r='2.2'/><circle class='pt' data-t='130' cx='392.4' cy='160' r='2.2'/><circle class='pt' data-t='131' cx='395' cy='149.8' r='2.2'/><circle class='pt' data-t='132' cx='397.7' cy='132.7' r='2.2'/><circle class='pt' data-t='133' cx='400.3' cy='139.9' r='2.2'/><circle class='pt' data-t='134' cx='403' cy='79.6' r='2.2'/><circle class='pt' data-t='135' cx='405.6' cy='83.5' r='2.2'/><circle class='pt' data-t='136' cx='408.3' cy='112.9' r='2.2'/><circle class='pt' data-t='137' cx='410.9' cy='107.3' r='2.2'/><circle class='pt' data-t='138' cx='413.6' cy='115' r='2.2'/><circle class='pt' data-t='139' cx='416.2' cy='111.4' r='2.2'/><circle class='pt' data-t='140' cx='418.9' cy='127.9' r='2.2'/><circle class='pt' data-t='141' cx='421.5' cy='106.6' r='2.2'/><circle class='pt' data-t='142' cx='424.2' cy='61.5' r='2.2'/><circle class='pt' data-t='143' cx='426.8' cy='120.5' r='2.2'/><circle class='pt' data-t='144' cx='429.5' cy='93.1' r='2.2'/><circle class='pt' data-t='145' cx='432.1' cy='111.9' r='2.2'/><circle class='pt' data-t='146' cx='434.8' cy='55.2' r='2.2'/><circle class='pt' data-t='147' cx='437.4' cy='147.2' r='2.2'/><circle class='pt' data-t='148' cx='440.1' cy='85.5' r='2.2'/><circle class='pt' data-t='149' cx='442.7' cy='69.2' r='2.2'/><circle class='pt' data-t='150' cx='445.4' cy='114.4' r='2.2'/></g></svg><svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 460 214' role='img' aria-label='Correlograma: ACF de los residuales' data-panel='acf-res' font-family='Montserrat, system-ui, sans-serif' font-size='12'><text x='230' y='17' text-anchor='middle' fill='#012820' font-size='13.5' font-weight='600'>ACF de los residuales</text><rect x='48' y='30' width='400' height='144' fill='none' stroke='#cbd5e1'/><g stroke='#e2e8f0'><line class='grid-y' data-v='-0.2' x1='48' x2='448' y1='150' y2='150'/><line class='grid-y' data-v='0' x1='48' x2='448' y1='102' y2='102'/><line class='grid-y' data-v='0.2' x1='48' x2='448' y1='54' y2='54'/></g><g fill='#475569' text-anchor='end'><text class='tick-y' data-v='-0.2' x='42' y='154'>−0.2</text><text class='tick-y' data-v='0' x='42' y='106'>0</text><text class='tick-y' data-v='0.2' x='42' y='58'>0.2</text></g><g stroke='#e2e8f0'><line class='grid-x' data-v='6' x1='112.9' x2='112.9' y1='30' y2='174'/><line class='grid-x' data-v='12' x1='177.7' x2='177.7' y1='30' y2='174'/><line class='grid-x' data-v='18' x1='242.6' x2='242.6' y1='30' y2='174'/><line class='grid-x' data-v='24' x1='307.5' x2='307.5' y1='30' y2='174'/><line class='grid-x' data-v='30' x1='372.3' x2='372.3' y1='30' y2='174'/><line class='grid-x' data-v='36' x1='437.2' x2='437.2' y1='30' y2='174'/></g><g fill='#475569' text-anchor='middle'><text class='tick-x' data-v='6' x='112.9' y='189'>6</text><text class='tick-x' data-v='12' x='177.7' y='189'>12</text><text class='tick-x' data-v='18' x='242.6' y='189'>18</text><text class='tick-x' data-v='24' x='307.5' y='189'>24</text><text class='tick-x' data-v='30' x='372.3' y='189'>30</text><text class='tick-x' data-v='36' x='437.2' y='189'>36</text></g><text x='248' y='206' text-anchor='middle' fill='#475569'>Rezago (meses)</text><line class='cero' x1='48' x2='448' y1='102' y2='102' stroke='#64748b' stroke-width='1'/><line class='banda' data-v='0.16' x1='48' x2='448' y1='63.6' y2='63.6' stroke='#2563eb' stroke-width='1.3' stroke-dasharray='5 4'/><line class='banda' data-v='-0.16' x1='48' x2='448' y1='140.4' y2='140.4' stroke='#2563eb' stroke-width='1.3' stroke-dasharray='5 4'/><g stroke='#012820' stroke-width='4' stroke-linecap='butt'><line class='barra' data-k='1' x1='58.8' x2='58.8' y1='102' y2='78.5'/><line class='barra' data-k='2' x1='69.6' x2='69.6' y1='102' y2='82.2'/><line class='barra' data-k='3' x1='80.4' x2='80.4' y1='102' y2='93.9'/><line class='barra' data-k='4' x1='91.2' x2='91.2' y1='102' y2='80.7'/><line class='barra' data-k='5' x1='102.1' x2='102.1' y1='102' y2='85.3'/><line class='barra' data-k='6' x1='112.9' x2='112.9' y1='102' y2='127.3'/><line class='barra' data-k='7' x1='123.7' x2='123.7' y1='102' y2='81.3'/><line class='barra' data-k='8' x1='134.5' x2='134.5' y1='102' y2='122.4'/><line class='barra' data-k='9' x1='145.3' x2='145.3' y1='102' y2='100.2'/><line class='barra' data-k='10' x1='156.1' x2='156.1' y1='102' y2='71.5'/><line class='barra' data-k='11' x1='166.9' x2='166.9' y1='102' y2='111.5'/><line class='barra' data-k='12' x1='177.7' x2='177.7' y1='102' y2='122'/><line class='barra' data-k='13' x1='188.5' x2='188.5' y1='102' y2='120.8'/><line class='barra' data-k='14' x1='199.4' x2='199.4' y1='102' y2='94.4'/><line class='barra' data-k='15' x1='210.2' x2='210.2' y1='102' y2='113.4'/><line class='barra' data-k='16' x1='221' x2='221' y1='102' y2='132.8'/><line class='barra' data-k='17' x1='231.8' x2='231.8' y1='102' y2='118.9'/><line class='barra' data-k='18' x1='242.6' x2='242.6' y1='102' y2='96.3'/><line class='barra' data-k='19' x1='253.4' x2='253.4' y1='102' y2='107.3'/><line class='barra' data-k='20' x1='264.2' x2='264.2' y1='102' y2='114'/><line class='barra' data-k='21' x1='275' x2='275' y1='102' y2='92.4'/><line class='barra' data-k='22' x1='285.8' x2='285.8' y1='102' y2='97.2'/><line class='barra' data-k='23' x1='296.6' x2='296.6' y1='102' y2='85.7'/><line class='barra' data-k='24' x1='307.5' x2='307.5' y1='102' y2='120.5'/><line class='barra' data-k='25' x1='318.3' x2='318.3' y1='102' y2='106.3'/><line class='barra' data-k='26' x1='329.1' x2='329.1' y1='102' y2='110.8'/><line class='barra' data-k='27' x1='339.9' x2='339.9' y1='102' y2='121.8'/><line class='barra' data-k='28' x1='350.7' x2='350.7' y1='102' y2='117'/><line class='barra' data-k='29' x1='361.5' x2='361.5' y1='102' y2='105.4'/><line class='barra' data-k='30' x1='372.3' x2='372.3' y1='102' y2='113.9'/><line class='barra' data-k='31' x1='383.1' x2='383.1' y1='102' y2='103.4'/><line class='barra' data-k='32' x1='393.9' x2='393.9' y1='102' y2='96.2'/><line class='barra' data-k='33' x1='404.8' x2='404.8' y1='102' y2='118.2'/><line class='barra' data-k='34' x1='415.6' x2='415.6' y1='102' y2='115.9'/><line class='barra' data-k='35' x1='426.4' x2='426.4' y1='102' y2='79.7'/><line class='barra' data-k='36' x1='437.2' x2='437.2' y1='102' y2='89.3'/></g></svg></div><figcaption>Arriba, cada residual dividido entre la desviación estándar de todos ellos, contra el número de mes; abajo, su ACF de los rezagos 1 a 36. La banda vale ±0.16.</figcaption></figure>",
              "opciones": [
                {
                  "texto": "Los residuales se abren con el tiempo: hay que revisar la transformación.",
                  "retro": "Contra el tiempo, los residuales se abren: la dispersión del último tercio es 2.4 veces la del primero. La varianza crece con el nivel, y eso no lo arregla ningún parámetro: hay que volver a la transformación, la etapa 1 (módulos 5.1 y 5.7)."
                },
                {
                  "texto": "Queda una barra fuera de la banda en el rezago 12: falta un término estacional.",
                  "retro": "La barra del rezago 12 vale r<sub>12</sub> = −0.08, dentro de la banda ±0.16: no falta un término estacional."
                },
                {
                  "texto": "Queda una barra fuera de la banda en el rezago 1: falta un término regular.",
                  "retro": "La barra del rezago 1 vale r<sub>1</sub> = 0.10, dentro de la banda ±0.16: no falta un término regular."
                },
                {
                  "texto": "Los residuales no muestran ningún problema: el modelo puede pronosticar.",
                  "retro": "Ljung–Box no rechaza (Q = 20.94 &lt; 33.92) y ninguna barra sale de la banda, pero el panel de arriba se abre: la dispersión del último tercio es 2.4 veces la del primero. Ljung–Box mira autocorrelaciones, no la varianza (módulo 5.7)."
                }
              ],
              "correcta": 0
            },
            {
              "n": 10,
              "id": "N10",
              "etapa": 2,
              "etiqueta": "cap. 5 · mód. 5.9 · Un regresor de calendario",
              "tipo": "numero",
              "enunciado": "<p>Una red de cajeros automáticos explica el logaritmo del valor retirado cada mes con dos variables de calendario —el logaritmo del número de días del mes y una variable que vale 1 en el mes de la Semana Santa— y errores SARIMA. Las estimaciones son β̂<sub>días</sub> = 2.0094 (error estándar 0.3601) y β̂<sub>Pascua</sub> = 0.0192 (error estándar 0.0107). Si el valor retirado fuera proporcional a la duración del mes, β<sub>días</sub> valdría 1. Calcule el estadístico t para contrastar H<sub>0</sub>: β<sub>días</sub> = 1. Responda con dos decimales; si es negativo, con su signo.</p>",
              "clave": {
                "valor": 2.8,
                "tol": 0.0224,
                "texto": "2.80"
              },
              "cuenta": "t = (β̂ − 1)/e.e. = (2.0094 − 1)/0.3601 = 2.80. Como |t| &gt; 1.96, se rechaza que el valor retirado sea proporcional a los días del mes: el efecto es mayor que el de la pura duración. Contrastar contra 0 daría 5.58, que solo dice si los días importan, no si importan en proporción.",
              "rutas": [
                {
                  "valor": 5.580117,
                  "cifra": "5.58",
                  "texto": "contrastó β = 0 y no β = 1"
                },
                {
                  "valor": -2.80311,
                  "cifra": "−2.80",
                  "texto": "cambió el signo: restó β̂ de 1"
                },
                {
                  "valor": 1.0094,
                  "cifra": "1.01",
                  "texto": "no dividió entre el error estándar"
                },
                {
                  "valor": 1.794393,
                  "cifra": "1.79",
                  "texto": "usó el coeficiente de Pascua"
                }
              ]
            },
            {
              "n": 11,
              "id": "S11",
              "etapa": 2,
              "etiqueta": "cap. 5 · mód. 5.10 · Fourier con m grande",
              "tipo": "opcion",
              "enunciado": "<p>Una aseguradora tiene las llamadas semanales a su línea de atención, en cientos, de cinco años: n = 260 semanas y m = 52. Se ajustó una regresión armónica con K pares de términos de Fourier y errores AR(1), para K = 1 a 7, y un ARIMA(1,0,0)(0,1,0)<sub>52</sub>:</p><table style=\"border-collapse:collapse;margin:6px 0 12px 0;font-size:95%\"><thead><tr><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">Modelo</th><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">D</th><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">n</th><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">Términos de Fourier</th><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">AICc</th></tr></thead><tbody><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">Armónica, K = 1</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">260</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">2</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1768.74</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">Armónica, K = 2</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">260</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">4</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1744.44</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">Armónica, K = 3</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">260</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">6</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1710.07</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">Armónica, K = 4</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">260</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">8</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1674.23</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">Armónica, K = 5</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">260</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">10</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1493.47</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">Armónica, K = 6</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">260</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">12</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1496.20</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">Armónica, K = 7</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">260</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">14</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1499.73</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">ARIMA(1,0,0)(0,1,0)<sub>52</sub></td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">208</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">—</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">1324.10</td></tr></tbody></table><p>¿Qué modelo permite elegir el AICc de esta tabla?</p>",
              "opciones": [
                {
                  "texto": "La armónica con K = 1.",
                  "retro": "Con K = 1 el patrón es una sinusoide pura, y su AICc (1768.74) queda 275.27 puntos por encima del de K = 5: le faltan armónicos (módulo 5.10)."
                },
                {
                  "texto": "La armónica con K = 7.",
                  "retro": "K = 7 añade 4 términos que no compran ajuste: su AICc, 1499.73, es mayor que el de K = 5, 1493.47 (módulo 5.10)."
                },
                {
                  "texto": "La armónica con K = 5.",
                  "retro": "Dentro de la familia armónica todos tienen D = 0 y se evalúan sobre las mismas 260 semanas, así que el AICc compara: el mínimo, 1493.47, está en K = 5, con 10 términos. Esos 2K términos no dependen de m; un SARIMA con m = 52 gasta 52 datos en ∇<sub>52</sub> y su polinomio llega al rezago 52 (módulo 5.10)."
                },
                {
                  "texto": "El ARIMA(1,0,0)(0,1,0)<sub>52</sub>.",
                  "retro": "Su AICc es el menor de la tabla, pero se calcula sobre 208 semanas y no sobre 260: ∇<sub>52</sub> gasta 52 datos y las cifras no viven en la misma escala. Entre familias distintas solo decide la comparación fuera de muestra (módulos 5.10 y 5.11)."
                }
              ],
              "correcta": 2
            },
            {
              "n": 12,
              "id": "S12",
              "etapa": 2,
              "etiqueta": "cap. 5 · mód. 5.11 · Una partición o muchas",
              "tipo": "opcion",
              "enunciado": "<p>Una empresa de mensajería compara cuatro métodos para pronosticar los envíos que despacha cada mes, en miles. Sobre una sola partición —entrenar hasta diciembre de 2023 y medir en los 24 meses siguientes— obtuvo:</p><table style=\"border-collapse:collapse;margin:6px 0 12px 0;font-size:95%\"><thead><tr><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">Método</th><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">RMSE</th><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">MAE</th><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">MAPE (%)</th></tr></thead><tbody><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">SARIMA estacional</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">44.04</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">35.69</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">5.09</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">ETS sobre el log</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">44.02</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">37.70</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">5.38</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">STL + ARIMA</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">25.62</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">20.49</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">2.95</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">Naïve estacional</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">39.40</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">31.76</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">4.72</td></tr></tbody></table><p>Y repitiendo la comparación sobre 48 orígenes, con el corte cada vez un mes más adelante y el error medido en los 12 meses que le siguen:</p><table style=\"border-collapse:collapse;margin:6px 0 12px 0;font-size:95%\"><thead><tr><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">Método</th><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">RMSE medio a 12 meses</th><th style=\"border:1px solid #999;padding:3px 8px;background:#eef\">Orígenes en que es el mejor (%)</th></tr></thead><tbody><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">SARIMA estacional</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">37.89</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">8.3</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">ETS sobre el log</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">25.55</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">87.5</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">STL + ARIMA</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">37.42</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">4.2</td></tr><tr><td style=\"border:1px solid #999;padding:3px 8px;text-align:left\">Naïve estacional</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">45.02</td><td style=\"border:1px solid #999;padding:3px 8px;text-align:right\">0.0</td></tr></tbody></table><p>¿Con qué método conviene pronosticar los próximos 12 meses?</p>",
              "opciones": [
                {
                  "texto": "Con el SARIMA estacional.",
                  "retro": "No es el mejor ni en la partición única ni sobre los 48 orígenes, donde su RMSE medio es 37.89 frente a 25.55 (módulo 5.11)."
                },
                {
                  "texto": "Con el ETS sobre el log.",
                  "retro": "Sobre 48 orígenes, con el horizonte (12 meses) y la métrica (RMSE) fijados de antemano, el ETS sobre el log tiene el menor error medio, 25.55, y es el mejor en el 87.5 % de los orígenes. La partición única la gana el STL + ARIMA, pero una sola partición depende de dónde cae el corte (módulo 5.11)."
                },
                {
                  "texto": "Con el STL + ARIMA.",
                  "retro": "Gana las tres métricas de la partición única, pero con una sola partición el azar de dónde cae el corte pesa más que la diferencia entre los métodos. Sobre 48 orígenes su RMSE medio es 37.42, por encima del de el ETS sobre el log, 25.55 (módulo 5.11)."
                },
                {
                  "texto": "Con el naïve estacional.",
                  "retro": "No es el mejor ni en la partición única ni sobre los 48 orígenes, donde su RMSE medio es 45.02 frente a 25.55 (módulo 5.11)."
                }
              ],
              "correcta": 1
            }
          ]
        }
      ]
    };
    // [fin · simulacro del quiz]
