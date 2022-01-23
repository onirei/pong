import random

import pygame as pg

from pong.colors import BLACK, WHITE
from pong.const import FPS, WIDTH, HEIGHT
from pong.scenes.base import AbstractGameScene
from pong.sprites import Ball, Racket


class Pong(AbstractGameScene):
    def scene(self, *args, **kwargs):
        ball = Ball(sfx=self.game.sfx_assets.rebound_sound)
        keys = self.game.conf.get('key_map')
        player_1 = Racket(playable=True, left_side=True, ball=ball, keys=keys)
        if kwargs.get('vs_cpu'):
            difficult = self.game.conf.get('difficult', 1)
            player_2 = Racket(ball=ball, difficult=difficult)
        else:
            player_2 = Racket(playable=True, ball=ball, keys=keys)

        all_sprites = pg.sprite.Group(player_1, player_2, ball)
        players = pg.sprite.Group(player_1, player_2)

        pg.key.set_repeat()

        move_up = False
        move_down = False

        self.running = True
        while self.running:
            self.game.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key in (pg.K_ESCAPE, pg.K_SPACE):
                        self.game.sfx_assets.rebound_sound.play()
                        self.game.scene.load(scene_name='pause_menu')

                if player_1.playable:
                    if player_1.up_key.get('joy') and player_1.up_key.get('axis') is not None:
                        if (event.type == pg.JOYAXISMOTION and event.axis == player_1.up_key.get('axis')
                                and int(round(event.value, 0)) == player_1.up_key.get('key')):
                            move_up = True
                        if (event.type == pg.JOYAXISMOTION and event.axis == player_1.up_key.get('axis')
                                and int(round(event.value, 0)) == 0):
                            move_up = False
                    elif player_1.up_key.get('joy'):
                        if event.type == pg.JOYBUTTONDOWN and event.button == player_1.up_key.get('key'):
                            move_up = True
                        if event.type == pg.JOYBUTTONUP and event.button == player_1.up_key.get('key'):
                            move_up = False
                    elif player_1.up_key.get('key'):
                        if event.type == pg.KEYDOWN and event.key == player_1.up_key.get('key'):
                            move_up = True
                        if event.type == pg.KEYUP and event.key == player_1.up_key.get('key'):
                            move_up = False
                    if player_1.down_key.get('joy') and player_1.down_key.get('axis') is not None:
                        if (event.type == pg.JOYAXISMOTION and event.axis == player_1.down_key.get('axis')
                                and int(event.value) == player_1.down_key.get('key')):
                            move_down = True
                        if (event.type == pg.JOYAXISMOTION and event.axis == player_1.down_key.get('axis')
                                and int(round(event.value, 0)) == 0):
                            move_down = False
                    elif player_1.down_key.get('joy'):
                        if event.type == pg.JOYBUTTONDOWN and event.button == player_1.down_key.get('key'):
                            move_down = True
                        if event.type == pg.JOYBUTTONUP and event.button == player_1.down_key.get('key'):
                            move_down = False
                    elif player_1.down_key.get('key'):
                        if event.type == pg.KEYDOWN and event.key == player_1.down_key.get('key'):
                            move_down = True
                        if event.type == pg.KEYUP and event.key == player_1.down_key.get('key'):
                            move_down = False

            collide = pg.sprite.spritecollideany(ball, players)
            if collide:
                self.game.sfx_assets.hit_sound.play()
                collide.update(collide=True)
            if ball.rect.right >= WIDTH:
                player_1.score += 1
                self.reset_positions(ball, player_1, player_2)
                self.game.sfx_assets.goal_sound.play()
            if ball.rect.left <= 0:
                player_2.score += 1
                self.reset_positions(ball, player_1, player_2)
                self.game.sfx_assets.goal_sound.play()
            self.game.screen.fill(BLACK)

            if move_up:
                player_1.move_up()
            elif move_down:
                player_1.move_down()

            players.update(bot=True)
            all_sprites.update(move=True)
            all_sprites.draw(self.game.screen)
            self.draw_field(player_1.score, player_2.score)
            pg.display.flip()
        pg.quit()
        quit()

    @staticmethod
    def reset_positions(ball, player1, player2):
        ball.reset_position()
        player1.reset_position()
        player2.reset_position()

    def draw_field(self, player1_score, player2_score):
        for i in range(0, HEIGHT, 10):
            pg.draw.line(self.game.screen, WHITE, [WIDTH / 2, i], [WIDTH / 2, i + 6], 1)
        score_text = self.game.font_assets.sub_font.render(f'{player1_score}     {player2_score}', False, WHITE)
        score = score_text.get_rect()
        score.center = (WIDTH / 2, 40)
        self.game.screen.blit(score_text, score)
