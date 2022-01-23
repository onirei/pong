import pygame as pg


class SoundGroup(object):
    def __init__(self, *sounds):
        self.sounds = []
        self.add(*sounds)

    def add(self, *sounds):
        for sound in sounds:
            self.sounds.append(sound)

    def set_master_volume(self, volume):
        for sound in self.sounds:
            sound.set_volume(volume)


class FontAssets:
    def __init__(self):
        self.font = pg.font.Font('assets/fonts/bit5x5.ttf', 128)
        self.sub_font = pg.font.Font('assets/fonts/bit5x3.ttf', 56)
        self.credits_font = pg.font.Font('assets/fonts/bit5x3.ttf', 24)


class SFXAssets:
    def __init__(self, volume: float):
        self.hit_sound = pg.mixer.Sound('assets/sounds/ping_pong_8bit_beeep.ogg')
        self.goal_sound = pg.mixer.Sound('assets/sounds/ping_pong_8bit_peeeeeep.ogg')
        self.rebound_sound = pg.mixer.Sound('assets/sounds/ping_pong_8bit_plop.ogg')
        self.sfx = SoundGroup(self.hit_sound, self.goal_sound, self.rebound_sound)
        self.sfx.set_master_volume(volume)
