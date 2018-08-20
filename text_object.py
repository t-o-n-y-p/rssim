import logging
import pygame


class TextObject:
    def __init__(self, position, text, color, font_name, font_size):
        self.logger = logging.getLogger('game.{}_text_object'.format(text))
        self.logger.debug('------- START INIT -------')
        self.pos = position
        self.text = text
        self.color = color
        self.logger.debug('position, text and color set: {} {} {}'.format(self.pos, self.text, self.color))
        self.font = pygame.font.SysFont(font_name, font_size)
        self.logger.debug('font set: {} {}'.format(font_name, font_size))
        self.text_surface = self.font.render(self.text, False, self.color)
        self.logger.debug('text render complete')
        self.logger.debug('------- END INIT -------')
        self.logger.warning('text object init completed')

    def draw(self, surface):
        self.logger.debug('------- START DRAWING -------')
        surface.blit(self.text_surface, (self.pos[0] - self.text_surface.get_width() // 2,
                                         self.pos[1] - self.text_surface.get_height() // 2))
        self.logger.debug('------- END DRAWING -------')
        self.logger.info('text is in place')

    def update(self, new_text):
        self.logger.debug('------- TEXT OBJECT UPDATE START -------')
        self.text = new_text
        self.logger.debug('new text: {}'.format(new_text))
        self.logger = logging.getLogger('game.{}_text_object'.format(new_text))
        self.logger.debug('new logger created')
        self.text_surface = self.font.render(self.text, False, self.color)
        self.logger.debug('new text render complete')
        self.logger.debug('------- TEXT OBJECT UPDATE END -------')
        self.logger.info('text object updated')
