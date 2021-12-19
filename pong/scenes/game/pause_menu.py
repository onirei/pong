from functools import partial

import pygame

from pong.colors import BLACK, WHITE, GRAY
from pong.const import FPS
from pong.scenes.base import AbstractMenuScene
from pong.sprites.menu import MenuCursor, MenuItem


class GamePause(AbstractMenuScene):
    def scene(self, *args, **kwargs):
        clock = pygame.time.Clock()

        blur = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
        blur.fill((0, 0, 0, 190))
        self.game.screen.blit(blur, (0, 0))

        font = pygame.font.SysFont('Comic Sans MS', 56)
        score_text = font.render('Paused', False, WHITE)
        score = score_text.get_rect()
        score.center = (self.game.width / 2, self.game.height / 2)
        self.game.screen.blit(score_text, score)

        menu_resume = MenuItem(name='resume', position=1)
        menu_main_screen = MenuItem(name='main screen', position=1)
        menu_exit = MenuItem(name='exit', position=2)
        menu_items = pygame.sprite.Group(menu_resume, menu_main_screen, menu_exit)

        cursor = MenuCursor(menu_elements=(menu_resume, menu_main_screen, menu_exit))

        all_sprites = pygame.sprite.Group()
        all_sprites.add(menu_resume, menu_exit, cursor)

        pause = True
        while pause:
            for event in pygame.event.get():
                self.game.clock.tick(FPS)
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game.assets.rebound_sound.play()
                        pause = False
                    cursor.navigate(event)

                    for sprite in menu_items:
                        sprite.rerender(GRAY)

                    collide = pygame.sprite.spritecollideany(cursor, menu_items)
                    if collide:
                        self.game.assets.rebound_sound.play()
                        collide.rerender(WHITE)

                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.game.assets.rebound_sound.play()
                        if collide is menu_exit:
                            pygame.quit()
                            quit()
                        if collide is menu_resume:
                            pause = False
                        if collide is full_screen:
                            screen = pygame.display.set_mode((self.game.width, self.game.height), pygame.FULLSCREEN)

            all_sprites.update()
            all_sprites.draw(self.game.screen)
            pygame.display.flip()
