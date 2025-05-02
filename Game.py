import pygame
import sys
from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Comatose')

        self.window = pygame.display.set_mode((864,540))

        self.display = pygame.Surface((288, 180)) #render on this resolution then scale it up to the window size

        self.clock = pygame.time.Clock()

        self.movement= [False, False]

        self.assets = {
            'decor' : load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'background_1': load_image('background_1.png'),
            'background_2': load_image('background_2.png'),
            'clouds': load_images('clouds'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur = 6),
            'player/run': Animation(load_images('entities/player/run'), img_dur = 4),
            'player/jump': Animation(load_images('entities/player/jump'), img_dur = 3),
            'player/slide': Animation(load_images('entities/player/slide'), img_dur = 2),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide'), img_dur = 2),

        }
        self.clouds = Clouds(self.assets['clouds'], count = 16)
        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))

        self.tilemap = Tilemap(self, tile_size = 16)

        self.scroll = [0,0]


    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0))
            self.display.blit(self.assets['background_1'], (0, 0))
            self.display.blit(self.assets['background_2'], (0, 0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            self.clouds.update()
            self.clouds.render(self.display, offset = render_scroll)

            self.tilemap.render(self.display, offset = render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0] , 0))
            self.player.render(self.display, offset = render_scroll)


            

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
                        self.player.velocity[1] = -2
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

# game loop
            self.window.blit(pygame.transform.scale(self.display, self.window.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
Game().run()
