class Controller:
    '''controls the jumpman's motion'''
    def __init__(self,model):
        '''initializes the model'''
        self.model = model
    
    def handleEvent(self, event):
        '''Defines all scenarios that can happen to jumpman and movements associated with said states
            Takes in arrow keys and WASD input, and spacebar to jump'''
        if event.type == QUIT:
            pygame.quit()
        pressed = pygame.key.get_pressed() #finds keys pressed so multiple input can be taken
        if self.model.mode == MODE_UNDERLADDER: 
            #should be able to move up, left, or right, jump
            self.model.jumpman.vx = 0
            self.model.jumpman.vy = 0
            if pressed[K_LEFT] or pressed[ord('a')]:
                self.model.jumpman.vx = -1.0*MOVESPEED
                walk.play()
            if pressed[K_RIGHT] or pressed[ord('d')]:
                self.model.jumpman.vx = 1.0*MOVESPEED
                walk.play()
            if pressed[K_UP] or pressed[ord('w')]:
                self.model.jumpman.vy = -1.0*MOVESPEED
                walk.play()
            if pressed[K_SPACE]:
                jumpNoise.play()
                self.model.jumpman.jump()
        elif self.model.mode == MODE_ABOVELADDER:
            #should be able to move, down, left, right, jump
            self.model.jumpman.vx = 0
            self.model.jumpman.vy = 0
            if pressed[K_LEFT] or pressed[ord('a')]:
                self.model.jumpman.vx = -1.0*MOVESPEED
                walk.play()
            if pressed[K_RIGHT] or pressed[ord('d')]:
                self.model.jumpman.vx = 1.0*MOVESPEED
                walk.play()
            if pressed[K_DOWN] or pressed[ord('s')]:
                self.model.jumpman.vy = 1.0*MOVESPEED
                walk.play()
            if pressed[K_SPACE]:
                jumpNoise.play()
                self.model.jumpman.jump()
        elif self.model.mode == MODE_ONLADDER:        
            #should be able to move up, down
            self.model.jumpman.vx = 0
            self.model.jumpman.vy = 0
            if pressed[K_LEFT] or pressed[ord('a')]:
                self.model.jumpman.vx = -1.0*MOVESPEED
                walk.play()
            if pressed[K_RIGHT] or pressed[ord('d')]:
                self.model.jumpman.vx = 1.0*MOVESPEED
                walk.play()
            if pressed[K_DOWN] or pressed[ord('s')]:
                self.model.jumpman.vy = 1.0*MOVESPEED
                walk.play()
            if pressed[K_UP] or pressed[ord('w')]:
                self.model.jumpman.vy = -1.0*MOVESPEED
                walk.play()
            if pressed[K_SPACE]:
                jumpNoise.play()
                self.model.jumpman.jump()
        elif self.model.mode == MODE_ONPLATFORM:
            #should be able to move left, right, jump
            self.model.jumpman.vx = 0
            self.model.jumpman.vy = 0
            if pressed[K_LEFT] or pressed[ord('a')]:
                self.model.jumpman.vx = -1.0*MOVESPEED
                walk.play()
            if pressed[K_RIGHT] or pressed[ord('d')]:
                self.model.jumpman.vx = 1.0*MOVESPEED
                walk.play()
            if pressed[K_SPACE]:
                jumpNoise.play()
                self.model.jumpman.jump()
        elif self.model.mode == MODE_FALLING:
            #should be able to move left, right
            self.model.jumpman.vx = 0
            if pressed[K_LEFT] or pressed[ord('a')]:
                self.model.jumpman.vx = -1.0*MOVESPEED
                walk.play()
            if pressed[K_RIGHT] or pressed[ord('d')]:
                self.model.jumpman.vx = 1.0*MOVESPEED
                walk.play()
        elif self.model.mode == MODE_UPDOWNLADDER:
            #should be able to move up down left right jump
            self.model.jumpman.vx = 0
            self.model.jumpman.vy = 0
            if event.type != KEYDOWN:
                return
            if pressed[K_LEFT] or pressed[ord('a')]:
                self.model.jumpman.vx = -1.0*MOVESPEED
                walk.play()
            if pressed[K_RIGHT] or pressed[ord('d')]:
                self.model.jumpman.vx = 1.0*MOVESPEED
                walk.play()
            if pressed[K_UP] or pressed[ord('w')]:
                self.model.jumpman.vy = -1.0*MOVESPEED
                walk.play()
            if pressed[K_DOWN] or pressed[ord('s')]:
                self.model.jumpman.vy = 1.0*MOVESPEED
                walk.play()
            if pressed[K_SPACE]:
                self.model.jumpman.jump()
                jumpNoise.play()
            
if __name__ == '__main__':
    '''THE MAIN GAME STUFF!'''
    controller = Controller()
    pygame.time.wait(2500)
    running = True
    #this loop is the running loop within a single game level
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