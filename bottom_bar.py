import pygame

import config as c
from game_object import GameObject


class BottomBar(GameObject):
    def __init__(self):
        super().__init__()
        # create bottom bar for buttons
        self.bottom_bar_surface = pygame.Surface((c.bottom_bar_width, c.bottom_bar_height), pygame.SRCALPHA)
        self.bottom_bar_surface.fill(c.colors.BLACKOPACITY75)

    def draw(self, surface, base_offset):
        # draw bottom bar for buttons
        surface.blit(self.bottom_bar_surface, (0, c.screen_resolution[1] - c.bottom_bar_height))
