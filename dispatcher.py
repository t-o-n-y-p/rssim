import configparser
import os
import random
import logging
from operator import attrgetter

import pyglet

from game_object import GameObject
from train import Train


def _game_is_not_paused(fn):
    def _update_if_game_is_not_paused(*args, **kwargs):
        if not args[1]:
            fn(*args, **kwargs)

    return _update_if_game_is_not_paused


class Dispatcher(GameObject):
    def __init__(self, batch, group, boarding_lights_group):
        super().__init__()
        self.logger = logging.getLogger('game.dispatcher')
        self.logger.debug('------- START INIT -------')
        self.config = configparser.RawConfigParser()
        self.logger.debug('config parser created')
        # timer since main entry was left by previous train before creating new one
        self.train_timer = []
        self.trains = []
        self.train_ids = []
        self.train_routes = []
        self.tracks = []
        self.signals = []
        self.batch = batch
        self.group = group
        self.boarding_lights_group = boarding_lights_group
        # next train ID, used by signals to distinguish trains
        self.train_counter = None
        self.supported_carts = []
        self.unlocked_tracks = 4
        self.train_head_image = {}
        self.train_mid_image = {}
        self.train_tail_image = {}
        self.boarding_lights_image = {}
        # ----------- left direction images -----------------
        self.train_head_image[self.c['direction']['left']] = \
            pyglet.image.load('{}_head_{}.png'.format(self.c['train_config']['train_cart_image_path'],
                                                      self.c['direction']['left']))
        self.train_mid_image[self.c['direction']['left']] = \
            pyglet.image.load('{}_mid_{}.png'.format(self.c['train_config']['train_cart_image_path'],
                                                     self.c['direction']['left']))
        self.train_tail_image[self.c['direction']['left']] = \
            pyglet.image.load('{}_tail_{}.png'.format(self.c['train_config']['train_cart_image_path'],
                                                      self.c['direction']['left']))
        # -------------------- right direction images ----------------------
        self.train_head_image[self.c['direction']['right']] = \
            pyglet.image.load('{}_head_{}.png'.format(self.c['train_config']['train_cart_image_path'],
                                                      self.c['direction']['right']))
        self.train_mid_image[self.c['direction']['right']] = \
            pyglet.image.load('{}_mid_{}.png'.format(self.c['train_config']['train_cart_image_path'],
                                                     self.c['direction']['right']))
        self.train_tail_image[self.c['direction']['right']] = \
            pyglet.image.load('{}_tail_{}.png'.format(self.c['train_config']['train_cart_image_path'],
                                                      self.c['direction']['right']))
        # ----------- left side direction images -----------------
        self.train_head_image[self.c['direction']['left_side']] = \
            pyglet.image.load('{}_head_{}.png'.format(self.c['train_config']['train_cart_image_path'],
                                                      self.c['direction']['left_side']))
        self.train_mid_image[self.c['direction']['left_side']] = \
            pyglet.image.load('{}_mid_{}.png'.format(self.c['train_config']['train_cart_image_path'],
                                                     self.c['direction']['left_side']))
        self.train_tail_image[self.c['direction']['left_side']] = \
            pyglet.image.load('{}_tail_{}.png'.format(self.c['train_config']['train_cart_image_path'],
                                                      self.c['direction']['left_side']))
        # -------------------- right side direction images ----------------------
        self.train_head_image[self.c['direction']['right_side']] = \
            pyglet.image.load('{}_head_{}.png'.format(self.c['train_config']['train_cart_image_path'],
                                                      self.c['direction']['right_side']))
        self.train_mid_image[self.c['direction']['right_side']] = \
            pyglet.image.load('{}_mid_{}.png'.format(self.c['train_config']['train_cart_image_path'],
                                                     self.c['direction']['right_side']))
        self.train_tail_image[self.c['direction']['right_side']] = \
            pyglet.image.load('{}_tail_{}.png'.format(self.c['train_config']['train_cart_image_path'],
                                                      self.c['direction']['right_side']))
        for i in (self.c['direction']['left'], self.c['direction']['right'],
                  self.c['direction']['left_side'], self.c['direction']['right_side']):
            self.train_head_image[i].anchor_x = self.train_head_image[i].width // 2
            self.train_head_image[i].anchor_y = self.train_head_image[i].height // 2
            self.train_mid_image[i].anchor_x = self.train_mid_image[i].width // 2
            self.train_mid_image[i].anchor_y = self.train_mid_image[i].height // 2
            self.train_tail_image[i].anchor_x = self.train_tail_image[i].width // 2
            self.train_tail_image[i].anchor_y = self.train_tail_image[i].height // 2

        self.boarding_lights_image[self.c['direction']['left']] = []
        self.boarding_lights_image[self.c['direction']['right']] = []
        self.boarding_lights_image[self.c['direction']['left_side']] = []
        self.boarding_lights_image[self.c['direction']['right_side']] = []
        for i in range(6):
            self.boarding_lights_image[self.c['direction']['left']].append(None)
            self.boarding_lights_image[self.c['direction']['right']].append(None)
            self.boarding_lights_image[self.c['direction']['left_side']].append(None)
            self.boarding_lights_image[self.c['direction']['right_side']].append(None)

        for i in range(6, 21):
            self.boarding_lights_image[self.c['direction']['left']]\
                .append(pyglet.image.load('img/boarding_lights/day/{}.png'.format(i)))
            self.boarding_lights_image[self.c['direction']['left']][i].anchor_x \
                = self.boarding_lights_image[self.c['direction']['left']][i].width - 126
            self.boarding_lights_image[self.c['direction']['left']][i].anchor_y = 20
            self.boarding_lights_image[self.c['direction']['left_side']]\
                .append(pyglet.image.load('img/boarding_lights/day/{}.png'.format(i)))
            self.boarding_lights_image[self.c['direction']['left_side']][i].anchor_x \
                = self.boarding_lights_image[self.c['direction']['left_side']][i].width - 126
            self.boarding_lights_image[self.c['direction']['left_side']][i].anchor_y = 20
            self.boarding_lights_image[self.c['direction']['right']]\
                .append(pyglet.image.load('img/boarding_lights/day/{}.png'.format(i)))
            self.boarding_lights_image[self.c['direction']['right']][i].anchor_x = 125
            self.boarding_lights_image[self.c['direction']['right']][i].anchor_y = 20
            self.boarding_lights_image[self.c['direction']['right_side']]\
                .append(pyglet.image.load('img/boarding_lights/day/{}.png'.format(i)))
            self.boarding_lights_image[self.c['direction']['right_side']][i].anchor_x = 125
            self.boarding_lights_image[self.c['direction']['right_side']][i].anchor_y = 20

        self.mini_map_tip = None
        self.logger.debug('------- END INIT -------')
        self.logger.warning('dispatcher init completed')

    def read_state(self):
        self.logger.debug('------- START READING STATE -------')
        if os.path.exists('user_cfg/dispatcher/config.ini'):
            self.config.read('user_cfg/dispatcher/config.ini')
            self.logger.debug('config parsed from user_cfg')
        else:
            self.config.read('default_cfg/dispatcher/config.ini')
            self.logger.debug('config parsed from default_cfg')

        self.unlocked_tracks = self.config['user_data'].getint('unlocked_tracks')
        train_timer_parsed = self.config['user_data']['train_timer'].split(',')
        self.train_timer = [int(train_timer_parsed[0]), int(train_timer_parsed[1])]
        self.logger.debug('train_timer: {}'.format(self.train_timer))
        self.train_counter = self.config['user_data'].getint('train_counter')
        self.logger.debug('train_counter: {}'.format(self.train_counter))
        supported_carts_parsed = self.config['user_data']['supported_carts'].split(',')
        self.supported_carts = [int(supported_carts_parsed[0]), int(supported_carts_parsed[1])]
        self.logger.debug('supported_carts: {}'.format(self.supported_carts))
        self.logger.info('dispatcher config parsed')

        if self.config['user_data']['train_ids'] == 'None':
            self.trains = []
            self.train_ids = []
            self.logger.debug('no trains are found in config')
        else:
            train_ids_parsed = self.config['user_data']['train_ids'].split(',')
            for i in range(len(train_ids_parsed)):
                train_ids_parsed[i] = int(train_ids_parsed[i])

            self.train_ids = train_ids_parsed
            self.logger.debug('train ids found in config: {}'.format(self.train_ids))
            for i in self.train_ids:
                self.logger.debug('reading config for train {}'.format(i))
                train_config = configparser.RawConfigParser()
                train_config.read('user_cfg/trains/train{}.ini'.format(i))
                self.logger.debug('config parsed from user_cfg')
                train_carts = train_config['user_data'].getint('carts')
                self.logger.debug('carts: {}'.format(train_carts))
                if train_config['user_data']['train_route_track_number'] == 'None':
                    train_route_track_number = None
                else:
                    train_route_track_number = train_config['user_data'].getint('train_route_track_number')

                self.logger.debug('route track number: {}'.format(train_route_track_number))
                if train_config['user_data']['train_route_type'] == 'None':
                    train_route_type = None
                else:
                    train_route_type = train_config['user_data']['train_route_type']

                self.logger.debug('route type: {}'.format(train_route_type))
                train_state = train_config['user_data']['state']
                self.logger.debug('state: {}'.format(train_state))
                train_direction = train_config['user_data'].getint('direction')
                train_new_direction = train_config['user_data'].getint('new_direction')
                self.logger.debug('direction: {}'.format(train_direction))
                if train_route_track_number is not None and train_route_type is not None:
                    saved_train = Train(carts=train_carts,
                                        train_route=self.train_routes[train_route_track_number][train_route_type],
                                        state=train_state, direction=train_direction,
                                        new_direction=train_new_direction, current_direction=train_direction,
                                        train_id=i,
                                        head_image=self.train_head_image,
                                        mid_image=self.train_mid_image,
                                        boarding_lights_image=self.boarding_lights_image,
                                        tail_image=self.train_tail_image,
                                        batch=self.batch, group=self.group,
                                        boarding_lights_group=self.boarding_lights_group,
                                        load_all_carts_at_once=True)
                else:
                    saved_train = Train(carts=train_carts, train_route=None, state=train_state,
                                        direction=train_direction,
                                        new_direction=train_new_direction, current_direction=train_direction,
                                        train_id=i,
                                        head_image=self.train_head_image,
                                        mid_image=self.train_mid_image,
                                        boarding_lights_image=self.boarding_lights_image,
                                        tail_image=self.train_tail_image,
                                        batch=self.batch, group=self.group,
                                        boarding_lights_group=self.boarding_lights_group,
                                        load_all_carts_at_once=True)

                self.logger.info('train {} created'.format(i))
                if train_config['user_data']['track_number'] == 'None':
                    saved_train.track_number = None
                else:
                    saved_train.track_number = train_config['user_data'].getint('track_number')

                self.logger.debug('train track number: {}'.format(saved_train.track_number))
                saved_train.speed = train_config['user_data'].getint('speed')
                self.logger.debug('speed: {}'.format(saved_train.speed))
                saved_train.speed_state = train_config['user_data']['speed_state']
                self.logger.debug('speed_state: {}'.format(saved_train.speed_state))
                saved_train.speed_factor_position = train_config['user_data'].getint('speed_factor_position')
                self.logger.debug('speed_factor_position: {}'.format(saved_train.speed_factor_position))
                saved_train.priority = train_config['user_data'].getint('priority')
                self.logger.debug('priority: {}'.format(saved_train.priority))
                saved_train.boarding_time = train_config['user_data'].getint('boarding_time')
                self.logger.debug('boarding_time: {}'.format(saved_train.boarding_time))
                if train_config['user_data']['carts_position'] == 'None':
                    saved_train.carts_position = []
                    self.logger.debug('carts_position is empty: in this case carts_position_abs must not be empty')
                else:
                    carts_position_parsed = train_config['user_data']['carts_position'].split('|')
                    for j in range(len(carts_position_parsed)):
                        carts_position_parsed[j] = carts_position_parsed[j].split(',')
                        carts_position_parsed[j] = [int(carts_position_parsed[j][0]), int(carts_position_parsed[j][1])]

                    saved_train.carts_position = carts_position_parsed
                    self.logger.debug('carts_position: {}'.format(saved_train.carts_position))

                if train_config['user_data']['carts_position_abs'] == 'None':
                    saved_train.carts_position_abs = []
                    self.logger.debug('carts_position_abs is empty: in this case carts_position must not be empty')
                else:
                    carts_position_abs_parsed = train_config['user_data']['carts_position_abs'].split('|')
                    for j in range(len(carts_position_abs_parsed)):
                        carts_position_abs_parsed[j] = carts_position_abs_parsed[j].split(',')
                        for k in range(len(carts_position_abs_parsed[j])):
                            carts_position_abs_parsed[j][k] = carts_position_abs_parsed[j][k].split('-')
                            carts_position_abs_parsed[j][k] = (int(carts_position_abs_parsed[j][k][0]),
                                                               int(carts_position_abs_parsed[j][k][1]))

                    saved_train.carts_position_abs = carts_position_abs_parsed
                    for w in range(len(saved_train.carts_position_abs)):
                        point_two = float(saved_train.carts_position_abs[w][0][0]
                                          - saved_train.carts_position_abs[w][1][0])
                        if round(point_two, 0) > 0:
                            self.logger.debug('no need to flip')
                        else:
                            saved_train.cart_sprites[w].rotation = 180.0
                            self.logger.debug('flipped cart image to match direction')

                    self.logger.debug('carts_position_abs: {}'.format(saved_train.carts_position_abs))

                saved_train.config = train_config
                self.logger.info('train {} config ready'.format(i))
                self.trains.append(saved_train)
                self.logger.info('train {} appended'.format(i))

        self.logger.info('all trains config ready')
        self.logger.debug('------- END READING STATE -------')
        self.logger.info('dispatcher state initialized')

    def save_state(self):
        self.logger.debug('------- START SAVING STATE -------')
        if not os.path.exists('user_cfg'):
            os.mkdir('user_cfg')
            self.logger.debug('created user_cfg folder')

        if not os.path.exists('user_cfg/dispatcher'):
            os.mkdir('user_cfg/dispatcher')
            self.logger.debug('created user_cfg/dispatcher folder')

        self.config['user_data']['unlocked_tracks'] = str(self.unlocked_tracks)
        self.config['user_data']['train_timer'] = str(self.train_timer[0])+','+str(self.train_timer[1])
        self.logger.debug('train_timer: {}'.format(self.config['user_data']['train_timer']))
        if len(self.train_ids) == 0:
            self.config['user_data']['train_ids'] = 'None'
        else:
            combined_string = ''
            for i in self.train_ids:
                combined_string += '{},'.format(i)

            combined_string = combined_string[0:len(combined_string)-1]
            self.config['user_data']['train_ids'] = combined_string

        self.logger.debug('train_ids: {}'.format(self.config['user_data']['train_ids']))
        self.config['user_data']['train_counter'] = str(self.train_counter)
        self.logger.debug('train_counter: {}'.format(self.config['user_data']['train_counter']))
        self.config['user_data']['supported_carts'] = str(self.supported_carts[0])+','+str(self.supported_carts[1])
        self.logger.debug('supported_carts: {}'.format(self.config['user_data']['supported_carts']))

        with open('user_cfg/dispatcher/config.ini', 'w') as configfile:
            self.config.write(configfile)

        self.logger.debug('------- END SAVING STATE -------')
        self.logger.info('dispatcher state saved to file user_cfg/dispatcher/config.ini')

        for i in self.trains:
            i.save_state()

        for i in self.tracks:
            i.save_state()

        for i in range(len(self.train_routes)):
            for j in self.train_routes[i]:
                self.train_routes[i][j].save_state()

    @_game_is_not_paused
    def update(self, game_paused):
        self.signals = sorted(self.signals, key=attrgetter('priority'), reverse=True)
        for s in self.signals:
            s.update(game_paused)

        self.logger.debug('------- DISPATCHER UPDATE START -------')
        for z3 in self.tracks:
            if not z3.locked:
                if z3.base_routes[0].route_config['supported_carts'][0] in range(1, self.supported_carts[0]):
                    self.supported_carts[0] = z3.base_routes[0].route_config['supported_carts'][0]

                if z3.track_number > self.unlocked_tracks:
                    self.unlocked_tracks = z3.track_number
                    if self.mini_map_tip is not None:
                        self.mini_map_tip.update_image(pyglet.image.load('img/mini_map/{}/mini_map.png'
                                                       .format(self.unlocked_tracks)))

        self.logger.debug('supported_carts: {}'.format(self.supported_carts))
        routes_created_inside_iteration = 0
        self.trains = sorted(self.trains, key=attrgetter('priority'), reverse=True)
        for i in self.trains:
            self.logger.debug('train id: {}'.format(i.train_id))
            self.logger.debug('train priority: {}'.format(i.priority))
            self.logger.debug('train state: {}'.format(i.state))
            if i.state == self.c['train_state_types']['boarding_in_progress']:
                # if boarding is in progress, track is busy, but no route is assigned,
                # so we need to override track settings
                i.boarding_time -= 1
                self.logger.debug('boarding_time: {}'.format(i.boarding_time))
                # when boarding time is about to expire, we open exit route,
                # and now it is up to exit signal to decide if train moves or not
                if i.boarding_time <= 240 and i.current_direction != i.new_direction:
                    if i.direction % 2 != i.new_direction % 2:
                        i.switch_direction()
                    else:
                        i.current_direction = i.new_direction

                if i.boarding_time <= 60 and i.train_route is None and routes_created_inside_iteration == 0:
                    i.assign_new_train_route(self.train_routes[i.track_number][
                                                self.c['train_route_types']['exit_train_route'][i.new_direction]
                                             ], game_paused)
                    routes_created_inside_iteration += 1
                    self.logger.info('train {} new route assigned: track {} {}'
                                     .format(i.train_id, i.train_route.track_number, i.train_route.route_type))
                    self.logger.debug('routes_created_inside_iteration: {}'.format(routes_created_inside_iteration))
                # when boarding time is expired, boarding is complete, and we unlock track settings
                if i.boarding_time <= 0:
                    self.tracks[i.track_number - 1].override = False
                    i.state = self.c['train_state_types']['boarding_complete']
                    i.boarding_lights_sprite.visible = False
                    self.logger.info('train {} status changed to {}'.format(i.train_id, i.state))

            if len(i.carts_position) > 0:
                if i.carts_position[0][0] == i.train_route.destination_point:
                    self.logger.debug('train {} reached route destination point'.format(i.train_id))
                    # if train arrives to the track, boarding begins
                    if i.state == self.c['train_state_types']['pending_boarding']:
                        i.state = self.c['train_state_types']['boarding_in_progress']
                        if i.boarding_time > 60:
                            i.boarding_lights_sprite.visible = True

                        self.logger.debug('train {} boarding begins'.format(i.train_id))
                        self.tracks[i.track_number - 1].override = True
                        self.tracks[i.track_number - 1].busy = True
                        self.tracks[i.track_number - 1].last_entered_by = i.train_id
                        self.logger.info('train {} status changed to {}'.format(i.train_id, i.state))
                        self.logger.info('train {} completed route: track {} {}'
                                         .format(i.train_id, i.train_route.track_number, i.train_route.route_type))
                        i.complete_train_route()

                    # if train arrives to the end of exit route, it just goes away
                    if i.state == self.c['train_state_types']['boarding_complete']:
                        self.logger.debug('train {} reached end of cycle'.format(i.train_id))
                        self.logger.info('train {} completed route: track {} {}'
                                         .format(i.train_id, i.train_route.track_number, i.train_route.route_type))
                        i.complete_train_route()
                        self.logger.info('train {} successfully processed and is about to be removed'
                                         .format(i.train_id))
                        for j in i.cart_sprites:
                            j.delete()

                        self.train_ids.remove(i.train_id)
                        self.trains.remove(i)

            # train is in approaching state if all tracks are busy,
            # so we wait for any compatible track to be available for this train
            if i.state == self.c['train_state_types']['approaching'] and routes_created_inside_iteration == 0:
                self.logger.debug('looking for route for train {}'.format(i.train_id))
                route_for_new_train = None
                for j in self.c['dispatcher_config']['first_priority_tracks'][i.new_direction]:
                    r = self.train_routes[j][self.c['train_route_types']['entry_train_route'][i.direction]]
                    self.logger.debug('checking track {}'.format(j))
                    self.logger.debug('track in busy: {}'.format(self.tracks[j - 1].busy))
                    self.logger.debug('opened: {}'.format(r.opened))
                    self.logger.debug('train carts: {}; route supports: {}'.format(i.carts, r.supported_carts))
                    # if compatible track is finally available,
                    # we open entry route for our train and leave loop
                    if i.carts in range(r.supported_carts[0], r.supported_carts[1] + 1) and not r.opened \
                            and not self.tracks[j - 1].locked and not self.tracks[j - 1].busy:
                        self.logger.debug('all requirements met')
                        route_for_new_train = r
                        self.tracks[j - 1].override = True
                        self.tracks[j - 1].busy = True
                        self.tracks[j - 1].last_entered_by = i.train_id
                        i.state = self.c['train_state_types']['pending_boarding']
                        self.logger.info('train {} status changed to {}'.format(i.train_id, i.state))
                        self.logger.info('train {} completed route: track {} {}'
                                         .format(i.train_id, i.train_route.track_number, i.train_route.route_type))
                        i.complete_train_route()
                        i.assign_new_train_route(route_for_new_train, game_paused)
                        routes_created_inside_iteration += 1
                        self.logger.debug('routes_created_inside_iteration: {}'
                                          .format(routes_created_inside_iteration))
                        self.logger.info('train {} new route assigned: track {} {}'
                                         .format(i.train_id, i.train_route.track_number, i.train_route.route_type))
                        break

                if route_for_new_train is None:
                    self.logger.debug('could not find first priority track')
                    self.logger.debug('still looking for route for train {}'.format(i.train_id))
                    for j in self.c['dispatcher_config']['second_priority_tracks'][i.new_direction]:
                        r = self.train_routes[j][self.c['train_route_types']['entry_train_route'][i.direction]]
                        self.logger.debug('checking track {}'.format(j))
                        self.logger.debug('track in busy: {}'.format(self.tracks[j - 1].busy))
                        self.logger.debug('opened: {}'.format(r.opened))
                        self.logger.debug('train carts: {}; route supports: {}'.format(i.carts, r.supported_carts))
                        # if compatible track is finally available,
                        # we open entry route for our train and leave loop
                        if i.carts in range(r.supported_carts[0], r.supported_carts[1] + 1) and not r.opened \
                                and not self.tracks[j - 1].busy and not self.tracks[j - 1].locked:
                            self.logger.debug('all requirements met')
                            route_for_new_train = r
                            self.tracks[j - 1].override = True
                            self.tracks[j - 1].busy = True
                            self.tracks[j - 1].last_entered_by = i.train_id
                            i.state = self.c['train_state_types']['pending_boarding']
                            self.logger.info('train {} status changed to {}'.format(i.train_id, i.state))
                            self.logger.info('train {} completed route: track {} {}'
                                             .format(i.train_id, i.train_route.track_number,
                                                     i.train_route.route_type))
                            i.complete_train_route()
                            i.assign_new_train_route(route_for_new_train, game_paused)
                            routes_created_inside_iteration += 1
                            self.logger.debug('routes_created_inside_iteration: {}'
                                              .format(routes_created_inside_iteration))
                            self.logger.info('train {} new route assigned: track {} {}'
                                             .format(i.train_id, i.train_route.track_number,
                                                     i.train_route.route_type))
                            break

                if route_for_new_train is None:
                    self.logger.debug('all tracks are busy, will try next time')

            if i.state == self.c['train_state_types']['approaching_pass_through'] \
                    and routes_created_inside_iteration == 0:
                self.logger.debug('looking for pass through route for train {}'.format(i.train_id))
                for j in self.c['dispatcher_config']['pass_through_priority_tracks'][i.direction]:
                    r = self.train_routes[j][self.c['train_route_types']['entry_train_route'][i.direction]]
                    self.logger.debug('checking track {}'.format(j))
                    self.logger.debug('track in busy: {}'.format(self.tracks[j - 1].busy))
                    self.logger.debug('opened: {}'.format(r.opened))
                    # if compatible track is finally available,
                    # we open entry route for our train and leave loop
                    if not r.opened and not self.tracks[j - 1].busy:
                        self.logger.debug('all requirements met')
                        route_for_new_train = r
                        self.tracks[j - 1].override = True
                        self.tracks[j - 1].busy = True
                        self.tracks[j - 1].last_entered_by = i.train_id
                        i.state = self.c['train_state_types']['pending_boarding']
                        self.logger.info('train {} status changed to {}'.format(i.train_id, i.state))
                        self.logger.info('train {} completed route: track {} {}'
                                         .format(i.train_id, i.train_route.track_number, i.train_route.route_type))
                        i.complete_train_route()
                        i.assign_new_train_route(route_for_new_train, game_paused)
                        routes_created_inside_iteration += 1
                        self.logger.debug('routes_created_inside_iteration: {}'
                                          .format(routes_created_inside_iteration))
                        self.logger.info('train {} new route assigned: track {} {}'
                                         .format(i.train_id, i.train_route.track_number, i.train_route.route_type))
                        break

        # it's time to check if we can spawn more trains
        if routes_created_inside_iteration == 0:
            self.logger.debug('since no routes assigned, we can create new train')
            self.create_new_trains(game_paused)

        self.logger.debug('------- DISPATCHER UPDATE END -------')
        self.logger.info('dispatcher updated')
        # dispatcher's logic iteration is done, now we update trains, routes and tracks
        for q4 in self.trains:
            q4.update(game_paused)
            if q4.train_route:
                q4.train_route.update(game_paused)

        for q3 in range(len(self.tracks)):
            self.tracks[q3].update(game_paused)

    def create_new_trains(self, game_paused):
        self.logger.debug('------- START CREATING NEW TRAINS -------')
        for i in (self.c['direction']['left'], self.c['direction']['right']):
            entry_busy = self.train_routes[0][
                self.c['train_route_types']['approaching_train_route'][i]
            ].base_routes[0].route_config['busy']
            self.logger.debug('entry is busy: {}'.format(entry_busy))
            # we wait until main entry is free
            if not entry_busy:
                self.train_timer[i] += 1
                self.logger.debug('train_timer: {}'.format(self.train_timer[i]))
                self.logger.debug('train_creation_timeout: {}'
                                  .format(self.c['dispatcher_config']['train_creation_timeout'][i]))
                if self.train_timer[i] >= self.c['dispatcher_config']['train_creation_timeout'][i]:
                    self.train_timer[i] = 0
                    self.logger.debug('timer flushed')
                    # randomly choose number of carts for train
                    random.seed()
                    new_direction = i
                    if i == self.c['direction']['left']:
                        carts = random.choice(range(6, 21))
                    else:
                        carts = random.choice(range(6, 8))
                        new_direction = self.c['direction']['right_side']

                    self.logger.debug('carts: {}'.format(carts))
                    if carts < self.supported_carts[0]:
                        self.logger.debug('{}-cart trains are not supported for now, assign pass through route'
                                          .format(carts))
                        route_for_new_train = self.train_routes[0][
                            self.c['train_route_types']['approaching_train_route'][i]]
                        new_train = Train(carts=carts, train_route=route_for_new_train,
                                          state=self.c['train_state_types']['approaching_pass_through'],
                                          direction=i, new_direction=new_direction, current_direction=i,
                                          train_id=self.train_counter,
                                          head_image=self.train_head_image, mid_image=self.train_mid_image,
                                          boarding_lights_image=self.boarding_lights_image,
                                          tail_image=self.train_tail_image,
                                          batch=self.batch, group=self.group,
                                          boarding_lights_group=self.boarding_lights_group)
                        self.train_ids.append(self.train_counter)
                        new_train.train_route.open_train_route(new_train.train_id, new_train.priority, game_paused)
                        new_train.train_route.set_stop_points(new_train.carts)
                        new_train.init_train_position()
                        self.logger.info('train created. id {}, track {}, route = {}, status = {}'
                                         .format(new_train.train_id, new_train.train_route.track_number,
                                                 new_train.train_route.route_type, new_train.state))
                        self.train_counter += 1
                    else:
                        self.logger.debug('{}-cart trains are supported, assign route'
                                          .format(carts))
                        route_for_new_train = self.train_routes[0][
                            self.c['train_route_types']['approaching_train_route'][i]]
                        new_train = Train(carts=carts, train_route=route_for_new_train,
                                          state=self.c['train_state_types']['approaching'],
                                          direction=i, new_direction=new_direction, current_direction=i,
                                          train_id=self.train_counter,
                                          head_image=self.train_head_image, mid_image=self.train_mid_image,
                                          boarding_lights_image=self.boarding_lights_image,
                                          tail_image=self.train_tail_image,
                                          batch=self.batch, group=self.group,
                                          boarding_lights_group=self.boarding_lights_group)
                        self.train_ids.append(self.train_counter)
                        new_train.train_route.open_train_route(new_train.train_id, new_train.priority, game_paused)
                        new_train.train_route.set_stop_points(new_train.carts)
                        new_train.init_train_position()
                        self.logger.info('train created. id {}, track {}, route = {}, status = {}'
                                         .format(new_train.train_id, new_train.train_route.track_number,
                                                 new_train.train_route.route_type, new_train.state))
                        self.train_counter += 1

                    self.trains.append(new_train)
                    self.logger.debug('train {} appended'.format(new_train.train_id))

        self.logger.debug('------- END CREATING NEW TRAINS -------')

    def update_sprite(self, base_offset):
        for i in self.trains:
            i.update_sprite(base_offset)
