import numpy as np

# numpy.roots recibe los coeficientes en orden DESCENDENTE de potencia,
# justo al reves que polyroot() de R: hay que invertir el vector.
phi = np.array([1.4, -0.75])
coef = np.r_[1.0, -phi]              # [1, -phi1, -phi2] en orden ascendente
raices = np.roots(coef[::-1])        # se invierte para numpy

print(raices)
print(np.abs(raices))                # modulo
print(bool(np.all(np.abs(raices) > 1)))

# statsmodels lo hace directamente y con el convenio correcto
from statsmodels.tsa.arima_process import ArmaProcess
proceso = ArmaProcess(np.r_[1, -phi], np.r_[1])
print(proceso.arroots, proceso.isstationary)