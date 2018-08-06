import pygame

import config as c
from game_object import GameObject


class BgImg(GameObject):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.bottom_bar_surface = pygame.Surface((c.screen_resolution[0], c.bottom_bar_height), pygame.SRCALPHA)
        self.bottom_bar_surface.fill(c.colors.BLACKOPACITY875)

    def draw(self, surface, base_offset):
        for i in range(c.number_of_background_tiles[0]):
            for j in range(c.number_of_background_tiles[1]):
                surface.blit(self.image, (base_offset[0] + i*c.background_tile_resolution[0],
                                          base_offset[1] + j*c.background_tile_resolution[1]))
        surface.blit(self.bottom_bar_surface, (0, c.screen_resolution[1] - c.bottom_bar_height))
