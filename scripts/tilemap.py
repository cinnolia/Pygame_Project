import pygame

import json

AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2, 
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}

NEIGHBOUR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)] # calculates all the possible positions for tiles to appear on the screen (creates the ongrid space i suppose?)
PHYSICS_TILES = {'stone', 'grass'} #physics tiles are the one that have physics (the decorational ones do not typically this is just to separate them (these are different from offgrid tiles))
AUTOTILE_TYPES = {'grass' , 'stone'}

class Tilemap:
    def __init__(self, game, tile_size = 16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(10):
            self.tilemap[str( 3 + i ) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}
            self.tilemap['10;' + str( 5 + i) ] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))

        for offset in NEIGHBOUR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbours = set()
            for shift in [(1,0), (-1,0), (0, -1), (0, 1)]:
                check_loc = str(tile['pos'][0] + shift) + ';' + str(tile['pos'][1] +shift[1])
                if check_loc in self.tilemap:
                    pass #this is where we're continuing from

    def render(self, surf, offset = (0, 0)):
        for tile in self.offgrid_tiles:
           surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1])) 

        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
              for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                  loc = str(x) + ';' + str(y)
                  if loc in self.tilemap:
                      tile = self.tilemap[loc]
                      surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))[1]