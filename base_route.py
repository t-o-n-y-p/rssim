import configparser
import logging
import os

import pygame

from game_object import GameObject
from railroad_switch import RailroadSwitch
from crossover import Crossover


class BaseRoute(GameObject):
    def __init__(self, track_number, route_type):
        super().__init__()
        self.logger = logging.getLogger('game.base_route_{}_{}'.format(track_number, route_type))
        self.logger.debug('------- START INIT -------')
        self.config = configparser.RawConfigParser()
        self.logger.debug('config parser created')
        self.route_type = route_type
        self.logger.debug('route type set: {}'.format(self.route_type))
        self.track_number = track_number
        self.logger.debug('track number set: {}'.format(self.track_number))
        # import config based on track number and route type
        self.route_config = {}
        self.junctions = []
        self.checkpoints = []
        self.junction_position = []
        self.read_state()
        if self.route_config['image_path'] is not None:
            self.image = pygame.image.load(self.route_config['image_path']).convert_alpha()
        else:
            self.image = None

        self.logger.debug('image is not None: {}'.format(self.image is None))
        self.logger.debug('------- END INIT -------')
        self.logger.warning('base route init completed')

    def read_state(self):
        self.logger.debug('------- START READING STATE -------')
        if os.path.exists('user_cfg/base_route/track{}/track{}_{}.ini'.format(self.track_number,
                                                                              self.track_number,
                                                                              self.route_type)):
            self.config.read('user_cfg/base_route/track{}/track{}_{}.ini'.format(self.track_number,
                                                                                 self.track_number,
                                                                                 self.route_type))
            self.logger.debug('config parsed from user_cfg')
        else:
            self.config.read('default_cfg/base_route/track{}/track{}_{}.ini'.format(self.track_number,
                                                                                    self.track_number,
                                                                                    self.route_type))
            self.logger.debug('config parsed from default_cfg')
        # parse user-related config
        self.route_config['locked'] = self.config['user_data'].getboolean('locked')
        self.logger.debug('locked: {}'.format(self.route_config['locked']))
        self.route_config['force_busy'] = self.config['user_data'].getboolean('force_busy')
        self.logger.debug('force_busy: {}'.format(self.route_config['force_busy']))
        self.route_config['busy'] = self.config['user_data'].getboolean('busy')
        self.logger.debug('busy: {}'.format(self.route_config['busy']))
        self.route_config['opened'] = self.config['user_data'].getboolean('opened')
        self.logger.debug('opened: {}'.format(self.route_config['opened']))
        self.route_config['under_construction'] = self.config['user_data'].getboolean('under_construction')
        self.logger.debug('under_construction: {}'.format(self.route_config['under_construction']))
        self.route_config['construction_time'] = self.config['user_data'].getint('construction_time')
        self.logger.debug('construction_time: {}'.format(self.route_config['construction_time']))
        self.route_config['last_opened_by'] = self.config['user_data'].getint('last_opened_by')
        self.logger.debug('last_opened_by: {}'.format(self.route_config['last_opened_by']))
        self.route_config['last_entered_by'] = self.config['user_data'].getint('last_entered_by')
        self.logger.debug('last_entered_by: {}'.format(self.route_config['last_entered_by']))
        self.logger.info('user-related config parsed')
        # parse stable config
        if self.config['route_config']['image_path'] == 'None':
            self.route_config['image_path'] = None
        else:
            self.route_config['image_path'] = self.config['route_config']['image_path']

        self.logger.debug('image_path: {}'.format(self.route_config['image_path']))
        if self.config['route_config']['image_position'] == 'None':
            self.route_config['image_position'] = None
        else:
            image_position_parsed = self.config['route_config']['image_position'].split(',')
            self.route_config['image_position'] = (int(image_position_parsed[0]), int(image_position_parsed[1]))

        supported_carts_parsed = self.config['route_config']['supported_carts'].split(',')
        self.route_config['supported_carts'] = (int(supported_carts_parsed[0]), int(supported_carts_parsed[1]))
        self.logger.debug('supported_carts: {}'.format(self.route_config['supported_carts']))
        if self.config['route_config']['stop_point'] == 'None':
            self.route_config['stop_point'] = None
        else:
            stop_point_parsed = self.config['route_config']['stop_point'].split('|')
            for i in range(len(stop_point_parsed)):
                stop_point_parsed[i] = stop_point_parsed[i].split(',')
                stop_point_parsed[i] = (int(stop_point_parsed[i][0]), int(stop_point_parsed[i][1]))

            self.route_config['stop_point'] = tuple(stop_point_parsed)

        self.logger.debug('stop_point: {}'.format(self.route_config['stop_point']))

        if self.config['route_config']['start_point'] == 'None':
            self.route_config['start_point'] = None
        else:
            start_point_parsed = self.config['route_config']['start_point'].split(',')
            self.route_config['start_point'] = (int(start_point_parsed[0]), int(start_point_parsed[1]))

        self.logger.debug('start_point: {}'.format(self.route_config['start_point']))
        self.route_config['exit_signal'] = None
        if self.config['route_config']['exit_signal_placement'] == 'None':
            self.route_config['exit_signal_placement'] = None
        else:
            exit_signal_placement_parsed = self.config['route_config']['exit_signal_placement'].split(',')
            self.route_config['exit_signal_placement'] = (int(exit_signal_placement_parsed[0]),
                                                          int(exit_signal_placement_parsed[1]))

        self.logger.debug('exit_signal_placement: {}'.format(self.route_config['exit_signal_placement']))
        self.route_config['flip_needed'] = self.config['route_config'].getboolean('flip_needed')
        self.logger.debug('flip_needed: {}'.format(self.route_config['flip_needed']))
        self.route_config['invisible_signal'] = self.config['route_config'].getboolean('invisible_signal')
        self.logger.debug('invisible_signal: {}'.format(self.route_config['invisible_signal']))
        self.logger.info('solid config parsed')
        self.logger.debug('------- END READING STATE -------')
        self.logger.info('base route state initialized')

    def read_trail_points(self):
        self.logger.debug('------- START READING TRAIL POINTS -------')
        self.route_config['trail_points'] = ()
        trail_points_parsed = []
        if self.config['route_config']['trail_points'] != 'None':
            trail_points_parsed = self.config['route_config']['trail_points'].split('|')
            for i in range(len(trail_points_parsed)):
                trail_points_parsed[i] = trail_points_parsed[i].split(',')
                trail_points_parsed[i] = (int(trail_points_parsed[i][0]), int(trail_points_parsed[i][1]))

        self.logger.debug('trail points parsed')
        self.logger.debug('junctions in this base route: {}'.format(len(self.junctions)))
        if len(self.junctions) > 0:
            for i in range(len(self.junctions)):
                if type(self.junctions[i]) == RailroadSwitch:
                    trail_points_parsed.extend(self.junctions[i].trail_points[self.junction_position[i]])
                elif type(self.junctions[i]) == Crossover:
                    trail_points_parsed.extend(self.junctions[i].trail_points[self.junction_position[i][0]]
                                               [self.junction_position[i][1]])

                self.logger.debug('added junction {} trail points'.format(i + 1))

        self.route_config['trail_points'] = tuple(trail_points_parsed)
        self.logger.debug('------- END READING TRAIL POINTS -------')
        self.logger.info('base route trail points fully initialized')

    def save_state(self):
        self.logger.debug('------- START SAVING STATE -------')
        if not os.path.exists('user_cfg'):
            os.mkdir('user_cfg')
            self.logger.debug('created user_cfg folder')

        if not os.path.exists('user_cfg/base_route'):
            os.mkdir('user_cfg/base_route')
            self.logger.debug('created user_cfg/base_route folder')

        if not os.path.exists('user_cfg/base_route/track{}'.format(self.track_number)):
            os.mkdir('user_cfg/base_route/track{}'.format(self.track_number))
            self.logger.debug('created user_cfg/base_route/track{} folder'.format(self.track_number))

        self.config['user_data']['locked'] = str(self.route_config['locked'])
        self.logger.debug('locked value to save: {}'.format(self.config['user_data']['locked']))
        self.config['user_data']['force_busy'] = str(self.route_config['force_busy'])
        self.logger.debug('force_busy value to save: {}'.format(self.config['user_data']['force_busy']))
        self.config['user_data']['busy'] = str(self.route_config['busy'])
        self.logger.debug('busy value to save: {}'.format(self.config['user_data']['busy']))
        self.config['user_data']['opened'] = str(self.route_config['opened'])
        self.logger.debug('opened value to save: {}'.format(self.config['user_data']['opened']))
        self.config['user_data']['under_construction'] = str(self.route_config['under_construction'])
        self.logger.debug('under_construction value to save: {}'.format(self.config['user_data']['under_construction']))
        self.config['user_data']['construction_time'] = str(self.route_config['construction_time'])
        self.logger.debug('construction_time value to save: {}'.format(self.config['user_data']['construction_time']))
        self.config['user_data']['last_opened_by'] = str(self.route_config['last_opened_by'])
        self.logger.debug('last_opened_by value to save: {}'.format(self.config['user_data']['last_opened_by']))
        self.config['user_data']['last_entered_by'] = str(self.route_config['last_entered_by'])
        self.logger.debug('last_entered_by value to save: {}'.format(self.config['user_data']['last_entered_by']))
        self.logger.info('config ready to be saved to ini file')

        with open('user_cfg/base_route/track{}/track{}_{}.ini'.format(
                self.track_number, self.track_number, self.route_type), 'w') as configfile:
            self.config.write(configfile)

        self.logger.debug('------- END SAVING STATE -------')
        self.logger.info('base route state saved to file user_cfg/base_route/track{}/track{}_{}.ini'
                         .format(self.track_number, self.track_number, self.route_type))

    def enter_base_route(self, train_id, game_paused):
        self.logger.debug('------- START ENTERING BASE ROUTE -------')
        self.checkpoints = []
        self.route_config['force_busy'] = True
        self.logger.debug('force_busy set to True')
        self.route_config['busy'] = True
        self.logger.debug('busy set to True')
        self.route_config['last_entered_by'] = train_id
        self.logger.debug('entered by train {}'.format(train_id))
        self.logger.debug('junctions in this base route: {}'.format(len(self.junctions)))
        if len(self.junctions) > 0:
            for i in range(len(self.junctions)):
                if type(self.junctions[i]) == RailroadSwitch:
                    self.junctions[i].force_busy = True
                    self.logger.debug('switch {} {} {} force_busy set to True'
                                      .format(self.junctions[i].straight_track, self.junctions[i].side_track,
                                              self.junctions[i].direction))
                    self.junctions[i].busy = True
                    self.logger.debug('switch {} {} {} busy set to True'
                                      .format(self.junctions[i].straight_track, self.junctions[i].side_track,
                                              self.junctions[i].direction))
                    self.junctions[i].last_entered_by = train_id
                    self.logger.debug('switch {} {} {} is busy by train {}'
                                      .format(self.junctions[i].straight_track, self.junctions[i].side_track,
                                              self.junctions[i].direction, train_id))
                    self.checkpoints.append(self.route_config['trail_points']
                                            .index(self.junctions[i].trail_points[self.junction_position[i]][-1]))
                    self.logger.debug('checkpoint added: {}'.format(self.checkpoints[-1]))
                elif type(self.junctions[i]) == Crossover:
                    self.junctions[i].force_busy[self.junction_position[i][0]][self.junction_position[i][1]] = True
                    self.logger.debug('crossover {} {} {} force_busy from track {} to track {} set to True'
                                      .format(self.junctions[i].straight_track_1, self.junctions[i].straight_track_2,
                                              self.junctions[i].direction,
                                              self.junction_position[i][0], self.junction_position[i][1]))
                    self.junctions[i].busy[self.junction_position[i][0]][self.junction_position[i][1]] = True
                    self.logger.debug('crossover {} {} {} busy from track {} to track {} set to True'
                                      .format(self.junctions[i].straight_track_1, self.junctions[i].straight_track_2,
                                              self.junctions[i].direction,
                                              self.junction_position[i][0], self.junction_position[i][1]))
                    self.junctions[i].last_entered_by[self.junction_position[i][0]][self.junction_position[i][1]] \
                        = train_id
                    self.logger.debug('crossover {} {} {} busy from track {} to track {} by train {}'
                                      .format(self.junctions[i].straight_track_1, self.junctions[i].straight_track_2,
                                              self.junctions[i].direction,
                                              self.junction_position[i][0], self.junction_position[i][1], train_id))
                    self.checkpoints \
                        .append(self.route_config['trail_points']
                                .index(self.junctions[i]
                                       .trail_points[self.junction_position[i][0]][self.junction_position[i][1]][-1]))
                    self.logger.debug('checkpoint added: {}'.format(self.checkpoints[-1]))

                self.junctions[i].update(game_paused)
                self.logger.debug('junction updated')
                self.junctions[i].dependency.update(game_paused)
                self.logger.debug('junction dependency updated')
                self.logger.info('junction {} processed'.format(i + 1))

        else:
            self.checkpoints.append(len(self.route_config['trail_points']) - 1)
            self.logger.debug('checkpoint added: {}'.format(self.checkpoints[-1]))

        self.logger.debug('------- END ENTERING BASE ROUTE -------')
        self.logger.info('train {} is ready to go'.format(train_id))

    def draw(self, surface, base_offset):
        self.logger.debug('------- START DRAWING -------')
        if self.image is not None:
            if not self.route_config['locked']:
                self.logger.debug('base route is not locked, regular image set')
                surface.blit(self.image, (base_offset[0] + self.route_config['image_position'][0],
                                          base_offset[1] + self.route_config['image_position'][1]))

        self.logger.debug('------- END DRAWING -------')
        self.logger.info('base route image is in place')

    def update_base_route_state(self, game_paused):
        if not game_paused:
            self.logger.debug('------- START UPDATING -------')
            self.logger.debug('force_busy = {}'.format(self.route_config['force_busy']))
            self.route_config['busy'] = self.route_config['force_busy']
            if len(self.junctions) > 0:
                for i in range(len(self.junctions)):
                    if type(self.junctions[i]) == RailroadSwitch:
                        self.route_config['busy'] = self.route_config['busy'] or self.junctions[i].busy
                        self.logger.debug('switch {} {} busy = {}'
                                          .format(self.junctions[i].straight_track, self.junctions[i].side_track,
                                                  self.junctions[i].busy))
                    elif type(self.junctions[i]) == Crossover:
                        self.route_config['busy'] = self.route_config['busy'] or self.junctions[i].busy[
                            self.junction_position[i][0]][self.junction_position[i][1]]
                        self.logger.debug('crossover {} {} busy = {}'
                                          .format(self.junctions[i].straight_track_1,
                                                  self.junctions[i].straight_track_2,
                                                  self.junctions[i]
                                                  .busy[self.junction_position[i][0]][self.junction_position[i][1]]))

            self.logger.debug('busy = {}'.format(self.route_config['busy']))
            self.logger.debug('------- END UPDATING -------')
            self.logger.info('base route updated')

    def update(self, game_paused):
        if not game_paused:
            self.update_base_route_state(game_paused)
            # unlock routes (not available at the moment)
            if self.route_config['under_construction']:
                self.logger.info('base route is under construction')
                self.route_config['construction_time'] -= 1
                self.logger.info('construction_time left: {}'.format(self.route_config['construction_time']))
                if self.route_config['construction_time'] <= 0:
                    self.route_config['locked'] = False
                    self.route_config['under_construction'] = False
                    self.logger.info('route unlocked and is no longer under construction')
