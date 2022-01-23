from typing import TYPE_CHECKING, NoReturn

import pygame as pg

from pong.scenes.pause_menu.pause_menu import GamePause
from pong.scenes.game.pong import Pong
from pong.scenes.main_menu.credits import MenuCredits
from pong.scenes.main_menu.keys import MenuKeys
from pong.scenes.main_menu.main_menu import MainMenu
from pong.scenes.main_menu.options import MenuOptions

if TYPE_CHECKING:
    from pong.core import GameCore


class SceneManager:
    def __init__(self, game: 'GameCore'):
        self.scene_list = {
            'main_menu': MainMenu(game=game).scene,
            'menu_options': MenuOptions(game=game).scene,
            'menu_credits': MenuCredits(game=game).scene,
            'pong': Pong(game=game).scene,
            'pause_menu': GamePause(game=game).scene,
            'menu_keys': MenuKeys(game=game).scene,
        }

    def load(self, scene_name: str, *args, **kwargs) -> NoReturn:
        pg.key.set_repeat(200)
        scene = self.scene_list.get(scene_name)
        scene(*args, **kwargs) if callable(scene) else None
