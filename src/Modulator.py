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
    def __init__(self, learner_textgrid, teacher_textgrid, learner_wav, teacher_wav):
        self.teacher_textgrid = TextGrid()
        self.teacher_textgrid.parse_file(teacher_textgrid)
        self.learner_textgrid = TextGrid()
        self.learner_textgrid.parse_file(learner_textgrid)

        self.learner_wav = td.read_wave(learner_wav)
        self.teacher_wav = td.read_wave(teacher_wav)

    def get_envelope(self, wave):
        # wave = td.read_wave(file_name)
        # hanning = np.hanning(len(wave.ys))
        # wave.window(hanning)
        spectrum = wave.make_spectrum()
        # spectrum.plot()   
        # tp.show()


        # wave = spectrum.make_wave()
        # wave.play("outtest.wav")
        ys = spectrum.hs

        indexes = peakutils.indexes(ys, thres=0.02/max(ys), min_dist=15)
        envelope = interpolate(indexes, np.real(ys))
        envelope = np.append(envelope, np.ones((len(ys) - len(envelope))))

        # fig1 = plt.figure(1)
        # plt.plot(ys, label="signal")
        # plt.plot(envelope, label="envelope")
        # plt.legend()
        # plt.show()

        return spectrum, envelope


    def convert_spectrum(self):
        ts = []
        ys = []
        for i in range(len(self.learner_textgrid.tiers["phones"])):
            word = self.learner_textgrid.tiers["phones"][i]
            print(word)
            if i == 36:
                break
            elif word["name"] != ' "sil"':
                learner_slice = self.learner_wav.segment(start=word["start"], duration=word["length"])
                teacher_slice = self.teacher_wav.segment(start=self.teacher_textgrid.tiers["phones"][i]["start"], duration=self.teacher_textgrid.tiers["phones"][i]["length"])


                learner_spec, learner_env = self.get_envelope(learner_slice)
                teacher_spec, teacher_env = self.get_envelope(teacher_slice)

                # fig1 = plt.figure(1)
                # plt.plot(learner_spec.fs, learner_spec.amps, label="learner")
                # plt.plot(teacher_spec.fs, teacher_spec.amps, label="teacher")                

                if len(learner_spec.hs) > len(teacher_spec.hs):
                    learner_amps = learner_spec.hs/learner_env
                    teacher_amps = np.append(teacher_spec.hs, np.zeros(len(learner_spec.hs) - len(teacher_spec.hs)))
                    teacher_env = np.append(teacher_env, np.zeros(len(learner_spec.hs) - len(teacher_env)))
                else:
                    learner_amps = np.append(learner_spec.hs/learner_env, np.zeros(len(teacher_spec.hs) - len(learner_spec.hs)))
                    teacher_amps = teacher_spec.hs

                learner_amps = learner_amps * teacher_env
                # plt.plot(np.absolute(learner_amps), label="after")
                # plt.legend()
                # plt.show()

                # wave = td.Spectrum(new_amps, learner_spec.fs[:len(new_amps)], teacher_slice.framerate, True).make_wave()
                # wave = td.Spectrum(learner_spec.hs, learner_spec.fs, teacher_slice.framerate, False).make_wave()
                print("TEACHER", teacher_slice.framerate)
                print("LEARNER", learner_slice.framerate)
                wave = td.Spectrum(learner_amps, learner_spec.fs, learner_slice.framerate, True).make_wave()


                # plt.plot(wave.ts, wave.ys, label="after")

                ts += [t for t in wave.ts]
                ys += [y for y in wave.ys]

        wave.ts = np.array(ts)
        wave.ys = np.array(ys)
        wave.play("outtest.wav") 

    def shift_accent(self):
        pass

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
    
    def parse_interval(self, interval):
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


def interpolate(indexes, amps):
    indexes = [0] + [i for i in indexes]
    ret_val = np.ones(len(amps))
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
    return ys


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
        if i2 >= 0:
            print("WINDOW SIZE: ", window_size)
            print("hanning_window: ", len(hanning_window))
            print("a3_rephased: ", len(a3_rephased))
            print("I2: ", i2)
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
    test = Modulator("../test/english44clipped.TextGrid","../test/japanese18clipped.TextGrid","../test/english44clipped.wav","../test/japanese18clipped.wav")
    

    test = Modulator("../test/japanese18clipped.TextGrid","../test/english44clipped.TextGrid","../test/japanese18clipped.wav","../test/english44clipped.wav")

    # test = Modulator("../test/english44clipped.TextGrid", "../test/japanese18clipped.TextGrid", "../test/english44clipped.wav", "../test/japanese18clipped.wav")
    # n = Modulator("../test/english44clipped.TextGrid")
    # current_word = 3
    # l_words = learner.text_grid.tiers["phones"]
    # l_start = l_words[current_word]["start"]
    # l_end = l_words[current_word]["end"]
    # t_words = teacher.text_grid.tiers["phones"]
    # t_start = t_words[current_word]["start"]
    # t_end = t_words[current_word]["end"]
    # slice_wav("../test/japanese18clipped.wav", "teacher_1.wav", int(t_start*1000), int(t_end*1000))
    # slice_wav("../test/english44clipped.wav", "learner_1.wav", int(l_start*1000), int(l_end*1000))
    # n.get_envelope("outTest.wav")


    test.convert_spectrum()


    # teacher = Modulator("../test/english44clipped.TextGrid")
    # learner = Modulator("../test/japanese18clipped.TextGrid")
    # alpha = prosodicRatio(test.learner_textgrid.tiers["words"],test.teacher_textgrid.tiers["words"])
    
    # fps, sound = wavfile.read('../test/english44clipped.wav')
    # sound1 = stich(test.learner_textgrid.tiers["words"], alpha, sound, fps)
    # print(len(sound),len(sound1))
    # wavfile.write('../test/jpToEng(prosodic2-11).wav',fps,sound1)

    # alpha = prosodicRatio(test.learner_textgrid.tiers["words"],test.teacher_textgrid.tiers["words"])
    
    # fps, sound = wavfile.read('../test/english44clipped.wav')
    # sound1 = stich(test.learner_textgrid.tiers["words"], alpha, sound, fps)
    # wavfile.write('../test/engToJp(prosodicsmoothed).wav',fps,sound1)
    # print(np.mean(sound), np.mean(sound1))
    # print(len(sound),len(sound1))
    # wavfile.write('../test/jpToEng(prosodic2-11).wav',fps,sound1)
