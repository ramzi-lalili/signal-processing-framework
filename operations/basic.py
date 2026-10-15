import numpy as np
from scipy import integrate, signal as sp_signal
from core.signal import Signal
from core.registry import register_operation
from core.utils import require_same_grid

class Amplify:
    def apply(self, a, gain=2.0, **_):
        return a.copy(name=f"{a.name} × {gain:g}", values=a.values*gain,
                      metadata={"operation":"amplification","gain":gain})
register_operation("Amplification", Amplify)

class Add:
    def apply(self, a, b, **_):
        require_same_grid(a,b)
        return a.copy(name=f"{a.name} + {b.name}", values=a.values+b.values,
                      metadata={"operation":"addition","inputs":[a.name,b.name]})
register_operation("Addition", Add)

class Multiply:
    def apply(self, a, b, **_):
        require_same_grid(a,b)
        return a.copy(name=f"{a.name} × {b.name}", values=a.values*b.values,
                      metadata={"operation":"multiplication","inputs":[a.name,b.name]})
register_operation("Multiplication", Multiply)

class Convolution:
    def apply(self, a, b, mode="full", **_):
        y = sp_signal.convolve(a.values, b.values, mode=mode)
        dt = a.dt if a.dt else 1.0
        t = np.arange(len(y))*dt
        return Signal(t,y,f"conv({a.name},{b.name})",a.sampling_rate,{"operation":"convolution"})
register_operation("Convolution", Convolution)

class Correlation:
    def apply(self, a, b, mode="full", **_):
        require_same_grid(a,b)
        y = sp_signal.correlate(a.values,b.values,mode=mode)
        lags = sp_signal.correlation_lags(len(a.values),len(b.values),mode=mode)
        return Signal(lags*a.dt,y,f"corr({a.name},{b.name})",a.sampling_rate,{"operation":"correlation"})
register_operation("Correlation", Correlation)

class Differentiate:
    def apply(self, a, **_):
        y = np.gradient(a.values, a.time)
        return a.copy(name=f"d/dt({a.name})",values=y,metadata={"operation":"differentiation"})
register_operation("Differentiation", Differentiate)

class Integrate:
    def apply(self, a, initial=0.0, **_):
        y = initial + integrate.cumulative_trapezoid(a.values,a.time,initial=0)
        return a.copy(name=f"∫({a.name})dt",values=y,metadata={"operation":"integration"})
register_operation("Integration", Integrate)

class Sample:
    def apply(self, a, new_fs=100.0, **_):
        if new_fs <= 0: raise ValueError("Sampling rate must be positive.")
        step = max(1, int(round((1/a.sampling_rate)/ (1/new_fs)))) if a.sampling_rate else 1
        idx = np.arange(0,len(a.values),step)
        return Signal(a.time[idx],a.values[idx],f"{a.name} sampled",new_fs,{"operation":"sampling"})
register_operation("Sampling", Sample)

class LinearReconstruct:
    def apply(self, a, output_fs=1000.0, **_):
        t = np.arange(a.time[0],a.time[-1]+1/output_fs/2,1/output_fs)
        y = np.interp(t,a.time,a.values)
        return Signal(t,y,f"{a.name} reconstructed",output_fs,{"operation":"linear reconstruction"})
register_operation("Linear Reconstruction", LinearReconstruct)
