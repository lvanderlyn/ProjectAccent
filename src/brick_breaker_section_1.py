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
        self.state = 'selection'
        self.voice = 'none'

    def handle_pygame_event(self, event):
        if event.type != KEYDOWN:
                return

        if self.state == 'selection':
            if event.key == pygame.K_w:
                self.voice = 'none'
                print('Someone is saying instructions right now')
                # Instructions = pygame.mixer.Sound()

            if event.key == pygame.K_a:
                poem = pygame.mixer.Sound("../poem/Bruce_Poem.wav")
                poem.play()
                self.voice = 'Bruce'
                print(self.voice)
     
            if event.key == pygame.K_s:
                poem = pygame.mixer.Sound("../poem/James_Poem.wav")
                poem.play()
                self.voice = 'James'
                print(self.voice)

            if event.key == pygame.K_d:
                poem = pygame.mixer.Sound("../poem/Jee_Poem.wav")
                poem.play()
                self.voice = 'Jee'
                print(self.voice)

            if event.key == pygame.K_f:
                poem = pygame.mixer.Sound("../poem/Jiaying_Poem.wav")
                poem.play()
                self.voice = 'Jiaying'
                print(self.voice)

            if event.key == pygame.K_g:
                poem = pygame.mixer.Sound("../poem/Pinar_Poem.wav")
                poem.play()
                self.voice = 'Pinar'
                print(self.voice)

            if event.key == pygame.K_6:
                poem = pygame.mixer.Sound("../poem/Dimitar_Poem.wav")
                poem.play()
                self.voice = 'Dimitar'
                print(self.voice)

            if event.key == pygame.K_r:
                if self.voice == 'none':
                    pass
                else:
                    print("start recording - press T to terminate recording")
                    CHUNK = 1024 
                    FORMAT = pyaudio.paInt16 #paInt8
                    CHANNELS = 2 
                    RATE = 44100 #sample rate
                    RECORD_SECONDS = 20
                    WAVE_OUTPUT_FILENAME = "learner.wav"

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
                            if newevent.type == KEYDOWN and newevent.key == pygame.K_t:
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
                #send the following to modulator teacher = self.voice's mp3, learner = recorded audio
                #play the modulated voice
                self.state = 'playback'
        if self.state == 'playback':
            if event.key == pygame.K_f:
                Replay = pygame.mixer.Sound("learner.wav")
                Replay.play()
                print('Hearing your modified voice')
            if event.key == pygame.K_s:
                self.voice = 'none'
                print('Someone is saying instructions right now')
                # Instructions = pygame.mixer.Sound()
                self.state = 'selection'
                self.voice = 'none'



if __name__ == '__main__':
    pygame.mixer.pre_init(48000, 16, 1, 4096)
    pygame.mixer.init()
    pygame.init()

    size = (640,480)
    screen = pygame.display.set_mode(size)

    view = PyGameBrickBreakerView(None,screen)
    controller = PyGameKeyboardController(None)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_pygame_event(event)
        time.sleep(.001)

    pygame.quit()