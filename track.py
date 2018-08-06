import pygame
from pygame.rect import Rect

from game_object import GameObject
from text_object import TextObject
import config as c


class Track(GameObject):
    def __init__(self):
        super().__init__()
        self.base_routes = []
        self.busy = False
        self.last_entered_by = None
        self.override = False

    def update(self):
        if not self.override:
            busy_1 = False
            for i in self.base_routes:
                busy_1 = busy_1 or i.route_config.busy
                if i.route_config.busy:
                    self.last_entered_by = i.last_entered_by

            self.busy = busy_1

