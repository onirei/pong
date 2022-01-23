# import tracemalloc
from functools import partial

import pygame as pg

from pong.colors import BLACK, WHITE
from pong.const import DEFAULT_ACCEPT_KEYS, FPS, HEIGHT, WIDTH
from pong.scenes.base import AbstractMenuScene
from pong.sprites.menu import MenuActionGroup, MenuCursor, MenuItem


class MainMenu(AbstractMenuScene):
    def scene(self, *args, **kwargs):
        self.game.screen.fill(BLACK)
        pg.mixer.music.set_volume(0)
        logo_text = self.game.font_assets.font.render('PONG', False, WHITE)
        logo_rect = logo_text.get_rect()
        logo_rect.center = (WIDTH / 2, HEIGHT / 4)
        self.game.screen.blit(logo_text, logo_rect)

        menu_cords = (WIDTH / 5 * 1.95, HEIGHT / 2)
        menu_1p = MenuItem(
            name='1 player',
            position=1,
            cords=menu_cords,
            align='left',
            action=MenuActionGroup(
                **DEFAULT_ACCEPT_KEYS,
                action=partial(self.game.scene.load, scene_name='pong', vs_cpu=True),
            ),
        )
        menu_2p = MenuItem(
            name='2 players',
            position=2,
            cords=menu_cords,
            align='left',
            action=MenuActionGroup(
                **DEFAULT_ACCEPT_KEYS,
                action=partial(self.game.scene.load, scene_name='pong'),
            ),
        )
        menu_options = MenuItem(
            name='options',
            position=3,
            cords=menu_cords,
            align='left',
            action=MenuActionGroup(
                **DEFAULT_ACCEPT_KEYS,
                action=partial(self.game.scene.load, scene_name='menu_options'),
            ),
        )
        menu_credits = MenuItem(
            name='credits',
            position=4,
            cords=menu_cords,
            align='left',
            action=MenuActionGroup(
                **DEFAULT_ACCEPT_KEYS,
                action=partial(self.game.scene.load, scene_name='menu_credits'),
            ),
        )
        menu_exit = MenuItem(
            name='exit game',
            position=5,
            cords=menu_cords,
            align='left',
            action=MenuActionGroup(
                **DEFAULT_ACCEPT_KEYS,
                action=self._stop_scene,
            ),
        )
        menu_sprites = pg.sprite.Group(menu_1p, menu_2p, menu_options, menu_credits, menu_exit)
        cursor = MenuCursor(menu_elements=(menu_1p, menu_2p, menu_options, menu_credits, menu_exit))
        all_sprites = pg.sprite.Group(menu_1p, menu_2p, menu_options, menu_credits, menu_exit, cursor)

        wait_for_key_up = kwargs.get('wait_for_key_up', True)
        while self.running:
            self.game.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYUP or event.type == pg.JOYBUTTONUP:
                    wait_for_key_up = False
                if wait_for_key_up:
                    continue
                self._menu_navigate(event=event, cursor=cursor, menu_sprites=menu_sprites)

            all_sprites.draw(self.game.screen)
            pg.display.flip()
        # current, pic = tracemalloc.get_traced_memory()
        # print(current, pic)
        pg.quit()
        quit()
