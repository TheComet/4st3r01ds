__author__ = 'thecomet'


class Updateable(object):

    def __init__(self, window):
        self.window = window

    def process_event(self, event):
        pass

    def update(self, time_step):
        pass

    def draw(self, surface):
        pass
