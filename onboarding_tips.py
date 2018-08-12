import pygame

import config as c
from game_object import GameObject


class OnboardingTips(GameObject):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.condition_met = False

    def draw(self, surface, base_offset):
        if self.condition_met:
            surface.blit(self.image, (c.screen_resolution[0] // 2 - self.image.get_width() // 2,
                                      c.screen_resolution[1] // 2 - self.image.get_height() // 2))

    def update(self, game_paused):
        if not game_paused:
            self.condition_met = False
