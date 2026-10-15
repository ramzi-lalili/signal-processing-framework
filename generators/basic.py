import numpy as np
from scipy import signal as sp_signal
from core.signal import Signal
from core.registry import register_generator
from core.utils import make_time

class BaseGenerator:
    def generate(self, **kwargs):
        raise NotImplementedError

class DCGenerator(BaseGenerator):
    def generate(self, amplitude=1.0, duration=1.0, fs=1000.0, **_):
        t = make_time(duration, fs)
        return Signal(t, np.full(len(t), amplitude), "DC", fs, {"generator":"DC","amplitude":amplitude})
register_generator("DC", DCGenerator)

class SineGenerator(BaseGenerator):
    def generate(self, amplitude=1.0, frequency=10.0, phase=0.0, offset=0.0, duration=1.0, fs=1000.0, **_):
        t = make_time(duration, fs)
        y = offset + amplitude*np.sin(2*np.pi*frequency*t + np.deg2rad(phase))
        return Signal(t, y, "Sine", fs, {"generator":"Sine","frequency":frequency})
register_generator("Sine / AC", SineGenerator)

class DeltaGenerator(BaseGenerator):
    def generate(self, amplitude=1.0, duration=1.0, fs=1000.0, **_):
        t = make_time(duration, fs); y = np.zeros_like(t); y[0] = amplitude
        return Signal(t, y, "Dirac", fs, {"generator":"Dirac"})
register_generator("Dirac Delta", DeltaGenerator)

class RampGenerator(BaseGenerator):
    def generate(self, slope=1.0, offset=0.0, duration=1.0, fs=1000.0, **_):
        t = make_time(duration, fs)
        return Signal(t, offset+slope*t, "Ramp", fs, {"generator":"Ramp","slope":slope})
register_generator("Ramp", RampGenerator)

class SignGenerator(BaseGenerator):
    def generate(self, amplitude=1.0, frequency=1.0, duration=1.0, fs=1000.0, **_):
        t = make_time(duration, fs)
        y = amplitude*np.sign(np.sin(2*np.pi*frequency*t))
        return Signal(t, y, "Sign", fs, {"generator":"Sign"})
register_generator("Sign", SignGenerator)

class SquareGenerator(BaseGenerator):
    def generate(self, amplitude=1.0, frequency=10.0, duty=50.0, duration=1.0, fs=1000.0, **_):
        t = make_time(duration, fs)
        y = amplitude*sp_signal.square(2*np.pi*frequency*t, duty=duty/100.0)
        return Signal(t, y, "Square", fs, {"generator":"Square"})
register_generator("Square", SquareGenerator)

class TriangleGenerator(BaseGenerator):
    def generate(self, amplitude=1.0, frequency=10.0, duration=1.0, fs=1000.0, **_):
        t = make_time(duration, fs)
        y = amplitude*sp_signal.sawtooth(2*np.pi*frequency*t, width=0.5)
        return Signal(t, y, "Triangle", fs, {"generator":"Triangle"})
register_generator("Triangle", TriangleGenerator)

class ChirpGenerator(BaseGenerator):
    def generate(self, amplitude=1.0, f0=5.0, f1=100.0, duration=1.0, fs=1000.0, **_):
        t = make_time(duration, fs)
        y = amplitude*sp_signal.chirp(t, f0=f0, f1=f1, t1=duration, method="linear")
        return Signal(t, y, "Chirp", fs, {"generator":"Chirp","f0":f0,"f1":f1})
register_generator("Chirp", ChirpGenerator)

class NoiseGenerator(BaseGenerator):
    def generate(self, amplitude=1.0, duration=1.0, fs=1000.0, seed=1, **_):
        t = make_time(duration, fs)
        rng = np.random.default_rng(int(seed))
        y = amplitude*rng.standard_normal(len(t))
        return Signal(t, y, "White Noise", fs, {"generator":"Noise","seed":seed})
register_generator("White Noise", NoiseGenerator)
