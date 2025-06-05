import pygame
import sys
import random
import math
import os

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.tilemap import Tilemap
from scripts.particle import Particle
from scripts.sparks import Spark
 
class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Sleepish')

        self.window = pygame.display.set_mode((640,480)) # sets the size of the window

        self.display = pygame.Surface((320, 240)) #render on this resolution then scale it up to the window size

        self.clock = pygame.time.Clock()

        self.movement= [False, False]

        self.assets = {
            'decor' : load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur= 6),
            'player/run': Animation(load_images('entities/player/run'), img_dur = 4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),

        } #preloads all assets?

        
        
        self.player = Player(self, (50, 50), (8, 15)) #assigns player parameters?0

        self.tilemap = Tilemap(self, tile_size = 16) # assigns the tilemap parameters

        self.level = 0 # current level
        self.load_level(self.level) # loads the level

        self.screenshake = 0

        
        
        self.projectiles = [] # list of projectiles
        self.particles = []
        self.sparks = []

        self.scroll = [0,0] 
        self.dead = 0
        self.transition = -30
    
    def load_level(self, map_id):
        self.tilemap.load('assets/maps/' + str(map_id) + '.json')  # loads the map from the assets folder

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        self.enemies = []  # list of enemies

        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
                self.player.dashing = 0
                self.player.velocity = [0, 0]
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))

        self.particles = []  # Clear all particles when the level is reset
        self.sparks = []  # Optionally clear sparks as well

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0)) # sets the background image

            self.screenshake = max(0, self.screenshake - 1)  # gradually reduce screenshake

            if not len(self.enemies):
                self.transition += 1
                if self.transition > 30:
                    self.level = min(self.level + 1, len(os.listdir('assets/maps/')) - 1)
                    self.load_level(self.level)
                    self.transition = -30  # Reset transition for the next level
            if self.transition < 0:
                self.transition += 1

            if self.dead:
                self.dead += 1
                if self.dead >= 1:
                    self.transition = min(30, self.transition + 1)

                if self.dead > 40:
                    self.load_level(self.level)  # Reload the level after death
                    self.dead = 0
                    self.transition = -30  # Reset transition for the new life

            #the camera. essentialy makes the rest of the world move to keep the player roughly at center
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))
            
            self.tilemap.render(self.display, offset = render_scroll)

            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset = render_scroll)
                if kill:
                    self.enemies.remove(enemy)

            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0] , 0))
                self.player.render(self.display, offset = render_scroll)

            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += projectile[1] 
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(Spark(projectile[0].copy(), random.random() -0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.dead += 1
                        self.screenshake = max(16, self.screenshake)  # Apply screenshake properly
                        for i in range(30):  # Generate particles only when the player is hit
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(Spark(list(self.player.rect().center), angle, 2 + random.random()))
                            self.particles.append(Particle(self, 'particle', list(self.player.rect().center), velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
            
            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)
            
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
                        self.player.jump()
                    if event.key == pygame.K_x:
                        self.player.dash()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() / 2, self.display.get_height() / 2), (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((225, 225, 255))
                self.display.blit(transition_surf, (0, 0))
# game loop

            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
            self.window.blit(pygame.transform.scale(self.display, self.window.get_size()), screenshake_offset)
            pygame.display.update()
            self.clock.tick(60)
Game().run()
