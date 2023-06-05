from cpp_module import RayCast as base_RayCast
import pygame as pg
from settings import *


class RayCasting(base_RayCast):
    def __init__(self, game):
        self.game = game
        self.map = self.game.map.map_obj
        self.objects_to_render = []
        self.ray_casting_result = []
        base_RayCast.__init__(self, self.map)
        self.HEIGHT_OF_VIEW = HEIGHT + 2 * PLAYER_MAX_ANGLE_X

    def update(self):
        self.ray_casting_result = self.ray_cast(self.game.player.x, self.game.player.y, self.game.player.angle)
        self.get_objects_to_render()

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            if proj_height < self.HEIGHT_OF_VIEW:
                wall_column = self.game.object_renderer.wall_textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (int(ray * SCALE), int(HALF_HEIGHT - proj_height // 2 + self.game.player.angle_X))
            else:
                height_aspect = self.HEIGHT_OF_VIEW / proj_height
                texture_height = TEXTURE_SIZE * height_aspect
                wall_column = self.game.object_renderer.wall_textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2 ,
                    SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, self.HEIGHT_OF_VIEW))
                wall_pos = (int(ray * SCALE), int(self.game.player.angle_X - PLAYER_MAX_ANGLE_X))

            self.objects_to_render.append((depth, wall_column, wall_pos))

