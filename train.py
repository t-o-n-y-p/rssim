import configparser
import logging
import os
import time

import pyglet

from game_object import GameObject


def _game_is_not_paused(fn):
    def _update_if_game_is_not_paused(*args, **kwargs):
        if not args[1]:
            fn(*args, **kwargs)

    return _update_if_game_is_not_paused


class Train(GameObject):
    def __init__(self, carts, train_route, state, direction, new_direction, current_direction, train_id,
                 head_image, mid_image, boarding_lights_image, tail_image, batch, group, boarding_lights_group,
                 load_all_carts_at_once=False):
        super().__init__()
        self.logger = logging.getLogger('game.train_{}'.format(train_id))
        self.logger.debug('------- START INIT -------')
        self.config = None
        self.track_number = None
        self.carts = carts
        self.train_route = train_route
        self.state = state
        self.direction = direction
        self.new_direction = new_direction
        self.current_direction = current_direction
        self.train_id = train_id
        self.batch = batch
        self.group = group
        self.boarding_lights_group = boarding_lights_group
        self.head_image = head_image
        self.mid_image = mid_image
        self.tail_image = tail_image
        self.boarding_lights_image = boarding_lights_image
        self.logger.debug('{} carts, route {}, state {}, direction {}, train_id {}'
                          .format(self.carts, self.train_route, self.state, self.direction, self.train_id))
        # all trains are created with maximum speed,
        # not accelerating and not decelerating
        self.speed = self.c['train_config']['train_maximum_speed']
        self.logger.debug('set maximum speed: {}'.format(self.c['train_config']['train_maximum_speed']))
        self.speed_state = 'move'
        self.logger.debug('set speed_state: {}'.format(self.speed_state))
        # train_acceleration_factor tuple includes absolute shifts
        # for acceleration and deceleration (in reversed order);
        # by default train has far right position for this
        self.speed_factor_position = self.c['train_config']['train_acceleration_factor_length'] - 1
        self.logger.debug('set speed_factor_position: {}'.format(self.speed_factor_position))
        if self.state == 'approaching_pass_through':
            self.priority = 0
            self.boarding_time = 60
        else:
            self.priority = 10000000
            self.boarding_time = self.carts * 300

        if self.train_route is not None:
            if self.train_route.train_route_sections[0].route_config['force_busy'] \
                    and self.train_route.train_route_sections[0].route_config['last_entered_by'] == self.train_id:
                self.train_route.train_route_sections[0].priority = self.priority

        self.logger.debug('set priority: {}'.format(self.priority))
        self.logger.debug('set boarding_time: {}'.format(self.boarding_time))
        self.cart_sprites = []
        self.cart_sprites.append(pyglet.sprite.Sprite(self.head_image[self.current_direction],
                                                      batch=self.batch, group=self.group))
        if not load_all_carts_at_once:
            for i in range(1, self.carts - 1):
                self.cart_sprites.append(None)

            self.cart_sprites.append(None)
            self.boarding_lights_sprite = None
        else:
            for i in range(1, self.carts - 1):
                self.cart_sprites.append(pyglet.sprite.Sprite(self.mid_image[self.current_direction],
                                                              batch=self.batch, group=self.group))

            self.cart_sprites.append(pyglet.sprite.Sprite(self.tail_image[self.current_direction],
                                                          batch=self.batch, group=self.group))
            self.boarding_lights_sprite \
                = pyglet.sprite.Sprite(self.boarding_lights_image[self.current_direction][self.carts],
                                       batch=self.batch, group=self.boarding_lights_group)
            if self.state == 'boarding_in_progress':
                self.boarding_lights_sprite.visible = True
            else:
                self.boarding_lights_sprite.visible = False

        # when train route is assigned, we use carts_position list;
        # it contains relative carts position based on route trail points
        self.carts_position = []
        # when train route is not assigned, we use carts_position_abs list;
        # it contains absolute carts position on the map
        self.carts_position_abs = []
        self.stop_point = None
        self.entire_train_is_visible = False
        self.logger.debug('------- END INIT -------')
        self.logger.warning('train init completed')

    def save_state(self):
        self.logger.debug('------- START SAVING STATE -------')
        if not os.path.exists('user_cfg'):
            os.mkdir('user_cfg')
            self.logger.debug('created user_cfg folder')

        if not os.path.exists('user_cfg/trains'):
            os.mkdir('user_cfg/trains')
            self.logger.debug('created user_cf/trains folder')

        if self.config is None:
            self.config = configparser.RawConfigParser()
            self.config['user_data'] = {}
            self.logger.debug('config parser created')

        self.config['user_data']['carts'] = str(self.carts)
        self.logger.debug('carts: {}'.format(self.config['user_data']['carts']))
        if self.train_route is not None:
            self.config['user_data']['train_route_track_number'] = str(self.train_route.track_number)
            self.config['user_data']['train_route_type'] = str(self.train_route.route_type)
        else:
            self.config['user_data']['train_route_track_number'] = 'None'
            self.config['user_data']['train_route_type'] = 'None'

        self.logger.debug('train_route_track_number: {}'.format(self.config['user_data']['train_route_track_number']))
        self.logger.debug('train_route_type: {}'.format(self.config['user_data']['train_route_type']))

        self.config['user_data']['state'] = self.state
        self.logger.debug('state: {}'.format(self.config['user_data']['state']))
        self.config['user_data']['direction'] = str(self.direction)
        self.config['user_data']['new_direction'] = str(self.new_direction)
        self.config['user_data']['current_direction'] = str(self.current_direction)
        self.logger.debug('direction: {}'.format(self.config['user_data']['direction']))
        if self.track_number is not None:
            self.config['user_data']['track_number'] = str(self.track_number)
        else:
            self.config['user_data']['track_number'] = 'None'

        self.logger.debug('track_number: {}'.format(self.config['user_data']['track_number']))

        self.config['user_data']['speed'] = str(self.speed)
        self.logger.debug('speed: {}'.format(self.config['user_data']['speed']))
        self.config['user_data']['speed_state'] = self.speed_state
        self.logger.debug('speed_state: {}'.format(self.config['user_data']['speed_state']))
        self.config['user_data']['speed_factor_position'] = str(self.speed_factor_position)
        self.logger.debug('speed_factor_position: {}'.format(self.config['user_data']['speed_factor_position']))
        self.config['user_data']['priority'] = str(self.priority)
        self.logger.debug('priority: {}'.format(self.config['user_data']['priority']))
        self.config['user_data']['boarding_time'] = str(self.boarding_time)
        self.logger.debug('boarding_time: {}'.format(self.config['user_data']['boarding_time']))
        if len(self.carts_position) == 0:
            self.config['user_data']['carts_position'] = 'None'
        else:
            combined_string = ''
            for i in self.carts_position:
                combined_string += '{},'.format(i)

            combined_string = combined_string[0:len(combined_string) - 1]
            self.config['user_data']['carts_position'] = combined_string

        self.logger.debug('carts_position: {}'.format(self.config['user_data']['carts_position']))

        if len(self.carts_position_abs) == 0:
            self.config['user_data']['carts_position_abs'] = 'None'
        else:
            combined_string = ''
            for i in self.carts_position_abs:
                combined_string += '{},{}|'.format(i[0], i[1])

            combined_string = combined_string[0:len(combined_string) - 1]
            self.config['user_data']['carts_position_abs'] = combined_string

        self.logger.debug('carts_position_abs: {}'.format(self.config['user_data']['carts_position_abs']))

        with open('user_cfg/trains/train{}.ini'.format(self.train_id), 'w') as configfile:
            self.config.write(configfile)

        self.logger.debug('------- END SAVING STATE -------')
        self.logger.info('train state saved to file user_cfg/trains/train{}.ini'.format(self.train_id))

    def init_train_position(self):
        self.logger.debug('------- START INIT TRAIN POSITION -------')
        # each cart position is based on front and back chassis position
        start_point_parsed = self.train_route.start_point_v2[self.carts]
        self.logger.debug('start point: {}'.format(start_point_parsed))
        for i in range(self.carts):
            self.carts_position.append(start_point_parsed - i * 251)

        self.logger.debug('carts_position: {}'.format(self.carts_position))
        self.logger.debug('------- START INIT TRAIN POSITION -------')
        self.logger.info('train position initialized')

    def complete_train_route(self):
        self.logger.debug('------- START COMPLETE_TRAIN_ROUTE FUNCTION -------')
        # when train reaches route destination point,
        # we close the route and convert carts positions to absolute for next route
        self.train_route.close_train_route()
        self.logger.debug('converting cart positions to absolute')
        self.carts_position_abs.clear()
        for i in self.carts_position:
            dot = self.train_route.trail_points_v2[i]
            self.carts_position_abs.append([dot[0], dot[1]])

        self.logger.debug('cart positions converted to absolute: {}'.format(self.carts_position_abs))
        self.carts_position.clear()
        self.logger.debug('relative cart positions cleared')
        self.train_route = None
        self.logger.debug('train route cleared')
        self.logger.debug('------- END COMPLETE_TRAIN_ROUTE FUNCTION -------')
        self.logger.info('train route completed')

    def assign_new_train_route(self, new_train_route):
        self.logger.debug('------- START ASSIGNING NEW TRAIN ROUTE -------')
        # when new route is assigned,
        # we open the route and convert carts positions to relative
        self.train_route = new_train_route
        self.train_route.open_train_route(self.train_id, self.priority)
        self.carts_position.clear()
        self.logger.debug('converting cart positions to relative')
        for i in self.carts_position_abs:
            self.carts_position.append(abs(i[0] - self.train_route.trail_points_v2[0][0]))

        self.logger.debug('cart positions converted to relative: {}'.format(self.carts_position))
        self.carts_position_abs.clear()
        self.stop_point = self.train_route.stop_point_v2[self.carts]
        self.logger.debug('absolute cart positions cleared')
        self.logger.debug('------- END ASSIGNING NEW TRAIN ROUTE -------')
        self.logger.info('train route assigned')

    @_game_is_not_paused
    def update(self, game_paused):
        self.logger.debug('------- TRAIN UPDATE START -------')
        self.logger.debug('carts: {}'.format(self.carts))
        if self.carts < 11:
            self.priority += 3
            self.logger.debug('increased priority by 3')
        elif self.carts < 16:
            self.priority += 2
            self.logger.debug('increased priority by 2')
        elif self.carts < 21:
            self.priority += 1
            self.logger.debug('increased priority by 1')

        if self.train_route is not None:
            if self.train_route.train_route_sections[0].route_config['force_busy'] \
                    and self.train_route.train_route_sections[0].route_config['last_entered_by'] == self.train_id:
                self.train_route.train_route_sections[0].priority = self.priority

        # while boarding is in progress, train does not move indeed
        self.logger.debug('state: {}'.format(self.state))
        if self.state == 'boarding_in_progress':
            self.speed = 0
            self.logger.debug('speed = 0')
            self.speed_factor_position = 0
            self.logger.debug('speed_factor_position = 0')
        else:
            # as soon as entry route is assigned, train knows its track number
            if self.train_route.route_type \
                    in (self.c['train_route_types']['entry_train_route'][self.c['direction']['left']],
                        self.c['train_route_types']['entry_train_route'][self.c['direction']['right']],
                        self.c['train_route_types']['entry_train_route'][self.c['direction']['left_side']],
                        self.c['train_route_types']['entry_train_route'][self.c['direction']['right_side']]):
                self.track_number = self.train_route.track_number

            self.logger.debug('track_number: {}'.format(self.track_number))

            # stop point is updated based on signal state
            if self.train_route.signal.state == 'red_signal' \
                    and self.carts_position[0] <= self.train_route.stop_point_v2[self.carts]:
                self.stop_point = self.train_route.stop_point_v2[self.carts]
            else:
                self.stop_point = self.train_route.destination_point_v2[self.carts]

            self.logger.debug('stop point: {}'.format(self.stop_point))

            # if train has reached red signal, stop it
            self.logger.debug('first cart position: {}'.format(self.carts_position[0]))
            if self.carts_position[0] == self.stop_point:
                self.speed_state = 'stop'
                self.logger.debug('train reached red signal, speed state = {}'.format(self.speed_state))
            # if it is time to decelerate train, do this;
            elif self.stop_point - self.carts_position[0] \
                    <= self.c['train_config']['train_acceleration_factor'][self.speed_factor_position]:
                self.speed_state = 'decelerate'
                self.logger.debug('distance less than {}, time to decelerate, speed state = {}'
                                  .format(self.c['train_config']['train_acceleration_factor'][
                                                                                self.speed_factor_position],
                                          'decelerate'))
            # if there is some free track space ahead and train is not at maximum speed,
            # accelerate
            else:
                self.logger.debug('free way ahead')
                if self.speed_state != 'move':
                    self.speed_state = 'accelerate'
                    self.logger.debug('not at maximum speed, accelerating, speed state = {}'
                                      .format(self.speed_state))
                else:
                    self.logger.debug('already at maximum speed, speed state = {}'
                                      .format('move'))

            # how to accelerate:
            # difference between next and current shifts indicates how much to move the train;
            # then increase factor position
            self.logger.debug('speed state: {}'.format(self.speed_state))
            if self.speed_state == 'accelerate':
                self.logger.debug('speed_factor_position: {}'.format(self.speed_factor_position))
                self.logger.debug('speed_factor_position limit: {}'
                                  .format(self.c['train_config']['train_acceleration_factor_length']))
                if self.speed_factor_position == self.c['train_config']['train_acceleration_factor_length'] - 1:
                    self.speed_state = 'move'
                    self.logger.debug('train has reached maximum speed')
                else:
                    self.speed \
                        = self.c['train_config']['train_acceleration_factor'][self.speed_factor_position + 1] \
                        - self.c['train_config']['train_acceleration_factor'][self.speed_factor_position]
                    self.logger.debug('speed: {}'.format(self.speed))
                    self.speed_factor_position += 1
                    self.logger.debug('new speed_factor_position: {}'.format(self.speed_factor_position))

            # just stay at maximum speed here
            if self.speed_state == 'move':
                self.logger.debug('train is at maximum speed')
                self.speed = self.c['train_config']['train_maximum_speed']
                self.logger.debug('speed: {}'.format(self.speed))

            # how to decelerate:
            # decrease factor position;
            # difference between next and current shifts indicates how much to move the train
            if self.speed_state == 'decelerate':
                self.speed_factor_position -= 1
                self.logger.debug('speed_factor_position: {}'.format(self.speed_factor_position))
                self.logger.debug('speed_factor_position limit: {}'
                                  .format(self.c['train_config']['train_acceleration_factor_length']))
                self.speed \
                    = self.c['train_config']['train_acceleration_factor'][self.speed_factor_position + 1] \
                    - self.c['train_config']['train_acceleration_factor'][self.speed_factor_position]
                self.logger.debug('speed: {}'.format(self.speed))

            # just stay sill here
            if self.speed_state == 'stop':
                self.speed = 0
                self.logger.debug('speed = 0')
                self.speed_factor_position = 0
                self.logger.debug('speed_factor_position = 0')

            # apply changes
            self.logger.debug('cart old position: {}'.format(self.carts_position))
            for i in range(len(self.carts_position)):
                self.carts_position[i] += self.speed

            self.logger.debug('cart new position: {}'.format(self.carts_position))

        self.logger.debug('------- TRAIN UPDATE END -------')
        self.logger.info('train updated')

    def update_sprite(self, base_offset):
        # in both cases, we use pivot points of both chassis,
        # calculate middle point and axis,
        # but for relative position we need to convert it to absolute positions
        self.logger.debug('------- START DRAWING -------')
        if len(self.carts_position_abs) > 0:
            self.logger.debug('using absolute positions')
            for i in range(len(self.carts_position_abs)):
                if self.cart_sprites[i] is not None:
                    self.update_single_cart_sprite_abs(i, base_offset)
                    self.logger.debug('cart {} is in place'.format(i + 1))
                else:
                    if i == len(self.carts_position_abs) - 1:
                        self.cart_sprites[i] = pyglet.sprite.Sprite(self.tail_image[self.current_direction],
                                                                    batch=self.batch, group=self.group)
                        self.cart_sprites[i].visible = False
                    else:
                        self.cart_sprites[i] = pyglet.sprite.Sprite(self.mid_image[self.current_direction],
                                                                    batch=self.batch, group=self.group)
                        self.cart_sprites[i].visible = False

                    break

        else:
            self.logger.debug('using relative positions')
            for i in range(len(self.carts_position)):
                if self.cart_sprites[i] is not None:
                    self.update_single_cart_sprite(i, base_offset)
                    self.logger.debug('cart {} is in place'.format(i + 1))
                else:
                    if i == len(self.carts_position) - 1:
                        self.cart_sprites[i] = pyglet.sprite.Sprite(self.tail_image[self.current_direction],
                                                                    batch=self.batch, group=self.group)
                        self.cart_sprites[i].visible = False
                    else:
                        self.cart_sprites[i] = pyglet.sprite.Sprite(self.mid_image[self.current_direction],
                                                                    batch=self.batch, group=self.group)
                        self.cart_sprites[i].visible = False

                    break

        if self.boarding_lights_sprite is None:
            self.boarding_lights_sprite \
                = pyglet.sprite.Sprite(self.boarding_lights_image[self.current_direction][self.carts],
                                       batch=self.batch, group=self.boarding_lights_group)
            self.boarding_lights_sprite.visible = False

        self.logger.debug('------- END DRAWING -------')
        self.logger.info('train is in place')

    def update_single_cart_sprite(self, cart_number, base_offset):
        dot = self.train_route.trail_points_v2[self.carts_position[cart_number]]
        x = base_offset[0] + dot[0]
        y = base_offset[1] + dot[1]
        self.logger.debug('dot for cart {}: {}'.format(cart_number, dot))
        if self.cart_sprites[cart_number].visible \
                and (x not in range(-150, self.c['graphics']['screen_resolution'][0] + 150)
                     or y not in range(-100, self.c['graphics']['screen_resolution'][0] + 100)):
            self.cart_sprites[cart_number].visible = False

        if not self.cart_sprites[cart_number].visible \
                and (x in range(-150, self.c['graphics']['screen_resolution'][0] + 150)
                     and y in range(-100, self.c['graphics']['screen_resolution'][0] + 100)):
            self.cart_sprites[cart_number].visible = True

        if self.cart_sprites[cart_number].visible:
            self.cart_sprites[cart_number].position = (x, y)
            self.cart_sprites[cart_number].rotation = dot[2]

        if cart_number == 1 and self.boarding_lights_sprite.visible:
            self.boarding_lights_sprite.position = (x, y)

    def update_single_cart_sprite_abs(self, cart_number, base_offset):
        x = base_offset[0] + self.carts_position_abs[cart_number][0]
        y = base_offset[1] + self.carts_position_abs[cart_number][1]
        if self.cart_sprites[cart_number].visible \
                and (x not in range(-150, self.c['graphics']['screen_resolution'][0] + 150)
                     or y not in range(-25, self.c['graphics']['screen_resolution'][0] + 25)):
            self.cart_sprites[cart_number].visible = False

        if not self.cart_sprites[cart_number].visible \
                and (x in range(-150, self.c['graphics']['screen_resolution'][0] + 150)
                     and y in range(-25, self.c['graphics']['screen_resolution'][0] + 25)):
            self.cart_sprites[cart_number].visible = True

        if self.cart_sprites[cart_number].visible:
            self.cart_sprites[cart_number].position = (x, y)
            self.cart_sprites[cart_number].rotation = 0

        if cart_number == 1 and self.boarding_lights_sprite.visible:
            self.boarding_lights_sprite.position = (x, y)

    def switch_direction(self):
        self.current_direction = self.new_direction
        self.carts_position_abs = list(reversed(self.carts_position_abs))
        self.cart_sprites[0].image = self.head_image[self.current_direction]
        for i in range(1, self.carts - 1):
            if self.cart_sprites[i] is not None:
                self.cart_sprites[i].image = self.mid_image[self.current_direction]

        if self.cart_sprites[self.carts - 1] is not None:
            self.cart_sprites[self.carts - 1].image = self.tail_image[self.current_direction]

        if self.boarding_lights_sprite is not None:
            self.boarding_lights_sprite.image = self.boarding_lights_image[self.current_direction][self.carts]
