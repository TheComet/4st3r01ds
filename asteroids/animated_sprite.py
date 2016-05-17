import pygame
from updateable import Updateable


class AnimatedSprite(Updateable):

    def __init__(self, window, image_resource, split_hor=1, split_vert=1):
        super(AnimatedSprite, self).__init__(window)
        self.__frame = list()
        self.__current_frame = 0
        self.__frame_length = 0.2
        self.__accumulated_time = 0
        self.__is_playing = False

        self.position = (0, 0)
        self.angle = 0
        self.dimensions = (0, 0)

        self.__extract_frames(image_resource, split_hor, split_vert)

    def __extract_frames(self, image_resource, split_hor, split_vert):
        image = pygame.image.load(image_resource)
        self.dimensions = (image.get_width() / split_hor, image.get_height() / split_vert)
        for y in range(split_vert):
            for x in range(split_hor):
                x1 = self.dimensions[0] * x
                y1 = self.dimensions[1] * y
                x2 = x1 + self.dimensions[0]
                y2 = y1 + self.dimensions[1]
                surface = pygame.Surface((self.dimensions[0], self.dimensions[1]))
                surface.blit(image, (0, 0), area=(x1, y1, x2, y2))
                surface.convert()
                self.__frame.append(surface)

    def set_frame_length(self, seconds):
        self.__frame_length = seconds

    def play(self):
        self.__is_playing = True

    def stop(self):
        self.__is_playing = False

    def reset(self):
        self.__current_frame = 0

    def update(self, time_step):
        if not self.__is_playing:
            return

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
        frame_surface = self.__frame[self.__current_frame]
        rotated_frame = pygame.transform.rotate(frame_surface, self.angle)
        center = rotated_frame.get_rect().center
        surface.blit(rotated_frame, (self.position[0]-center[0], self.position[1]-center[1]))
