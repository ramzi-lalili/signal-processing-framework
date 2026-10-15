from dataclasses import dataclass, field
import numpy as np

@dataclass
class Signal:
    time: np.ndarray
    values: np.ndarray
    name: str = "Signal"
    sampling_rate: float | None = None
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        self.time = np.asarray(self.time, dtype=float)
        self.values = np.asarray(self.values)
        if self.time.ndim != 1 or self.values.ndim != 1:
            raise ValueError("Signal time and values must be 1-D arrays.")
        if len(self.time) != len(self.values):
            raise ValueError("time and values must have the same length.")
        if len(self.time) == 0:
            raise ValueError("Signal cannot be empty.")

    @property
    def dt(self):
        if len(self.time) < 2:
            return 0.0
        return float(np.mean(np.diff(self.time)))

    @property
    def duration(self):
        return float(self.time[-1] - self.time[0]) if len(self.time) > 1 else 0.0

    def copy(self, name=None, values=None, time=None, metadata=None):
        return Signal(
            self.time.copy() if time is None else time,
            self.values.copy() if values is None else values,
            self.name if name is None else name,
            self.sampling_rate,
            {**self.metadata, **(metadata or {})},
        )

    def describe(self):
        return f"{self.name}: {len(self.values)} samples, Fs={self.sampling_rate or (1/self.dt if self.dt else 0):.3g} Hz"
