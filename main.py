import pygame

from pong.main_loop import main_loop

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    main_loop()
