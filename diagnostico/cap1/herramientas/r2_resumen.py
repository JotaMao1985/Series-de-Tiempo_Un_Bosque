import json,sys
d=json.load(open(sys.argv[1]))
print('eventos:',d['medidas'].get('eventos'))
for modo,mm in d['medidas'].items():
    if modo=='eventos': continue
    for n,m in mm.items():
        desb=[x for x in m['desbordan'] if x['tag'] not in ('path','math','semantics','SPAN','CODE','THEAD','TBODY','mrow','annotation')]
        print(f"{modo} M{n} docSw={m['docSw']} main={m['mainW']} desbordan(no fórmula/código/tabla)={desb} katex={[(k['sw'],k['contCw']) for k in m['katex']]} mapa={m['mapa']} par={[(p['cw'],p['sw'],p['cols']) for p in m['par']]}")
        print('   h4:',[(h['disp'],h['h']) for h in m['h4']])
        for c in m['canv']:
            ex=[e for e in c['escalas'] if e['id']=='x'][0]; ey=[e for e in c['escalas'] if e['id']=='y'][0]
            mal=[]
            if ex['pisan']: mal.append('PISAN')
            if c['fueraDeCaja']: mal.append('FUERA')
            if not ey['title']: mal.append('SIN-TITULO-Y')
            print(f"   {c['sim']}#{c['i']} area={c['area']['w']}x{c['area']['h']} x:{ex['ticks'][:13]} y[{ey['title']}]:{ey['ticks']} ley={c['legend']['display'] and c['legend']['items']} {' '.join(mal)}")
        for l in m['lecturas']: print('   lectura',l['sim'],'live=',l['live'],'|',l['txt'][:90])
