import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Comatose')

        self.window = pygame.display.set_mode((640,480))

        self.clock = pygame.time.Clock() 

        self.image.load('')

def run(self):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()    
    
        pygame.display.update()
        self.clock.tick(60)
Game().run()
