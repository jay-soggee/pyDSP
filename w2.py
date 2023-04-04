import numpy as np
from scipy import signal
from scipy.io import wavfile
import fft_filter
import sys

WL = 256
WR = 128


fs, data = wavfile.read(sys.argv[1])
fcut = float(sys.argv[3])
w = signal.hann(WL)
Xf = fft_filter.stft(data, w, WR)

Mag = np.abs(Xf)
Phs = np.angle(Xf)
fMag = fft_filter.filter_ft(Mag, fcut, sys.argv[4])
Xfr = fMag*np.exp(1j * Phs)

y = fft_filter.istft(Xfr, w, WR, len(data))
wavfile.write(sys.argv[2], fs, y.astype(np.int16))
print(f"{data.shape}"+f"{w.shape}"+","+f"{Xf.shape}")
