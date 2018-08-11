import math
import random

import pygame

import config as c
from game_object import GameObject


class Train(GameObject):
    def __init__(self, carts, train_route, state, direction, train_id):
        super().__init__()
        self.track_number = None
        self.carts = carts
        self.direction = direction
        self.train_id = train_id
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
        # initialize train route
        self.train_route.open_train_route(self.train_id)
        self.train_route.set_stop_points(self.carts)
        # randomly choose cart color
        random.seed()
        self.train_cart_image = pygame.image.load(c.train_cart_image_path[
                                                      random.choice(range(len(c.train_cart_image_path)))
                                                  ]).convert_alpha()
        # when train route is assigned, we use carts_position list;
        # it contains relative carts position based on route trail points
        self.carts_position = []
        # when train route is not assigned, we use carts_position_abs list;
        # it contains absolute carts position on the map
        self.carts_position_abs = []
        self.init_train_position()

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
                        if self.train_route.trail_points[self.carts_position[len(self.carts_position) - 1][1]][0] > \
                                self.train_route.base_routes[k].route_config['trail_points'][
                                    len(self.train_route.base_routes[k].route_config['trail_points']) - 1][0]:
                            self.train_route.base_routes[k].route_config['busy'] = False
                            self.train_route.busy_routes.remove(k)
                            self.train_route.base_routes[k].route_config['opened'] = False
                            self.train_route.opened_routes.remove(k)

                # base route is not busy and not opened as soon as back chassis of last cart leaves it
                if self.direction == c.RIGHT:
                    for k in self.train_route.busy_routes:
                        if self.train_route.trail_points[self.carts_position[len(self.carts_position) - 1][1]][0] < \
                                self.train_route.base_routes[k].route_config['trail_points'][
                                    len(self.train_route.base_routes[k].route_config['trail_points']) - 1][0]:
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
                elif self.train_route.next_stop_point - self.carts_position[0][0] \
                        <= c.train_braking_distance:
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
                        self.speed = c.train_acceleration_factor[self.speed_factor_position + 1] - \
                                     c.train_acceleration_factor[self.speed_factor_position]
                        self.speed_factor_position += 1

                # just stay at maximum speed here
                if self.speed_state == c.MOVE:
                    self.speed = c.train_maximum_speed

                # how to decelerate:
                # decrease factor position;
                # difference between next and current shifts indicates how much to move the train
                if self.speed_state == c.DECELERATE:
                    self.speed_factor_position -= 1
                    self.speed = c.train_acceleration_factor[self.speed_factor_position + 1] - \
                                 c.train_acceleration_factor[self.speed_factor_position]

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
            for i in self.carts_position_abs:
                point_one = float(i[1][1] - i[0][1])
                point_two = float(i[0][0] - i[1][0])
                axis = math.atan2(point_one, point_two) * float(180) / math.pi
                new_cart = pygame.transform.rotate(self.train_cart_image, axis)
                new_size = new_cart.get_size()
                surface.blit(new_cart,
                             (round((i[1][0] + i[0][0]) // 2 -
                                    new_size[0] // 2 + base_offset[0]),
                              round((i[0][1] + i[1][1]) // 2 -
                                    new_size[1] // 2 + base_offset[1])))
        else:
            for i in self.carts_position:
                point_one = float(self.train_route.trail_points[i[1]][1] - self.train_route.trail_points[i[0]][1])
                point_two = float(self.train_route.trail_points[i[0]][0] - self.train_route.trail_points[i[1]][0])
                axis = math.atan2(point_one, point_two) * float(180) / math.pi
                new_cart = pygame.transform.rotate(self.train_cart_image, axis)
                new_size = new_cart.get_size()
                surface.blit(new_cart,
                             (round((self.train_route.trail_points[i[0]][0] + self.train_route.trail_points[i[1]][0])
                                    // 2 - new_size[0] // 2 + base_offset[0]),
                              round((self.train_route.trail_points[i[1]][1] + self.train_route.trail_points[i[0]][1])
                                    // 2 - new_size[1] // 2 + base_offset[1])))
