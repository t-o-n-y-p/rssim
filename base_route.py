import configparser
import logging
import os

from game_object import GameObject
from railroad_switch import RailroadSwitch
from crossover import Crossover


def _game_is_not_paused(fn):
    def _update_if_game_is_not_paused(*args, **kwargs):
        if not args[1]:
            fn(*args, **kwargs)

    return _update_if_game_is_not_paused


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
        self.priority = 0
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
        self.route_config['force_busy'] = self.config['user_data'].getboolean('force_busy')
        self.logger.debug('force_busy: {}'.format(self.route_config['force_busy']))
        self.route_config['busy'] = self.config['user_data'].getboolean('busy')
        self.logger.debug('busy: {}'.format(self.route_config['busy']))
        self.route_config['opened'] = self.config['user_data'].getboolean('opened')
        self.logger.debug('opened: {}'.format(self.route_config['opened']))
        self.route_config['last_opened_by'] = self.config['user_data'].getint('last_opened_by')
        self.logger.debug('last_opened_by: {}'.format(self.route_config['last_opened_by']))
        self.route_config['last_entered_by'] = self.config['user_data'].getint('last_entered_by')
        self.logger.debug('last_entered_by: {}'.format(self.route_config['last_entered_by']))
        if self.config['user_data']['checkpoints'] == 'None':
            self.checkpoints = []
        else:
            checkpoints_parsed = self.config['user_data']['checkpoints'].split(',')
            for i in range(len(checkpoints_parsed)):
                checkpoints_parsed[i] = int(checkpoints_parsed[i])

            self.checkpoints = checkpoints_parsed

        self.logger.info('user-related config parsed')
        # parse stable config
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

        self.config['user_data']['force_busy'] = str(self.route_config['force_busy'])
        self.logger.debug('force_busy value to save: {}'.format(self.config['user_data']['force_busy']))
        self.config['user_data']['busy'] = str(self.route_config['busy'])
        self.logger.debug('busy value to save: {}'.format(self.config['user_data']['busy']))
        self.config['user_data']['opened'] = str(self.route_config['opened'])
        self.logger.debug('opened value to save: {}'.format(self.config['user_data']['opened']))
        self.config['user_data']['last_opened_by'] = str(self.route_config['last_opened_by'])
        self.logger.debug('last_opened_by value to save: {}'.format(self.config['user_data']['last_opened_by']))
        self.config['user_data']['last_entered_by'] = str(self.route_config['last_entered_by'])
        self.logger.debug('last_entered_by value to save: {}'.format(self.config['user_data']['last_entered_by']))
        if len(self.checkpoints) == 0:
            self.config['user_data']['checkpoints'] = 'None'
        else:
            combined_string = ''
            for i in self.checkpoints:
                combined_string += '{},'.format(i)

            combined_string = combined_string[0:len(combined_string)-1]
            self.config['user_data']['checkpoints'] = combined_string

        self.logger.info('config ready to be saved to ini file')

        with open('user_cfg/base_route/track{}/track{}_{}.ini'.format(
                self.track_number, self.track_number, self.route_type), 'w') as configfile:
            self.config.write(configfile)

        self.logger.debug('------- END SAVING STATE -------')
        self.logger.info('base route state saved to file user_cfg/base_route/track{}/track{}_{}.ini'
                         .format(self.track_number, self.track_number, self.route_type))

    def enter_base_route(self, train_id):
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

                self.junctions[i].update(False)
                self.logger.debug('junction updated')
                self.junctions[i].dependency.update(False)
                self.logger.debug('junction dependency updated')
                self.logger.info('junction {} processed'.format(i + 1))

        else:
            self.checkpoints.append(len(self.route_config['trail_points']) - 1)
            self.logger.debug('checkpoint added: {}'.format(self.checkpoints[-1]))

        self.update_base_route_state()
        self.logger.debug('------- END ENTERING BASE ROUTE -------')
        self.logger.info('train {} is ready to go'.format(train_id))

    def update_base_route_state(self):
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
