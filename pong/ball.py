import pygame
import random

from pong.colors import WHITE
from pong.const import WIDTH, HEIGHT
from pong.sound import rebound_sound


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((7, 7))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.dx = 1
        self.dy = random.uniform(0.5, 1.5)
        self.speed = 5

    def __str__(self):
        return 'ball'

    def update(self):
        self.rect.x += self.speed * self.dx
        self.rect.y += self.speed * self.dy
        # if self.rect.right > WIDTH or self.rect.left <= 0:
        #     self.dx = self.dx * -1
        if self.rect.bottom > HEIGHT or self.rect.top <= 0:
            rebound_sound.play()
            self.dy = self.dy * -1

    def direction(self):
        return self.dx, self.dy, self.speed

        # Wall and Paddle Bounces
        # if self.rect.y > WIDTH:
        #     self.dy = -1
        # if self.rect.y < 1:
        #     self.dy = 1

        # if self.rect.x > 740:
        #     self.rect.x, self.rect.y = 375, 250
        #     self.dx = -1
        #     paddle1.points += 1
        #
        # if self.rect.x < 1:
        #     self.rect.x, self.rect.y = 375, 250
        #     self.dx = 1
        #     paddle2.points += 1

        # if paddle1.rect.colliderect(self.rect):
        #     self.dx = 1
        #
        # if paddle2.rect.colliderect(self.rect):
        #     self.dx = -1
