import pyaudio  
import wave  
import pygame
import time

class Controller:
    '''controls the jumpman's motion'''
    # def __init__(self,model):
    #     '''initializes the model'''
    #     self.model = model
    
    def handleEvent(self, event):
        '''Defines all scenarios that can happen to the Transpose controller'''
        pressed = pygame.key.get_pressed() #finds keys pressed so multiple input can be taken
        # if self.model.mode == MODE_INSTRUCT: 
            # if pressed[K_s]:
            #     #play instructions recording
            #     #set voice = nothing
        print(pressed)
        if pressed[K_q]:
            pygame.quit()

        if pressed[K_1]:
            #PLAY PERSON1 INTRO
            #set voice = to PERSON1
            Jee_Intro= pygame.mixer.Sound("../intros/Jee_Intro.wav")
            Jee_Intro.play()

        if pressed[K_2]:
            Pinar_Intro= pygame.mixer.Sound("../intros/Pinar_Intro.wav")
            Pinar_Intro.play()  
            # if pressed[K_3]:

            # if pressed[K_4]:
            # if pressed[K_5]:
            # if pressed[K_6]:

            # if pressed[K_r]:
            #     #start recording 
            # if pressed[K_t]:
            #     #stop recording
            #     #save recording and send it through modulator
            #     #save the modulator sound as a .wav
            #     #play the recording
            #     #play the outro
        # elif self.model.mode == MODE_PLAYBACK:
        #     if pressed[K_f]:
        #         #replay the stored .wavfile
        #     if pressed[K_s]:
        #         #play instructions recording
        #         #set voice = nothing
        #         self.model.mode == MODE_INSTRUCT

            
if __name__ == '__main__':
    '''THE MAIN STUFF!'''
    controller = Controller()
    pygame.init()
    pygame.mixer.init()
    pygame.time.wait(2500)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handleEvent(event)
        time.sleep(.001)
    view.gameOver(font, level)
    pygame.display.update()
    time.sleep(5)
    pygame.quit()