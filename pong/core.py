import json
# import random
# import tracemalloc
from typing import Dict, NoReturn

import pygame

from pong.assets import Assets
from pong.colors import BLACK, GRAY, GREEN, RED, WHITE
from pong.const import FPS, HEIGHT, WIDTH
from pong.scenes.scene_manager import SceneManager


class GameCore:
    def __init__(self):
        # tracemalloc.start()
        pygame.init()
        pygame.display.set_caption("pong")
        self.clock = pygame.time.Clock()
        self.assets = Assets()
        # screen
        self.width = WIDTH
        self.height = HEIGHT
        conf = self.read_config()
        self.screen_mode = pygame.FULLSCREEN if conf.get('fullscreen') else 0
        self.screen = pygame.display.set_mode(size=(self.width, self.height), flags=self.screen_mode)

        self.scene = SceneManager(self)
        self.scene.load(scene_name='main_menu')

    @staticmethod
    def read_config() -> Dict:
        # возможно лучше вставить проверку на извлечение и ресет настроек
        with open('pong/config.json', 'r') as json_conf:
            conf = json.load(json_conf)
            return conf

    @staticmethod
    def write_config(conf: Dict) -> NoReturn:
        with open('pong/config.json', 'w') as json_conf:
            json.dump(conf, json_conf)

    def _debug(self, *args, **kwargs):
        font = pygame.font.SysFont('arial', 24)
        info_text = font.render(str(args), False, GREEN)
        info_rect = info_text.get_rect()
        info_rect.topleft = (0, 0)
        self.screen.blit(info_text, info_rect)
        for i in range(0, WIDTH, 10):
            pygame.draw.line(self.screen, WHITE, [i, 0], [i, HEIGHT], 1 if i % 50 else 3)
        for i in range(0, HEIGHT, 10):
            pygame.draw.line(self.screen, WHITE, [0, i], [WIDTH, i], 1 if i % 50 else 3)
