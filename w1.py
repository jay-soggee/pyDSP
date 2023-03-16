import numpy as np
import pyaudio
import time
import sys
import wave
import keyboard
import scipy.signal as signal

## user imports
import fplot
import convs

## kernel variables
kernel_size = 15
kernel = np.full(kernel_size, 1/kernel_size)

## input variables
RATE = 16000
CHUNK = int(RATE/10)
in_data = np.zeros(CHUNK+kernel_size, dtype=np.int16)
filter_on = 0
print(1000/RATE*2)
## filter declaration
win_rect = signal.firwin(   numtaps=kernel_size,
                            cutoff=1000/RATE*2, 
                            window="boxcar", 
                            pass_zero='lowpass')
win_hamm = signal.firwin(   numtaps=kernel_size, 
                            cutoff=1000/RATE*2, 
                            window="hamming", 
                            pass_zero='lowpass')
win_cos = signal.firwin(    numtaps=kernel_size, 
                            cutoff=1000/RATE*2, 
                            window="cosine", 
                            pass_zero='lowpass')
win_tri = signal.firwin(    numtaps=kernel_size, 
                            cutoff=1000/RATE*2, 
                            window="triang", 
                            pass_zero='lowpass')
fplot.mfreqz(win_rect)
fplot.mfreqz(win_hamm)
fplot.mfreqz(win_cos)
fplot.mfreqz(win_tri)
fplot.show()
## main
p=pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, \
            channels=1,                 \
            rate=RATE,                  \
            input=True,                 \
            output=True,                \
            frames_per_buffer=CHUNK,    \
            input_device_index=0)

p=pyaudio.PyAudio()
while(True):
    samples = stream.read(CHUNK)
    in_data[kernel_size:kernel_size+CHUNK] = np.fromstring(samples, dtype=np.int16)
    if filter_on == 0:
        out = convs.convolution(in_data, win_rect, filter_on=True)
    elif filter_on == 1:
        out = convs.convolution(in_data, win_hamm, filter_on=True)
    elif filter_on == 2:
        out = convs.convolution(in_data, win_cos, filter_on=True)
    elif filter_on == 3:
        out = convs.convolution(in_data, win_tri, filter_on=True)
    y = out.tostring()
    stream.write(y)
    if keyboard.is_pressed('q'):
        break
    if keyboard.is_pressed('f'):
        filter_on = (filter_on + 1) % 4
        if filter_on == 0:
            print("Filter = Rect.")
        elif filter_on == 1:
            print("Filter = Hamm.")
        elif filter_on == 2:
            print("Filter = cos.")
        elif filter_on == 3:
            print("Filter = tri.")

stream.stop_stream()
stream.close()

p.terminate()