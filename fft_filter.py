import numpy as np
from scipy import signal
from scipy.io import wavfile


def stft(x, w, step):
    wlen = len(w)
    nsampl = len(x)
    Xtf = np.array([ np.fft.rfft(w*x[i:i+wlen])for i in range(0, nsampl - wlen + 1, step) ] ) + 1e-12*(1+1j)
    return Xtf

def istft(Xtf, w, step, nsampl):
    nframe = len(Xtf)
    wlen = len(w)
    y = np.zeros(nsampl)
    ws = np.zeros(nsampl)
    ind = 0
    for i in range(0, nsampl - wlen + 1, step):
        y[i:i + wlen] += w*np.fft.irfft(Xtf[ind])
        ws[i:i+wlen] += w*w
        ind += 1
    ws[ws==0] = 1
    y = y / ws
    return y

def filter_ft(mag, fcut, ftype):
    Nf, ft_bin = mag.shape
    fmag = np.zeros([Nf, ft_bin])
    fcut_pos = int(ft_bin*fcut)
    if ftype=='lowpass':
        fmag[:,0:fcut_pos]=mag[:,0:fcut_pos]
    elif ftype=='highpass':
        fmag[:,fcut_pos:ft_bin]=mag[:,fcut_pos:ft_bin]
    elif ftype=='w4bp':
        fmag[:,3:26]=mag[:,3:26]
    elif ftype=='w4bs':
        fmag[:,0:3]=mag[:,0:3]
        fmag[:,26:ft_bin]=mag[:,26:ft_bin]
    return fmag
