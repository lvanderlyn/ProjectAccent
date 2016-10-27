import thinkdsp as td
import thinkplot as tp
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert, chirp
import scipy


##time domain plotting (original vs non-hanninged)

wave = td.read_wave('japanese18(IH).wav')
fig1 = plt.figure(1)
plt.subplot(211)
plt.plot(wave.ts, wave.ys)
plt.title('Original Wave Clip')

hanning = np.hanning(len(wave))

hanwave = wave
hanwave.window(hanning)
plt.subplot(212)
plt.plot(hanwave.ts, hanwave.ys)
plt.title('Hanninged Wave Clip')

##plots the hanning window

fig2 = plt.figure(2)
plt.plot(wave.ts, hanning)
plt.title('Hanning wave')

##frequency domain plotting stuff
spec = wave.make_spectrum()
hanspec = hanwave.make_spectrum()

fig3 = plt.figure(3)
plt.subplot(211)
plt.plot(spec.fs, spec.amps)
plt.yscale('log')
plt.title('Original Spectrum')
plt.xlim([0,8000])
plt.subplot(212)
plt.plot(hanspec.fs, hanspec.amps)
plt.yscale('log')
plt.title('Hanninged Spectrum')
plt.xlim([0,8000])


##Trying to get the spectral envelope using the hilbert transform
analytic_signal = hilbert(spec.amps)
amplitude_envelope = np.abs(analytic_signal)
fig4 = plt.figure()
plt.plot(spec.fs, spec.amps, label='signal')
#plt.plot(spec.fs, amplitude_envelope, label='envelope')
plt.yscale('log')
plt.legend()
plt.xlim([0,8000])

##Low pass filter the analytic signal
# spell out the args that were passed to the Matlab function
N=10
Fc=40
Fs=1600
# provide them to firwin
h=scipy.signal.firwin( numtaps=N, cutoff=2, nyq = 800)
filtEnve=scipy.signal.lfilter( h, 1.0, hanspec.amps) # 'x' is the time-series data you are filtering
#plt.plot(spec.fs, filtEnve, label='envelope')
#plt.plot(spec.fs, spec.amps/filtEnve, label='envelope')



#Trying to use peaks to generate envelope
peaks = scipy.signal.find_peaks_cwt(hanspec.amps, np.arange(1,100))
plt.plot(peaks, hanspec.amps[peaks])
plt.yscale('log')
plt.show()


