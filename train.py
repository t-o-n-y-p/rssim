from configparser import RawConfigParser
from logging import getLogger
from os import path, mkdir

from pyglet.sprite import Sprite

from game_object import GameObject


def _game_is_not_paused(fn):
    def _update_if_game_is_not_paused(*args, **kwargs):
        if not args[1]:
            fn(*args, **kwargs)

    return _update_if_game_is_not_paused


class Train(GameObject):
    def __init__(self, cars, train_route, state, direction, new_direction, current_direction, train_id,
                 head_image, mid_image, boarding_lights_image, tail_image, batch, group, boarding_lights_group,
                 game_config):
        super().__init__(game_config)
        self.logger = getLogger('game.train_{}'.format(train_id))
        self.logger.debug('------- START INIT -------')
        self.config = None
        self.track_number = None
        self.cars = cars
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
        self.logger.debug('{} cars, route {}, state {}, direction {}, train_id {}'
                          .format(self.cars, self.train_route, self.state, self.direction, self.train_id))
        # all trains are created with maximum speed,
        # not accelerating and not decelerating
        self.speed = self.c.train_maximum_speed
        self.logger.debug('set maximum speed: {}'.format(self.c.train_maximum_speed))
        self.speed_state = 'move'
        self.logger.debug('set speed_state: {}'.format(self.speed_state))
        # train_acceleration_factor tuple includes absolute shifts
        # for acceleration and deceleration (in reversed order);
        # by default train has far right position for this
        self.speed_factor_position = len(self.c.train_acceleration_factor) - 1
        self.speed_factor_position_limit = len(self.c.train_acceleration_factor) - 1
        self.logger.debug('set speed_factor_position: {}'.format(self.speed_factor_position))
        self.boarding_time = 5
        self.exp = 0.0
        self.money = 0.0
        if self.state == 'approaching_pass_through':
            self.priority = 10000000
        else:
            self.priority = 0

        if self.train_route is not None:
            if self.train_route.train_route_sections[0].route_config['force_busy'] \
                    and self.train_route.train_route_sections[0].route_config['last_entered_by'] == self.train_id:
                self.train_route.train_route_sections[0].priority = self.priority

        self.logger.debug('set priority: {}'.format(self.priority))
        self.car_sprites = []
        self.boarding_light_sprites = []
        self.car_sprites.append(None)
        for i in range(1, self.cars - 1):
            self.car_sprites.append(None)

        self.car_sprites.append(None)

        self.boarding_light_sprites.append(None)
        for i in range(1, self.cars - 1):
            self.boarding_light_sprites.append(None)

        self.boarding_light_sprites.append(None)

        # when train route is assigned, we use cars_position list;
        # it contains relative cars position based on route trail points
        self.cars_position = []
        # when train route is not assigned, we use cars_position_abs list;
        # it contains absolute cars position on the map
        self.cars_position_abs = []
        self.stop_point = None
        self.logger.debug('------- END INIT -------')
        self.logger.warning('train init completed')

    def save_state(self):
        self.logger.debug('------- START SAVING STATE -------')
        if not path.exists('user_cfg'):
            mkdir('user_cfg')
            self.logger.debug('created user_cfg folder')

        if not path.exists('user_cfg/trains'):
            mkdir('user_cfg/trains')
            self.logger.debug('created user_cf/trains folder')

        if self.config is None:
            self.config = RawConfigParser()
            self.config['user_data'] = {}
            self.logger.debug('config parser created')

        self.config['user_data']['cars'] = str(self.cars)
        self.logger.debug('cars: {}'.format(self.config['user_data']['cars']))
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
        self.config['user_data']['exp'] = str(self.exp)
        self.config['user_data']['money'] = str(self.money)
        self.logger.debug('boarding_time: {}'.format(self.config['user_data']['boarding_time']))
        if len(self.cars_position) == 0:
            self.config['user_data']['cars_position'] = 'None'
        else:
            combined_string = ''
            for i in self.cars_position:
                combined_string += '{},'.format(i)

            combined_string = combined_string[0:len(combined_string) - 1]
            self.config['user_data']['cars_position'] = combined_string

        self.logger.debug('cars_position: {}'.format(self.config['user_data']['cars_position']))

        if len(self.cars_position_abs) == 0:
            self.config['user_data']['cars_position_abs'] = 'None'
        else:
            combined_string = ''
            for i in self.cars_position_abs:
                combined_string += '{},{}|'.format(i[0], i[1])

            combined_string = combined_string[0:len(combined_string) - 1]
            self.config['user_data']['cars_position_abs'] = combined_string

        self.logger.debug('cars_position_abs: {}'.format(self.config['user_data']['cars_position_abs']))

        with open('user_cfg/trains/train{}.ini'.format(self.train_id), 'w') as configfile:
            self.config.write(configfile)

        self.logger.debug('------- END SAVING STATE -------')
        self.logger.info('train state saved to file user_cfg/trains/train{}.ini'.format(self.train_id))

    def init_train_position(self):
        self.logger.debug('------- START INIT TRAIN POSITION -------')
        # each car position is based on front and back chassis position
        start_point_parsed = self.train_route.start_point_v2[self.cars]
        self.logger.debug('start point: {}'.format(start_point_parsed))
        for i in range(self.cars):
            self.cars_position.append(start_point_parsed - i * 251)

        self.logger.debug('cars_position: {}'.format(self.cars_position))
        self.logger.debug('------- START INIT TRAIN POSITION -------')
        self.logger.info('train position initialized')

    def complete_train_route(self, convert_cars_positions=True):
        self.logger.debug('------- START COMPLETE_TRAIN_ROUTE FUNCTION -------')
        # when train reaches route destination point,
        # we close the route and convert cars positions to absolute for next route
        self.train_route.close_train_route()
        if convert_cars_positions:
            self.logger.debug('converting car positions to absolute')
            self.cars_position_abs.clear()
            for i in self.cars_position:
                dot = self.train_route.trail_points_v2[i]
                self.cars_position_abs.append([dot[0], dot[1]])

            self.logger.debug('car positions converted to absolute: {}'.format(self.cars_position_abs))
            self.cars_position.clear()
            self.logger.debug('relative car positions cleared')

        self.train_route = None
        self.logger.debug('train route cleared')
        self.logger.debug('------- END COMPLETE_TRAIN_ROUTE FUNCTION -------')
        self.logger.info('train route completed')

    def assign_new_train_route(self, new_train_route, convert_cars_positions=True):
        self.logger.debug('------- START ASSIGNING NEW TRAIN ROUTE -------')
        # when new route is assigned,
        # we open the route and convert cars positions to relative
        self.train_route = new_train_route
        self.train_route.open_train_route(self.train_id, self.priority)
        if convert_cars_positions:
            self.cars_position.clear()
            self.logger.debug('converting car positions to relative')
            for i in self.cars_position_abs:
                self.cars_position.append(abs(i[0] - self.train_route.trail_points_v2[0][0]))

            self.logger.debug('car positions converted to relative: {}'.format(self.cars_position))
            self.cars_position_abs.clear()

        self.stop_point = self.train_route.stop_point_v2[self.cars]
        self.logger.debug('absolute car positions cleared')
        self.logger.debug('------- END ASSIGNING NEW TRAIN ROUTE -------')
        self.logger.info('train route assigned')

    @_game_is_not_paused
    def update(self, game_paused):
        self.logger.debug('------- TRAIN UPDATE START -------')
        self.logger.debug('cars: {}'.format(self.cars))
        if self.cars < 9:
            self.priority += 1
            self.logger.debug('increased priority by 1')
        elif self.cars < 12:
            self.priority += 2
            self.logger.debug('increased priority by 2')
        elif self.cars < 15:
            self.priority += 3
            self.logger.debug('increased priority by 3')
        elif self.cars < 18:
            self.priority += 4
            self.logger.debug('increased priority by 4')
        elif self.cars < 21:
            self.priority += 5
            self.logger.debug('increased priority by 5')

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
                    in (self.c.entry_train_route[self.c.direction_from_left_to_right],
                        self.c.entry_train_route[self.c.direction_from_right_to_left],
                        self.c.entry_train_route[self.c.direction_from_left_to_right_side],
                        self.c.entry_train_route[self.c.direction_from_right_to_left_side]):
                self.track_number = self.train_route.track_number

            self.logger.debug('track_number: {}'.format(self.track_number))

            # stop point is updated based on signal state
            if self.train_route.signal.state == 'red_signal' \
                    and self.cars_position[0] <= self.train_route.stop_point_v2[self.cars]:
                self.stop_point = self.train_route.stop_point_v2[self.cars]
            else:
                self.stop_point = self.train_route.destination_point_v2[self.cars]

            self.logger.debug('stop point: {}'.format(self.stop_point))

            # if train has reached red signal, stop it
            self.logger.debug('first car position: {}'.format(self.cars_position[0]))
            if self.cars_position[0] == self.stop_point:
                self.speed_state = 'stop'
                self.logger.debug('train reached red signal, speed state = {}'.format(self.speed_state))
            # if it is time to decelerate train, do this;
            elif self.stop_point - self.cars_position[0] \
                    <= self.c.train_acceleration_factor[self.speed_factor_position]:
                self.speed_state = 'decelerate'
                self.logger.debug('distance less than {}, time to decelerate, speed state = {}'
                                  .format(self.c.train_acceleration_factor[self.speed_factor_position], 'decelerate'))
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
                                  .format(self.speed_factor_position_limit))
                if self.speed_factor_position == self.speed_factor_position_limit:
                    self.speed_state = 'move'
                    self.logger.debug('train has reached maximum speed')
                else:
                    self.speed \
                        = self.c.train_acceleration_factor[self.speed_factor_position + 1] \
                        - self.c.train_acceleration_factor[self.speed_factor_position]
                    self.logger.debug('speed: {}'.format(self.speed))
                    self.speed_factor_position += 1
                    self.logger.debug('new speed_factor_position: {}'.format(self.speed_factor_position))

            # just stay at maximum speed here
            if self.speed_state == 'move':
                self.logger.debug('train is at maximum speed')
                self.speed = self.c.train_maximum_speed
                self.logger.debug('speed: {}'.format(self.speed))

            # how to decelerate:
            # decrease factor position;
            # difference between next and current shifts indicates how much to move the train
            if self.speed_state == 'decelerate':
                self.speed_factor_position -= 1
                self.logger.debug('speed_factor_position: {}'.format(self.speed_factor_position))
                self.logger.debug('speed_factor_position limit: {}'
                                  .format(self.speed_factor_position_limit))
                self.speed \
                    = self.c.train_acceleration_factor[self.speed_factor_position + 1] \
                    - self.c.train_acceleration_factor[self.speed_factor_position]
                self.logger.debug('speed: {}'.format(self.speed))

            # just stay sill here
            if self.speed_state == 'stop':
                self.speed = 0
                self.logger.debug('speed = 0')
                self.speed_factor_position = 0
                self.logger.debug('speed_factor_position = 0')

            # apply changes
            self.logger.debug('car old position: {}'.format(self.cars_position))
            for i in range(len(self.cars_position)):
                self.cars_position[i] += self.speed

            self.logger.debug('car new position: {}'.format(self.cars_position))

        self.logger.debug('------- TRAIN UPDATE END -------')
        self.logger.info('train updated')

    def update_sprite(self, base_offset):
        # in both cases, we use pivot points of both chassis,
        # calculate middle point and axis,
        # but for relative position we need to convert it to absolute positions
        self.logger.debug('------- START DRAWING -------')
        if len(self.cars_position_abs) > 0:
            self.logger.debug('using absolute positions')
            for i in range(len(self.cars_position_abs)):
                self.update_single_car_sprite_abs(i, base_offset)
                self.logger.debug('car {} is in place'.format(i + 1))

        else:
            self.logger.debug('using relative positions')
            for i in range(len(self.cars_position)):
                self.update_single_car_sprite(i, base_offset)
                self.logger.debug('car {} is in place'.format(i + 1))

        self.logger.debug('------- END DRAWING -------')
        self.logger.info('train is in place')

    def update_single_car_sprite(self, car_number, base_offset):
        dot = self.train_route.trail_points_v2[self.cars_position[car_number]]
        x = base_offset[0] + dot[0]
        y = base_offset[1] + dot[1]
        self.logger.debug('dot for car {}: {}'.format(car_number, dot))
        if not self.car_is_visible(x, y, dx=150, dy=100) and self.car_sprites[car_number] is not None:
            self.car_sprites[car_number].delete()
            self.car_sprites[car_number] = None
            if car_number in range(1, self.cars - 1):
                self.boarding_light_sprites[car_number].delete()
                self.boarding_light_sprites[car_number] = None

        if self.car_is_visible(x, y, dx=150, dy=100) and self.car_sprites[car_number] is None:
            if car_number == 0:
                self.car_sprites[car_number] = Sprite(self.head_image[self.current_direction],
                                                      batch=self.batch, group=self.group)
            elif car_number == self.cars - 1:
                self.car_sprites[car_number] = Sprite(self.tail_image[self.current_direction],
                                                      batch=self.batch, group=self.group)
            else:
                self.car_sprites[car_number] = Sprite(self.mid_image[self.current_direction],
                                                      batch=self.batch, group=self.group)
                self.boarding_light_sprites[car_number] = Sprite(self.boarding_lights_image,
                                                                 batch=self.batch, group=self.boarding_lights_group)

        if self.boarding_light_sprites[car_number] is not None:
            self.boarding_light_sprites[car_number].visible = False

        if self.car_sprites[car_number] is not None:
            self.car_sprites[car_number].update(x, y, dot[2])

        if self.boarding_light_sprites[car_number] is not None:
            self.boarding_light_sprites[car_number].position = (x, y)

    def update_single_car_sprite_abs(self, car_number, base_offset):
        x = base_offset[0] + self.cars_position_abs[car_number][0]
        y = base_offset[1] + self.cars_position_abs[car_number][1]
        if not self.car_is_visible(x, y, dx=150, dy=25) and self.car_sprites[car_number] is not None:
            self.car_sprites[car_number].delete()
            self.car_sprites[car_number] = None
            if car_number in range(1, self.cars - 1):
                self.boarding_light_sprites[car_number].delete()
                self.boarding_light_sprites[car_number] = None

        if self.car_is_visible(x, y, dx=150, dy=25) and self.car_sprites[car_number] is None:
            if car_number == 0:
                self.car_sprites[car_number] = Sprite(self.head_image[self.current_direction],
                                                      batch=self.batch, group=self.group)
            elif car_number == self.cars - 1:
                self.car_sprites[car_number] = Sprite(self.tail_image[self.current_direction],
                                                      batch=self.batch, group=self.group)
            else:
                self.car_sprites[car_number] = Sprite(self.mid_image[self.current_direction],
                                                      batch=self.batch, group=self.group)
                self.boarding_light_sprites[car_number] = Sprite(self.boarding_lights_image,
                                                                 batch=self.batch, group=self.boarding_lights_group)

        if self.boarding_light_sprites[car_number] is not None:
            if self.state == 'boarding_in_progress' and self.boarding_time > 5:
                self.boarding_light_sprites[car_number].visible = True
            else:
                self.boarding_light_sprites[car_number].visible = False

        if self.car_sprites[car_number] is not None:
            self.car_sprites[car_number].update(x, y, 0)

        if self.boarding_light_sprites[car_number] is not None:
            self.boarding_light_sprites[car_number].position = (x, y)

    def switch_direction(self):
        self.current_direction = self.new_direction
        self.cars_position_abs = list(reversed(self.cars_position_abs))
        if self.car_sprites[0] is not None:
            self.car_sprites[0].image = self.head_image[self.current_direction]

        for i in range(1, self.cars - 1):
            if self.car_sprites[i] is not None:
                self.car_sprites[i].image = self.mid_image[self.current_direction]

        if self.car_sprites[self.cars - 1] is not None:
            self.car_sprites[self.cars - 1].image = self.tail_image[self.current_direction]

    def car_is_visible(self, x, y, dx, dy):
        if x in range(-dx, self.c.screen_resolution[0] + dx) and y in range(-dy, self.c.screen_resolution[0] + dy):
            return True
        else:
            return False
