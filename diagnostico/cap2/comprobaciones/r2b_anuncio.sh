#!/bin/sh
# R2b · el anuncio de las lecturas: nada al cargar; una sola vez tras una ráfaga de 12 pasos del
# deslizador; la lectura visible cambia en cada paso. Capítulos 2 (M5), 3 (M5) y 5 (M2).
cd "$(dirname "$0")"
EXPR='(async () => {
  const region = document.getElementById("anuncio-lectura");
  const alCargar = region ? region.textContent : "(sin región)";
  let anuncios = 0, visibles = 0;
  new MutationObserver(() => anuncios++).observe(region, { childList: true, characterData: true, subtree: true });
  const raiz = [...document.querySelectorAll("[data-simulador]")].find(s => s.querySelector("input[type=range]") && s.querySelector(".simulador-lectura"));
  const lectura = raiz.querySelector(".simulador-lectura");
  new MutationObserver(() => visibles++).observe(lectura, { childList: true });
  const d = raiz.querySelector("input[type=range]");
  const paso = Number(d.step) || 1;
  for (let k = 0; k < 12; k++) { d.value = Number(d.min) + k * paso; d.dispatchEvent(new Event("input", { bubbles: true })); await new Promise(r => setTimeout(r, 30)); }
  const durante = anuncios;
  await new Promise(r => setTimeout(r, 1200));
  return { simulador: raiz.dataset.simulador, regionAlCargar: alCargar, lecturaAriaLive: lectura.getAttribute("aria-live"),
    cambiosVisibles: visibles, anunciosDuranteLaRafaga: durante, anunciosTrasLaPausa: anuncios,
    anuncio: region.textContent.slice(0, 160), igualQueLaLectura: region.textContent.replace(/[;\s]/g, "") === lectura.textContent.replace(/\s/g, ""),
    desbordePagina: document.documentElement.scrollWidth - window.innerWidth };
})()'
for par in "2 5" "3 5" "5 2"; do set -- $par; echo "== capítulo $1, módulo $2"; PUERTO=9276 node r2b_sonda.js $1 $2 1200 "$EXPR"; done
