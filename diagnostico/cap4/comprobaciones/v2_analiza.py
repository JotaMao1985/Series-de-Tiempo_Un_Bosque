import json,sys,re
d=json.load(open('v2_medidas.json'))
E=d['estados']
def gr(ancho,clave): return E[ancho][clave]['graficos']
def ejes(g): return {e['id']:e for e in g.get('escalas',[])}
if __name__=='__main__':
    # M6 ΔAICc
    for ancho in ['1200','800','375']:
        print('=====',ancho)
        for k,v in E[ancho].items():
            if not k.startswith('explorador-modelos:pdq'): continue
            g=v['graficos'][1]
            ex=ejes(g)
            ejeCat = ex['x'] if g['tipo']=='bar' and 'x' in ex and ex['x']['type']=='category' else ex.get('y')
            cat=[e for e in g['escalas'] if e['type']=='category'][0]
            print(k[-3:], 'area',g['area']['w'],'x',g['area']['h'],'leyenda',g['legend']['lineas'],[ (i['text'],i['fill']) for i in g['legend']['items']], 'cat',cat['id'],cat.get('nCategorias'),'rotulados',cat.get('nRotulados'),'nTicks',cat['nTicks'], cat['ticks'][:10] if ancho=='1200' and k.endswith(('021','020','122')) else '')
