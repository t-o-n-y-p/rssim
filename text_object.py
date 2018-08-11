import pygame
import config as c


class TextObject:
    def __init__(self, position, text, color, font_size):
        self.pos = position
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont(c.font_name, font_size)
        self.text_surface = self.font.render(self.text, False, self.color)

    def draw(self, surface):
        surface.blit(self.text_surface, self.pos)

