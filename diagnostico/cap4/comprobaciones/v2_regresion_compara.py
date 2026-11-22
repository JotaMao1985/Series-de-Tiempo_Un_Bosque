import json,glob,collections
def carga(et,cap,an): return json.load(open(f'v2_regresion_{et}-cap{cap}-{an}.json'))
tot=collections.Counter()
formas=collections.defaultdict(set)
for cap in ['2','3','5','6']:
    for an in ['1200','375']:
        n=carga('nuevo',cap,an); v=carga('viejo',cap,an)
        ev=[e['txt'] for e in n['eventos']+v['eventos'] if 'favicon' not in e['txt'] and 'getImageData' not in e['txt']]
        print(f'--- cap{cap} {an}: eventos de consola (sin favicon ni mi sonda): {ev}')
        nn=0; dif=[]
        for m,estn in n['modulos'].items():
            estv=v['modulos'][m]
            if set(estn)!=set(estv): dif.append((m,'estados distintos',set(estn)^set(estv)))
            for est,lienzosN in estn.items():
                lienzosV=estv.get(est)
                if lienzosV is None: continue
                if len(lienzosN)!=len(lienzosV): dif.append((m,est,'nº lienzos',len(lienzosV),len(lienzosN))); continue
                for a,b in zip(lienzosV,lienzosN):
                    nn+=1
                    clave=(cap,an,m,est,a['i'])
                    if b.get('sinChart') or a.get('sinChart'):
                        if a.get('sinChart')!=b.get('sinChart'): dif.append((m,est,a['i'],'sinChart',a.get('sinChart'),b.get('sinChart')))
                        continue
                    if a['nDatasets']!=b['nDatasets']: dif.append((m,est,a['i'],'nDatasets',a['nDatasets'],b['nDatasets']))
                    ta=[x['text'] for x in a['legend']['items']]; tb=[x['text'] for x in b['legend']['items']]
                    if ta!=tb: dif.append((m,est,a['i'],'LEYENDA texto',ta,tb))
                    if a['legend']['display']!=b['legend']['display']: dif.append((m,est,a['i'],'legend.display',a['legend']['display'],b['legend']['display']))
                    # en blanco
                    if isinstance(b['tinta'],(int,float)) and b['tinta']<0.003: dif.append((m,est,a['i'],'TINTA baja',a['tinta'],b['tinta']))
                    if isinstance(b['tintaArea'],(int,float)) and a['tintaArea']>0 and b['tintaArea']<0.5*a['tintaArea']: dif.append((m,est,a['i'],'TINTA area cae',a['tintaArea'],b['tintaArea']))
                    if abs(a['area']['h']-b['area']['h'])>0.5 or abs(a['area']['w']-b['area']['w'])>0.5: dif.append((m,est,a['i'],'area',a['area'],b['area']))
                    if a['aria']!=b['aria']: dif.append((m,est,a['i'],'aria distinto'))
                    for x,y in zip(a['legend']['items'],b['legend']['items']):
                        formas[(cap,y['text'][:30] if False else None)]
                    # formas nuevas
                    for it,ds in zip(b['legend']['items'],range(len(b['legend']['items']))):
                        pass
                    for it in b['legend']['items']:
                        formas[(cap, a.get('tipo'))].add((it['text'][:34], it.get('ps'), str(it.get('dash'))))
        print(f'   comparados {nn} lienzos/estados; diferencias: {len(dif)}')
        cuenta=collections.Counter(d[3] if len(d)>3 else d[1] for d in dif)
        print('   tipos de diferencia:',dict(cuenta))
        for d in dif:
            if len(d)>3 and d[3] in ('LEYENDA texto','nDatasets','TINTA baja','TINTA area cae','sinChart','legend.display'): print('     ',d)
            elif len(d)<=3 or d[1]=='estados distintos' or d[1]=='nº lienzos': print('     ',d)
json.dump({f'{k[0]}|{k[1]}':sorted(v) for k,v in formas.items() if k[1]}, open('v2_regresion_formas.json','w'), ensure_ascii=False, indent=1)
