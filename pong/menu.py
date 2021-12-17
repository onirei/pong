import pygame
from typing import Tuple

from pong.colors import WHITE, GRAY
from pong.const import WIDTH, HEIGHT


class MenuItem(pygame.sprite.Sprite):
    def __init__(self, position=1, name='empty'):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.font = pygame.font.SysFont('Comic Sans MS', 42)
        self.menu_text = self.font.render(name, False, GRAY)
        rect = self.menu_text.get_rect()
        self.image = pygame.Surface((rect.width, rect.height))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2 + HEIGHT / 10 * position)
        self.image.blit(self.menu_text, (0, 0))

    def __str__(self):
        return f'menu item {self.name}'

    def update(self):
        # self.rerender(WHITE)
        pass

    def rerender(self, color):
        self.menu_text = self.font.render(self.name, False, color)
        self.image.blit(self.menu_text, (0, 0))


class MenuCursor(pygame.sprite.Sprite):
    def __init__(self, menu_elements: Tuple[MenuItem, ...], action=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()
        first_element = menu_elements[0]
        first_element.rerender(WHITE)
        self.rect.center = (first_element.rect.centerx, first_element.rect.y)
        self.menu_elements = menu_elements
        self.position = 1
        self.action = action

    def update(self, *args, **kwargs):
        pass
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_UP]:
        #     if self.position == 1:
        #         self.position = len(self.menu_elements)
        #     else:
        #         self.position -= 1
        #     self.rect.y = self.menu_elements[self.position-1].rect.centery
        # if keys[pygame.K_DOWN]:
        #     if self.position == len(self.menu_elements):
        #         self.position = 1
        #     else:
        #         self.position += 1
        #     self.rect.y = self.menu_elements[self.position-1].rect.centery

    def navigate(self, event):
        if event.key == pygame.K_UP:
            if self.position == 1:
                self.position = len(self.menu_elements)
            else:
                self.position -= 1
            self.rect.y = self.menu_elements[self.position-1].rect.centery
        if event.key == pygame.K_DOWN:
            if self.position == len(self.menu_elements):
                self.position = 1
            else:
                self.position += 1
            self.rect.y = self.menu_elements[self.position-1].rect.centery

