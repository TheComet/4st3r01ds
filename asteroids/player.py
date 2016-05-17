import os
import pygame
from animated_sprite import AnimatedSprite


class Player(AnimatedSprite):

    LEFT = 1
    RIGHT = 2
    SHOOT = 4
    GAS = 8

    def __init__(self, position):
        super(Player, self).__init__(os.path.join("res", "images", "player.png"), 2, 1)
        self.position = list(position)
        self.__input = 0

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.__input |= self.LEFT
            if event.key == pygame.K_w:
                self.__input |= self.RIGHT
            if event.key == pygame.K_e:
                self.__input |= self.SHOOT
            if event.key == pygame.K_r:
                self.__input |= self.GAS

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                self.__input &= ~self.LEFT
            if event.key == pygame.K_w:
                self.__input &= ~self.RIGHT
            if event.key == pygame.K_e:
                self.__input &= ~self.SHOOT
            if event.key == pygame.K_r:
                self.__input &= ~self.GAS

    def update(self, time_step):
        super(Player, self).update(time_step)
