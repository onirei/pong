from functools import partial

import pygame

from pong.colors import BLACK, WHITE, GRAY
from pong.const import FPS
from pong.scenes.base import AbstractMenuScene
from pong.sprites.menu import MenuItem, MenuCursor


class MenuOptions(AbstractMenuScene):
    def scene(self, *args, **kwargs):
        self.game.screen.fill(BLACK)
        menu_cords = (self.game.width / 5, self.game.height / 5)
        menu_fullscreen = MenuItem(
            name='fullscreen', position=1, cords=menu_cords, align='left', action=self._change_screen_mode
        )
        menu_back = MenuItem(
            name='back', position=2, cords=menu_cords, align='left', action=self._stop_scene
        )

        menu_sprites = pygame.sprite.Group(menu_fullscreen, menu_back)
        cursor = MenuCursor(menu_elements=(menu_fullscreen, menu_back))
        all_sprites = pygame.sprite.Group(menu_fullscreen, cursor, menu_back)
        self.update_main_menu_options(cursor=cursor)

        self.running = True
        while self.running:
            self.game.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                self.game.screen.fill(BLACK)
                self.update_main_menu_options(cursor=cursor)
                self._menu_navigate(event=event, cursor=cursor, menu_sprites=menu_sprites)

            all_sprites.draw(self.game.screen)
            pygame.display.flip()
        self.game.scene.load(scene_name='main_menu')

    def update_main_menu_options(self, cursor):
        conf = self.game.read_config()
        for menu_item in cursor.menu_elements:
            menu_item.max_width = cursor.rect.width
            menu_item.state = str(conf.get(menu_item.name)) if conf.get(menu_item.name) is not None else None
            menu_item.update(color=GRAY)

    def _change_screen_mode(self):
        # переделать под конфиг и выводить состояние
        if self.game.screen_mode:
            self.game.screen_mode = 0
            self.game.screen = pygame.display.set_mode(
                size=(self.game.width, self.game.height), flags=self.game.screen_mode
            )
            self.game.write_config({"fullscreen": False})
        else:
            self.game.screen_mode = pygame.FULLSCREEN
            self.game.screen = pygame.display.set_mode(
                size=(self.game.width, self.game.height), flags=pygame.FULLSCREEN
            )
            self.game.write_config({"fullscreen": True})
