import configparser
from game_object import GameObject
import pygame
import config as c
import os


class Signal(GameObject):
    def __init__(self, placement, flip_needed, invisible, track_number, route_type):
        super().__init__()
        self.track_number = track_number
        self.route_type = route_type
        self.config = None
        self.invisible = invisible
        # where to place signal on map
        self.placement = placement
        # for left-directed routes we need to flip signal (its default image is for right-directed routes)
        self.flip_needed = flip_needed
        # initialize signal state
        self.state = None
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

    def read_state(self):
        self.config = configparser.RawConfigParser()
        if os.path.exists('user_cfg/signals/track{}/track{}_{}.ini'.format(self.track_number,
                                                                           self.track_number,
                                                                           self.route_type)):
            self.config.read('user_cfg/signals/track{}/track{}_{}.ini'.format(self.track_number,
                                                                              self.track_number,
                                                                              self.route_type))
        else:
            self.config.read('default_cfg/signals/track{}/track{}_{}.ini'.format(self.track_number,
                                                                                 self.track_number,
                                                                                 self.route_type))

        self.state = self.config['user_data']['state']

    def save_state(self):
        if not os.path.exists('user_cfg'):
            os.mkdir('user_cfg')

        if not os.path.exists('user_cfg/signals'):
            os.mkdir('user_cfg/signals')

        if not os.path.exists('user_cfg/signals/track{}'.format(self.track_number)):
            os.mkdir('user_cfg/signals/track{}'.format(self.track_number))

        self.config['user_data']['state'] = self.state

        with open('user_cfg/signals/track{}/track{}_{}.ini'.format(
                self.track_number, self.track_number, self.route_type), 'w') as configfile:
            self.config.write(configfile)

    def update(self, game_paused):
        if not game_paused:
            approaching_track = None
            busy_logical = False
            busy_extended_logical = False
            opened_by = []

            if not self.base_route_exit.route_config['opened']:
                self.state = c.RED_SIGNAL
            else:
                for i in self.base_route_opened_list:
                    if i.route_config['opened']:
                        opened_by.append(i.route_config['last_opened_by'])

                if self.base_route_exit.route_config['last_opened_by'] not in opened_by:
                    self.state = c.RED_SIGNAL
                else:
                    for i in self.base_route_busy_list:
                        if not (i.route_config['opened'] and i.route_config['last_opened_by'] ==
                                self.base_route_exit.route_config['last_opened_by']):
                            busy_logical = busy_logical or i.route_config['busy']

                    for j in self.base_route_busy_additional_list:
                        busy_logical = busy_logical or j.route_config['busy']

                    if busy_logical:
                        self.state = c.RED_SIGNAL
                    else:
                        if len(self.base_route_busy_extended_list) > 0:
                            for i in self.base_route_opened_list:
                                if i.route_config['opened'] and i.route_config['last_opened_by'] == \
                                        self.base_route_exit.route_config['last_opened_by']:
                                    approaching_track = i.track_number

                            for j in self.base_route_busy_extended_list:
                                if j.track_number % 2 == approaching_track % 2:
                                    busy_extended_logical = busy_extended_logical or j.route_config['busy']

                            if busy_extended_logical:
                                self.state = c.RED_SIGNAL
                            else:
                                self.state = c.GREEN_SIGNAL
                                for i in self.base_route_opened_list:
                                    if i.route_config['opened'] and i.route_config['last_opened_by'] == \
                                            self.base_route_exit.route_config['last_opened_by']:
                                        i.route_config['busy'] = True
                                        i.route_config['last_entered_by'] = \
                                            self.base_route_exit.route_config['last_opened_by']
                        else:
                            self.state = c.GREEN_SIGNAL
                            for i in self.base_route_opened_list:
                                if i.route_config['opened'] and i.route_config['last_opened_by'] == \
                                        self.base_route_exit.route_config['last_opened_by']:
                                    i.route_config['busy'] = True
                                    i.route_config['last_entered_by'] = \
                                        self.base_route_exit.route_config['last_opened_by']
