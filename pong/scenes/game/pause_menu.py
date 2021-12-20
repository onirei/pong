from functools import partial

import pygame

from pong.colors import BLACK, WHITE, GRAY
from pong.const import FPS
from pong.scenes.base import AbstractMenuScene
from pong.sprites.menu import MenuCursor, MenuItem


class GamePause(AbstractMenuScene):
    def scene(self, *args, **kwargs):
        self.running = True
        blur = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
        blur.fill((20, 20, 20, 190))
        self.game.screen.blit(blur, (0, 0))
        pause_text = self.game.assets.font.render('Paused', False, WHITE)
        pause_rect = pause_text.get_rect()
        pause_rect.center = (self.game.width / 2, self.game.height / 4)
        self.game.screen.blit(pause_text, pause_rect)
        menu_cords = (self.game.width / 5 * 1.95, self.game.height / 2)
        menu_resume = MenuItem(
            name='resume',
            position=1,
            cords=menu_cords,
            align='left',
            action=self._stop_scene,
        )
        menu_main_screen = MenuItem(
            name='main screen',
            position=2,
            cords=menu_cords,
            align='left',
            action=partial(self.game.scene.load, scene_name='main_menu'),
        )
        menu_exit = MenuItem(
            name='exit',
            position=3,
            cords=menu_cords,
            align='left',
            action=self._exit,
        )
        menu_sprites = pygame.sprite.Group(menu_resume, menu_main_screen, menu_exit)
        cursor = MenuCursor(menu_elements=(menu_resume, menu_main_screen, menu_exit))
        all_sprites = pygame.sprite.Group(menu_resume, menu_main_screen, menu_exit, cursor)

        self.running = True
        while self.running:
            self.game.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                self._menu_navigate(event=event, cursor=cursor, menu_sprites=menu_sprites)
            all_sprites.draw(self.game.screen)
            pygame.display.flip()
