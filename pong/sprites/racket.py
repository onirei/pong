from typing import Dict, Optional

import pygame as pg

from pong.colors import WHITE
from pong.const import HEIGHT, WIDTH
from pong.sprites import Ball


class Racket(pg.sprite.Sprite):
    def __init__(
            self,
            ball: 'Ball',
            playable: bool = False,
            left_side: bool = False,
            difficult: Optional[str] = None,
            keys: Optional[Dict] = None,
    ):
        pg.sprite.Sprite.__init__(self)
        self.playable = playable
        self.left_side = left_side
        self.image = pg.Surface((7, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = self._get_position()
        self.score = 0
        self.ball = ball

        difficult_mods = {
            'easy': dict(react_mod=1.5, bot_move_speed=6),
            'normal': dict(react_mod=2.5, bot_move_speed=8),
            'hard': dict(react_mod=3.5, bot_move_speed=10),
        }
        self.react_mod = difficult_mods.get(difficult, dict()).get('react_mod', 1)
        self.bot_move_speed = difficult_mods.get(difficult, dict()).get('bot_move_speed', 0)
        # key joy joy_axis
        self.up_key = {}
        self.down_key = {}
        if self.playable:
            self._setup_keys(keys)

    def __str__(self):
        if self.playable:
            return 'Player'
        else:
            return 'Bot'

    def _setup_keys(self, keys: Dict):
        if self.left_side:
            self.up_key = keys.get('player 1 up')
            self.down_key = keys.get('player 1 down')
        else:
            self.up_key = keys.get('player 2 up')
            self.down_key = keys.get('player 2 down')

    def _get_position(self):
        if self.left_side:
            return WIDTH * 0.05, HEIGHT / 2
        return WIDTH - WIDTH * 0.05, HEIGHT / 2

    def collide(self):
        pass
        # 0-10 10-24 24-29 29-40 40-50
        vectors = {
            10: {'speed': 5, 'angle': 1.5},
            24: {'speed': 4.5, 'angle': 1},
            29: {'speed': 4, 'angle': 0},
            40: {'speed': 4.5, 'angle': 1},
            50: {'speed': 5, 'angle': 1.5}
        }
        keys = [pg.K_UP, pg.K_DOWN]
        clip = self.rect.clip(self.ball.rect)
        collide_point = self.rect.y + self.rect.height - clip.y
        self.ball.dx = self.ball.dx * -1
        sign = -1 if self.ball.dy < 0 else 1
        for vector in vectors:
            speed_mod = 0
            if list(key for key in keys if pg.key.get_pressed()[key]):
                speed_mod = 1
            if collide_point <= vector:
                self.ball.dy = vectors.get(vector).get('angle') * sign
                self.ball.speed = vectors.get(vector).get('speed') + speed_mod
                break
        if self.ball.rect.x > WIDTH / 2:
            self.ball.rect.x = self.rect.x - self.ball.rect.width
        else:
            self.ball.rect.x = self.rect.x + self.rect.width + self.ball.rect.width

    def update(self, *args, **kwargs):
        if kwargs.get('bot'):
            self._bot()
        if kwargs.get('collide'):
            self.collide()

    def move_up(self):
        if self.playable and self.rect.top > HEIGHT*0.05:
            self.rect.y -= 8

    def move_down(self):
        if self.playable and self.rect.bottom < HEIGHT - HEIGHT*0.05:
            self.rect.y += 8

    def reset_position(self):
        self.rect.center = self._get_position()

    def _bot(self):
        if not self.playable:
            cord_x, cord_y = self.ball.rect.center
            dx, *_ = self.ball.direction()
            # чем ниже этот кооф, тем меньше зона реакции 1 - нулевая зона, стандартно - 3
            # 1.3 - 2 - very easy
            react_zone = cord_x < WIDTH - WIDTH / self.react_mod if self.left_side else cord_x > WIDTH / self.react_mod
            if (not self.left_side and react_zone and dx == 1) or (self.left_side and react_zone and dx == -1):
                self._bot_action(cord_y)

    def _bot_action(self, cord_y):
        # снизить для ослабления повысить для сложности
        if self.rect.centery > cord_y and self.rect.top > HEIGHT * 0.05:
            self.rect.y -= self.bot_move_speed
        if self.rect.centery < cord_y and self.rect.bottom < HEIGHT - HEIGHT * 0.05:
            self.rect.y += self.bot_move_speed
