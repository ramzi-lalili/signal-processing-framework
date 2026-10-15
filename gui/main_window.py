import sys
from PySide6.QtWidgets import (
    QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QFormLayout,
    QPushButton,QComboBox,QDoubleSpinBox,QListWidget,QLabel,QGroupBox,
    QMessageBox,QSplitter,QLineEdit
)
from PySide6.QtCore import Qt
from core.registry import GENERATORS, OPERATIONS
import generators, operations
from visualization.plotter import PlotCanvas

def dbl(value=1.0, minimum=-1e9, maximum=1e9, decimals=4):
    w=QDoubleSpinBox()
    w.setRange(minimum,maximum); w.setDecimals(decimals); w.setValue(value)
    w.setSingleStep(0.1)
    return w

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signal Processing Framework")
        self.resize(1400,820)
        self.signals={}
        self.build_ui()

    def build_ui(self):
        root=QWidget(); main=QHBoxLayout(root)
        left=QVBoxLayout(); center=QVBoxLayout(); right=QVBoxLayout()

        genbox=QGroupBox("1. Signal Generator"); gl=QFormLayout(genbox)
        self.gen_type=QComboBox(); self.gen_type.addItems(GENERATORS.keys())
        gl.addRow("Type",self.gen_type)
        self.g_amp=dbl(1); self.g_freq=dbl(10,0); self.g_phase=dbl(0,-360,360)
        self.g_fs=dbl(1000,1); self.g_dur=dbl(1,0.001)
        gl.addRow("Amplitude",self.g_amp); gl.addRow("Frequency",self.g_freq)
        gl.addRow("Phase (deg)",self.g_phase); gl.addRow("Sampling Fs",self.g_fs)
        gl.addRow("Duration (s)",self.g_dur)
        b=QPushButton("Generate Signal"); b.clicked.connect(self.generate); gl.addRow(b)
        left.addWidget(genbox)

        sigbox=QGroupBox("Signals"); sl=QVBoxLayout(sigbox)
        self.sig_list=QListWidget(); self.sig_list.currentTextChanged.connect(self.show_selected)
        sl.addWidget(self.sig_list)
        left.addWidget(sigbox,1)

        opbox=QGroupBox("2. Processing Operation"); ol=QFormLayout(opbox)
        self.op_type=QComboBox(); self.op_type.addItems(OPERATIONS.keys())
        self.op_type.currentTextChanged.connect(self.update_op_ui)
        ol.addRow("Operation",self.op_type)

        self.input2=QComboBox()
        ol.addRow("Second input",self.input2)

        self.param1=dbl(100,0,1e9); ol.addRow("Parameter 1",self.param1)
        self.param2=dbl(50,0,1e9); ol.addRow("Parameter 2",self.param2)

        self.window=QComboBox()
        self.window.addItems(["Rectangular","Hann","Hamming","Blackman","Kaiser"])
        ol.addRow("FFT window",self.window)

        ob=QPushButton("Apply Operation"); ob.clicked.connect(self.apply_operation); ol.addRow(ob)
        left.addWidget(opbox)

        self.canvas=PlotCanvas(); center.addWidget(self.canvas,1)
        self.info=QLabel("Generate or select a signal."); self.info.setWordWrap(True)
        center.addWidget(self.info)

        viewbox=QGroupBox("3. Visualization"); vl=QVBoxLayout(viewbox)
        c=QPushButton("Plot All Signals"); c.clicked.connect(self.compare_all); vl.addWidget(c)
        cl=QPushButton("Clear All"); cl.clicked.connect(self.clear_all); vl.addWidget(cl)
        right.addWidget(viewbox); right.addStretch()

        split=QSplitter(Qt.Horizontal)
        for layout in (left,center,right):
            w=QWidget(); w.setLayout(layout); split.addWidget(w)
        split.setSizes([390,760,200])
        main.addWidget(split); self.setCentralWidget(root)
        self.update_op_ui(self.op_type.currentText())

    def refresh_inputs(self):
        current=self.input2.currentText()
        self.input2.clear()
        self.input2.addItems(self.signals.keys())
        if current in self.signals: self.input2.setCurrentText(current)

    def generate(self):
        try:
            cls=GENERATORS[self.gen_type.currentText()]
            s=cls().generate(
                amplitude=self.g_amp.value(), frequency=self.g_freq.value(),
                phase=self.g_phase.value(), duration=self.g_dur.value(),
                fs=self.g_fs.value()
            )
            base=s.name; i=1; name=base
            while name in self.signals:
                i+=1; name=f"{base}_{i}"
            s.name=name; self.signals[name]=s
            self.sig_list.addItem(name); self.refresh_inputs()
            self.sig_list.setCurrentRow(self.sig_list.count()-1)
        except Exception as e:
            QMessageBox.critical(self,"Generation error",str(e))

    def show_selected(self,name):
        if name in self.signals:
            s=self.signals[name]
            self.canvas.plot(s)
            fs=s.sampling_rate or 0
            self.info.setText(
                f"<b>{s.name}</b><br>"
                f"Samples: {len(s.values)}<br>"
                f"Sampling rate: {fs:.6g} Hz<br>"
                f"Duration: {s.duration:.6g} s<br>"
                f"Min/Max: {s.values.min():.6g} / {s.values.max():.6g}"
            )

    def update_op_ui(self,name):
        self.param1.setValue(100.0)
        self.param2.setValue(50.0)
        self.window.setEnabled(name=="FFT")
        self.input2.setEnabled(name in {"Addition","Multiplication","Convolution","Correlation"})
        if name=="Amplification": self.param1.setValue(2.0)
        elif name in {"Low-Pass Filter","High-Pass Filter"}: self.param1.setValue(100.0)
        elif name in {"Band-Pass Filter","Band-Stop Filter"}:
            self.param1.setValue(10.0); self.param2.setValue(100.0)
        elif name=="Sampling": self.param1.setValue(100.0)
        elif name=="Integration": self.param1.setValue(0.0)
        elif name in {"AM Modulation","AM Demodulation"}:
            self.param1.setValue(1000.0); self.param2.setValue(100.0)

    def apply_operation(self):
        item=self.sig_list.currentItem()
        if not item: return
        name=item.text()
        opname=self.op_type.currentText()
        try:
            op=OPERATIONS[opname]()
            a=self.signals[name]
            p1=self.param1.value(); p2=self.param2.value()
            binary={"Addition","Multiplication","Convolution","Correlation"}
            if opname in binary:
                other=self.input2.currentText()
                if other not in self.signals: raise ValueError("Select a second input signal.")
                out=op.apply(a,self.signals[other])
            elif opname=="Amplification": out=op.apply(a,gain=p1)
            elif "Filter" in opname and opname not in {"Band-Pass Filter","Band-Stop Filter"}:
                out=op.apply(a,cutoff=p1)
            elif opname in {"Band-Pass Filter","Band-Stop Filter"}:
                out=op.apply(a,low=p1,high=p2)
            elif opname=="FFT": out=op.apply(a,window=self.window.currentText())
            elif opname=="Sampling": out=op.apply(a,new_fs=p1)
            elif opname=="Integration": out=op.apply(a,initial=p1)
            elif opname=="Linear Reconstruction": out=op.apply(a,output_fs=p1)
            elif opname=="AM Modulation": out=op.apply(a,carrier_frequency=p1,modulation_index=p2)
            elif opname=="AM Demodulation": out=op.apply(a,carrier_frequency=p1,cutoff=p2)
            else: out=op.apply(a)

            base=out.name; i=1; new=base
            while new in self.signals:
                i+=1; new=f"{base}_{i}"
            out.name=new; self.signals[new]=out
            self.sig_list.addItem(new); self.refresh_inputs()
            self.sig_list.setCurrentRow(self.sig_list.count()-1)
        except Exception as e:
            QMessageBox.critical(self,"Operation error",str(e))

    def compare_all(self):
        if self.signals: self.canvas.compare(list(self.signals.values()))

    def clear_all(self):
        self.signals.clear(); self.sig_list.clear(); self.refresh_inputs()
        self.canvas.ax.clear(); self.canvas.draw(); self.info.setText("No signals.")

def run():
    app=QApplication.instance() or QApplication(sys.argv)
    w=MainWindow(); w.show(); sys.exit(app.exec())
