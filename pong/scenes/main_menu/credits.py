import pygame as pg

from pong.colors import BLACK, WHITE
from pong.const import FPS, HEIGHT, JOY_BUTTON_CROSS, JOY_BUTTON_START, WIDTH
from pong.helper import resource_path
from pong.scenes.base import AbstractMenuScene


class MenuCredits(AbstractMenuScene):
    def scene(self, *args, **kwargs):
        self.game.screen.fill(BLACK)
        with open(resource_path('common/credits.txt'), 'r') as file:
            lines = file.read().splitlines()
        credits_text = pg.Surface((WIDTH, len(lines) * 30))
        for i, line in enumerate(lines):
            text = self.game.font_assets.credits_font.render(line, False, WHITE)
            credits_text.blit(text, ((WIDTH-text.get_rect().w)/2, 30 * i))
        wait_for_key_up = kwargs.get('wait_for_key_up', True)
        scrolling_speed = 0.5
        height = HEIGHT
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
                if event.type == pg.KEYDOWN and event.key in (pg.K_SPACE, pg.K_RETURN):
                    scrolling_speed = 5
                if event.type == pg.KEYUP and event.key in (pg.K_SPACE, pg.K_RETURN):
                    scrolling_speed = 0.5
                if self.game.joy:
                    if event.type == pg.JOYBUTTONDOWN and event.button in (JOY_BUTTON_CROSS, JOY_BUTTON_START):
                        scrolling_speed = 5
                    if event.type == pg.JOYBUTTONUP and event.button in (JOY_BUTTON_CROSS, JOY_BUTTON_START):
                        scrolling_speed = 0.5
            height -= scrolling_speed
            if height < -1 * (credits_text.get_rect().h + 50):
                self.running = False
            self.game.screen.fill(BLACK)
            self.game.screen.blit(credits_text, (0, height))
            pg.display.flip()
        self.game.scene.load(scene_name='main_menu')
