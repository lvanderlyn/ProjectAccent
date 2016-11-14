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
from scipy.io import wavfile


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
        # run = int(fs[index2] - fs[index1])
        run = int(index2 - index1)
        k = float(rise/float(run))
        c = amps[index1]

        ret_val[index1:index2] = [(k*x) + c for x in range(0, index2-index1)]
    N = 10
    ys = np.convolve(ret_val, np.ones((N))/N, mode='valid')
    # ys = ret_val
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
    
    # def parse_interval(self, interval):
    #     return dict([("start", float(stripWhite(interval[0]))), ("end", float(stripWhite(interval[1]))), ("name", stripWhite(interval[2]))])
    
    def parseInterval(self, interval):
        return dict([("start", float(stripWhite(interval[0]))), ("end", float(stripWhite(interval[1]))), ("name", stripWhite(interval[2])), ("length", float(stripWhite(interval[1])) -  float(stripWhite(interval[0])))])

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

def prosodicRatio(learner_tiers, teacher_tiers):
    alpha = []
    for i in range(len(teacher_tiers)):
        alpha.append(learner_tiers[i]["length"]/teacher_tiers[i]["length"])
    return alpha

def stretch(sound_array, f, window_size, h):
    """ Stretches the sound by a factor `f` """

    phase  = np.zeros(window_size)
    hanning_window = np.hanning(window_size)
    result = np.zeros( len(sound_array) /f + window_size)

    for i in np.arange(0, len(sound_array)-(window_size+h), h*f):

        # two potentially overlapping subarrays
        a1 = sound_array[i: i + window_size]
        a2 = sound_array[i + h: i + window_size + h]

        # resynchronize the second array on the first
        s1 =  np.fft.fft(hanning_window * a1)
        s2 =  np.fft.fft(hanning_window * a2)
        phase = (phase + np.angle(s2/s1)) % 2*np.pi
        a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))
        a3_rephased = [float(i) for i in a2_rephased]


        # add to result
        i2 = int(i/f)
        result[i2 : i2 + window_size] += hanning_window*a3_rephased

    result = ((2**(16-4)) * result/result.max()) # normalize (16bit)

    return result.astype('int16')

def stich(learner_text_grid_words, alpha, learner_sound_array, fps):
    #cut the learner sound array into each word segment section
    np.set_printoptions(threshold=np.nan)
    word_segment = []
    for i in range(len(alpha)):
        start_frame = int(learner_text_grid_words[i]["start"]*fps)
        end_frame = int(learner_text_grid_words[i]["end"]*fps)
        word_segment.append(learner_sound_array[start_frame:end_frame])
        
    #stretches and stiches together the different time-segments
    stiched = []
    midword = [0]
    for i in range(len(alpha)):
        n = 2**11
        h = n/4
        if alpha[i]>= 4:
            factor = 4
        elif alpha[i] <=0.25:
            factor = 0.25
        else:
            factor = alpha[i]
        stretched = stretch(word_segment[i], factor, n,h)
        stiched.extend(np.trim_zeros(stretched))
        midword.append(int(len(stiched) - len(stretched)/2))
    midword.append(len(stiched))
    return np.asarray(stiched)


if __name__ == '__main__':
<<<<<<< HEAD
    learner = Modulator("../test/english44clipped.TextGrid")
    teacher = Modulator("../test/japanese18clipped.TextGrid")
=======
    n = Modulator("../test/english44clipped.TextGrid")
    n.get_envelope()
    # words = n.text_grid.tiers["phones"]
    # start = words[2]["start"]
    # end = words[2]["end"]
    # print(start, end)
    # slice_wav("../test/english44clipped.wav", "outTest.wav", int(start*1000), int(end*1000))

    teacher = Modulator("../test/english44clipped.TextGrid")
    learner = Modulator("../test/japanese18clipped.TextGrid")
>>>>>>> origin/master
    alpha = prosodicRatio(learner.text_grid.tiers["words"],teacher.text_grid.tiers["words"])
    
    fps, sound = wavfile.read('../test/english44clipped.wav')
    sound1 = stich(learner.text_grid.tiers["words"], alpha, sound, fps)
<<<<<<< HEAD
    wavfile.write('../test/engToJp(prosodicsmoothed).wav',fps,sound1)
    print(np.mean(sound), np.mean(sound1))

    # words = n.text_grid.tiers["phones"]
    # start = words[1]["start"]
    # end = words[1]["end"]
    # name = words[1]["name"]
    # length = words[1]["length"]

    # print(start, end, name, length)
    # slice_wav("../test/english44clipped.wav", "outTest.wav", int(2*1000), int(3*1000))

=======
    print(len(sound),len(sound1))
    wavfile.write('../test/jpToEng(prosodic2-11).wav',fps,sound1)
>>>>>>> origin/master
