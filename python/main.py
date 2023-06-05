import sys
sys.path.append("C:/Users/Oleg/Desktop/kursova/build/Debug")
import pygame as pg
from settings import *
from map import Map, Mini_Map
from object_renderer import ObjectRenderer
from player import Player
from raycasting import RayCasting
from sprites import *
from object_handler import ObjectHandler


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.sc = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()
        self.show_mini_map = True

    def new_game(self):
        self.map = Map(self)
        self.mini_map = Mini_Map(self)
        self.player = Player(self)
        self.raycasting = RayCasting(self)
        self.object_renderer = ObjectRenderer(self)
        self.object_handler = ObjectHandler(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{NAME_PROG}   {self.clock.get_fps() :.1f}')

    def draw(self):
        self.object_renderer.draw()
        if self.show_mini_map:
            self.mini_map.draw()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit(0)
            if (event.type == pg.KEYDOWN and event.key == pg.K_m):
                self.show_mini_map = False if self.show_mini_map else True
            

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
