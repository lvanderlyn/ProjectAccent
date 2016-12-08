# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 19:34:24 2014

@author: pruvolo
"""
import sys
import pygame
from pygame.locals import *
import random
import math
import time
import wave
import pyaudio
import time
sys.path.insert(0, '../lib')
# import thinkdsp as td



class PyGameBrickBreakerView:
    """ renders the BrickBreakerModel to a pygame window """
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
    
    def draw(self):
        pass


class PyGameKeyboardController:
    """ Manipulate game state based on keyboard input """
    def __init__(self, model):
        self.model = model
        '''These are the state values:
        selection: picking a voice
        playback: allows playback after transformations
        '''
        self.mode = "intro"
        self.button = 'none'
        self.user_num = 0
        self.start_time = time.time()

    def handle_pygame_event(self, event):

        if self.mode == "intro":
            if event.type == KEYDOWN:
                if event.key == pygame.K_d:
                    self.button = 'Start'
                    print('Intro')
                    sound = pygame.mixer.Sound("../poem/Intro.wav")
                    sound.play()
                    self.mode = "record"
                    self.start_time = time.time()

        if self.mode == "record":
            if event.type == KEYDOWN:
                if event.key == pygame.K_f:
                    if self.button == 'none':
                        pass
                    else:
                        print("start recording - press stop to terminate recording")
                        CHUNK = 1024 
                        FORMAT = pyaudio.paInt16 #paInt8
                        CHANNELS = 2 
                        RATE = 44100 #sample rate
                        RECORD_SECONDS = 20
                        WAVE_OUTPUT_FILENAME = "voice{0}.wav".format(self.user_num)
                        self.user_num = (self.user_num + 1) % 3

                        p = pyaudio.PyAudio()

                        stream = p.open(format=FORMAT,
                                        channels=CHANNELS,
                                        rate=RATE,
                                        input=True,
                                        frames_per_buffer=CHUNK) #buffer

                        print("* recording")

                        frames = []

                        done = False
                        while(done == False):
                            data = stream.read(CHUNK)
                            frames.append(data)
                            for newevent in pygame.event.get():
                                if newevent.type == KEYDOWN and newevent.key == pygame.K_g:
                                    done = True

                        print ("finished recording")
                        stream.stop_stream()
                        stream.close()
                        p.terminate()

                        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                        wf.setnchannels(CHANNELS)
                        wf.setsampwidth(p.get_sample_size(FORMAT))
                        wf.setframerate(RATE)
                        wf.writeframes(b''.join(frames))
                        wf.close()  

                        self.mode = "play"              
                        self.start_time = time.time()


        if self.mode == "play":
            if  event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1: #left click
                    poem = pygame.mixer.Sound("../poem/Pinar_Poem.wav")
                    poem.play()
                    self.button = 'Pinar'
                    print(self.button)
                    self.start_time = time.time()                    

                if event.button == 3: #right click
                    poem = pygame.mixer.Sound("../poem/Dimitar_Poem.wav")
                    poem.play()
                    self.button = 'Dimitar'
                    print(self.button)
                    self.start_time = time.time()


            if event.type == KEYDOWN:

                if event.key == pygame.K_d:
                    self.button = 'Start'
                    print('Intro')
                    sound = pygame.mixer.Sound("../poem/Intro.wav")
                    sound.play()
                    self.mode = "record"
                    self.start_time = time.time()

                if event.key == pygame.K_w:
                    poem = pygame.mixer.Sound("../poem/voice0.wav")
                    poem.play()
                    self.button = 'V1'
                    print(self.button)
                    self.start_time = time.time()                    

                if event.key == pygame.K_a:
                    poem = pygame.mixer.Sound("../poem/voice1.wav")
                    poem.play()
                    self.button = 'V2'
                    print(self.button)
                    self.start_time = time.time()                    

                if event.key == pygame.K_s:
                    poem = pygame.mixer.Sound("../poem/voice2.wav")
                    poem.play()
                    self.button = 'V3'
                    print(self.button)
                    self.start_time = time.time()                    

                if event.key == pygame.K_DOWN:
                    poem = pygame.mixer.Sound("../poem/Bruce_Poem.wav")
                    poem.play()
                    self.button = 'Bruce'
                    print(self.button)
                    self.start_time = time.time()         

                if event.key == pygame.K_UP:
                    poem = pygame.mixer.Sound("../poem/James_Poem.wav")
                    poem.play()
                    self.button = 'James'
                    print(self.button)
                    self.start_time = time.time()

                if event.key == pygame.K_RIGHT:
                    poem = pygame.mixer.Sound("../poem/Jee_Poem.wav")
                    poem.play()
                    self.button = 'Jee'
                    print(self.button)
                    self.start_time = time.time()                    

                if event.key == pygame.K_LEFT:
                    poem = pygame.mixer.Sound("../poem/Jiaying_Poem.wav")
                    poem.play()
                    self.button = 'Jiaying'
                    print(self.button)
                    self.start_time = time.time()                    


                




if __name__ == '__main__':
    pygame.mixer.pre_init(48000, 16, 1, 4096)
    pygame.mixer.init()
    pygame.init()

    size = (640,480)
    screen = pygame.display.set_mode(size)

    view = PyGameBrickBreakerView(None,screen)
    controller = PyGameKeyboardController(None)
    running = True
    start_time = time.time()
    while running:
        d_time = time.time() - controller.start_time

        if d_time > 45:
            controller.mode = "intro"

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_pygame_event(event)
            start_time = time.time()
        time.sleep(.001)

    pygame.quit()