import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Comatose')

        self.window = pygame.display.set_mode((640,480))

        self.clock = pygame.time.Clock() 

        self.img = pygame.image.load('assets\images\clouds\cloud_2.png')
        self.img.set_colorkey((0,0,0))
        self.img_pos = [160,260]
        self.movement = [False, False]

        self.collisoion_area = pygame.Rect(50, 50, 300, 50)
    
    def run(self):
        while True:
            self.window.fill((0,56,0))

            img_r = pygame.Rect(self.img_pos[0], self.img_pos[1], self.img.get_width(), self.img.get_height())
            
            if img_r.colliderect(self.collisoion_area):
                pygame.draw.rect(self.window, (0,100,225),self.collisoion_area)
            else:
                pygame.draw.rect(self.window, (0,100,125),self.collisoion_area)
            
            self.img_pos[1] += (self.movement[1] - self.movement[0]) * 5
            self.window.blit(self.img, self.img_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()   
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = False
                 
        
            pygame.display.update()
            self.clock.tick(60)
Game().run()
#picture this: eating a burger on the job, boss or customer walks inshe literally puts whats left of it in her pocket and when they leave she just like... yoinks it out and continues eating it... (lol me core)