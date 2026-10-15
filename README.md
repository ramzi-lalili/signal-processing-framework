# Signal Processing Framework

A modular desktop DSP application built with Python, NumPy, SciPy, PySide6 and Matplotlib.

## Features

* Signal generators: DC, sine/AC, Dirac impulse, ramp, sign, square, triangle, chirp and white noise.
* Operations: amplification, addition, multiplication, convolution, correlation, integration, differentiation.
* Filters: low-pass, high-pass, band-pass and band-stop Butterworth filters.
* FFT/IFFT with selectable windows (Rectangular, Hann, Hamming, Blackman, Kaiser).
* Sampling and linear reconstruction.
* AM modulation and demodulation.
* Dynamic time/frequency visualization.
* Processing pipeline with intermediate results.
* Extensible generator and operation registries.

## Run

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
python main.py
```

## Architecture

`core/` contains the data model and registries.
`generators/` contains signal generators.
`operations/` contains DSP operations and filters.
`visualization/` contains plotting.
`gui/` contains the PySide6 application.

The application keeps source signals immutable by creating a new Signal for each operation. The GUI supports binary operations through a second-input selector.



## Auteur

lalili mohamed ramzi – https://www.linkedin.com/in/ramzi-lalili-2948a8310/ – ramzilalili@gmail.comLicence



MIT, voir LICENSE.

