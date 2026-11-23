import warnings; warnings.filterwarnings("ignore")
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
nilo = sm.datasets.nile.load_pandas().data["volume"].values
m = ARIMA(nilo, order=(1,1,1), trend="n")
print("inicialización del espacio de estados:", m.ssm.initialization.initialization_type if m.ssm.initialization is not None else None)
print("loglikelihood_burn:", m.ssm.loglikelihood_burn, " · k_diffuse_states:", getattr(m.ssm, "k_diffuse_states", None))
