import pygame as pg
from settings import *
from cpp_module import Map as base_map

_ = False
mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, 1],
    [1, _, _, 1, 1, 1, 1, _, _, _, 1, 1, 1, _, _, 1],
    [1, _, _, _, _, _, 1, _, _, _, _, _, 1, _, _, 1],
    [1, _, _, _, _, _, 1, _, _, _, _, _, 1, _, _, 1],
    [1, _, _, 1, 1, 1, 1, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 1, _, _, _, _, _, _, 1, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class Map(base_map):
    def __init__(self, game):
        base_map.__init__(self, MAP_PATH)
        self.game = game
        self.map_obj = base_map.get_this(self)
        self.map = base_map.get_map(self)
        self.rows = len(self.map)
        self.cols = len(self.map[0])
        self.world_map = base_map.get_world_set(self)


class Mini_Map(Map):
    def __init__(self, game):
        base_map.__init__(self)
        self.game = game
        self.mini_map = self.game.map.map
        self.rows = len(self.mini_map)
        self.cols = len(self.mini_map[0])
        self.world_set = self.game.map.world_map
    
    def draw(self):
        pg.draw.rect(self.game.sc, (0, 0, 0), (0, 0, self.cols * MINI_MAP_SIZE_BLOCK, self.rows * MINI_MAP_SIZE_BLOCK))
        [pg.draw.rect(self.game.sc, DARKGRAY, (pos[0] * MINI_MAP_SIZE_BLOCK, pos[1] * MINI_MAP_SIZE_BLOCK,
                                            MINI_MAP_SIZE_BLOCK, MINI_MAP_SIZE_BLOCK), 2)
        for pos in self.world_set]
        pg.draw.line(self.game.sc, GREEN, (self.game.player.x * MINI_MAP_SIZE_BLOCK, self.game.player.y * MINI_MAP_SIZE_BLOCK),
                     (self.game.player.x * MINI_MAP_SIZE_BLOCK + 10 * math.cos(self.game.player.angle),
                      self.game.player.y * MINI_MAP_SIZE_BLOCK + 10 * math.sin(self.game.player.angle)), 2)
        pg.draw.circle(self.game.sc, RED, (self.game.player.x * MINI_MAP_SIZE_BLOCK, self.game.player.y * MINI_MAP_SIZE_BLOCK), 5)
    
