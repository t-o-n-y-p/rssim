from configparser import RawConfigParser
from logging import getLogger
from os import path, mkdir

from game_object import GameObject
from base_route import BaseRoute
from railroad_switch import RailroadSwitch
from crossover import Crossover


def _game_is_not_paused(fn):
    def _update_if_game_is_not_paused(*args, **kwargs):
        if not args[1]:
            fn(*args, **kwargs)

    return _update_if_game_is_not_paused


def _train_has_passed_train_route_section(fn):
    def _allow_other_trains_to_pass_if_train_has_passed_train_route_section(*args, **kwargs):
        if args[2] >= args[0].checkpoints_v2[args[0].current_checkpoint]:
            fn(*args, **kwargs)

    return _allow_other_trains_to_pass_if_train_has_passed_train_route_section


class TrainRoute(GameObject):
    def __init__(self, track_number, route_type, supported_carts, train_route_sections, train_route_sections_positions,
                 game_config):
        super().__init__(game_config)
        self.logger = getLogger('game.train_route_{}_{}'.format(track_number, route_type))
        self.logger.debug('------- START INIT -------')
        self.config = RawConfigParser()
        self.logger.debug('config parser created')
        self.route_type = route_type
        self.track_number = track_number
        self.logger.debug('track number ans route type set: {} {}'.format(self.track_number, self.route_type))
        self.logger.debug('base routes set')
        # while train moves, some pieces of train route become free
        self.opened = False
        self.last_opened_by = None
        self.trail_points_v2 = ()
        self.start_point_v2 = ()
        # to aggregate all possible stop points
        self.stop_point_v2 = ()
        # single stop point which is closest to the first chassis of the train
        self.destination_point_v2 = ()
        self.train_route_sections = train_route_sections
        self.train_route_sections_positions = train_route_sections_positions
        self.checkpoints_v2 = []
        counter = 0
        for i in range(len(self.train_route_sections)):
            if type(self.train_route_sections[i]) == BaseRoute:
                counter += self.train_route_sections[i].route_config['length']
            elif type(self.train_route_sections[i]) == RailroadSwitch:
                counter += self.train_route_sections[i].length[self.train_route_sections_positions[i]]
            elif type(self.train_route_sections[i]) == Crossover:
                counter += self.train_route_sections[i]\
                    .length[self.train_route_sections_positions[i][0]][self.train_route_sections_positions[i][1]]

            self.checkpoints_v2.append(counter)

        self.checkpoints_v2 = tuple(self.checkpoints_v2)
        self.logger.debug('checkpoints_v2 = {}'.format(self.checkpoints_v2))
        self.current_checkpoint = 0
        self.signal = self.train_route_sections[0].route_config['exit_signal']
        # number of supported carts is decided below
        self.supported_carts = supported_carts
        self.logger.debug('supported carts: {}'.format(self.supported_carts))
        self.read_state()
        self.logger.debug('------- END INIT -------')
        self.logger.warning('train route init completed')

    def read_state(self):
        self.logger.debug('------- START READING STATE -------')
        if path.exists('user_cfg/train_route/track{}/track{}_{}.ini'
                          .format(self.track_number, self.track_number, self.route_type)):
            self.config.read('user_cfg/train_route/track{}/track{}_{}.ini'
                             .format(self.track_number, self.track_number, self.route_type))
            self.logger.debug('config parsed from user_cfg')
        else:
            self.config.read('default_cfg/train_route/track{}/track{}_{}.ini'
                             .format(self.track_number, self.track_number, self.route_type))
            self.logger.debug('config parsed from default_cfg')

        self.opened = self.config['user_data'].getboolean('opened')
        self.logger.debug('opened: {}'.format(self.opened))
        self.last_opened_by = self.config['user_data'].getint('last_opened_by')
        self.logger.debug('last_opened_by: {}'.format(self.last_opened_by))
        self.current_checkpoint = self.config['user_data'].getint('current_checkpoint')

        if self.config['train_route_config']['start_point_v2'] == 'None':
            self.start_point_v2 = None
        else:
            start_point_v2_parsed = self.config['train_route_config']['start_point_v2'].split(',')
            for i in range(len(start_point_v2_parsed)):
                start_point_v2_parsed[i] = int(start_point_v2_parsed[i])

            self.start_point_v2 = tuple(start_point_v2_parsed)

        stop_point_v2_parsed = self.config['train_route_config']['stop_point_v2'].split(',')
        for i in range(len(stop_point_v2_parsed)):
            stop_point_v2_parsed[i] = int(stop_point_v2_parsed[i])

        self.stop_point_v2 = tuple(stop_point_v2_parsed)

        destination_point_v2_parsed = self.config['train_route_config']['destination_point_v2'].split(',')
        for i in range(len(destination_point_v2_parsed)):
            destination_point_v2_parsed[i] = int(destination_point_v2_parsed[i])

        self.destination_point_v2 = tuple(destination_point_v2_parsed)

        trail_points_v2_parsed = self.config['train_route_config']['trail_points_v2'].split('|')
        for i in range(len(trail_points_v2_parsed)):
            trail_points_v2_parsed[i] = trail_points_v2_parsed[i].split(',')
            trail_points_v2_parsed[i] = (int(trail_points_v2_parsed[i][0]),
                                         int(trail_points_v2_parsed[i][1]),
                                         float(trail_points_v2_parsed[i][2]))

        self.trail_points_v2 = tuple(trail_points_v2_parsed)
        self.logger.debug('------- END READING STATE -------')
        self.logger.info('train route state initialized')

    def save_state(self):
        self.logger.debug('------- START SAVING STATE -------')
        if not path.exists('user_cfg'):
            mkdir('user_cfg')
            self.logger.debug('created user_cfg folder')

        if not path.exists('user_cfg/train_route'):
            mkdir('user_cfg/train_route')
            self.logger.debug('created user_cfg/train_route folder')

        if not path.exists('user_cfg/train_route/track{}'.format(self.track_number)):
            mkdir('user_cfg/train_route/track{}'.format(self.track_number))
            self.logger.debug('created user_cfg/train_route/track{} folder'.format(self.track_number))

        self.config['user_data']['opened'] = str(self.opened)
        self.logger.debug('opened = {}'.format(self.config['user_data']['opened']))
        self.config['user_data']['last_opened_by'] = str(self.last_opened_by)
        self.logger.debug('last_opened_by = {}'.format(self.config['user_data']['last_opened_by']))
        self.config['user_data']['current_checkpoint'] = str(self.current_checkpoint)

        with open('user_cfg/train_route/track{}/track{}_{}.ini'
                  .format(self.track_number, self.track_number, self.route_type), 'w') as configfile:
            self.config.write(configfile)

        self.logger.debug('------- END SAVING STATE -------')
        self.logger.info('train route state saved to file user_cfg/train_route/track{}/track{}_{}.ini'
                         .format(self.track_number, self.track_number, self.route_type))

    def open_train_route(self, train_id, priority):
        # open route and all base routes included;
        # remember which train opens it
        self.opened = True
        self.logger.debug('train route opened is set to True')
        self.last_opened_by = train_id
        self.logger.debug('train route last_opened_by: {}'.format(self.last_opened_by))
        self.current_checkpoint = 0
        for i in range(len(self.train_route_sections)):
            if type(self.train_route_sections[i]) == BaseRoute:
                self.train_route_sections[i].route_config['opened'] = True
                self.train_route_sections[i].route_config['last_opened_by'] = train_id
                self.train_route_sections[i].priority = priority

        self.train_route_sections[0].route_config['force_busy'] = True
        self.train_route_sections[0].route_config['last_entered_by'] = train_id
        self.train_route_sections[0].update_base_route_state()

    def close_train_route(self):
        # fully unlock entire route and remaining base routes
        self.opened = False
        self.logger.debug('train route opened is set to False')
        self.current_checkpoint = 0
        self.train_route_sections[-1].route_config['force_busy'] = False
        self.train_route_sections[-1].route_config['opened'] = False
        self.train_route_sections[-1].update_base_route_state()

    @_game_is_not_paused
    @_train_has_passed_train_route_section
    def update_train_route_sections(self, game_paused, last_cart_position):
        if type(self.train_route_sections[self.current_checkpoint]) == BaseRoute:
            self.train_route_sections[self.current_checkpoint].route_config['force_busy'] = False
            self.train_route_sections[self.current_checkpoint].route_config['opened'] = False
            self.train_route_sections[self.current_checkpoint].update_base_route_state()
        elif type(self.train_route_sections[self.current_checkpoint]) == RailroadSwitch:
            self.train_route_sections[self.current_checkpoint].force_busy = False
            self.train_route_sections[self.current_checkpoint].update(False)
            self.train_route_sections[self.current_checkpoint].dependency.update(False)
        elif type(self.train_route_sections[self.current_checkpoint]) == Crossover:
            self.train_route_sections[self.current_checkpoint].force_busy[
                self.train_route_sections_positions[self.current_checkpoint][0]
            ][self.train_route_sections_positions[self.current_checkpoint][1]] = False
            self.train_route_sections[self.current_checkpoint].update(False)
            self.train_route_sections[self.current_checkpoint].dependency.update(False)

        self.current_checkpoint += 1
