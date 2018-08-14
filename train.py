import logging
import math
import configparser
import os
import concurrent.futures
import time

import pygame

import config as c
from game_object import GameObject
from railroad_switch import RailroadSwitch
from crossover import Crossover


class Train(GameObject):
    def __init__(self, carts, train_route, state, direction, train_id):
        super().__init__()
        self.config = None
        self.track_number = None
        self.carts = carts
        self.direction = direction
        self.train_id = train_id
        self.logger = logging.getLogger('train {}'.format(self.train_id))
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.fh)
        # all trains are created with maximum speed,
        # not accelerating and not decelerating
        self.speed = c.train_maximum_speed
        self.speed_state = c.MOVE
        # train_acceleration_factor tuple includes absolute shifts
        # for acceleration and deceleration (in reversed order);
        # by default train has far right position for this
        self.speed_factor_position = c.train_acceleration_factor_length - 1
        self.state = state
        if self.state == c.APPROACHING_PASS_THROUGH:
            self.priority = 100000000
            self.boarding_time = 1
        else:
            self.priority = 0
            self.boarding_time = self.carts * 300
        self.train_route = train_route
        self.cart_images = [pygame.image.load('{}_head.png'.format(c.train_cart_image_path)).convert_alpha(), ]
        for i in range(1, self.carts - 1):
            self.cart_images.append(pygame.image.load('{}_mid.png'.format(c.train_cart_image_path)).convert_alpha())

        self.cart_images.append(pygame.image.load('{}_tail.png'.format(c.train_cart_image_path)).convert_alpha())
        # when train route is assigned, we use carts_position list;
        # it contains relative carts position based on route trail points
        self.carts_position = []
        # when train route is not assigned, we use carts_position_abs list;
        # it contains absolute carts position on the map
        self.carts_position_abs = []

    def save_state(self):
        if not os.path.exists('user_cfg'):
            os.mkdir('user_cfg')

        if not os.path.exists('user_cfg/trains'):
            os.mkdir('user_cfg/trains')

        if self.config is None:
            self.config = configparser.RawConfigParser()
            self.config['user_data'] = {}

        self.config['user_data']['carts'] = str(self.carts)
        if self.train_route is not None:
            self.config['user_data']['train_route_track_number'] = str(self.train_route.track_number)
            self.config['user_data']['train_route_type'] = str(self.train_route.route_type)
        else:
            self.config['user_data']['train_route_track_number'] = 'None'
            self.config['user_data']['train_route_type'] = 'None'

        self.config['user_data']['state'] = self.state
        self.config['user_data']['direction'] = str(self.direction)
        if self.track_number is not None:
            self.config['user_data']['track_number'] = str(self.track_number)
        else:
            self.config['user_data']['track_number'] = 'None'

        self.config['user_data']['speed'] = str(self.speed)
        self.config['user_data']['speed_state'] = self.speed_state
        self.config['user_data']['speed_factor_position'] = str(self.speed_factor_position)
        self.config['user_data']['priority'] = str(self.priority)
        self.config['user_data']['boarding_time'] = str(self.boarding_time)
        if len(self.carts_position) == 0:
            self.config['user_data']['carts_position'] = 'None'
        else:
            combined_string = ''
            for i in self.carts_position:
                combined_string += '{},{}|'.format(i[0], i[1])

            combined_string = combined_string[0:len(combined_string) - 1]
            self.config['user_data']['carts_position'] = combined_string

        if len(self.carts_position_abs) == 0:
            self.config['user_data']['carts_position_abs'] = 'None'
        else:
            combined_string = ''
            for i in self.carts_position_abs:
                for j in i:
                    combined_string += '{}-{},'.format(j[0], j[1])

                combined_string = combined_string[0:len(combined_string) - 1]
                combined_string += '|'

            combined_string = combined_string[0:len(combined_string) - 1]
            self.config['user_data']['carts_position_abs'] = combined_string

        with open('user_cfg/trains/train{}.ini'.format(self.train_id), 'w') as configfile:
            self.config.write(configfile)

    def init_train_position(self):
        # each cart position is based on front and back chassis position
        for i in range(self.carts):
            self.carts_position.append([self.train_route.start_point - i * 251,
                                        self.train_route.start_point - i * 251 - 178])

    def complete_train_route(self):
        # when train reaches route destination point,
        # we close the route and convert carts positions to absolute for next route
        self.train_route.close_train_route()
        for i in self.carts_position:
            self.carts_position_abs.append([self.train_route.trail_points[i[0]], self.train_route.trail_points[i[1]]])

        self.carts_position.clear()
        self.train_route = None

    def assign_new_train_route(self, new_train_route, train_id):
        # when new route is assigned,
        # we open the route and convert carts positions to relative
        self.train_route = new_train_route
        self.train_route.set_stop_points(self.carts)
        self.train_route.open_train_route(train_id)
        for i in self.carts_position_abs:
            self.carts_position.append([self.train_route.trail_points.index(i[0]),
                                        self.train_route.trail_points.index(i[1])])

        self.carts_position_abs.clear()

    def update(self, game_paused):
        if not game_paused:
            if self.carts < 11:
                self.priority += 3
            elif self.carts < 16:
                self.priority += 2
            elif self.carts < 21:
                self.priority += 1

            # while boarding is in progress, train does not move indeed
            if self.state in c.BOARDING_IN_PROGRESS:
                self.speed = 0
                self.speed_factor_position = 0
            else:
                # as soon as entry route is assigned, train knows its track number
                if self.train_route.route_type in (c.ENTRY_TRAIN_ROUTE[c.LEFT], c.ENTRY_TRAIN_ROUTE[c.RIGHT]):
                    self.track_number = self.train_route.track_number

                # base route is not busy and not opened as soon as back chassis of last cart leaves it
                if self.direction == c.LEFT:
                    for k in self.train_route.busy_routes:
                        if len(self.train_route.base_routes[k].checkpoints) > 0:
                            next_checkpoint_index = self.train_route.base_routes[k].checkpoints.count(0)
                            k2 = self.train_route.base_routes[k].checkpoints[next_checkpoint_index]
                            if self.train_route.trail_points[self.carts_position[len(self.carts_position) - 1][1]][0] \
                                    > self.train_route.base_routes[k].route_config['trail_points'][k2][0]:
                                if len(self.train_route.base_routes[k].checkpoints) == 1:
                                    self.train_route.base_routes[k].checkpoints.clear()
                                    self.train_route.base_routes[k].route_config['busy'] = False
                                    self.train_route.busy_routes.remove(k)
                                    self.train_route.base_routes[k].route_config['opened'] = False
                                    self.train_route.opened_routes.remove(k)
                                else:
                                    self.train_route.base_routes[k].checkpoints[next_checkpoint_index] = 0
                                    if type(self.train_route.base_routes[k].junctions[next_checkpoint_index]) \
                                            == type(RailroadSwitch):
                                        self.train_route.base_routes[k].junctions[next_checkpoint_index].force_busy \
                                            = False
                                    elif type(self.train_route.base_routes[k].junctions[next_checkpoint_index]) \
                                            == type(Crossover):
                                        self.train_route.base_routes[k].junctions[next_checkpoint_index].force_busy[
                                            self.train_route.base_routes[k].junction_position[next_checkpoint_index][0]
                                        ][
                                            self.train_route.base_routes[k].junction_position[next_checkpoint_index][1]
                                        ] = False

                                    if self.train_route.base_routes[k].checkpoints.count(0) \
                                            == len(self.train_route.base_routes[k].checkpoints):
                                        self.train_route.base_routes[k].checkpoints.clear()
                                        self.train_route.base_routes[k].route_config['busy'] = False
                                        self.train_route.busy_routes.remove(k)
                                        self.train_route.base_routes[k].route_config['opened'] = False
                                        self.train_route.opened_routes.remove(k)

                # base route is not busy and not opened as soon as back chassis of last cart leaves it
                if self.direction == c.RIGHT:
                    for k in self.train_route.busy_routes:
                        if len(self.train_route.base_routes[k].checkpoints) > 0:
                            next_checkpoint_index = self.train_route.base_routes[k].checkpoints.count(0)
                            k2 = self.train_route.base_routes[k].checkpoints[next_checkpoint_index]
                            if self.train_route.trail_points[self.carts_position[len(self.carts_position) - 1][1]][0] \
                                    < self.train_route.base_routes[k].route_config['trail_points'][k2][0]:
                                if len(self.train_route.base_routes[k].checkpoints) == 1:
                                    self.train_route.base_routes[k].checkpoints.clear()
                                    self.train_route.base_routes[k].route_config['busy'] = False
                                    self.train_route.busy_routes.remove(k)
                                    self.train_route.base_routes[k].route_config['opened'] = False
                                    self.train_route.opened_routes.remove(k)
                                else:
                                    self.train_route.base_routes[k].checkpoints[next_checkpoint_index] = 0
                                    if type(self.train_route.base_routes[k].junctions[next_checkpoint_index]) \
                                            == type(RailroadSwitch):
                                        self.train_route.base_routes[k].junctions[next_checkpoint_index].force_busy \
                                            = False
                                    elif type(self.train_route.base_routes[k].junctions[next_checkpoint_index]) \
                                            == type(Crossover):
                                        self.train_route.base_routes[k].junctions[next_checkpoint_index].force_busy[
                                            self.train_route.base_routes[k].junction_position[next_checkpoint_index][0]
                                        ][
                                            self.train_route.base_routes[k].junction_position[next_checkpoint_index][1]
                                        ] = False

                                    if self.train_route.base_routes[k].checkpoints.count(0) \
                                            == len(self.train_route.base_routes[k].checkpoints):
                                        self.train_route.base_routes[k].checkpoints.clear()
                                        self.train_route.base_routes[k].route_config['busy'] = False
                                        self.train_route.busy_routes.remove(k)
                                        self.train_route.base_routes[k].route_config['opened'] = False
                                        self.train_route.opened_routes.remove(k)

                # stop point is updated based on signal state
                self.train_route.set_next_stop_point(self.carts_position[0][0])
                # if train has reached red signal, stop it
                if self.carts_position[0][0] == self.train_route.next_stop_point:
                    self.speed_state = c.STOP
                # if it is time to decelerate train, do this;
                elif self.train_route.next_stop_point - self.carts_position[0][0] <= c.train_braking_distance:
                    self.speed_state = c.DECELERATE
                # if there is some free track space ahead and train is not at maximum speed,
                # accelerate
                else:
                    if self.speed_state != c.MOVE:
                        self.speed_state = c.ACCELERATE

                # how to accelerate:
                # difference between next and current shifts indicates how much to move the train;
                # then increase factor position
                if self.speed_state == c.ACCELERATE:
                    if self.speed_factor_position == c.train_acceleration_factor_length - 1:
                        self.speed_state = c.MOVE
                    else:
                        self.speed = c.train_acceleration_factor[self.speed_factor_position + 1] \
                                     - c.train_acceleration_factor[self.speed_factor_position]
                        self.speed_factor_position += 1

                # just stay at maximum speed here
                if self.speed_state == c.MOVE:
                    self.speed = c.train_maximum_speed

                # how to decelerate:
                # decrease factor position;
                # difference between next and current shifts indicates how much to move the train
                if self.speed_state == c.DECELERATE:
                    self.speed_factor_position -= 1
                    self.speed = c.train_acceleration_factor[self.speed_factor_position + 1] \
                                 - c.train_acceleration_factor[self.speed_factor_position]

                # just stay sill here
                if self.speed_state == c.STOP:
                    self.speed = 0
                    self.speed_factor_position = 0

                # apply changes
                for i in self.carts_position:
                    i[0] += self.speed
                    i[1] += self.speed

    def draw(self, surface, base_offset):
        # in both cases, we use pivot points of both chassis,
        # calculate middle point and axis,
        # but for relative position we need to convert it to absolute positions
        if len(self.carts_position_abs) > 0:
            # draw_timer = time.time_ns()
            for i in range(len(self.carts_position_abs)):
                self.draw_single_cart_abs(i, surface, base_offset)

            # self.logger.info('drawing train {} took {} ns'.format(self.train_id, time.time_ns() - draw_timer))
        else:
            # draw_timer = time.time_ns()
            # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            #     carts_drawer = {executor.submit(self.draw_single_cart, i, surface, base_offset):
            #                     i for i in list(range(len(self.carts_position)))}
            for i in range(len(self.carts_position)):
                self.draw_single_cart(i, surface, base_offset)

            # self.logger.info('drawing train {} took {} ns'.format(self.train_id, time.time_ns() - draw_timer))

    def draw_single_cart(self, cart_number, surface, base_offset):
        point_one = float(self.train_route.trail_points[self.carts_position[cart_number][1]][1]
                          - self.train_route.trail_points[self.carts_position[cart_number][0]][1])
        point_two = float(self.train_route.trail_points[self.carts_position[cart_number][0]][0]
                          - self.train_route.trail_points[self.carts_position[cart_number][1]][0])
        if round(point_one, 0) == 0:
            x = (self.train_route.trail_points[self.carts_position[cart_number][0]][0]
                 + self.train_route.trail_points[self.carts_position[cart_number][1]][0]) // 2
            y = self.train_route.trail_points[self.carts_position[cart_number][0]][1]
            if round(point_two, 0) > 0:
                surface.blit(self.cart_images[cart_number], (x - self.cart_images[cart_number].get_width() // 2
                                                             + base_offset[0],
                                                             y - self.cart_images[cart_number].get_height() // 2
                                                             + base_offset[1]))
            else:
                new_cart = pygame.transform.flip(self.cart_images[cart_number], True, False)
                surface.blit(new_cart, (x - self.cart_images[cart_number].get_width() // 2 + base_offset[0],
                                        y - self.cart_images[cart_number].get_height() // 2 + base_offset[1]))
        else:
            axis = math.atan2(point_one, point_two) * float(180) / math.pi
            new_cart = pygame.transform.rotate(self.cart_images[cart_number], axis)
            new_size = new_cart.get_size()
            surface.blit(new_cart,
                         (round((self.train_route.trail_points[self.carts_position[cart_number][0]][0]
                                 + self.train_route.trail_points[self.carts_position[cart_number][1]][0])
                                // 2 - new_size[0] // 2 + base_offset[0]),
                          round((self.train_route.trail_points[self.carts_position[cart_number][1]][1]
                                 + self.train_route.trail_points[self.carts_position[cart_number][0]][1])
                                // 2 - new_size[1] // 2 + base_offset[1])))

    def draw_single_cart_abs(self, cart_number, surface, base_offset):
        point_one = float(self.carts_position_abs[cart_number][1][1] - self.carts_position_abs[cart_number][0][1])
        point_two = float(self.carts_position_abs[cart_number][0][0] - self.carts_position_abs[cart_number][1][0])
        if round(point_one, 0) == 0:
            x = (self.carts_position_abs[cart_number][0][0] + self.carts_position_abs[cart_number][1][0]) // 2
            y = self.carts_position_abs[cart_number][0][1]
            if round(point_two, 0) > 0:
                surface.blit(self.cart_images[cart_number], (x - self.cart_images[cart_number].get_width() // 2
                                                             + base_offset[0],
                                                             y - self.cart_images[cart_number].get_height() // 2
                                                             + base_offset[1]))
            else:
                new_cart = pygame.transform.flip(self.cart_images[cart_number], True, False)
                surface.blit(new_cart, (x - self.cart_images[cart_number].get_width() // 2 + base_offset[0],
                                        y - self.cart_images[cart_number].get_height() // 2 + base_offset[1]))
        else:
            axis = math.atan2(point_one, point_two) * float(180) / math.pi
            new_cart = pygame.transform.rotate(self.cart_images[cart_number], axis)
            new_size = new_cart.get_size()
            surface.blit(new_cart,
                         (round((self.carts_position_abs[cart_number][1][0]
                                 + self.carts_position_abs[cart_number][0][0]) // 2
                                - new_size[0] // 2 + base_offset[0]),
                          round((self.carts_position_abs[cart_number][0][1]
                                 + self.carts_position_abs[cart_number][1][1]) // 2
                                - new_size[1] // 2 + base_offset[1])))
