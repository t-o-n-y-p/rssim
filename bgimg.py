import pygame

import config as c
from game_object import GameObject


class BgImg(GameObject):
    def __init__(self, image):
        super().__init__()
        # load background texture tile
        self.image = pygame.image.load(image).convert_alpha()
        # create bottom bar for buttons
        self.bottom_bar_surface = pygame.Surface((c.screen_resolution[0], c.bottom_bar_height), pygame.SRCALPHA)
        self.bottom_bar_surface.fill(c.colors.BLACKOPACITY875)

    def draw(self, surface, base_offset):
        # fill map with background texture tile
        for i in range(c.number_of_background_tiles[0]):
            for j in range(c.number_of_background_tiles[1]):
                surface.blit(self.image, (base_offset[0] + i*c.background_tile_resolution[0],
                                          base_offset[1] + j*c.background_tile_resolution[1]))
        # draw bottom bar for buttons
        surface.blit(self.bottom_bar_surface, (0, c.screen_resolution[1] - c.bottom_bar_height))
