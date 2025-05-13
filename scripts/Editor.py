import pygame
import sys
from scripts.utils import load_images
from scripts.tilemap import Tilemap

RENDER_SCALE=2.0

 
class Editor:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Editor')

        self.window = pygame.display.set_mode((640,480)) # sets the size of the window

        self.display = pygame.Surface((320, 240)) #render on this resolution then scale it up to the window size

        self.clock = pygame.time.Clock()



        self.assets = {
            'decor' : load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone')
        } #preloads all assets?

        self.movement= [False, False, False, False]        

        self.tilemap = Tilemap(self, tile_size = 16) # assigns the tilemap parameters

        self.scroll = [0,0] 


    def run(self):
        while True:
            self.display.fill((0, 0, 0)) # sets the background image
            

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
                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False

# game loop
            self.window.blit(pygame.transform.scale(self.display, self.window.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
Editor().run()
