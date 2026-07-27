    // ================================================================
    // Componente .ciclo — diagrama de etapas recorrible
    // ================================================================
    // Cada `<div class="ciclo">` lleva una lista `role="tablist"` de
    // botones `.ciclo-boton` con aria-controls apuntando a su panel. Se
    // muestra una etapa a la vez; las flechas del teclado recorren el
    // ciclo (y dan la vuelta al llegar al final, que es justo lo que hace
    // el procedimiento que representa).
    function iniciarCiclos() {
      mainContent.querySelectorAll('.ciclo').forEach(raiz => {
        const botones = Array.from(raiz.querySelectorAll('.ciclo-boton'));
        const paneles = botones.map(b => document.getElementById(b.getAttribute('aria-controls')));
        if (!botones.length || paneles.some(p => !p)) return;

        function seleccionar(i, moverFoco) {
          botones.forEach((boton, j) => {
            const activo = j === i;
            boton.setAttribute('aria-selected', String(activo));
            boton.tabIndex = activo ? 0 : -1;
            paneles[j].hidden = !activo;
          });
          katexEn(paneles[i]);
          if (moverFoco) botones[i].focus();
        }

        botones.forEach((boton, i) => {
          boton.addEventListener('click', () => seleccionar(i, false));
          boton.addEventListener('keydown', evento => {
            const paso = (evento.key === 'ArrowRight' || evento.key === 'ArrowDown') ? 1
              : (evento.key === 'ArrowLeft' || evento.key === 'ArrowUp') ? -1 : 0;
            if (paso === 0) return;
            evento.preventDefault();
            seleccionar((i + paso + botones.length) % botones.length, true);
          });
        });

        const inicial = botones.findIndex(b => b.getAttribute('aria-selected') === 'true');
        seleccionar(inicial >= 0 ? inicial : 0, false);
      });
    }

