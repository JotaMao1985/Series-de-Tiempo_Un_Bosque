import re, html, subprocess, sys, os
src=open(sys.argv[1],encoding="utf-8").read()
NUM=re.compile(r'-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?')
for m in re.finditer(r'<div class="ejercicio-panel solucion" id="(c2[^"]+)"[^>]*>(.*?)\n          </div>', src, re.S):
    pid, body = m.group(1), m.group(2)
    for k,code in enumerate(re.findall(r'<pre><code class="language-r">(.*?)</code></pre>', body, re.S)):
        code=html.unescape(code)
        if pid=="c2e4-sol": continue
        f=f"blk_{pid}_{k}.R"; open(f,"w").write(code)
        r=subprocess.run(["Rscript",f],capture_output=True,text=True,timeout=300)
        out=r.stdout+r.stderr
        exp=[]
        for l in code.splitlines():
            s=l.strip()
            if s.startswith("#>"): exp+=NUM.findall(s[2:])
        got=set(NUM.findall(out))
        miss=[e for e in exp if e not in got]
        print(pid,k,"rc",r.returncode,"esperados",len(exp),"faltan",miss[:10])
        if r.returncode: print(out[-800:])
