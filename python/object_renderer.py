import pygame as pg
from settings import *
from cpp_module import ObjectRenderer as base_ObjectRenderer


class ObjectRenderer(base_ObjectRenderer):
    def __init__(self, game):
        self.game = game
        self.screen = game.sc
        base_ObjectRenderer.__init__(self, self.game.sc)
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT + PLAYER_MAX_ANGLE_X))
        self.sky_offset = 0

    def draw(self):
        self.draw_background()
        self.render_game_objects(self.game.raycasting.objects_to_render)

    def draw_background(self):
        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, 0, WIDTH, HEIGHT))
        # sky
        self.sky_offset = (self.sky_offset + 2.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0), (0, HALF_HEIGHT - self.game.player.angle_X - 20, WIDTH, HALF_HEIGHT + PLAYER_MAX_ANGLE_X))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0), (0, HALF_HEIGHT - self.game.player.angle_X - 20, WIDTH, HALF_HEIGHT + PLAYER_MAX_ANGLE_X))

    def render_game_objects_2(self):
        for depth, image, pos in self.game.raycasting.objects_to_render:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
        }