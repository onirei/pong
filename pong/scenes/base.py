import abc
from typing import TYPE_CHECKING

import pygame

from pong.colors import GRAY, WHITE

if TYPE_CHECKING:
    from pong.core import GameCore


class AbstractMenuScene(abc.ABC):
    def __init__(self, game: 'GameCore'):
        self.game = game
        self.running = True

    def _menu_navigate(self, event, cursor, menu_sprites):
        collide = pygame.sprite.spritecollideany(cursor, menu_sprites)
        if collide:
            collide.update(color=WHITE)
        if event.type == pygame.KEYDOWN:
            cursor.navigate(event)
            for sprite in menu_sprites:
                sprite.update(color=GRAY)
            collide = pygame.sprite.spritecollideany(cursor, menu_sprites)
            if collide:
                self.game.assets.rebound_sound.play()
                collide.update(color=WHITE)
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                self.game.assets.rebound_sound.play()
                collide.update(action=True)

    def _stop_scene(self):
        self.running = False

    @staticmethod
    def _exit():
        pygame.quit()
        quit()

    @abc.abstractmethod
    def scene(self):
        ...


class AbstractGameScene(abc.ABC):
    def __init__(self, game: 'GameCore'):
        self.game = game
        self.running = True

    @abc.abstractmethod
    def scene(self):
        ...
