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
        self.boarding_time = self.carts * 2
        self.speed = c.train_maximum_speed
        self.state = state
        self.train_route = train_route
        self.train_route.open_train_route(self.train_id)
        self.train_route.set_stop_points(self.carts)
        random.seed()
        self.train_cart_image = pygame.image.load(c.train_cart_image_path[
                                                      random.choice(range(len(c.train_cart_image_path)))
                                                  ]).convert_alpha()
        self.carts_position = []
        self.carts_position_abs = []
        self.init_train_position()

    def init_train_position(self):
        for i in range(self.carts):
            self.carts_position.append([self.train_route.start_point - i * 251,
                                        self.train_route.start_point - i * 251 - 179])

    def complete_train_route(self):
        self.train_route.close_train_route()
        for i in self.carts_position:
            self.carts_position_abs.append([self.train_route.trail_points[i[0]], self.train_route.trail_points[i[1]]])

        self.carts_position.clear()
        self.train_route = None

    def assign_new_train_route(self, new_train_route, train_id):
        self.train_route = new_train_route
        self.train_route.set_stop_points(self.carts)
        self.train_route.open_train_route(train_id)
        for i in self.carts_position_abs:
            self.carts_position.append([self.train_route.trail_points.index(i[0]),
                                        self.train_route.trail_points.index(i[1])])

        self.carts_position_abs.clear()

    def update(self, game_paused):
        if not game_paused:
            if self.state not in (c.train_state_flags[3]):
                if self.train_route.route_type in (c.ENTRY_TRAIN_ROUTE[c.LEFT], c.ENTRY_TRAIN_ROUTE[c.RIGHT]):
                    self.track_number = self.train_route.track_number

                if self.direction == 0:
                    for k in self.train_route.busy_routes:
                        if self.train_route.trail_points[self.carts_position[len(self.carts_position) - 1][1]][0] > \
                                k.route_config.trail_points[len(k.route_config.trail_points) - 1][0]:
                            k.route_config.busy = False
                            self.train_route.busy_routes.remove(k)

                if self.direction == 1:
                    for k in self.train_route.busy_routes:
                        if self.train_route.trail_points[self.carts_position[len(self.carts_position) - 1][1]][0] < \
                                k.route_config.trail_points[len(k.route_config.trail_points) - 1][0]:
                            k.route_config.busy = False
                            self.train_route.busy_routes.remove(k)

                self.train_route.set_next_stop_point(self.carts_position[0][0])
                if self.carts_position[0][0] == self.train_route.next_stop_point:
                    self.speed = 0
                elif self.train_route.next_stop_point - self.carts_position[0][0] \
                        <= self.speed * c.train_deceleration_factor:
                    self.speed -= 1
                    if self.speed < 1:
                        self.speed = 1
                else:
                    # refactor later for train to accelerate slower
                    if self.speed < c.train_maximum_speed:
                        self.speed += 1

            for i in self.carts_position:
                i[0] += self.speed
                i[1] += self.speed

    def draw(self, surface, base_offset):
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
