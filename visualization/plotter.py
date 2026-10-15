from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class PlotCanvas(FigureCanvas):
    def __init__(self):
        self.figure=Figure(figsize=(8,5),tight_layout=True)
        super().__init__(self.figure)
        self.ax=self.figure.add_subplot(111)

    def plot(self, signal, title=None):
        self.ax.clear()
        self.ax.plot(signal.time, signal.values, linewidth=1.2)
        self.ax.set_title(title or signal.name)
        self.ax.set_xlabel("Time / X")
        self.ax.set_ylabel("Amplitude / Magnitude")
        self.ax.grid(True, alpha=0.3)
        self.figure.tight_layout()
        self.draw()

    def compare(self, signals):
        self.ax.clear()
        for s in signals:
            self.ax.plot(s.time,s.values,label=s.name,linewidth=1.1)
        self.ax.set_xlabel("Time / X")
        self.ax.set_ylabel("Amplitude")
        self.ax.grid(True,alpha=0.3)
        self.ax.legend()
        self.figure.tight_layout()
        self.draw()
