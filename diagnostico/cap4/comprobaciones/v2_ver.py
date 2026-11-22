import json,sys
d=json.load(open('v2_medidas.json'))
E=d['estados']
def show(sim, estados, anchos=('1200','800','375'), canv=None, ejes=True, puntos=False):
    for ancho in anchos:
        for est in estados:
            v=E[ancho].get(f'{sim}:{est}')
            if not v: print('FALTA',ancho,est); continue
            for i,g in enumerate(v['graficos']):
                if canv is not None and i not in canv: continue
                ex={e['id']:e for e in g['escalas']}
                print(f"[{ancho}] {est} c{i} {g['w']}x{g['h']} area {g['area']['w']}x{g['area']['h']} leyenda {g['legend']['lineas']}l h{g['legend']['h']}")
                if ejes:
                    for k,e in ex.items():
                        print(f"    {k} {e['type']} [{e['min']},{e['max']}] ticks {e['ticks']} rot {e['rot']} gap {e.get('minGap')} sol {e.get('solapes')} fuera {e.get('fuera')} guion {e['guion']}")
                if puntos:
                    for p in g['puntos']:
                        print('    puntos',p['label'],'clip',p['clip'],'n',p['n'],'pasan',p['pasan'], p.get('todos'))
if __name__=='__main__':
    sim=sys.argv[1]; est=sys.argv[2].split(','); an=sys.argv[3].split(',') if len(sys.argv)>3 else ('1200','800','375')
    canv=[int(x) for x in sys.argv[4].split(',')] if len(sys.argv)>4 and sys.argv[4] else None
    show(sim,est,an,canv,puntos=len(sys.argv)>5)
