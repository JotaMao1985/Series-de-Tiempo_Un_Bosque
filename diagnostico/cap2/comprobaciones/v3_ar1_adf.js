// Serie del simulador del M5 (mismo generador y semilla) para phi = 0.95 y 1, en CSV para R.
function generarRuidoNormal(n, semilla) { let estado = semilla >>> 0;
  function uniforme() { estado |= 0; estado = (estado + 0x6D2B79F5) | 0;
    let t = Math.imul(estado ^ (estado >>> 15), 1 | estado); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }
  const r = []; for (let i = 0; i < n; i++) { const u1 = Math.max(uniforme(), 1e-12), u2 = uniforme();
    r.push(Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2)); } return r; }
const e = generarRuidoNormal(200, 20260726);
const sim = phi => { const y = [e[0]]; for (let t = 1; t < 200; t++) y.push(phi * y[t - 1] + e[t]); return y; };
const a = sim(0.95), b = sim(1);
console.log('phi095,phi1'); a.forEach((v, i) => console.log(v + ',' + b[i]));
