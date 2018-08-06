import pygame

from game_object import GameObject
import config as c


class Signal(GameObject):
    def __init__(self, placement, flip_needed):
        super().__init__()
        self.placement = placement
        self.flip_needed = flip_needed
        self.state = c.signal_flags[0]
        self.image = {c.signal_flags[0]: pygame.image.load(c.signal_image_path[0]).convert_alpha(),
                      c.signal_flags[1]: pygame.image.load(c.signal_image_path[1]).convert_alpha()}
        if self.flip_needed:
            self.image = {c.signal_flags[0]: pygame.transform.flip(self.image[c.signal_flags[0]], True, False),
                          c.signal_flags[1]: pygame.transform.flip(self.image[c.signal_flags[1]], True, False)}

        self.base_route_busy_list = []
        self.base_route_opened_list = []
        self.base_route_exit_list = []

    def draw(self, surface, base_offset):
        signal_position = (base_offset[0] + self.placement[0], base_offset[1] + self.placement[1])
        surface.blit(self.image[self.state], signal_position)

    def update(self, game_paused):
        if not game_paused:
            busy_logical = False
            opened_logical = False
            opened_by = []
            is_busy_by = None
            exit_logical = False
            for i in self.base_route_opened_list:
                opened_logical = opened_logical or i.route_config.opened
                if i.route_config.opened:
                    opened_by.append(i.last_opened_by)

            if not opened_logical:
                self.state = c.signal_flags[0]
            else:
                for i in self.base_route_busy_list:
                    if i not in self.base_route_opened_list:
                        busy_logical = busy_logical or i.route_config.busy

                if busy_logical:
                    self.state = c.signal_flags[0]
                else:
                    for i in self.base_route_exit_list:
                        exit_logical = exit_logical or i.route_config.busy
                        if i.route_config.busy:
                            is_busy_by = i.last_entered_by

                    if exit_logical and is_busy_by in opened_by:
                        self.state = c.signal_flags[1]
                    else:
                        self.state = c.signal_flags[0]
