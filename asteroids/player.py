import os
import pygame
import math
from animated_sprite import AnimatedSprite


class Player(AnimatedSprite):
    LEFT = 1
    RIGHT = 2
    SHOOT = 4
    HIT_THE_GAS_PEDAL_BRO = 8

    def __init__(self, window, position):
        super(Player, self).__init__(window, os.path.join("res", "images", "player.png"), 2, 1)
        self.position = list(position)
        self.__input = 0
        self.__acceleration = 400
        self.__stop_acceleration = 70
        self.__velocity = [0, 0]
        self.__max_velocity = 600
        self.__rotation_speed = 200

        self.set_frame_length(0.08)

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.__input |= self.RIGHT
            if event.key == pygame.K_w:
                self.__input |= self.LEFT
            if event.key == pygame.K_e:
                self.__input |= self.SHOOT
            if event.key == pygame.K_r:
                self.__input |= self.HIT_THE_GAS_PEDAL_BRO
                self.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                self.__input &= ~self.RIGHT
            if event.key == pygame.K_w:
                self.__input &= ~self.LEFT
            if event.key == pygame.K_e:
                self.__input &= ~self.SHOOT
            if event.key == pygame.K_r:
                self.__input &= ~self.HIT_THE_GAS_PEDAL_BRO
                self.stop()
                self.reset()

    def update(self, time_step):
        self.__update_rotation(time_step)
        self.__hit_the_gas_bro(time_step)
        self.__wrap_around()
        super(Player, self).update(time_step)

    def __update_rotation(self, time_step):
        if self.__input & self.LEFT:                  self.angle -= time_step * self.__rotation_speed
        if self.__input & self.RIGHT:                 self.angle += time_step * self.__rotation_speed

    def __hit_the_gas_bro(self, time_step):
        """
        Hits the gas, bro (updates player position depending on the "gas" input button).
        """
        # Is the player pressing the gas button? Integrate acceleration to get velocity.
        if self.__input & self.HIT_THE_GAS_PEDAL_BRO:
            self.__velocity[0] += -math.sin(self.angle/180*math.pi) * self.__acceleration * time_step
            self.__velocity[1] += -math.cos(self.angle/180*math.pi) * self.__acceleration * time_step

            # limit the maximum velocity
            if self.__velocity[0]**2 + self.__velocity[1]**2 > self.__max_velocity**2:
                vector_length = math.sqrt(self.__velocity[0]**2 + self.__velocity[1]**2)
                self.__velocity[0] = self.__velocity[0] / vector_length * self.__max_velocity
                self.__velocity[1] = self.__velocity[1] / vector_length * self.__max_velocity

        # The player is not pressing the gas button, slowly
        else:
            vector_length = math.sqrt(self.__velocity[0]**2 + self.__velocity[1]**2)
            if not vector_length == 0:
                normalized = [self.__velocity[0] / vector_length, self.__velocity[1] / vector_length]
                self.__velocity[0] -= normalized[0] * self.__stop_acceleration * time_step
                self.__velocity[1] -= normalized[1] * self.__stop_acceleration * time_step
        self.position[0] += self.__velocity[0] * time_step
        self.position[1] += self.__velocity[1] * time_step

    def __wrap_around(self):
        half_width  = self.dimensions[0] / 2
        half_height = self.dimensions[1] / 2
        if self.position[0] > self.window.dimensions[0] + half_width:
            self.position[0] = -self.dimensions[0] + half_width
        if self.position[0] < - self.dimensions[0] + half_width:
            self.position[0] = self.window.dimensions[0] + half_width
        if self.position[1] > self.window.dimensions[1] + half_height:
            self.position[1] = -self.dimensions[1] + half_height
        if self.position[1] < - self.dimensions[1] + half_height:
            self.position[1] = self.window.dimensions[1] + half_height
