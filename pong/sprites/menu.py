from typing import Callable, Optional, Tuple, Union

import pygame as pg

from pong.colors import BLACK, GRAY
from pong.sprites.exceptions import NoKeyAssignException


class MenuActionGroup(object):
    def __init__(
            self,
            event_key: Optional[Union[int, Tuple[int, ...]]] = None,
            event_joy_key: Optional[Union[int, Tuple[int, ...]]] = None,
            action: Optional[Callable] = None,
    ):
        self.actions = dict(key=dict(), joy=dict())
        self.add(event_key=event_key, event_joy_key=event_joy_key, action=action)

    def __call__(self, event_key: int = None, event_joy_key: int = None, sfx=None, *args, **kwargs):
        action = None
        if event_key is not None:
            action = self.actions.get('key').get(event_key)
        elif event_joy_key is not None:
            action = self.actions.get('joy').get(event_joy_key)
        if callable(action):
            if sfx:
                sfx.play()
            action()

    def add(
            self,
            action: Optional[Callable],
            event_key: Union[int, Tuple[int, ...]] = None,
            event_joy_key: Union[int, Tuple[int, ...]] = None,
    ):
        if not event_key and not event_joy_key and action:
            raise NoKeyAssignException

        if type(event_key) is int:
            self.actions.get('key').update({event_key: action})
        elif type(event_key) is tuple:
            for key in event_key:
                self.actions.get('key').update({key: action})

        if type(event_joy_key) is int:
            self.actions.get('joy').update({event_joy_key: action})
        elif type(event_joy_key) is tuple:
            for key in event_joy_key:
                self.actions.get('joy').update({key: action})


class MenuItem(pg.sprite.Sprite):
    def __init__(
            self,
            name: str = 'blank',
            position: int = 1,
            align: str = None,
            cords: Tuple[int, int] = (0, 0),
            action: MenuActionGroup = None,
            state: Optional[str] = None,
            max_width: Optional[int] = 0,
    ):
        pg.sprite.Sprite.__init__(self)
        self.name = name
        self.state = state
        self.max_width = max_width

        font_size = 32
        line_spacing = 16
        cord_x, cord_y = cords
        self.font = pg.font.Font('assets/fonts/bit5x5.ttf', font_size)
        self.menu_text = self.font.render(name, False, GRAY)
        rect = self.menu_text.get_rect()
        self.image = pg.Surface((rect.width, rect.height), pg.SRCALPHA)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()

        if align == 'left':
            self.rect.topleft = (cord_x, cord_y + (font_size * position + line_spacing * (position - 1)))
        elif align == 'right':
            self.rect.topright = (cord_x, cord_y + (font_size * position + line_spacing * (position - 1)))
        else:
            self.rect.midtop = (cord_x, cord_y + (font_size * position + line_spacing * (position - 1)))
        self.image.blit(self.menu_text, (0, 0))
        self.action = action

    def __str__(self):
        return f'menu item {self.name}'

    def update(self, *args, **kwargs):
        if kwargs.get('color'):
            self.rerender(color=kwargs.get('color'))
        if kwargs.get('action') and kwargs.get('event_key') is not None or kwargs.get('event_joy_key') is not None:
            sfx = kwargs.get('sfx')
            if self.action:
                self.action(event_key=kwargs.get('event_key'), event_joy_key=kwargs.get('event_joy_key'), sfx=sfx)

    def rerender(self, color):
        self.menu_text = self.font.render(self.name, False, color)
        if self.state:
            menu_state = self.font.render(self.state, False, color)
            rect = menu_state.get_rect()
            self.image = pg.transform.scale(self.image, (self.max_width + rect.w + 50, self.rect.h))
            self.image.fill(BLACK)
            self.image.blit(menu_state, (self.max_width + 50, 0))
        self.image.blit(self.menu_text, (0, 0))


class MenuCursor(pg.sprite.Sprite):
    def __init__(self, menu_elements: Tuple[MenuItem, ...], action=None):
        pg.sprite.Sprite.__init__(self)
        max_element_width = max(element.rect.width for element in menu_elements)
        self.image = pg.Surface((max_element_width, 1), pg.SRCALPHA)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        first_element = menu_elements[0]
        # self.image.fill(RED)
        self.rect.center = (first_element.rect.centerx, first_element.rect.y)
        self.menu_elements = menu_elements
        self.position = 1
        self.action = action

    def update(self, *args, **kwargs):
        pass

    def navigate_up(self):
        if self.position == 1:
            self.position = len(self.menu_elements)
        else:
            self.position -= 1
        self.rect.y = self.menu_elements[self.position - 1].rect.centery

    def navigate_down(self):
        if self.position == len(self.menu_elements):
            self.position = 1
        else:
            self.position += 1
        self.rect.y = self.menu_elements[self.position - 1].rect.centery
