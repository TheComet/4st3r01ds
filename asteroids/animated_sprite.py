import pygame
from updateable import Updateable


class AnimatedSprite(Updateable):

    def __init__(self, image_resource, split_hor=1, split_vert=1):
        self.__frame = list()
        self.__current_frame = 0
        self.__frame_length = 0.2
        self.__accumulated_time = 0

        self.position = (0, 0)
        self.rotation = 0

        self.__extract_frames(image_resource, split_hor, split_vert)

    def __extract_frames(self, image_resource, split_hor, split_vert):
        image = pygame.image.load(image_resource)
        frame_width = image.get_width() / split_hor
        frame_height = image.get_height() / split_vert
        for y in range(split_vert):
            for x in range(split_hor):
                x1 = frame_width * x
                y1 = frame_height * y
                x2 = x1 + frame_width
                y2 = y1 + frame_height
                surface = pygame.Surface((frame_width, frame_height))
                surface.blit(image, (0, 0), area=(x1, y1, x2, y2))
                surface.convert()
                self.__frame.append(surface)

    def set_frame_length(self, seconds):
        self.__frame_length = seconds

    def update(self, time_step):
        # check to see if it's time to go to the next frame
        self.__accumulated_time += time_step
        if self.__accumulated_time < self.__frame_length:
            return
        self.__accumulated_time -= self.__frame_length

        # go to next frame
        self.__current_frame += 1
        if self.__current_frame >= len(self.__frame):
            self.__current_frame = 0

    def draw(self, surface):
        surface.blit(self.__frame[self.__current_frame], self.position)
