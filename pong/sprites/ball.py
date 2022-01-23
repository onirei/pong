import pygame as pg
import random

from pong.colors import WHITE
from pong.const import WIDTH, HEIGHT


class Ball(pg.sprite.Sprite):
    def __init__(self, sfx: pg.mixer.Sound):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((8, 8))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.dx = -1
        self.dy = round(random.uniform(-0.6, 0.6), 1,)
        self.speed = 5
        self.rebound_sound = sfx

    def __str__(self):
        return 'ball'

    def _move(self):
        self.rect.x += self.speed * self.dx
        self.rect.y += self.speed * self.dy
        if self.rect.bottom > HEIGHT or self.rect.top <= 0:
            self.rebound_sound.play()
            self.dy = self.dy * -1

    def update(self, *args, **kwargs):
        if kwargs.get('move'):
            self._move()

    def direction(self):
        return self.dx, self.dy, self.speed

    def reset_position(self):
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.dy = round(random.uniform(-0.6, 0.6), 1,)
        self.speed = 5
