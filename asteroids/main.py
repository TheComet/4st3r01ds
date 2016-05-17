__author__ = 'thecomet'

import sys
import pygame
from window import Window

if __name__ == '__main__':
    pygame.init()
    window = Window(1024, 768)
    window.enter_main_loop()
    pygame.quit()
    sys.exit(0)
