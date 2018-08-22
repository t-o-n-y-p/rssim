import logging

import pygame

from game_object import GameObject
from text_object import TextObject


class Button(GameObject):
    def __init__(self, position, button_size, text, on_click, draw_only_if_game_paused):
        super().__init__()
        self.logger = logging.getLogger('game.{} button'.format(text[0]))
        self.logger.debug('------- START INIT -------')
        self.draw_only_if_game_paused = draw_only_if_game_paused
        self.logger.debug('draw only if game paused set: {}'.format(self.draw_only_if_game_paused))
        self.allowed_to_be_drawn = False
        self.logger.debug('allowed_to_be_drawn set: {}'.format(self.allowed_to_be_drawn))
        self.state = 'normal'
        self.logger.debug('state set: {}'.format(self.state))
        self.position = position
        self.button_size = button_size
        self.logger.debug('position set: {}'.format(self.position))
        self.text_objects = []
        self.on_click = on_click
        self.on_click_actual = self.on_click[0]
        self.logger.debug('on click action set: {}'.format(self.on_click_actual))
        self.image = {'normal': pygame.Surface(button_size, pygame.SRCALPHA),
                      'hover': pygame.Surface(button_size, pygame.SRCALPHA),
                      'pressed': pygame.Surface(button_size, pygame.SRCALPHA)}
        self.image['normal'].fill((0, 0, 0))
        self.image['hover'].fill((127, 0, 0))
        self.image['pressed'].fill((192, 0, 0))
        for i in self.image:
            pygame.draw.line(self.image[i], (255, 255, 255), (0, 0), (button_size[0] - 2, 0), 2)
            pygame.draw.line(self.image[i], (255, 255, 255), (0, 0), (0, button_size[1] - 2), 2)
            pygame.draw.line(self.image[i], (255, 255, 255),
                             (0, button_size[1] - 2), (button_size[0] - 2, button_size[1] - 2), 2)
            pygame.draw.line(self.image[i], (255, 255, 255),
                             (button_size[0] - 2, 0), (button_size[0] - 2, button_size[1] - 2), 2)

        self.logger.debug('images set: {}'.format(self.image))
        self.text = text
        for i in range(len(on_click)):
            self.text_objects.append(TextObject((self.position[0] + button_size[0] // 2,
                                                 self.position[1] + button_size[1] // 2), text[i],
                                                self.c['graphics']['button_text_color'],
                                                self.c['graphics']['font_name'],
                                                self.c['graphics']['button_font_size']))
        self.logger.debug('text objects set: {}'.format(self.text))
        self.text_object_actual = self.text_objects[0]
        self.logger.debug('current text set: {}'.format(self.text[0]))
        self.logger.debug('------- END INIT -------')
        self.logger.warning('button init completed')

    def draw(self, surface, base_offset):
        self.logger.debug('------- START DRAWING -------')
        if self.allowed_to_be_drawn:
            surface.blit(self.image[self.state], self.position)
            self.text_object_actual.draw(surface)

        self.logger.debug('------- END DRAWING -------')
        self.logger.info('button is in place')

    def update(self, game_paused):
        self.logger.debug('------- START UPDATING -------')
        if not game_paused and self.draw_only_if_game_paused:
            self.allowed_to_be_drawn = False
            self.logger.debug('game is not paused and this button is drawn only if game paused')
            self.logger.debug('so hide the button')
        else:
            self.allowed_to_be_drawn = True
            self.logger.info('button is always present on the screen')
            self.logger.info('so it is not hidden')

        self.logger.debug('------- END UPDATING -------')
        self.logger.info('button updated')

    def handle_mouse_event(self, event_type, pos):
        self.logger.debug('------- START HANDLING MOUSE EVENTS -------')
        if event_type == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
        elif event_type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
        elif event_type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)

        self.logger.debug('------- END HANDLING MOUSE EVENTS -------')
        self.logger.info('mouse events handled')

    def handle_mouse_move(self, pos):
        if pos[0] in range(self.position[0] + 2, self.position[0] + self.button_size[0] - 2) \
                and pos[1] in range(self.position[1] + 2, self.position[1] + self.button_size[1] - 2):
            if self.state != 'pressed':
                self.state = 'hover'
                self.logger.info('cursor is on the button')
        else:
            self.state = 'normal'
            self.logger.debug('cursor is not on the button')

    def handle_mouse_down(self, pos):
        if pos[0] in range(self.position[0] + 2, self.position[0] + self.button_size[0] - 2) \
                and pos[1] in range(self.position[1] + 2, self.position[1] + self.button_size[1] - 2):
            self.state = 'pressed'
            self.logger.info('cursor is on the button and user holds mouse button')

    def handle_mouse_up(self, pos):
        if self.state == 'pressed':
            self.state = 'hover'
            self.logger.info('cursor is on the button and user released mouse button')
            self.logger.info('start onclick action')
            self.on_click_actual(self)
            if self.on_click_actual == self.on_click[0] and len(self.on_click) == 2:
                self.on_click_actual = self.on_click[1]
                self.logger.info('button is switched to second action')
            else:
                self.on_click_actual = self.on_click[0]
                self.logger.debug('button has only 1 action, so it remains the same')

            if self.text_object_actual == self.text_objects[0] and len(self.text_objects) == 2:
                self.text_object_actual = self.text_objects[1]
                self.logger.info('button is switched to second text')
            else:
                self.text_object_actual = self.text_objects[0]
                self.logger.debug('button has only 1 text, so it remains the same')
