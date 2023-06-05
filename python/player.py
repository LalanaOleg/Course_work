from settings import *
import pygame as pg


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = float(PLAYER_ANGLE)
        self.angle_X = 0.0
        self.rel = 0
        
    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        dx, dy = 0, 0
        keys = pg.key.get_pressed()

        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        self.check_wall_collision(dx, dy)

        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
            self.rel = -PLAYER_ROT_SPEED * self.game.delta_time * MOUSE_MAX_REL * (PLAYER_ROT_SPEED // MOUSE_SENSITIVITY)
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time
            self.rel = PLAYER_ROT_SPEED * self.game.delta_time * MOUSE_MAX_REL * (PLAYER_ROT_SPEED // MOUSE_SENSITIVITY)
        self.angle %= math.tau

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT \
                or my < MOUSE_BORDER_UPPER or my > MOUSE_BORDER_LOWER:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        
        self.rel, rel_X = pg.mouse.get_rel()
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time
        self.angle %= math.tau
        self.rel *= 4 / 3.5

        d_angle_x = self.angle_X
        rel_X = -max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, rel_X))
        d_angle_x += rel_X * MOUSE_SENSITIVITY * self.game.delta_time * 1000
        self.angle_X = max(-PLAYER_MAX_ANGLE_X, min(PLAYER_MAX_ANGLE_X, d_angle_x))

    def update(self):
        self.mouse_control()
        self.movement()

    def draw(self):
        pg.draw.line(self.game.sc, GREEN, (self.x * MINI_MAP_SIZE_BLOCK, self.y * MINI_MAP_SIZE_BLOCK),
                     (self.x * MINI_MAP_SIZE_BLOCK + 10 * math.cos(self.angle),
                      self.y * MINI_MAP_SIZE_BLOCK + 10 * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.sc, RED, (self.x * MINI_MAP_SIZE_BLOCK, self.y * MINI_MAP_SIZE_BLOCK), 5)

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
