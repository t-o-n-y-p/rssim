import configparser
import os
import logging

import config as c
from game_object import GameObject


class TrainRoute(GameObject):
    def __init__(self, base_routes, track_number, route_type):
        super().__init__()
        self.logger = logging.getLogger('game.train_route_{}_{}'.format(track_number, route_type))
        self.logger.debug('------- START INIT -------')
        self.config = configparser.RawConfigParser()
        self.logger.debug('config parser created')
        self.route_type = route_type
        self.track_number = track_number
        self.logger.debug('track number ans route type set: {} {}'.format(self.track_number, self.route_type))
        self.base_routes = base_routes
        self.logger.debug('base routes set')
        # while train moves, some pieces of train route become free
        self.busy_routes = []
        self.opened_routes = []
        self.opened = False
        self.last_opened_by = None
        self.trail_points = []
        self.start_point = None
        # to aggregate all possible stop points
        self.stop_points = []
        # to aggregate stop points based on red signals
        self.active_stop_points = []
        # single stop point which is closest to the first chassis of the train
        self.next_stop_point = None
        self.destination_point = None
        self.supported_carts = [0, 0]
        self.signals = []
        self.locked = False
        # number of supported carts is decided below
        for j in self.base_routes:
            self.locked = self.locked or j.route_config['locked']
            if j.route_config['supported_carts'][0] > self.supported_carts[0]:
                self.supported_carts[0] = j.route_config['supported_carts'][0]

            if j.route_config['supported_carts'][1] > self.supported_carts[1]:
                self.supported_carts[1] = j.route_config['supported_carts'][1]

        self.logger.debug('supported carts: {}'.format(self.supported_carts))

        # merge trail points of all base routes into single route
        for i in self.base_routes:
            self.trail_points.extend(list(i.route_config['trail_points']))

        self.logger.debug('trail points merged')

        # get start point for entire route if it exists
        if len(self.base_routes) > 0:
            if self.base_routes[0].route_config['start_point']:
                self.start_point = self.trail_points.index(self.base_routes[0].route_config['start_point'])

        self.logger.debug('start point = {}'.format(self.start_point))

        # get all signals along the way
        for j in self.base_routes:
            if j.route_config['exit_signal'] is not None:
                self.signals.append(j.route_config['exit_signal'])

        self.logger.debug('signals merged')

        self.read_state()
        self.logger.debug('------- END INIT -------')
        self.logger.warning('train route init completed')

    def read_state(self):
        self.logger.debug('------- START READING STATE -------')
        if os.path.exists('user_cfg/train_route/track{}_{}.ini'.format(self.track_number, self.route_type)):
            self.config.read('user_cfg/train_route/track{}_{}.ini'.format(self.track_number, self.route_type))
            self.logger.debug('config parsed from user_cfg')
        else:
            self.config.read('default_cfg/train_route/track{}_{}.ini'.format(self.track_number, self.route_type))
            self.logger.debug('config parsed from default_cfg')

        if self.config['user_data']['busy_routes'] == 'None':
            self.busy_routes = []
        else:
            busy_routes_parsed = self.config['user_data']['busy_routes'].split(',')
            for i in range(len(busy_routes_parsed)):
                busy_routes_parsed[i] = int(busy_routes_parsed[i])

            self.busy_routes = busy_routes_parsed

        self.logger.debug('busy routes: {}'.format(self.busy_routes))

        if self.config['user_data']['opened_routes'] == 'None':
            self.opened_routes = []
        else:
            opened_routes_parsed = self.config['user_data']['opened_routes'].split(',')
            for i in range(len(opened_routes_parsed)):
                opened_routes_parsed[i] = int(opened_routes_parsed[i])

            self.opened_routes = opened_routes_parsed

        self.logger.debug('opened routes: {}'.format(self.opened_routes))

        self.opened = self.config['user_data'].getboolean('opened')
        self.logger.debug('opened: {}'.format(self.opened))
        self.last_opened_by = self.config['user_data'].getint('last_opened_by')
        self.logger.debug('last_opened_by: {}'.format(self.last_opened_by))
        if self.config['user_data']['stop_points'] == 'None':
            self.stop_points = []
        else:
            stop_points_parsed = self.config['user_data']['stop_points'].split(',')
            for i in range(len(stop_points_parsed)):
                stop_points_parsed[i] = int(stop_points_parsed[i])

            self.stop_points = stop_points_parsed

        self.logger.debug('stop_points: {}'.format(self.stop_points))

        if self.config['user_data']['active_stop_points'] == 'None':
            self.active_stop_points = []
        else:
            active_stop_points_parsed = self.config['user_data']['active_stop_points'].split(',')
            for i in range(len(active_stop_points_parsed)):
                active_stop_points_parsed[i] = int(active_stop_points_parsed[i])

            self.active_stop_points = active_stop_points_parsed

        self.logger.debug('active_stop_points: {}'.format(self.active_stop_points))

        if self.config['user_data']['destination_point'] == 'None':
            self.destination_point = None
        else:
            self.destination_point = self.config['user_data'].getint('destination_point')

        self.logger.debug('destination_point: {}'.format(self.destination_point))

        if self.config['user_data']['next_stop_point'] == 'None':
            self.next_stop_point = None
        else:
            self.next_stop_point = self.config['user_data'].getint('next_stop_point')

        self.logger.debug('next_stop_point: {}'.format(self.next_stop_point))
        self.logger.debug('------- END READING STATE -------')
        self.logger.info('train route state initialized')

    def save_state(self):
        self.logger.debug('------- START SAVING STATE -------')
        if not os.path.exists('user_cfg'):
            os.mkdir('user_cfg')
            self.logger.debug('created user_cfg folder')

        if not os.path.exists('user_cfg/train_route'):
            os.mkdir('user_cfg/train_route')
            self.logger.debug('created user_cfg/train_route folder')

        if len(self.busy_routes) == 0:
            self.config['user_data']['busy_routes'] = 'None'
        else:
            combined_string = ''
            for i in self.busy_routes:
                combined_string += '{},'.format(i)

            combined_string = combined_string[0:len(combined_string)-1]
            self.config['user_data']['busy_routes'] = combined_string

        self.logger.debug('busy_routes = {}'.format(self.config['user_data']['busy_routes']))

        if len(self.opened_routes) == 0:
            self.config['user_data']['opened_routes'] = 'None'
        else:
            combined_string = ''
            for i in self.opened_routes:
                combined_string += '{},'.format(i)

            combined_string = combined_string[0:len(combined_string)-1]
            self.config['user_data']['opened_routes'] = combined_string

        self.logger.debug('opened_routes = {}'.format(self.config['user_data']['opened_routes']))

        self.config['user_data']['opened'] = str(self.opened)
        self.logger.debug('opened = {}'.format(self.config['user_data']['opened']))
        self.config['user_data']['last_opened_by'] = str(self.last_opened_by)
        self.logger.debug('last_opened_by = {}'.format(self.config['user_data']['last_opened_by']))

        if len(self.stop_points) == 0:
            self.config['user_data']['stop_points'] = 'None'
        else:
            combined_string = ''
            for i in self.stop_points:
                combined_string += '{},'.format(i)

            combined_string = combined_string[0:len(combined_string)-1]
            self.config['user_data']['stop_points'] = combined_string

        self.logger.debug('stop_points = {}'.format(self.config['user_data']['stop_points']))

        if len(self.active_stop_points) == 0:
            self.config['user_data']['active_stop_points'] = 'None'
        else:
            combined_string = ''
            for i in self.active_stop_points:
                combined_string += '{},'.format(i)

            combined_string = combined_string[0:len(combined_string)-1]
            self.config['user_data']['active_stop_points'] = combined_string

        self.logger.debug('active_stop_points = {}'.format(self.config['user_data']['active_stop_points']))

        if self.destination_point is None:
            self.config['user_data']['destination_point'] = 'None'
        else:
            self.config['user_data']['destination_point'] = str(self.destination_point)

        self.logger.debug('destination_point = {}'.format(self.config['user_data']['destination_point']))

        if self.next_stop_point is None:
            self.config['user_data']['next_stop_point'] = 'None'
        else:
            self.config['user_data']['next_stop_point'] = str(self.next_stop_point)

        self.logger.debug('next_stop_point = {}'.format(self.config['user_data']['next_stop_point']))

        with open('user_cfg/train_route/track{}_{}.ini'.format(self.track_number, self.route_type), 'w') as configfile:
            self.config.write(configfile)

        self.logger.debug('------- END SAVING STATE -------')
        self.logger.info('train route state saved to file user_cfg/train_route/track{}_{}.ini'
                         .format(self.track_number, self.route_type))

    def set_next_stop_point(self, first_cart_position):
        # update single stop point which is closest to the first chassis of the train
        self.logger.debug('active stop points: {}'.format(self.active_stop_points))
        self.logger.debug('first_cart_position: {}'.format(first_cart_position))
        index = len(self.active_stop_points)
        if index == 1:
            if first_cart_position <= self.active_stop_points[0]:
                self.next_stop_point = self.active_stop_points[0]
        elif index > 1:
            if first_cart_position <= self.active_stop_points[0]:
                self.next_stop_point = self.active_stop_points[0]
            else:
                for i in range(index-1):
                    if first_cart_position in (self.active_stop_points[i]+1, self.active_stop_points[i+1]+1):
                        self.next_stop_point = self.active_stop_points[i+1]

        self.logger.debug('next_stop_point: {}'.format(self.next_stop_point))

    def set_stop_points(self, carts):
        self.stop_points = []
        self.active_stop_points = []
        self.destination_point = None
        for j in self.base_routes:
            if j.route_config['stop_point'] is not None:
                self.stop_points.append(self.trail_points.index(j.route_config['stop_point'][carts]))

        self.logger.debug('stop points: {}'.format(self.stop_points))

        if len(self.stop_points) > 0:
            for i in self.stop_points:
                self.active_stop_points.append(i)

            self.logger.debug('active stop points: {}'.format(self.active_stop_points))
            self.destination_point = self.stop_points[-1]
            self.logger.debug('destination_point: {}'.format(self.destination_point))

        self.supported_carts = tuple(self.supported_carts)
        self.set_next_stop_point(0)

    def open_train_route(self, train_id, game_paused):
        # open route and all base routes included;
        # remember which train opens it
        self.busy_routes.clear()
        self.opened_routes.clear()
        self.opened = True
        self.logger.debug('train route opened is set to True')
        self.last_opened_by = train_id
        self.logger.debug('train route last_opened_by: {}'.format(self.last_opened_by))
        self.base_routes[0].enter_base_route(train_id, game_paused)
        for i in range(len(self.base_routes)):
            self.base_routes[i].route_config['opened'] = True
            self.logger.debug('base route {} {} opened is set to True'
                              .format(self.base_routes[i].track_number, self.base_routes[i].route_type))
            self.base_routes[i].route_config['last_opened_by'] = train_id
            self.logger.debug('base route {} {} last_opened_by: {}'
                              .format(self.base_routes[i].track_number, self.base_routes[i].route_type,
                                      self.base_routes[i].route_config['last_opened_by']))
            self.busy_routes.append(i)
            self.logger.debug('{} appended to busy routes list'.format(i))
            self.opened_routes.append(i)
            self.logger.debug('{} appended to opened routes list'.format(i))

        self.logger.debug('busy_routes = {}'.format(self.busy_routes))
        self.logger.debug('opened_routes = {}'.format(self.opened_routes))

    def close_train_route(self):
        # fully unlock entire route and remaining base routes
        self.opened = False
        self.logger.debug('train route opened is set to False')
        for i in self.opened_routes:
            self.base_routes[i].route_config['opened'] = False
            self.logger.debug('base route {} {} opened is set to False'
                              .format(self.base_routes[i].track_number, self.base_routes[i].route_type))

        for i in self.busy_routes:
            self.base_routes[i].route_config['force_busy'] = False
            self.logger.debug('base route {} {} force_busy is set to False'
                              .format(self.base_routes[i].track_number, self.base_routes[i].route_type))

    def update(self, game_paused):
        if not game_paused:
            self.logger.debug('------- TRAIN ROUTE UPDATE START -------')
            # if signal turns green, make this stop point inactive
            self.active_stop_points = []
            index = list(range(len(self.signals)))
            for i in index:
                if self.signals[i].state != c.GREEN_SIGNAL and len(self.stop_points) > 0:
                    self.active_stop_points.append(self.stop_points[i])

            self.logger.debug('active stop points: {}'.format(self.active_stop_points))
            self.logger.debug('------- TRAIN ROUTE UPDATE END -------')
            self.logger.info('train route updated')
