import importlib
import pygame
import config as c
from game_object import GameObject


class BaseRoute(GameObject):
    def __init__(self, track_number, route_type):
        super().__init__()
        # import config based on track number and route type
        self.route_config = importlib.import_module('track{}_{}_config'.format(track_number, route_type))
        self.route_type = route_type
        self.track_number = track_number
        # last_opened_by and last_entered_by are used by signals to determine if next route is opened by the same train
        self.last_opened_by = None
        self.last_entered_by = None
        self.image = pygame.image.load(self.route_config.image_path).convert_alpha()

    def draw(self, surface, base_offset):
        if not self.route_config.locked:
            width = self.image.get_width()
            height = self.image.get_height()
            # entry routes are left-aligned
            if self.route_type == c.base_route_flags[0]:
                surface.blit(self.image, tuple((base_offset[0],
                                                base_offset[1] + (c.map_resolution[1] - height) // 2)))
            # exit routes are right-aligned
            elif self.route_type == c.base_route_flags[2]:
                surface.blit(self.image, tuple((base_offset[0] + c.map_resolution[0] - width,
                                                base_offset[1] + (c.map_resolution[1] - height) // 2)))
            # platform routes are centralized
            elif self.route_type == c.base_route_flags[4]:
                surface.blit(self.image, tuple((base_offset[0] + (c.map_resolution[0] - width) // 2,
                                                base_offset[1] + (c.map_resolution[1] - height) // 2)))

    def update(self, game_paused):
        if not game_paused:
            # unlock routes (not available at the moment)
            self.route_config.update_config(self.route_config)
