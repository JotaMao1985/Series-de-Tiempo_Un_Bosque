"""v4_software.py — verificador independiente de la R4 del capítulo 2.
acf(adjusted=False) con divisor T; pacf ywm y ldb frente a Durbin-Levinson; y
la regresión MCO (método 'ols') para ver si «ajustar la regresión equivale a
Yule-Walker» se cumple con datos. Salida: v4_software_py.out"""
import numpy as np, statsmodels
from statsmodels.datasets import get_rdataset
from statsmodels.tsa.stattools import acf, pacf
y = np.log(np.array([112,118,132,129,121,135,148,148,136,119,104,118,115,126,141,135,125,149,170,170,158,133,114,140,145,150,178,163,172,178,199,199,184,162,146,166,171,180,193,181,183,218,230,242,209,191,172,194,196,196,236,235,229,243,264,272,237,211,180,201,204,188,235,227,234,264,302,293,259,229,203,229,242,233,267,269,270,315,364,347,312,274,237,278,284,277,317,313,318,374,413,405,355,306,271,306,315,301,356,348,355,422,465,467,404,347,305,336,340,318,362,348,363,435,491,505,404,359,310,337,360,342,406,396,420,472,548,559,463,407,362,405,417,391,419,461,472,535,622,606,508,461,390,432],float))
print("statsmodels", statsmodels.__version__, "· T =", len(y))
T=len(y); m=y.mean()
g=lambda k: np.sum((y[:T-k]-m)*(y[k:]-m))/T
r=np.array([g(k)/g(0) for k in range(1,25)])
print("max|acf(adjusted=False) - divisor T| =", np.max(np.abs(acf(y,nlags=24,adjusted=False)[1:]-r)))
def dl(r):
    K=len(r); phi=np.zeros((K+1,K+1)); out=[]
    phi[1,1]=r[0]; out.append(r[0])
    for k in range(2,K+1):
        j=np.arange(1,k)
        phi[k,k]=(r[k-1]-np.sum(phi[k-1,j]*r[k-1-j]))/(1-np.sum(phi[k-1,j]*r[j-1]))
        phi[k,j]=phi[k-1,j]-phi[k,k]*phi[k-1,k-j]; out.append(phi[k,k])
    return np.array(out)
d=dl(r)
for meth in ("ywm","ldb","ols"):
    p=pacf(y,nlags=24,method=meth)[1:]
    print(f"max|pacf({meth}) - DL| =", np.max(np.abs(p-d)))
