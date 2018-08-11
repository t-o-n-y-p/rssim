import pygame

from game_object import GameObject
from text_object import TextObject
import config as c


class Button(GameObject):
    def __init__(self, position, text1, text2, on_click_1=lambda x: None, on_click_2=lambda y: None):
        super().__init__()
        self.state = 'normal'
        self.on_click_1 = on_click_1
        self.on_click_2 = on_click_2
        self.on_click_actual = on_click_1
        self.image = {'normal': pygame.image.load('img/button_normal.png').convert_alpha(),
                      'hover': pygame.image.load('img/button_hover.png').convert_alpha(),
                      'pressed': pygame.image.load('img/button_pressed.png').convert_alpha()}

        self.position = position
        self.text_object_1 = TextObject((self.position[0] + 27, self.position[1] + 8), text1,
                                        c.button_text_color, c.font_size)
        self.text_object_2 = TextObject((self.position[0] + 27, self.position[1] + 8), text2,
                                        c.button_text_color, c.font_size)
        self.text_object_actual = self.text_object_1

    def draw(self, surface, base_offset):
        surface.blit(self.image[self.state], self.position)
        self.text_object_actual.draw(surface)

    def handle_mouse_event(self, event_type, pos):
        if event_type == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
        elif event_type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
        elif event_type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)

    def handle_mouse_move(self, pos):
        if pos[0] in range(self.position[0], self.position[0] + 100) and \
                pos[1] in range(self.position[1], self.position[1] + 40):
            if self.state != 'pressed':
                self.state = 'hover'
        else:
            self.state = 'normal'

    def handle_mouse_down(self, pos):
        if pos[0] in range(self.position[0], self.position[0] + 100) and \
                pos[1] in range(self.position[1], self.position[1] + 40):
            self.state = 'pressed'

    def handle_mouse_up(self, pos):
        if self.state == 'pressed':
            self.on_click_actual(self)
            self.state = 'hover'
            if self.on_click_actual == self.on_click_1:
                self.on_click_actual = self.on_click_2
            else:
                self.on_click_actual = self.on_click_1

            if self.text_object_actual == self.text_object_1:
                self.text_object_actual = self.text_object_2
            else:
                self.text_object_actual = self.text_object_1
