import pygame

from game_object import GameObject
import config as c


class Signal(GameObject):
    def __init__(self, placement, flip_needed, invisible):
        super().__init__()
        self.invisible = invisible
        # where to place signal on map
        self.placement = placement
        # for left-directed routes we need to flip signal (its default image is for right-directed routes)
        self.flip_needed = flip_needed
        # by default all signals are red, just like IRL :)
        self.state = c.RED_SIGNAL
        self.base_image = pygame.image.load(c.signal_image_base_path).convert_alpha()
        self.image = {c.RED_SIGNAL: pygame.image.load(c.signal_image_path[c.RED_SIGNAL]).convert_alpha(),
                      c.GREEN_SIGNAL: pygame.image.load(c.signal_image_path[c.GREEN_SIGNAL]).convert_alpha()}
        if self.flip_needed:
            self.base_image = pygame.transform.flip(self.base_image, True, False)

        self.base_route_busy_list = []
        self.base_route_busy_additional_list = []
        self.base_route_busy_extended_list = []
        self.base_route_opened_list = []
        self.base_route_exit = None

    def draw(self, surface, base_offset):
        if not self.invisible:
            signal_position = (base_offset[0] + self.placement[0], base_offset[1] + self.placement[1])
            # reserved for future transition between states,
            # for now there are only 2 states: pure red and pure green
            surface.blit(self.image[self.state], signal_position)
            surface.blit(self.base_image, signal_position)

    def update(self, game_paused):
        if not game_paused:
            approaching_track = None
            busy_logical = False
            busy_extended_logical = False
            opened_by = []

            if not self.base_route_exit.route_config.opened:
                self.state = c.RED_SIGNAL
            else:
                for i in self.base_route_opened_list:
                    if i.route_config.opened:
                        opened_by.append(i.last_opened_by)

                if self.base_route_exit.last_opened_by not in opened_by:
                    self.state = c.RED_SIGNAL
                else:
                    for i in self.base_route_busy_list:
                        if not (i.route_config.opened and i.last_opened_by == self.base_route_exit.last_opened_by):
                            busy_logical = busy_logical or i.route_config.busy

                    for j in self.base_route_busy_additional_list:
                        busy_logical = busy_logical or j.route_config.busy

                    if busy_logical:
                        self.state = c.RED_SIGNAL
                    else:
                        if len(self.base_route_busy_extended_list) > 0:
                            for i in self.base_route_opened_list:
                                if i.route_config.opened and i.last_opened_by == self.base_route_exit.last_opened_by:
                                    approaching_track = i.track_number

                            for j in self.base_route_busy_extended_list:
                                if j.track_number % 2 == approaching_track % 2:
                                    busy_extended_logical = busy_extended_logical or j.route_config.busy

                            if busy_extended_logical:
                                self.state = c.RED_SIGNAL
                            else:
                                self.state = c.GREEN_SIGNAL
                                for i in self.base_route_opened_list:
                                    if i.route_config.opened and \
                                            i.last_opened_by == self.base_route_exit.last_opened_by:
                                        i.route_config.busy = True
                                        i.last_entered_by = self.base_route_exit.last_opened_by
                        else:
                            self.state = c.GREEN_SIGNAL
                            for i in self.base_route_opened_list:
                                if i.route_config.opened and i.last_opened_by == self.base_route_exit.last_opened_by:
                                    i.route_config.busy = True
                                    i.last_entered_by = self.base_route_exit.last_opened_by
