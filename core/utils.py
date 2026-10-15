import numpy as np

def make_time(duration, fs):
    if duration <= 0 or fs <= 0:
        raise ValueError("Duration and sampling rate must be positive.")
    n = int(round(duration * fs))
    n = max(n, 2)
    return np.arange(n) / fs

def same_grid(a, b, tol=1e-9):
    return (
        len(a.time) == len(b.time)
        and np.isclose(a.sampling_rate, b.sampling_rate, rtol=tol, atol=tol)
        and np.allclose(a.time, b.time, rtol=tol, atol=tol)
    )

def require_same_grid(a, b):
    if not same_grid(a, b):
        raise ValueError("Signals must have the same time grid and sampling rate.")
