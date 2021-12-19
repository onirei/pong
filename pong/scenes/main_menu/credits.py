import pygame

from pong.colors import BLACK
from pong.const import FPS
from pong.scenes.base import AbstractMenuScene


class MenuCredits(AbstractMenuScene):
    def scene(self, *args, **kwargs):
        self.game.screen.fill(BLACK)

        while self.running:
            self.game.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.game.assets.rebound_sound.play()
                        self.running = False
            pygame.display.flip()
        self.game.scene.load(scene_name='main_menu')
