from functools import partial

import pygame

from pong.colors import BLACK, WHITE, GRAY
from pong.const import FPS
from pong.scenes.base import AbstractMenuScene
from pong.sprites.menu import MenuItem, MenuCursor


class MenuKeys(AbstractMenuScene):
    def scene(self, *args, **kwargs):
        self.game.screen.fill(BLACK)
        menu_cords = (self.game.width / 5, self.game.height / 5)
        menu_key_up_1 = MenuItem(
            name='player 1 up', position=1, cords=menu_cords, align='left', action=None,
        )
        menu_key_down_1 = MenuItem(
            name='player 1 down', position=2, cords=menu_cords, align='left', action=None,
        )
        menu_key_up_2 = MenuItem(
            name='player 2 up', position=3, cords=menu_cords, align='left', action=None,
        )
        menu_key_down_2 = MenuItem(
            name='player 2 down', position=4, cords=menu_cords, align='left', action=None,
        )
        menu_back = MenuItem(
            name='back', position=5, cords=menu_cords, align='left', action=self._stop_scene,
        )

        menu_sprites = pygame.sprite.Group(menu_key_up_1, menu_key_down_1, menu_key_up_2, menu_key_down_2, menu_back)
        cursor = MenuCursor(menu_elements=(menu_key_up_1, menu_key_down_1, menu_key_up_2, menu_key_down_2, menu_back))
        all_sprites = pygame.sprite.Group(
            menu_key_up_1, menu_key_down_1, menu_key_up_2, menu_key_down_2, menu_back, cursor,
        )
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
        self.game.scene.load(scene_name='menu_options')

    def update_main_menu_options(self, cursor):
        conf = self.game.read_config()
        for menu_item in cursor.menu_elements:
            menu_item.max_width = cursor.rect.width
            menu_item.state = str(conf.get(menu_item.name)) if conf.get(menu_item.name) is not None else None
            menu_item.update(color=GRAY)
