from functools import partial

import pygame as pg

from pong.colors import WHITE
from pong.const import DEFAULT_ACCEPT_KEYS, FPS, HEIGHT, WIDTH
from pong.scenes.base import AbstractMenuScene
from pong.sprites.menu import MenuActionGroup, MenuCursor, MenuItem


class GamePause(AbstractMenuScene):
    def scene(self, *args, **kwargs):
        self.running = True
        blur = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        blur.fill((20, 20, 20, 190))
        self.game.screen.blit(blur, (0, 0))
        pause_text = self.game.font_assets.font.render('Paused', False, WHITE)
        pause_rect = pause_text.get_rect()
        pause_rect.center = (WIDTH / 2, HEIGHT / 4)
        self.game.screen.blit(pause_text, pause_rect)
        menu_cords = (WIDTH / 5 * 1.95, HEIGHT / 2)
        menu_resume = MenuItem(
            name='resume',
            position=1,
            cords=menu_cords,
            align='left',
            action=MenuActionGroup(**DEFAULT_ACCEPT_KEYS, action=self._stop_scene),)
        menu_main_screen = MenuItem(
            name='main screen',
            position=2,
            cords=menu_cords,
            align='left',
            action=MenuActionGroup(
                **DEFAULT_ACCEPT_KEYS, action=partial(self.game.scene.load, scene_name='main_menu')
            ),
        )
        menu_exit = MenuItem(
            name='exit',
            position=3,
            cords=menu_cords,
            align='left',
            action=MenuActionGroup(**DEFAULT_ACCEPT_KEYS, action=self._exit),
        )
        menu_sprites = pg.sprite.Group(menu_resume, menu_main_screen, menu_exit)
        cursor = MenuCursor(menu_elements=(menu_resume, menu_main_screen, menu_exit))
        all_sprites = pg.sprite.Group(menu_resume, menu_main_screen, menu_exit, cursor)

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
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                self._menu_navigate(event=event, cursor=cursor, menu_sprites=menu_sprites)
            all_sprites.draw(self.game.screen)
            pg.display.flip()

        pg.key.set_repeat()
