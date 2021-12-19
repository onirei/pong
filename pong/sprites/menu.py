import pygame
from typing import Tuple, List, Callable, Optional

from pong.colors import WHITE, GRAY, RED, BLACK


class MenuItem(pygame.sprite.Sprite):
    def __init__(
            self,
            name: str = 'blank',
            position: int = 1,
            align: str = None,
            cords: Tuple[int, int] = (0, 0),
            action: Callable = None,
            state: Optional[str] = None,
            max_width: Optional[int] = 0
    ):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.state = state
        self.max_width = max_width

        font_size = 32
        leading = 16
        cord_x, cord_y = cords
        self.font = pygame.font.Font('assets/fonts/bit5x5.ttf', font_size)
        self.menu_text = self.font.render(name, False, GRAY)
        rect = self.menu_text.get_rect()
        self.image = pygame.Surface((rect.width, rect.height))
        self.rect = self.image.get_rect()

        if align == 'left':
            self.rect.topleft = (cord_x, cord_y + (font_size * position + leading * (position - 1)))
        elif align == 'right':
            self.rect.topright = (cord_x, cord_y + (font_size * position + leading * (position - 1)))
        else:
            self.rect.midtop = (cord_x, cord_y + (font_size * position + leading * (position - 1)))
        self.image.blit(self.menu_text, (0, 0))
        self.action = action

    def __str__(self):
        return f'menu item {self.name}'

    def update(self, *args, **kwargs):
        if kwargs.get('color'):
            self.rerender(color=kwargs.get('color'))
        if kwargs.get('action'):
            if self.action:
                self.action()

    def rerender(self, color):
        self.menu_text = self.font.render(self.name, False, color)
        if self.state:
            menu_state = self.font.render(self.state, False, color)
            rect = menu_state.get_rect()
            self.image = pygame.transform.scale(self.image, (self.max_width + rect.w + 50, self.rect.h))
            self.image.fill(BLACK)
            self.image.blit(menu_state, (self.max_width + 50, 0))
        self.image.blit(self.menu_text, (0, 0))


class MenuCursor(pygame.sprite.Sprite):
    def __init__(self, menu_elements: Tuple[MenuItem, ...], action=None):
        pygame.sprite.Sprite.__init__(self)
        max_element_width = max(element.rect.width for element in menu_elements)
        self.image = pygame.Surface((max_element_width, 1), pygame.SRCALPHA)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        first_element = menu_elements[0]
        # first_element.rerender(WHITE)
        self.image.fill(RED)
        self.rect.center = (first_element.rect.centerx, first_element.rect.y)
        self.menu_elements = menu_elements
        self.position = 1
        self.action = action

    def update(self, *args, **kwargs):
        pass

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
