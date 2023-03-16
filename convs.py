import numpy as np

def convolution(signal, kernel, filter_on):
    n_sig = signal.size
    n_ker = kernel.size
    rev_kernel = kernel[::-1].copy()
    result = np.zeros(n_sig - n_ker, dtype=np.int16)
    for i in range(n_sig - n_ker):
        if filter_on:
            result[i] = np.dot(signal[i:i+n_ker], rev_kernel)
        else:
            result[i] = signal[i+n_ker]
    signal[0:n_ker] = signal[n_sig-n_ker:n_sig]
    return result