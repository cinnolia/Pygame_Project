import pygame
import sys
from scripts.utils import load_image
from scripts.entities import PhysicsEntity


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Comatose')

        self.window = pygame.display.set_mode((640,480))

        self.clock = pygame.time.Clock() 

        self.movement= [False, False]

        self.assets = {
            'player': load_image('entities\player.png')
        }
        
        self.player = PhysicsEntity(self, 'player', (50,50), (8, 15))


    def run(self):
        while True:
            self.window.fill((0,28,0))

            self.player.update((self.movement[1] - self.movement[0]))
            self.player.render(self.window)   
#input management?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()   
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

# game loop
            pygame.display.update()
            self.clock.tick(60)
Game().run()
#picture this: eating a burger on the job, boss or customer walks inshe literally puts whats left of it in her pocket and when they leave she just like... yoinks it out and continues eating it... (lol me core)