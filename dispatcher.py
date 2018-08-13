import configparser
import os
import random
import logging
from operator import attrgetter

import config as c
from game_object import GameObject
from train import Train


class Dispatcher(GameObject):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('dispatcher')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.fh)
        # timer since main entry was left by previous train before creating new one
        self.train_timer = []
        self.trains = []
        self.train_ids = []
        self.train_routes = []
        self.tracks = []
        # next train ID, used by signals to distinguish trains
        self.train_counter = None
        self.supported_carts = []
        self.config = None

    def read_state(self):
        self.config = configparser.RawConfigParser()
        if os.path.exists('user_cfg/dispatcher/config.ini'):
            self.config.read('user_cfg/dispatcher/config.ini')
        else:
            self.config.read('default_cfg/dispatcher/config.ini')

        train_timer_parsed = self.config['user_data']['train_timer'].split(',')
        self.train_timer = [int(train_timer_parsed[0]), int(train_timer_parsed[1])]
        self.train_counter = self.config['user_data'].getint('train_counter')
        supported_carts_parsed = self.config['user_data']['supported_carts'].split(',')
        self.supported_carts = [int(supported_carts_parsed[0]), int(supported_carts_parsed[1])]

        if self.config['user_data']['train_ids'] == 'None':
            self.trains = []
            self.train_ids = []
        else:
            train_ids_parsed = self.config['user_data']['train_ids'].split(',')
            for i in range(len(train_ids_parsed)):
                train_ids_parsed[i] = int(train_ids_parsed[i])

            self.train_ids = train_ids_parsed
            for i in self.train_ids:
                train_config = configparser.RawConfigParser()
                train_config.read('user_cfg/trains/train{}.ini'.format(i))
                train_carts = train_config['user_data'].getint('carts')
                if train_config['user_data']['train_route_track_number'] == 'None':
                    train_route_track_number = None
                else:
                    train_route_track_number = train_config['user_data'].getint('train_route_track_number')

                if train_config['user_data']['train_route_type'] == 'None':
                    train_route_type = None
                else:
                    train_route_type = train_config['user_data']['train_route_type']

                train_state = train_config['user_data']['state']
                train_direction = train_config['user_data'].getint('direction')
                if train_route_track_number is not None and train_route_type is not None:
                    saved_train = Train(train_carts, self.train_routes[train_route_track_number][train_route_type],
                                        train_state, train_direction, i)
                else:
                    saved_train = Train(train_carts, None, train_state, train_direction, i)

                if train_config['user_data']['track_number'] == 'None':
                    saved_train.track_number = None
                else:
                    saved_train.track_number = train_config['user_data'].getint('track_number')

                saved_train.speed = train_config['user_data'].getint('speed')
                saved_train.speed_state = train_config['user_data']['speed_state']
                saved_train.speed_factor_position = train_config['user_data'].getint('speed_factor_position')
                saved_train.priority = train_config['user_data'].getint('priority')
                saved_train.boarding_time = train_config['user_data'].getint('boarding_time')
                if train_config['user_data']['carts_position'] == 'None':
                    saved_train.carts_position = []
                else:
                    carts_position_parsed = train_config['user_data']['carts_position'].split('|')
                    for j in range(len(carts_position_parsed)):
                        carts_position_parsed[j] = carts_position_parsed[j].split(',')
                        carts_position_parsed[j] = [int(carts_position_parsed[j][0]), int(carts_position_parsed[j][1])]

                    saved_train.carts_position = carts_position_parsed

                if train_config['user_data']['carts_position_abs'] == 'None':
                    saved_train.carts_position_abs = []
                else:
                    carts_position_abs_parsed = train_config['user_data']['carts_position_abs'].split('|')
                    for j in range(len(carts_position_abs_parsed)):
                        carts_position_abs_parsed[j] = carts_position_abs_parsed[j].split(',')
                        for k in range(len(carts_position_abs_parsed[j])):
                            carts_position_abs_parsed[j][k] = carts_position_abs_parsed[j][k].split('-')
                            carts_position_abs_parsed[j][k] = (int(carts_position_abs_parsed[j][k][0]),
                                                               int(carts_position_abs_parsed[j][k][1]))

                    saved_train.carts_position_abs = carts_position_abs_parsed

                saved_train.config = train_config
                self.trains.append(saved_train)

    def save_state(self):
        if not os.path.exists('user_cfg'):
            os.mkdir('user_cfg')

        if not os.path.exists('user_cfg/dispatcher'):
            os.mkdir('user_cfg/dispatcher')

        self.config['user_data']['train_timer'] = str(self.train_timer[0])+','+str(self.train_timer[1])
        if len(self.train_ids) == 0:
            self.config['user_data']['train_ids'] = 'None'
        else:
            combined_string = ''
            for i in self.train_ids:
                combined_string += '{},'.format(i)

            combined_string = combined_string[0:len(combined_string)-1]
            self.config['user_data']['train_ids'] = combined_string

        self.config['user_data']['train_counter'] = str(self.train_counter)
        self.config['user_data']['supported_carts'] = str(self.supported_carts[0])+','+str(self.supported_carts[1])

        with open('user_cfg/dispatcher/config.ini', 'w') as configfile:
            self.config.write(configfile)

        for i in self.trains:
            i.save_state()

        for i in self.tracks:
            i.save_state()

        for i in range(len(self.train_routes)):
            for j in self.train_routes[i]:
                self.train_routes[i][j].save_state()

    def update(self, game_paused):
        # if game is paused, dispatcher does not work
        if not game_paused:
            for z1 in range(len(self.train_routes)):
                for z2 in self.train_routes[z1]:
                    if self.train_routes[z1][z2].supported_carts[0] in range(1, self.supported_carts[0]) \
                            and not self.train_routes[z1][z2].locked:
                        self.supported_carts[0] = self.train_routes[z1][z2].supported_carts[0]

            self.trains = sorted(self.trains, key=attrgetter('priority'), reverse=True)
            routes_created_inside_iteration = 0
            for i in self.trains:
                if i.state == c.BOARDING_IN_PROGRESS:
                    # if boarding is in progress, track is busy, but no route is assigned,
                    # so we need to override track settings
                    self.tracks[i.track_number - 1].override = True
                    self.tracks[i.track_number - 1].busy = True
                    self.tracks[i.track_number - 1].last_entered_by = i.train_id
                    i.boarding_time -= 1
                    # when boarding time is expired, boarding is complete, and we unlock track settings
                    if i.boarding_time <= 0:
                        self.tracks[i.track_number - 1].override = False
                        i.state = c.BOARDING_COMPLETE
                        self.logger.info('train {} status changed to {}'.format(i.train_id, i.state))

                    # when boarding time is about to expire, we open exit route,
                    # and now it is up to exit signal to decide if train moves or not
                    if i.boarding_time in range(11) and i.train_route is None and routes_created_inside_iteration == 0:
                        i.assign_new_train_route(self.train_routes[i.track_number][c.EXIT_TRAIN_ROUTE[i.direction]],
                                                 i.train_id)
                        routes_created_inside_iteration += 1
                        self.logger.info('train {} new route assigned: track {} {}'
                                         .format(i.train_id, i.train_route.track_number, i.train_route.route_type))

                if len(i.carts_position) > 0:
                    if i.carts_position[0][0] == i.train_route.destination_point:
                        # if train arrives to the track, boarding begins
                        if i.state == c.PENDING_BOARDING:
                            i.state = c.BOARDING_IN_PROGRESS
                            self.logger.info('train {} status changed to {}'.format(i.train_id, i.state))
                            self.logger.info('train {} completed route: track {} {}'
                                             .format(i.train_id, i.train_route.track_number, i.train_route.route_type))
                            i.complete_train_route()

                        # if train arrives to the end of exit route, it just goes away
                        if i.state == c.BOARDING_COMPLETE:
                            self.logger.info('train {} completed route: track {} {}'
                                             .format(i.train_id, i.train_route.track_number, i.train_route.route_type))
                            i.complete_train_route()
                            self.logger.info('train {} successfully processed and is about to be removed'
                                             .format(i.train_id))
                            self.trains.remove(i)

                # train is in approaching state if all tracks are busy,
                # so we wait for any compatible track to be available for this train
                if i.state == c.APPROACHING and routes_created_inside_iteration == 0:
                    route_for_new_train = None
                    for j in range(c.first_priority_tracks[i.direction][0],
                                   c.first_priority_tracks[i.direction][1],
                                   c.first_priority_tracks[i.direction][2]):
                        r = self.train_routes[j][c.ENTRY_TRAIN_ROUTE[i.direction]]
                        # if compatible track is finally available,
                        # we open entry route for our train and leave loop
                        if i.carts in range(r.supported_carts[0], r.supported_carts[1] + 1) and not r.opened \
                                and not self.tracks[j - 1].busy:
                            route_for_new_train = r
                            self.tracks[j - 1].override = True
                            self.tracks[j - 1].busy = True
                            self.tracks[j - 1].last_entered_by = i.train_id
                            i.state = c.PENDING_BOARDING
                            self.logger.info('train {} status changed to {}'.format(i.train_id, i.state))
                            self.logger.info('train {} completed route: track {} {}'
                                             .format(i.train_id, i.train_route.track_number, i.train_route.route_type))
                            i.complete_train_route()
                            i.assign_new_train_route(route_for_new_train, i.train_id)
                            routes_created_inside_iteration += 1
                            self.logger.info('train {} new route assigned: track {} {}'
                                             .format(i.train_id, i.train_route.track_number, i.train_route.route_type))
                            break

                    if route_for_new_train is None:
                        for j in range(c.second_priority_tracks[i.direction][0],
                                       c.second_priority_tracks[i.direction][1],
                                       c.second_priority_tracks[i.direction][2]):
                            r = self.train_routes[j][c.ENTRY_TRAIN_ROUTE[i.direction]]
                            # if compatible track is finally available,
                            # we open entry route for our train and leave loop
                            if i.carts in range(r.supported_carts[0], r.supported_carts[1] + 1) and not r.opened \
                                    and not self.tracks[j - 1].busy:
                                route_for_new_train = r
                                self.tracks[j - 1].override = True
                                self.tracks[j - 1].busy = True
                                self.tracks[j - 1].last_entered_by = i.train_id
                                i.state = c.PENDING_BOARDING
                                self.logger.info('train {} status changed to {}'.format(i.train_id, i.state))
                                self.logger.info('train {} completed route: track {} {}'
                                                 .format(i.train_id, i.train_route.track_number,
                                                         i.train_route.route_type))
                                i.complete_train_route()
                                i.assign_new_train_route(route_for_new_train, i.train_id)
                                routes_created_inside_iteration += 1
                                self.logger.info('train {} new route assigned: track {} {}'
                                                 .format(i.train_id, i.train_route.track_number,
                                                         i.train_route.route_type))
                                break

                if i.state == c.APPROACHING_PASS_THROUGH and routes_created_inside_iteration == 0:
                    for j in range(c.pass_through_priority_tracks[i.direction][0],
                                   c.pass_through_priority_tracks[i.direction][1],
                                   c.pass_through_priority_tracks[i.direction][2]):
                        r = self.train_routes[j][c.ENTRY_TRAIN_ROUTE[i.direction]]
                        # if compatible track is finally available,
                        # we open entry route for our train and leave loop
                        if not r.opened and not self.tracks[j - 1].busy:
                            route_for_new_train = r
                            self.tracks[j - 1].override = True
                            self.tracks[j - 1].busy = True
                            self.tracks[j - 1].last_entered_by = i.train_id
                            i.state = c.PENDING_BOARDING
                            self.logger.info('train {} status changed to {}'.format(i.train_id, i.state))
                            self.logger.info('train {} completed route: track {} {}'
                                             .format(i.train_id, i.train_route.track_number, i.train_route.route_type))
                            i.complete_train_route()
                            i.assign_new_train_route(route_for_new_train, i.train_id)
                            routes_created_inside_iteration += 1
                            self.logger.info('train {} new route assigned: track {} {}'
                                             .format(i.train_id, i.train_route.track_number, i.train_route.route_type))
                            break

            # it's time to check if we can spawn more trains
            if routes_created_inside_iteration == 0:
                self.create_new_trains()

            # dispatcher's logic iteration is done, now we update trains, routes and tracks
            for q4 in self.trains:
                q4.update(game_paused)
                if q4.train_route:
                    q4.train_route.update(game_paused)
                for q3 in range(len(self.tracks)):
                    self.tracks[q3].update(game_paused)
                    self.logger.info('track {} busy = {}'.format(q3 + 1, self.tracks[q3].busy))
                    self.logger.info('track {} last entered by {}'.format(q3 + 1, self.tracks[q3].last_entered_by))

    def create_new_trains(self):
        for i in (c.LEFT, c.RIGHT):
            entry_busy = self.train_routes[0][c.APPROACHING_TRAIN_ROUTE[i]].base_routes[0].route_config['busy']
            # we wait until main entry is free
            if not entry_busy:
                self.train_timer[i] += 1
                if self.train_timer[i] >= c.train_creation_timeout[i]:
                    self.train_timer[i] = 0
                    # randomly choose number of carts for train
                    random.seed()
                    carts = random.choice(range(6, 21))
                    if carts < self.supported_carts[0]:
                        route_for_new_train = self.train_routes[0][c.APPROACHING_TRAIN_ROUTE[i]]
                        new_train = Train(carts, route_for_new_train, c.APPROACHING_PASS_THROUGH,
                                          i, self.train_counter)
                        self.train_ids.append(self.train_counter)
                        new_train.train_route.open_train_route(new_train.train_id)
                        new_train.train_route.set_stop_points(new_train.carts)
                        new_train.init_train_position()
                        self.logger.info('train created. id {}, track {}, route = {}, status = {}'
                                         .format(new_train.train_id, new_train.train_route.track_number,
                                                 new_train.train_route.route_type, new_train.state))
                        self.train_counter += 1
                    else:
                        route_for_new_train = self.train_routes[0][c.APPROACHING_TRAIN_ROUTE[i]]
                        new_train = Train(carts, route_for_new_train, c.APPROACHING, i, self.train_counter)
                        self.train_ids.append(self.train_counter)
                        new_train.train_route.open_train_route(new_train.train_id)
                        new_train.train_route.set_stop_points(new_train.carts)
                        new_train.init_train_position()
                        self.logger.info('train created. id {}, track {}, route = {}, status = {}'
                                         .format(new_train.train_id, new_train.train_route.track_number,
                                                 new_train.train_route.route_type, new_train.state))
                        self.train_counter += 1

                    self.trains.append(new_train)

    def draw(self, surface, base_offset):
        for i in self.trains:
            i.draw(surface, base_offset)
