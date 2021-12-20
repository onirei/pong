import random

import pygame

from pong.colors import BLACK, WHITE
from pong.const import FPS
from pong.scenes.base import AbstractGameScene
from pong.sprites import Ball, Racket


class Pong(AbstractGameScene):
    def scene(self, *args, **kwargs):
        player1 = Racket(playable=True, left_side=True)

        if kwargs.get('vs_cpu'):
            player2 = Racket()
        else:
            player2 = Racket(playable=True)
        ball = Ball()
        all_sprites = pygame.sprite.Group(player1, player2, ball)
        players = pygame.sprite.Group(player1, player2)
        vectors = {
            15: {'speed': 7.5, 'angle': 1.5},
            35: {'speed': 5, 'angle': 1},
            # 50: {'speed': 3.5, 'angle': 0},
            55: {'speed': 5, 'angle': 1},
            75: {'speed': 7.5, 'angle': 1.5}
        }
        keys = [pygame.K_UP, pygame.K_DOWN]
        if pygame.joystick.get_count():
            gamepad = pygame.joystick.Joystick(0)
            gamepad.init()

        self.running = True
        while self.running:
            self.game.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_SPACE):
                        self.game.assets.rebound_sound.play()
                        self.game.scene.load(scene_name='pause_menu')
            collide = pygame.sprite.spritecollideany(ball, players)
            if collide:
                self.game.assets.hit_sound.play()
                clip = collide.rect.clip(ball.rect)
                collide_point = collide.rect.y + collide.rect.height - clip.y
                ball.dx = ball.dx * -1
                sign = -1 if ball.dy < 0 else 1
                for vector in vectors:
                    speed_mod = 0
                    if list(key for key in keys if pygame.key.get_pressed()[key]):
                        speed_mod = 2
                    if collide_point <= vector:
                        ball.dy = vectors.get(vector).get('angle') * sign
                        ball.speed = vectors.get(vector).get('speed') + speed_mod
                        break
                if ball.rect.x > self.game.width / 2:
                    ball.rect.x = player2.rect.x - ball.rect.width
                else:
                    ball.rect.x = player1.rect.x + player1.rect.width + ball.rect.width
            if ball.rect.right >= self.game.width:
                player1.score += 1
                self.reset_positions(ball, player1, player2)
                self.game.assets.goal_sound.play()
            if ball.rect.left <= 0:
                player2.score += 1
                self.reset_positions(ball, player1, player2)
                self.game.assets.goal_sound.play()
            player1.bot_1(ball.rect.center, ball.direction())
            player2.bot_1(ball.rect.center, ball.direction())
            self.game.screen.fill(BLACK)
            all_sprites.update()
            all_sprites.draw(self.game.screen)
            self.draw_field(player1.score, player2.score)
            pygame.display.flip()

        pygame.quit()
        quit()

    def reset_positions(self, ball, player1, player2):
        ball.rect.center = (self.game.width / 2, self.game.height / 2)
        ball.dy = random.uniform(-1.5, 1.5)
        ball.speed = 5
        player1.reset_position()
        player2.reset_position()

    def draw_field(self, player1_score, player2_score):
        for i in range(0, self.game.height, 10):
            pygame.draw.line(self.game.screen, WHITE, [self.game.width / 2, i], [self.game.width / 2, i + 6], 1)
        font = pygame.font.SysFont('Comic Sans MS', 56)
        score_text = font.render(f'{player1_score}     {player2_score}', False, WHITE)
        score = score_text.get_rect()
        score.center = (self.game.width / 2, 40)
        self.game.screen.blit(score_text, score)
