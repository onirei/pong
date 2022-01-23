import abc
from typing import TYPE_CHECKING

import pygame as pg

from pong.colors import GRAY, WHITE
from pong.const import (
    JOY_BUTTON_CROSS,
    JOY_BUTTON_START,
    JOY_DPAD_DOWN,
    JOY_DPAD_LEFT,
    JOY_DPAD_RIGHT,
    JOY_DPAD_UP,
    JOY_LEFT_STICK_AXIS_X,
    JOY_LEFT_STICK_AXIS_Y,
)

if TYPE_CHECKING:
    from pong.core import GameCore


class AbstractMenuScene(abc.ABC):
    def __init__(self, game: 'GameCore'):
        self.game = game
        self.running = True

        # костыль для того, чтобы не прокидывать ассеты в класс меню и не собирать все кнопки управления
        self.navigate_keys = (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT, pg.K_SPACE, pg.K_RETURN, pg.K_ESCAPE)
        self.navigate_joy_axis = (JOY_LEFT_STICK_AXIS_X, JOY_LEFT_STICK_AXIS_Y)
        self.navigate_joy_buttons = (
            JOY_DPAD_UP, JOY_DPAD_DOWN, JOY_DPAD_LEFT, JOY_DPAD_RIGHT, JOY_BUTTON_CROSS, JOY_BUTTON_START,
        )

    def _menu_navigate(self, event, cursor, menu_sprites):
        collide = pg.sprite.spritecollideany(cursor, menu_sprites)
        if collide:
            collide.update(color=WHITE)

        if event.type == pg.KEYDOWN:
            # cursor.navigate(event_key=event.key)  # устаревшее
            if event.key == pg.K_UP:
                self.game.sfx_assets.rebound_sound.play()
                cursor.navigate_up()
            elif event.key == pg.K_DOWN:
                self.game.sfx_assets.rebound_sound.play()
                cursor.navigate_down()
            for sprite in menu_sprites:
                sprite.update(color=GRAY)
            collide = pg.sprite.spritecollideany(cursor, menu_sprites)
            if collide:
                collide.update(color=WHITE)
            if event.key in self.navigate_keys:
                sfx = self.game.sfx_assets.rebound_sound
                collide.update(action=True, event_key=event.key, sfx=sfx)

        if self.game.joy:
            if event.type == pg.JOYAXISMOTION and abs(event.dict.get('value')) >= 1:
                if event.value < 0 and event.axis == JOY_LEFT_STICK_AXIS_Y:
                    self.game.sfx_assets.rebound_sound.play()
                    cursor.navigate_up()
                elif event.value > 0 and event.axis == JOY_LEFT_STICK_AXIS_Y:
                    self.game.sfx_assets.rebound_sound.play()
                    cursor.navigate_down()
                for sprite in menu_sprites:
                    sprite.update(color=GRAY)
                collide = pg.sprite.spritecollideany(cursor, menu_sprites)
                if collide:
                    collide.update(color=WHITE)
                if event.axis in self.navigate_joy_axis:
                    sfx = self.game.sfx_assets.rebound_sound
                    collide.update(action=True, event_axis=event.axis, event_axis_value=event.value, sfx=sfx)

            if event.type == pg.JOYBUTTONDOWN:
                if event.button == JOY_DPAD_UP:
                    self.game.sfx_assets.rebound_sound.play()
                    cursor.navigate_up()
                elif event.button == JOY_DPAD_DOWN:
                    self.game.sfx_assets.rebound_sound.play()
                    cursor.navigate_down()
                for sprite in menu_sprites:
                    sprite.update(color=GRAY)
                collide = pg.sprite.spritecollideany(cursor, menu_sprites)
                if collide:
                    collide.update(color=WHITE)
                if event.button in self.navigate_joy_buttons:
                    sfx = self.game.sfx_assets.rebound_sound
                    # collide.update(action=True, event_button=event.button, sfx=sfx)
                    collide.update(action=True, event_joy_key=event.button, sfx=sfx)

    def _stop_scene(self):
        self.running = False

    @staticmethod
    def _exit():
        pg.quit()
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
