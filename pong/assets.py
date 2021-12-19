import pygame


class Assets:
    def __init__(self):
        # font
        self.font = pygame.font.Font('assets/fonts/bit5x5.ttf', 128)
        self.sub_font = pygame.font.Font('assets/fonts/bit5x3.ttf', 56)
        # sound
        pygame.mixer.init()
        self.hit_sound = pygame.mixer.Sound('assets/sounds/ping_pong_8bit_beeep.ogg')
        self.goal_sound = pygame.mixer.Sound('assets/sounds/ping_pong_8bit_peeeeeep.ogg')
        self.rebound_sound = pygame.mixer.Sound('assets/sounds/ping_pong_8bit_plop.ogg')
