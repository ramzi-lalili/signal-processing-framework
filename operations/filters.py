import numpy as np
from scipy import signal as sp_signal
from core.registry import register_operation

class Butterworth:
    kind = "lowpass"
    def apply(self, a, cutoff=100.0, order=4, **_):
        fs = a.sampling_rate
        if not fs: raise ValueError("Sampling rate is required.")
        if cutoff <= 0 or cutoff >= fs/2: raise ValueError("Cutoff must be between 0 and Nyquist frequency.")
        sos = sp_signal.butter(int(order), cutoff, btype=self.kind, fs=fs, output="sos")
        try:
            y = sp_signal.sosfiltfilt(sos, a.values)
        except ValueError:
            y = sp_signal.sosfilt(sos, a.values)
        return a.copy(name=f"{self.kind}({a.name})", values=y,
                      metadata={"operation":self.kind,"cutoff":cutoff,"order":order})

class LowPass(Butterworth): kind="lowpass"
class HighPass(Butterworth): kind="highpass"

class BandFilter:
    kind="bandpass"
    def apply(self,a,low=10.0,high=100.0,order=4,**_):
        fs=a.sampling_rate
        if not fs: raise ValueError("Sampling rate is required.")
        if not (0<low<high<fs/2): raise ValueError("Require 0 < low < high < Nyquist.")
        sos=sp_signal.butter(int(order),[low,high],btype=self.kind,fs=fs,output="sos")
        try:
            y=sp_signal.sosfiltfilt(sos,a.values)
        except ValueError:
            y=sp_signal.sosfilt(sos,a.values)
        return a.copy(name=f"{self.kind}({a.name})",values=y,
                      metadata={"operation":self.kind,"low":low,"high":high,"order":order})
class BandPass(BandFilter): kind="bandpass"
class BandStop(BandFilter): kind="bandstop"

register_operation("Low-Pass Filter", LowPass)
register_operation("High-Pass Filter", HighPass)
register_operation("Band-Pass Filter", BandPass)
register_operation("Band-Stop Filter", BandStop)
