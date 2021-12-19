import pygame

from pong.colors import WHITE
from pong.const import WIDTH, HEIGHT


class Racket(pygame.sprite.Sprite):
    def __init__(self, playable: bool = False, left_side: bool = False):
        pygame.sprite.Sprite.__init__(self)
        self.playable = playable
        self.left_side = left_side
        self.image = pygame.Surface((7, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = self._get_position()
        self.score = 0

    def __str__(self):
        if self.playable:
            return 'Player'
        else:
            return 'Bot'
            # if pygame.joystick.get_count() and pygame.joystick.get_init():
            #     gamepad = pygame.joystick.Joystick(0)
            #     if gamepad.get_button(0):
            #         print('крест')
            #     if gamepad.get_button(1):
            #         print('круг')
            #     if gamepad.get_button(2):
            #         print('квадрат')
            #     if gamepad.get_button(3):
            #         print('треугольник')
            #
            #     if gamepad.get_button(5):
            #         print(5)
            #     if gamepad.get_axis(1) > 0.1 and self.rect.bottom < HEIGHT:
            #         self.rect.y += 5
            #     if gamepad.get_axis(1) < -0.1 and self.rect.top > 0:
            #         self.rect.y -= 5

    def _get_position(self):
        if self.left_side:
            return WIDTH * 0.05, HEIGHT / 2
        return WIDTH - WIDTH * 0.05, HEIGHT / 2

    def update(self):
        if self.playable:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.rect.top > HEIGHT*0.05:
                self.rect.y -= 10
            if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT - HEIGHT*0.05:
                self.rect.y += 10

    def reset_position(self):
        if self.left_side:
            self.rect.center = (WIDTH*0.05, HEIGHT / 2)
        else:
            self.rect.center = (WIDTH-WIDTH*0.05, HEIGHT / 2)
        # self.score = 0

    def _bot_1_action(self, cord_y):
        if self.rect.centery > cord_y and self.rect.top > HEIGHT * 0.05:
            self.rect.y -= 10
        if self.rect.centery < cord_y and self.rect.bottom < HEIGHT - HEIGHT * 0.05:
            self.rect.y += 10

    def bot_1(self, coords, direction):
        if not self.playable:
            cord_x, cord_y = coords
            dx, *_ = direction
            react_mod = 3
            react_zone = cord_x < WIDTH - WIDTH / react_mod if self.left_side else cord_x > WIDTH / react_mod
            if (not self.left_side and react_zone and dx == 1) or (self.left_side and react_zone and dx == -1):
                self._bot_1_action(cord_y)

    def bot_2(self, point_xy):
        print(point_xy)

