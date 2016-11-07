import sys
sys.path.insert(0, '../lib')
import wave
import thinkdsp as td
import thinkplot as tp
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert, chirp
import scipy
import peakutils
from scipy.interpolate import interp1d
import math

class Modulator(object):
    """docstring for Modulator"""
    def __init__(self, file_name):
        self.text_grid = TextGrid()
        self.text_grid.parse_file(file_name)


    def get_envelope(self):
        wave = td.read_wave('outTest.wav')
        # fig1 = plt.figure(1)
        # plt.subplot(211)
        # plt.plot(wave.ts, wave.ys)
        # plt.title('Original Wave Clip')

        hanning = np.hanning(len(wave))

        hanwave = wave
        hanwave.window(hanning)

        ##frequency domain plotting stuff
        spec = wave.make_spectrum()
        hanspec = hanwave.make_spectrum()

        ys = hanspec.amps
        xs = hanspec.fs
        indexes = peakutils.indexes(ys, thres=0.02/max(ys), min_dist=15)

        env_xs, env_ys = interpolate(indexes, xs, ys)

        fig4 = plt.figure()
        plt.plot(spec.fs, spec.amps, label="signal")
        plt.plot(env_xs, env_ys, label='window')
        plt.plot([spec.fs[i] for i in indexes], [spec.amps[i] for i in indexes], label='peaks')

        plt.legend()
        plt.xlim([0,8000])

        ##Low pass filter the analytic signal
        N=10
        Fc=40
        Fs=1600
        # provide them to firwin
        h=scipy.signal.firwin( numtaps=N, cutoff=2, nyq = 800)
        # filtEnve=scipy.signal.lfilter( h, 1.0, hanspec.amps) # 'x' is the time-series data you are filtering

        # plt.plot(spec.fs, filtEnve, label='envelope')
        # plt.plot(spec.fs, spec.amps/filtEnve, label='envelope')



        #Trying to use peaks to generate envelope
        peaks = scipy.signal.find_peaks_cwt(hanspec.amps, np.arange(1,100))
        # plt.plot(peaks, hanspec.amps[peaks])
        plt.yscale('log')
        plt.show()

def interpolate(indexes, fs, amps):
    indexes = [0] + [i for i in indexes]
    ret_val = np.ones(len(fs))
    ret_val = [n for n in ret_val]

    for i in range(len(indexes)-1):
        index1 = indexes[i]
        index2 = indexes[i+1]

        rise = int(amps[index2] - amps[index1])
        run = int(fs[index2] - fs[index1])
        k = float(rise/float(run))
        c = amps[index1]

        ret_val[index1:index2] = [(k*x) + c for x in range(0, index2-index1)]
    N = 30
    ys = np.convolve(ret_val, np.ones((N))/N, mode='valid')

    return fs[:len(ys)], ys



class TextGrid(object):
    """
    x_min is start time
    x_max is end time
    tiers = [{(phones: intervals), (words: intervals)}]
    * Intervals are dict (start, stop, name) 
    eg. intervals: [(start = 0.0, end = 0.44, name = "sil")... (start = 4.4, end = 5.0, name = "sil")]
    """
    def __init__(self, x_min=None, x_max=None, tiers=None):
        self.start_time = x_min
        self.end_time = x_max
        self.tiers = tiers

    def parse_file(self, file_name):
        with open(file_name) as f:
            content = f.readlines()
        self.start_time = content[3]
        self.start_time = content[4]
        tier_1 = []
        tier_2 = []
        first = True
        for line in content[9:]:
            if "item" in line:
                first = False
                continue
            if first:
                tier_1.append(line)
            else:
                tier_2.append(line)
        inf1 = self.parse_tier(tier_1)
        inf2 = self.parse_tier(tier_2)
        self.tiers = dict([(inf1[0], inf1[1]), (inf2[0], inf2[1])])

    def parse_tier(self, lines):
        name = lines[1][10:-2] 
        intervals = []
        interval = []
        for line in lines[6:]:
            if "interval" in line:
                intervals.append(self.parse_interval(interval))
                interval = []
            else:
                interval.append(line)
        return name, intervals
    
    def parse_interval(self, interval):
        return dict([("start", float(stripWhite(interval[0]))), ("end", float(stripWhite(interval[1]))), ("name", stripWhite(interval[2]))])

"""
Utilities
"""        

def slice_wav(in_name, out_filename, start_ms, end_ms):
    infile = wave.open(in_name, "r")
    width = infile.getsampwidth()
    rate = infile.getframerate()
    fpms = rate / 1000 # frames per ms
    length = (end_ms - start_ms) * fpms
    start_index = start_ms * fpms

    out = wave.open(out_filename, "w")
    out.setparams((infile.getnchannels(), width, rate, length, infile.getcomptype(), infile.getcompname()))
    
    infile.rewind()
    anchor = infile.tell()
    infile.setpos(anchor + start_index)
    out.writeframes(infile.readframes(length))
    out.close()
    infile.close()

def stripWhite(string):
    start = string.find("=")+1
    return string[start:-1]
    

if __name__ == '__main__':
    n = Modulator("../test/english44clipped.TextGrid")
    n.get_envelope()
    # n.cepstral_env_estimate()
    # words = n.text_grid.tiers["phones"]
    # start = words[2]["start"]
    # end = words[2]["end"]
    # print(start, end)
    # slice_wav("../test/english44clipped.wav", "outTest.wav", int(start*1000), int(end*1000))

