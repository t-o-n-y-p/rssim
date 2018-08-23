import time
import sys
import logging
from collections import defaultdict
import configparser
import os
import io

import pygame


class Game:
    def __init__(self, caption):
        self.logs_config = configparser.RawConfigParser()
        self.logger = logging.getLogger('game')
        self.logs_stream = io.StringIO()
        self.logs_file = None
        self.manage_logs_config()
        self.logger.debug('main logger created')
        self.c = {}
        self.game_config = configparser.RawConfigParser()
        self.game_config.read('game_config.ini')
        self.parse_game_config()
        # since map can be moved, all objects should also be moved, that's why we need base offset here
        self.base_offset = self.c['graphics']['base_offset']
        self.logger.debug('base offset set: {} {}'.format(self.base_offset[0], self.base_offset[1]))
        self.frame_rate = self.c['graphics']['frame_rate']
        self.logger.debug('frame rate set: {}'.format(self.frame_rate))
        self.game_paused = False
        self.logger.debug('game paused set: {}'.format(self.game_paused))
        self.objects = []
        pygame.init()
        self.logger.debug('pygame module core initialized')
        pygame.font.init()
        self.logger.debug('pygame fonts module initialized')
        self.surface = pygame.display.set_mode(self.c['graphics']['screen_resolution'],
                                               pygame.SRCALPHA | pygame.NOFRAME)
        self.logger.debug('created screen with resolution {}'
                          .format(self.c['graphics']['screen_resolution']))
        pygame.display.set_caption(caption)
        pygame.display.set_icon(pygame.image.load('icon.ico').convert_alpha())
        self.logger.debug('caption set: {}'.format(caption))
        self.clock = pygame.time.Clock()
        self.logger.debug('clock created')
        self.key_down_handlers = defaultdict(list)
        self.key_up_handlers = defaultdict(list)
        self.mouse_movement = ()
        self.mouse_handlers = []
        self.logger.warning('game init completed')

    def manage_logs_config(self):
        self.logs_config.read('logs_config.ini')
        if not os.path.exists('logs'):
            os.mkdir('logs')

        self.logger.setLevel(self.logs_config['logs_config']['level'])
        session = self.logs_config['logs_config'].getint('session')
        # logs_handler = logging.FileHandler('logs/session_{}.log'.format(session))
        logs_handler = logging.StreamHandler(stream=self.logs_stream)
        logs_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(logs_handler)
        self.logs_file = open('logs/session_{}.log'.format(session), 'w')
        session += 1
        self.logs_config['logs_config']['session'] = str(session)

        with open('logs_config.ini', 'w') as configfile:
            self.logs_config.write(configfile)

    def parse_game_config(self):
        self.c['graphics'] = {}
        screen_resolution = self.game_config['graphics']['screen_resolution'].split(',')
        self.c['graphics']['screen_resolution'] = (int(screen_resolution[0]), int(screen_resolution[1]))
        self.c['graphics']['frame_rate'] = self.game_config['graphics'].getint('frame_rate')
        self.c['graphics']['background_image'] = self.game_config['graphics']['background_image']
        background_tile_resolution = self.game_config['graphics']['background_tile_resolution'].split(',')
        self.c['graphics']['background_tile_resolution'] = (int(background_tile_resolution[0]),
                                                            int(background_tile_resolution[1]))
        number_of_background_tiles = self.game_config['graphics']['number_of_background_tiles'].split(',')
        self.c['graphics']['number_of_background_tiles'] = (int(number_of_background_tiles[0]),
                                                            int(number_of_background_tiles[1]))
        map_resolution = self.game_config['graphics']['map_resolution'].split(',')
        self.c['graphics']['map_resolution'] = (int(map_resolution[0]), int(map_resolution[1]))
        base_offset_upper_left_limit = self.game_config['graphics']['base_offset_upper_left_limit'].split(',')
        self.c['graphics']['base_offset_upper_left_limit'] = (int(base_offset_upper_left_limit[0]),
                                                              int(base_offset_upper_left_limit[1]))
        base_offset_lower_right_limit = self.game_config['graphics']['base_offset_lower_right_limit'].split(',')
        self.c['graphics']['base_offset_lower_right_limit'] = (int(base_offset_lower_right_limit[0]),
                                                               int(base_offset_lower_right_limit[1]))
        base_offset = self.game_config['graphics']['base_offset'].split(',')
        self.c['graphics']['base_offset'] = (int(base_offset[0]), int(base_offset[1]))
        self.c['graphics']['top_bar_height'] = self.game_config['graphics'].getint('top_bar_height')
        self.c['graphics']['bottom_bar_height'] = self.game_config['graphics'].getint('bottom_bar_height')
        self.c['graphics']['bottom_bar_width'] = self.game_config['graphics'].getint('bottom_bar_width')
        self.c['graphics']['font_name'] = self.game_config['graphics']['font_name']
        self.c['graphics']['button_font_size'] = self.game_config['graphics'].getint('button_font_size')
        self.c['graphics']['day_font_size'] = self.game_config['graphics'].getint('day_font_size')
        button_text_color = self.game_config['graphics']['button_text_color'].split(',')
        for i in range(len(button_text_color)):
            button_text_color[i] = int(button_text_color[i])

        self.c['graphics']['button_text_color'] = tuple(button_text_color)
        bottom_bar_color = self.game_config['graphics']['bottom_bar_color'].split(',')
        for i in range(len(bottom_bar_color)):
            bottom_bar_color[i] = int(bottom_bar_color[i])

        self.c['graphics']['bottom_bar_color'] = tuple(bottom_bar_color)
        day_text_color = self.game_config['graphics']['day_text_color'].split(',')
        for i in range(len(day_text_color)):
            day_text_color[i] = int(day_text_color[i])

        self.c['graphics']['day_text_color'] = tuple(day_text_color)

        self.c['base_route_types'] = {}
        self.c['base_route_types']['left_entry_base_route'] \
            = self.game_config['base_route_types']['left_entry_base_route']
        self.c['base_route_types']['left_exit_base_route'] \
            = self.game_config['base_route_types']['left_exit_base_route']
        self.c['base_route_types']['right_entry_base_route'] \
            = self.game_config['base_route_types']['right_entry_base_route']
        self.c['base_route_types']['right_exit_base_route'] \
            = self.game_config['base_route_types']['right_exit_base_route']
        self.c['base_route_types']['left_entry_platform_base_route'] \
            = self.game_config['base_route_types']['left_entry_platform_base_route']
        self.c['base_route_types']['right_entry_platform_base_route'] \
            = self.game_config['base_route_types']['right_entry_platform_base_route']
        self.c['base_route_types']['right_exit_platform_base_route'] \
            = self.game_config['base_route_types']['right_exit_platform_base_route']
        self.c['base_route_types']['left_exit_platform_base_route'] \
            = self.game_config['base_route_types']['left_exit_platform_base_route']

        self.c['direction'] = {}
        self.c['direction']['left'] = self.game_config['direction'].getint('left')
        self.c['direction']['right'] = self.game_config['direction'].getint('right')

        self.c['train_route_types'] = {}
        self.c['train_route_types']['entry_train_route'] \
            = self.game_config['train_route_types']['entry_train_route'].split(',')
        self.c['train_route_types']['exit_train_route'] \
            = self.game_config['train_route_types']['exit_train_route'].split(',')
        self.c['train_route_types']['approaching_train_route'] \
            = self.game_config['train_route_types']['approaching_train_route'].split(',')

        self.c['signal_config'] = {}
        self.c['signal_config']['red_signal'] = self.game_config['signal_config']['red_signal']
        self.c['signal_config']['green_signal'] = self.game_config['signal_config']['green_signal']
        self.c['signal_config']['signal_image_base_path'] = self.game_config['signal_config']['signal_image_base_path']

        self.c['signal_image_path'] = {}
        self.c['signal_image_path'][self.c['signal_config']['red_signal']] \
            = self.game_config['signal_image_path']['red_signal']
        self.c['signal_image_path'][self.c['signal_config']['green_signal']] \
            = self.game_config['signal_image_path']['green_signal']

        self.c['train_config'] = {}
        self.c['train_config']['train_cart_image_path'] = self.game_config['train_config']['train_cart_image_path']
        train_acceleration_factor = self.game_config['train_config']['train_acceleration_factor'].split(',')
        for i in range(len(train_acceleration_factor)):
            train_acceleration_factor[i] = int(train_acceleration_factor[i])

        self.c['train_config']['train_acceleration_factor'] = tuple(train_acceleration_factor)
        self.c['train_config']['train_acceleration_factor_length'] \
            = self.game_config['train_config'].getint('train_acceleration_factor_length')
        self.c['train_config']['train_maximum_speed'] = self.game_config['train_config'].getint('train_maximum_speed')
        self.c['train_config']['train_braking_distance'] \
            = self.game_config['train_config'].getint('train_braking_distance')

        self.c['train_state_types'] = {}
        self.c['train_state_types']['pass_through'] = self.game_config['train_state_types']['pass_through']
        self.c['train_state_types']['approaching'] = self.game_config['train_state_types']['approaching']
        self.c['train_state_types']['approaching_pass_through'] \
            = self.game_config['train_state_types']['approaching_pass_through']
        self.c['train_state_types']['pending_boarding'] = self.game_config['train_state_types']['pending_boarding']
        self.c['train_state_types']['boarding_in_progress'] \
            = self.game_config['train_state_types']['boarding_in_progress']
        self.c['train_state_types']['boarding_complete'] = self.game_config['train_state_types']['boarding_complete']

        self.c['train_speed_state_types'] = {}
        self.c['train_speed_state_types']['move'] = self.game_config['train_speed_state_types']['move']
        self.c['train_speed_state_types']['accelerate'] = self.game_config['train_speed_state_types']['accelerate']
        self.c['train_speed_state_types']['decelerate'] = self.game_config['train_speed_state_types']['decelerate']
        self.c['train_speed_state_types']['stop'] = self.game_config['train_speed_state_types']['stop']

        self.c['dispatcher_config'] = {}
        self.c['dispatcher_config']['tracks_ready'] = self.game_config['dispatcher_config'].getint('tracks_ready')
        first_priority_tracks = self.game_config['dispatcher_config']['first_priority_tracks'].split('|')
        for i in range(len(first_priority_tracks)):
            first_priority_tracks[i] = first_priority_tracks[i].split(',')
            for j in range(len(first_priority_tracks[i])):
                first_priority_tracks[i][j] = int(first_priority_tracks[i][j])

            first_priority_tracks[i] = tuple(first_priority_tracks[i])

        self.c['dispatcher_config']['first_priority_tracks'] = tuple(first_priority_tracks)
        second_priority_tracks = self.game_config['dispatcher_config']['second_priority_tracks'].split('|')
        for i in range(len(second_priority_tracks)):
            second_priority_tracks[i] = second_priority_tracks[i].split(',')
            for j in range(len(second_priority_tracks[i])):
                second_priority_tracks[i][j] = int(second_priority_tracks[i][j])

            second_priority_tracks[i] = tuple(second_priority_tracks[i])

        self.c['dispatcher_config']['second_priority_tracks'] = tuple(second_priority_tracks)
        pass_through_priority_tracks = self.game_config['dispatcher_config']['pass_through_priority_tracks'].split('|')
        for i in range(len(pass_through_priority_tracks)):
            pass_through_priority_tracks[i] = pass_through_priority_tracks[i].split(',')
            for j in range(len(pass_through_priority_tracks[i])):
                pass_through_priority_tracks[i][j] = int(pass_through_priority_tracks[i][j])

            pass_through_priority_tracks[i] = tuple(pass_through_priority_tracks[i])

        self.c['dispatcher_config']['pass_through_priority_tracks'] = tuple(pass_through_priority_tracks)
        train_creation_timeout = self.game_config['dispatcher_config']['train_creation_timeout'].split(',')
        self.c['dispatcher_config']['train_creation_timeout'] = (int(train_creation_timeout[0]),
                                                                 int(train_creation_timeout[1]))

        self.c['switch_types'] = {}
        self.c['switch_types']['left_entry_railroad_switch'] \
            = self.game_config['switch_types']['left_entry_railroad_switch']
        self.c['switch_types']['left_exit_railroad_switch'] \
            = self.game_config['switch_types']['left_exit_railroad_switch']
        self.c['switch_types']['right_entry_railroad_switch'] \
            = self.game_config['switch_types']['right_entry_railroad_switch']
        self.c['switch_types']['right_exit_railroad_switch'] \
            = self.game_config['switch_types']['right_exit_railroad_switch']

        self.c['crossover_types'] = {}
        self.c['crossover_types']['left_entry_crossover'] = self.game_config['crossover_types']['left_entry_crossover']
        self.c['crossover_types']['left_exit_crossover'] = self.game_config['crossover_types']['left_exit_crossover']
        self.c['crossover_types']['right_entry_crossover'] \
            = self.game_config['crossover_types']['right_entry_crossover']
        self.c['crossover_types']['right_exit_crossover'] = self.game_config['crossover_types']['right_exit_crossover']

    def update(self):
        for o in self.objects:
            # some objects should be updated even after game is paused
            o.update(self.game_paused)

    def draw(self):
        for o in self.objects:
            o.draw(self.surface, self.base_offset)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                for handler in self.key_down_handlers[event.key]:
                    handler(event.key)
            elif event.type == pygame.KEYUP:
                for handler in self.key_up_handlers[event.key]:
                    handler(event.key)
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                for handler in self.mouse_handlers:
                    handler(event.type, event.pos)

    def run(self):
        while True:
            self.logger.warning('frame begins')
            time_1 = time.perf_counter()
            self.handle_events()
            time_2 = time.perf_counter()
            self.update()
            time_3 = time.perf_counter()
            self.draw()
            time_4 = time.perf_counter()
            pygame.display.update(pygame.Rect(0, 0, self.c['graphics']['screen_resolution'][0],
                                              self.c['graphics']['screen_resolution'][1]))
            self.logger.warning('frame ends')
            self.logger.critical('handling events: {} sec'.format(time_2 - time_1))
            self.logger.critical('updating: {} sec'.format(time_3 - time_2))
            self.logger.critical('drawing: {} sec'.format(time_4 - time_3))
            new_lines = self.logs_stream.getvalue()
            self.logs_stream.seek(0, 0)
            self.logs_stream.truncate(0)
            if new_lines is not None:
                self.logs_file.write(new_lines)

            self.clock.tick(self.frame_rate)
            if self.clock.get_fps() > 0:
                self.logger.critical('FPS: {}'.format(round(self.clock.get_fps())))
