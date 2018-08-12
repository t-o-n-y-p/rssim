import pygame

from game_object import GameObject
from text_object import TextObject
import config as c


class Button(GameObject):
    def __init__(self, position, text, on_click, draw_only_if_game_paused):
        super().__init__()
        self.draw_only_if_game_paused = draw_only_if_game_paused
        self.allowed_to_be_drawn = False
        self.state = 'normal'
        self.text_objects = []
        self.on_click = on_click
        self.on_click_actual = self.on_click[0]
        self.image = {'normal': pygame.image.load('img/button_normal.png').convert_alpha(),
                      'hover': pygame.image.load('img/button_hover.png').convert_alpha(),
                      'pressed': pygame.image.load('img/button_pressed.png').convert_alpha()}

        self.position = position
        self.text = text
        for i in range(len(on_click)):
            self.text_objects.append(TextObject((self.position[0] + 50, self.position[1] + 20), text[i],
                                                c.button_text_color, c.font_size))

        self.text_object_actual = self.text_objects[0]

    def draw(self, surface, base_offset):
        if self.allowed_to_be_drawn:
            surface.blit(self.image[self.state], self.position)
            self.text_object_actual.draw(surface)

    def update(self, game_paused):
        if not game_paused and self.draw_only_if_game_paused:
            self.allowed_to_be_drawn = False
        else:
            self.allowed_to_be_drawn = True

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
            if self.on_click_actual == self.on_click[0] and len(self.on_click) == 2:
                self.on_click_actual = self.on_click[1]
            else:
                self.on_click_actual = self.on_click[0]

            if self.text_object_actual == self.text_objects[0] and len(self.text_objects) == 2:
                self.text_object_actual = self.text_objects[1]
            else:
                self.text_object_actual = self.text_objects[0]
