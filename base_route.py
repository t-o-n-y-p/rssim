import configparser
import pygame
import config as c
import logging
import os

from game_object import GameObject


class BaseRoute(GameObject):
    def __init__(self, track_number, route_type):
        super().__init__()
        self.config = None
        self.logger = logging.getLogger('base_route {} {}'.format(route_type, track_number))
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.fh)
        self.route_type = route_type
        self.track_number = track_number
        # import config based on track number and route type
        self.route_config = {}
        self.read_state()
        if self.route_config['image_path'] is not None:
            self.image = pygame.image.load(self.route_config['image_path']).convert_alpha()
        else:
            self.image = None

    def read_state(self):
        self.config = configparser.RawConfigParser()
        if os.path.exists('user_cfg/base_route/track{}/track{}_{}.ini'.format(self.track_number,
                                                                              self.track_number,
                                                                              self.route_type)):
            self.config.read('user_cfg/base_route/track{}/track{}_{}.ini'.format(self.track_number,
                                                                                 self.track_number,
                                                                                 self.route_type))
        else:
            self.config.read('default_cfg/base_route/track{}/track{}_{}.ini'.format(self.track_number,
                                                                                    self.track_number,
                                                                                    self.route_type))
        # parse user-related config
        self.route_config['locked'] = self.config['user_data'].getboolean('locked')
        self.route_config['busy'] = self.config['user_data'].getboolean('busy')
        self.route_config['opened'] = self.config['user_data'].getboolean('opened')
        self.route_config['under_construction'] = self.config['user_data'].getboolean('under_construction')
        self.route_config['construction_time'] = self.config['user_data'].getint('construction_time')
        self.route_config['last_opened_by'] = self.config['user_data'].getint('last_opened_by')
        self.route_config['last_entered_by'] = self.config['user_data'].getint('last_entered_by')
        # parse stable config
        if self.config['route_config']['image_path'] == 'None':
            self.route_config['image_path'] = None
        else:
            self.route_config['image_path'] = self.config['route_config']['image_path']

        supported_carts_parsed = self.config['route_config']['supported_carts'].split(',')
        self.route_config['supported_carts'] = (int(supported_carts_parsed[0]), int(supported_carts_parsed[1]))
        trail_points_parsed = self.config['route_config']['trail_points'].split('|')
        for i in range(len(trail_points_parsed)):
            trail_points_parsed[i] = trail_points_parsed[i].split(',')
            trail_points_parsed[i] = (int(trail_points_parsed[i][0]), int(trail_points_parsed[i][1]))

        self.route_config['trail_points'] = tuple(trail_points_parsed)
        if self.config['route_config']['stop_point'] == 'None':
            self.route_config['stop_point'] = None
        else:
            stop_point_parsed = self.config['route_config']['stop_point'].split('|')
            for i in range(len(stop_point_parsed)):
                stop_point_parsed[i] = stop_point_parsed[i].split(',')
                stop_point_parsed[i] = (int(stop_point_parsed[i][0]), int(stop_point_parsed[i][1]))

            self.route_config['stop_point'] = tuple(stop_point_parsed)

        if self.config['route_config']['start_point'] == 'None':
            self.route_config['start_point'] = None
        else:
            start_point_parsed = self.config['route_config']['start_point'].split(',')
            self.route_config['start_point'] = (int(start_point_parsed[0]), int(start_point_parsed[1]))

        self.route_config['exit_signal'] = None
        if self.config['route_config']['exit_signal_placement'] == 'None':
            self.route_config['exit_signal_placement'] = None
        else:
            exit_signal_placement_parsed = self.config['route_config']['exit_signal_placement'].split(',')
            self.route_config['exit_signal_placement'] = (int(exit_signal_placement_parsed[0]),
                                                          int(exit_signal_placement_parsed[1]))

        self.route_config['flip_needed'] = self.config['route_config'].getboolean('flip_needed')
        self.route_config['invisible_signal'] = self.config['route_config'].getboolean('invisible_signal')

    def save_state(self):
        if not os.path.exists('user_cfg'):
            os.mkdir('user_cfg')

        if not os.path.exists('user_cfg/base_route'):
            os.mkdir('user_cfg/base_route')

        if not os.path.exists('user_cfg/base_route/track{}'.format(self.track_number)):
            os.mkdir('user_cfg/base_route/track{}'.format(self.track_number))

        self.config['user_data']['locked'] = str(self.route_config['locked'])
        self.config['user_data']['busy'] = str(self.route_config['busy'])
        self.config['user_data']['opened'] = str(self.route_config['opened'])
        self.config['user_data']['under_construction'] = str(self.route_config['under_construction'])
        self.config['user_data']['construction_time'] = str(self.route_config['construction_time'])
        self.config['user_data']['last_opened_by'] = str(self.route_config['last_opened_by'])
        self.config['user_data']['last_entered_by'] = str(self.route_config['last_entered_by'])

        with open('user_cfg/base_route/track{}/track{}_{}.ini'.format(
                self.track_number, self.track_number, self.route_type), 'w') as configfile:
            self.config.write(configfile)

    def draw(self, surface, base_offset):
        if not self.route_config['locked'] and self.image is not None:
            width = self.image.get_width()
            height = self.image.get_height()
            # left entry routes are left-aligned
            if self.route_type == c.LEFT_ENTRY_BASE_ROUTE:
                surface.blit(self.image, tuple((base_offset[0],
                                                base_offset[1] + (c.map_resolution[1] - height) // 2)))
            # right entry routes are right-aligned
            elif self.route_type == c.RIGHT_ENTRY_BASE_ROUTE:
                surface.blit(self.image, tuple((base_offset[0] + c.map_resolution[0] - width,
                                                base_offset[1] + (c.map_resolution[1] - height) // 2)))
            # platform routes are centralized
            elif self.route_type == c.LEFT_ENTRY_PLATFORM_BASE_ROUTE:
                surface.blit(self.image, tuple((base_offset[0] + (c.map_resolution[0] - width) // 2,
                                                base_offset[1] + (c.map_resolution[1] - height) // 2)))

    def update(self, game_paused):
        if not game_paused:
            # unlock routes (not available at the moment)
            if self.route_config['under_construction']:
                self.route_config['construction_time'] -= 1
                if self.route_config['construction_time'] <= 0:
                    self.route_config['locked'] = False
                    self.route_config['under_construction'] = False
