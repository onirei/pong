from functools import partial

import pygame as pg

from pong.colors import BLACK, GRAY
from pong.const import (
    DEFAULT_ACCEPT_KEYS, FPS, HEIGHT, JOY_BUTTON_CROSS, JOY_BUTTON_START, JOY_DPAD_LEFT, JOY_DPAD_RIGHT, WIDTH,
)
from pong.scenes.base import AbstractMenuScene
from pong.sprites.menu import MenuActionGroup, MenuCursor, MenuItem


class MenuOptions(AbstractMenuScene):
    def scene(self, *args, **kwargs):
        self.game.screen.fill(BLACK)
        menu_cords = (WIDTH / 5, HEIGHT / 5)
        menu_fullscreen = MenuItem(
            name='fullscreen',
            position=1,
            cords=menu_cords,
            align='left',
            action=MenuActionGroup(
                event_key=(pg.K_SPACE, pg.K_RETURN, pg.K_LEFT, pg.K_RIGHT),
                event_joy_key=(JOY_BUTTON_CROSS, JOY_BUTTON_START, JOY_DPAD_LEFT, JOY_DPAD_RIGHT),
                action=self._change_screen_mode),
        )
        volume_action = MenuActionGroup()
        volume_action.add(
            event_key=pg.K_LEFT,
            event_joy_key=JOY_DPAD_LEFT,
            action=self._down_volume,
        )
        volume_action.add(
            event_key=pg.K_RIGHT,
            event_joy_key=JOY_DPAD_RIGHT,
            action=self._up_volume,
        )
        menu_volume = MenuItem(
            name='volume', position=2, cords=menu_cords, align='left', action=volume_action,
        )
        menu_keys = MenuItem(
            name='keys',
            position=3,
            cords=menu_cords,
            align='left',
            action=MenuActionGroup(
                **DEFAULT_ACCEPT_KEYS,
                action=partial(self.game.scene.load, scene_name='menu_keys'),
            ),
        )
        difficult_action = MenuActionGroup()
        difficult_action.add(
            event_key=pg.K_LEFT,
            event_joy_key=JOY_DPAD_LEFT,
            action=partial(self._change_difficult, mod=-1)
        )
        difficult_action.add(
            event_key=pg.K_RIGHT,
            event_joy_key=JOY_DPAD_RIGHT,
            action=partial(self._change_difficult, mod=1)
        )
        menu_difficult = MenuItem(
            name='difficult', position=4, cords=menu_cords, align='left', action=difficult_action,
        )
        menu_back = MenuItem(
            name='back',
            position=5,
            cords=menu_cords,
            align='left',
            action=MenuActionGroup(**DEFAULT_ACCEPT_KEYS, action=self._stop_scene),
        )

        menu_sprites = pg.sprite.Group(menu_fullscreen, menu_volume, menu_keys, menu_difficult, menu_back)
        cursor = MenuCursor(menu_elements=(menu_fullscreen, menu_volume, menu_keys, menu_difficult, menu_back))
        all_sprites = pg.sprite.Group(menu_fullscreen, menu_volume, menu_keys, menu_back, menu_difficult, cursor)
        self.update_main_menu_options(cursor=cursor)

        wait_for_key_up = kwargs.get('wait_for_key_up', True)
        self.running = True
        while self.running:
            self.game.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYUP or event.type == pg.JOYBUTTONUP:
                    wait_for_key_up = False
                if wait_for_key_up:
                    continue
                self.game.screen.fill(BLACK)
                self.update_main_menu_options(cursor=cursor)
                self._menu_navigate(event=event, cursor=cursor, menu_sprites=menu_sprites)

            all_sprites.draw(self.game.screen)
            pg.display.flip()
        self.game.scene.load(scene_name='main_menu')

    def update_main_menu_options(self, cursor):
        conf = self.game.conf
        for menu_item in cursor.menu_elements:
            menu_item.max_width = cursor.rect.width
            menu_item.state = str(conf.get(menu_item.name)) if conf.get(menu_item.name) is not None else None
            menu_item.update(color=GRAY)

    def _change_screen_mode(self):
        screen_mode = self.game.conf.get('fullscreen')
        if screen_mode:
            self.game.screen_mode = 0
            self.game.screen = pg.display.set_mode(
                size=(WIDTH, HEIGHT), flags=self.game.screen_mode
            )
            self.game.conf.update(dict(fullscreen=False))
            self.game.write_config()
        else:
            self.game.screen_mode = pg.FULLSCREEN
            self.game.screen = pg.display.set_mode(
                size=(WIDTH, HEIGHT), flags=pg.FULLSCREEN
            )
            self.game.conf.update(dict(fullscreen=True))
            self.game.write_config()

    def _change_volume(self, step: float):
        volume = self.game.conf.get('volume')
        volume = round(volume + step, 1)
        if 0 <= volume <= 1:
            self.game.sfx_assets.sfx.set_master_volume(volume)
            self.game.conf.update({'volume': volume})
            self.game.write_config()

    def _up_volume(self):
        self._change_volume(step=0.1)

    def _down_volume(self):
        self._change_volume(step=-0.1)

    def _change_difficult(self, mod: int = 0):
        difficult_values = {0: 'easy', 1: 'normal', 2: 'hard'}
        difficult_keys = {'easy': 0, 'normal': 1, 'hard': 2}
        difficult = difficult_keys.get(self.game.conf.get('difficult', 1))
        difficult += mod
        if 0 <= difficult <= 2:
            self.game.conf.update({'difficult': difficult_values.get(difficult)})
            self.game.write_config()
