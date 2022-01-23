from functools import partial

import pygame as pg

from pong.colors import BLACK, GRAY
from pong.const import DEFAULT_ACCEPT_KEYS, FPS, HEIGHT, JOY_AXIS, JOY_KEYS, WIDTH
from pong.scenes.base import AbstractMenuScene
from pong.sprites.menu import MenuActionGroup, MenuCursor, MenuItem


class MenuKeys(AbstractMenuScene):
    def scene(self, *args, **kwargs):
        self.game.screen.fill(BLACK)
        menu_cords = (WIDTH / 10, HEIGHT / 5)
        menu_key_up_1 = MenuItem(
            name='player 1 up',
            position=1,
            cords=menu_cords,
            align='left',
            action=MenuActionGroup(
                **DEFAULT_ACCEPT_KEYS,
                action=partial(self._change_key, key='player 1 up')
            ),
        )
        menu_key_down_1 = MenuItem(
            name='player 1 down',
            position=2,
            cords=menu_cords,
            align='left',
            action=MenuActionGroup(
                **DEFAULT_ACCEPT_KEYS,
                action=partial(self._change_key, key='player 1 down')
            ),
        )
        menu_key_up_2 = MenuItem(
            name='player 2 up',
            position=3,
            cords=menu_cords,
            align='left',
            action=MenuActionGroup(
                **DEFAULT_ACCEPT_KEYS,
                action=partial(self._change_key, key='player 2 up')
            ),
        )
        menu_key_down_2 = MenuItem(
            name='player 2 down',
            position=4,
            cords=menu_cords,
            align='left',
            action=MenuActionGroup(
                **DEFAULT_ACCEPT_KEYS,
                action=partial(self._change_key, key='player 2 down')
            ),
        )
        menu_back = MenuItem(
            name='back',
            position=5,
            cords=menu_cords,
            align='left',
            action=MenuActionGroup(
                **DEFAULT_ACCEPT_KEYS, action=self._stop_scene
            ),
        )

        menu_sprites = pg.sprite.Group(menu_key_up_1, menu_key_down_1, menu_key_up_2, menu_key_down_2, menu_back)
        cursor = MenuCursor(menu_elements=(menu_key_up_1, menu_key_down_1, menu_key_up_2, menu_key_down_2, menu_back))
        all_sprites = pg.sprite.Group(
            menu_key_up_1, menu_key_down_1, menu_key_up_2, menu_key_down_2, menu_back, cursor,
        )
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
        self.game.scene.load(scene_name='menu_options')

    def update_main_menu_options(self, cursor):
        keys = self.game.conf.get('key_map')
        for menu_item in cursor.menu_elements:
            menu_item.max_width = cursor.rect.width
            key = keys.get(menu_item.name)
            if key is not None:
                if key.get('joy') and key.get('axis') is not None:
                    menu_item.state = JOY_AXIS.get(key.get('axis')).get(key.get('key'))
                elif key.get('joy'):
                    menu_item.state = JOY_KEYS.get(key.get('key'))
                else:
                    menu_item.state = pg.key.name(key.get('key'))
            else:
                menu_item.state = ''
            menu_item.update(color=GRAY)

    def _change_key(self, key: str):
        keys = self.game.conf.get('key_map')
        wait_key = True
        while wait_key:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.JOYAXISMOTION and abs(event.dict.get('value')) >= 1:
                    self.game.sfx_assets.rebound_sound.play()
                    keys.get(key).update(dict(joy=True, axis=event.axis, key=int(event.value)))
                    wait_key = False
                if event.type == pg.JOYBUTTONDOWN:
                    self.game.sfx_assets.rebound_sound.play()
                    keys.get(key).update(dict(joy=True, axis=None, key=event.button))
                    wait_key = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.game.sfx_assets.rebound_sound.play()
                        self.wait_key = False
                        return
                    self.game.sfx_assets.rebound_sound.play()
                    keys.get(key).update(dict(joy=False, axis=None, key=event.key))
                    wait_key = False
        self.game.write_config()
