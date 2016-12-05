# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 19:34:24 2014

@author: pruvolo
"""

import pygame
from pygame.locals import *
import random
import math
import time
import wave
import pyaudio

class BrickBreakerModel:
    """ Encodes the game state of Brick Breaker """
    def __init__(self):
        self.number_of_lives = 3
        self.bricks = []
        for i in range(640//110):
            for j in range(240//30):              
                new_brick = Brick(10+110*i,10+30*j,100,20,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
                self.bricks.append(new_brick)
        self.paddle = Paddle(200,450,100,20)
    
    def update(self):
        self.paddle.update()
        
class Brick:
    """ Encodes the state of a brick in Brick Breaker """
    def __init__(self,x,y,width,height,color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    
class Paddle:
    """ Encode the state of the paddle in Brick Breaker """
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (255,255,255)
        self.vx = 0.0
    
    def update(self):
        self.x += self.vx

class PyGameBrickBreakerView:
    """ renders the BrickBreakerModel to a pygame window """
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
    
    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        for brick in self.model.bricks:
            pygame.draw.rect(self.screen, pygame.Color(brick.color[0], brick.color[1], brick.color[2]), pygame.Rect(brick.x, brick.y, brick.width, brick.height))
        pygame.draw.rect(self.screen, pygame.Color(self.model.paddle.color[0], self.model.paddle.color[1], self.model.paddle.color[2]), pygame.Rect(self.model.paddle.x, self.model.paddle.y, self.model.paddle.width, self.model.paddle.height))
        pygame.display.update()

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
            if event.key == pygame.K_s:
                self.voice = 'none'
                print('Someone is saying instructions right now')
                # Instructions = pygame.mixer.Sound()

            if event.key == pygame.K_1:
                Intro= pygame.mixer.Sound("../intros/Jee_Intro.wav")
                Intro.play()
                self.voice = 'Jee'
                print(self.voice)
     
            if event.key == pygame.K_2:
                Intro= pygame.mixer.Sound("../intros/Pinar_Intro.wav")
                Intro.play()
                self.voice = 'Pinar'
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







        #     for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        #         data = stream.read(CHUNK)
        #         frames.append(data) # 2 bytes(16 bits) per channel

        # if event.key == pygame.K_t:
        #     print("* done recording")
        #     stream.stop_stream()
        #     stream.close()
        #     p.terminate()

        #     wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        #     wf.setnchannels(CHANNELS)
        #     wf.setsampwidth(p.get_sample_size(FORMAT))
        #     wf.setframerate(RATE)
        #     wf.writeframes(b''.join(frames))
        #     wf.close()

if __name__ == '__main__':
    pygame.mixer.pre_init(48000, 16, 1, 4096)
    pygame.mixer.init()
    pygame.init()

    size = (640,480)
    screen = pygame.display.set_mode(size)

    model = BrickBreakerModel()
    view = PyGameBrickBreakerView(model,screen)
    controller = PyGameKeyboardController(model)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_pygame_event(event)
        model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()