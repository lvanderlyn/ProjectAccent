import wave

class Modulator(object):
    """docstring for Modulator"""
    def __init__(self, file_name):
        self.text_grid = TextGrid()
        self.text_grid.parseFile(file_name)



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

    def parseFile(self, file_name):
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
        inf1 = self.parseTier(tier_1)
        inf2 = self.parseTier(tier_2)
        self.tiers = dict([(inf1[0], inf1[1]), (inf2[0], inf2[1])])

    def parseTier(self, lines):
        name = lines[1][10:-2] 
        intervals = []
        interval = []
        for line in lines[6:]:
            if "interval" in line:
                intervals.append(self.parseInterval(interval))
                interval = []
            else:
                interval.append(line)
        return name, intervals
    
    def parseInterval(self, interval):
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
    words = n.text_grid.tiers["words"]
    start = words[1]["start"]
    end = words[1]["end"]
    print(start, end)
    slice_wav("../test/english44clipped.wav", "outTest.wav", int(start*1000), int(end*1000))

