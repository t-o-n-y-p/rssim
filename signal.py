import pygame

from game_object import GameObject
import config as c


class Signal(GameObject):
    def __init__(self, placement, flip_needed):
        super().__init__()
        # where to place signal on map
        self.placement = placement
        # for left-directed routes we need to flip signal (its default image is for right-directed routes)
        self.flip_needed = flip_needed
        # by default all signals are red, just like IRL :)
        self.state = c.RED_SIGNAL
        self.image = {c.RED_SIGNAL: pygame.image.load(c.signal_image_path[c.RED_SIGNAL]).convert_alpha(),
                      c.GREEN_SIGNAL: pygame.image.load(c.signal_image_path[c.GREEN_SIGNAL]).convert_alpha()}
        if self.flip_needed:
            self.image = {c.RED_SIGNAL: pygame.transform.flip(self.image[c.RED_SIGNAL], True, False),
                          c.GREEN_SIGNAL: pygame.transform.flip(self.image[c.GREEN_SIGNAL], True, False)}

        self.base_route_busy_list = []
        self.base_route_opened_list = []
        self.base_route_exit = None

    def draw(self, surface, base_offset):
        signal_position = (base_offset[0] + self.placement[0], base_offset[1] + self.placement[1])
        # reserved for future transition between states,
        # for now there are only 2 states: pure red and pure green
        if self.state in (c.RED_SIGNAL, c.GREEN_SIGNAL):
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

            # if no single route is opened, signal should be red indeed;
            # if something is opened, we check busy route list
            if not opened_logical:
                self.state = c.RED_SIGNAL
            else:
                for i in self.base_route_busy_list:
                    if i not in self.base_route_opened_list or \
                            (i in self.base_route_opened_list and
                             i.last_opened_by != self.base_route_exit.last_opened_by):
                        busy_logical = busy_logical or i.route_config.busy

                # if some route behind the signal is busy not by train
                # which is located before the signal, it should be red indeed;
                # if not, let's check if train before the signal has passed it
                if busy_logical:
                    self.state = c.RED_SIGNAL
                else:
                    exit_logical = exit_logical or self.base_route_exit.route_config.busy
                    if self.base_route_exit.route_config.busy:
                        is_busy_by = self.base_route_exit.last_entered_by

                    # if train has passed signal, turn it red
                    if exit_logical and is_busy_by in opened_by:
                        self.state = c.GREEN_SIGNAL
                    else:
                        self.state = c.RED_SIGNAL
