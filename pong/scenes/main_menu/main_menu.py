# import tracemalloc
from functools import partial

import pygame

from pong.colors import BLACK, WHITE
from pong.const import FPS
from pong.scenes.base import AbstractMenuScene
from pong.sprites.menu import MenuCursor, MenuItem


class MainMenu(AbstractMenuScene):
    def scene(self, *args, **kwarg):
        self.game.screen.fill(BLACK)
        logo_text = self.game.assets.font.render('PONG', False, WHITE)
        logo_rect = logo_text.get_rect()
        logo_rect.center = (self.game.width / 2, self.game.height / 4)
        self.game.screen.blit(logo_text, logo_rect)

        menu_cords = (self.game.width / 5 * 1.95, self.game.height / 2)
        menu_1p = MenuItem(
            name='1 player',
            position=1,
            cords=menu_cords,
            align='left',
            action=partial(self.game.scene.load, scene_name='pong', vs_cpu=True),
        )
        menu_2p = MenuItem(
            name='2 players',
            position=2,
            cords=menu_cords,
            align='left',
            action=partial(self.game.scene.load, scene_name='pong'),
        )
        menu_options = MenuItem(
            name='options',
            position=3,
            cords=menu_cords,
            align='left',
            action=partial(self.game.scene.load, scene_name='menu_options'),
        )
        menu_credits = MenuItem(
            name='credits',
            position=4,
            cords=menu_cords,
            align='left',
            action=partial(self.game.scene.load, scene_name='menu_credits'),
        )
        menu_exit = MenuItem(
            name='exit game', position=5, cords=menu_cords, align='left', action=self._stop_scene,
        )
        menu_sprites = pygame.sprite.Group(menu_1p, menu_2p, menu_options, menu_credits, menu_exit)
        cursor = MenuCursor(menu_elements=(menu_1p, menu_2p, menu_options, menu_credits, menu_exit))
        all_sprites = pygame.sprite.Group(menu_1p, menu_2p, menu_options, menu_credits, menu_exit, cursor)

        while self.running:
            self.game.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self._menu_navigate(event=event, cursor=cursor, menu_sprites=menu_sprites)

            all_sprites.draw(self.game.screen)
            pygame.display.flip()
        # current, pic = tracemalloc.get_traced_memory()
        # print(current, pic)
        pygame.quit()
        quit()
