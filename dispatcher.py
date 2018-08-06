import pygame
import random

from game_object import GameObject
import config as c
from train import Train


class Dispatcher(GameObject):
    def __init__(self):
        super().__init__()
        self.train_timer = [0, 0]
        self.trains = []
        self.train_routes = []
        self.tracks = []
        self.train_counter = 0

    def update(self):
        track = None

        for i in self.trains:
            if i.state == c.train_state_flags[3]:
                self.tracks[i.track_number - 1].override = True
                self.tracks[i.track_number - 1].busy = True
                self.tracks[i.track_number - 1].last_entered_by = i.train_id
                i.boarding_time -= 1
                if i.boarding_time == 0:
                    self.tracks[i.track_number - 1].override = False
                    i.state = c.train_state_flags[4]

                if i.boarding_time in range(11):
                    track = i.track_number
                    direction = i.direction
                    # i.complete_train_route()
                    i.assign_new_train_route(self.train_routes[track][c.train_route_flags[1+direction*2]], i.train_id)

            if len(i.carts_position) > 0:
                if i.carts_position[0][0] == i.train_route.destination_point:
                    if i.state == c.train_state_flags[2]:
                        i.state = c.train_state_flags[3]
                        # track = i.train_route.track_number
                        i.complete_train_route()
                        # i.assign_new_train_route(self.train_routes[track][c.train_route_flags[6]])

                    if i.state == c.train_state_flags[4]:
                        i.complete_train_route()
                        self.trains.remove(i)

            if i.state == c.train_state_flags[1]:
                route_for_new_train = None
                for j in (1,):
                    r = self.train_routes[j][c.train_route_flags[i.direction * 2]]
                    if i.carts in range(r.supported_carts[0], r.supported_carts[1]+1) and not r.opened and not self.tracks[j-1].busy:
                        route_for_new_train = self.train_routes[j][c.train_route_flags[i.direction * 2]]
                        self.tracks[j-1].busy = True
                        self.tracks[j-1].last_entered_by = i.train_id

                if route_for_new_train:
                    i.state = c.train_state_flags[2]
                    i.complete_train_route()
                    i.assign_new_train_route(route_for_new_train, i.train_id)

        self.create_new_trains()

        # for q1 in range(len(self.train_routes)):
        #     for q2 in self.train_routes[q1].keys():
        #         self.train_routes[q1][q2].update()

        for q4 in self.trains:
            q4.update()
            if q4.train_route:
                q4.train_route.update()
            for q3 in self.tracks:
                q3.update()

    def create_new_trains(self):
        r = None
        for i in range(2):
            entry_busy = self.train_routes[0][c.train_route_flags[i+4]].base_routes[0].route_config.busy
            if not entry_busy:
                self.train_timer[i] += 1
                if self.train_timer[i] == c.train_creation_timeout * (i+1):
                    self.train_timer[i] = 0
                    new_train = None
                    random.seed()
                    carts = random.choice(range(2, 3))
                    route_for_new_train = None
                    for j in (1, ):
                        r = self.train_routes[j][c.train_route_flags[i*2]]
                        if carts in range(r.supported_carts[0], r.supported_carts[1]+1) and not r.opened and not \
                        self.tracks[j-1].busy:
                            route_for_new_train = self.train_routes[j][c.train_route_flags[i*2]]
                            self.train_counter += 1
                            new_train = Train(carts, route_for_new_train, c.train_state_flags[2], i, self.train_counter)

                    if route_for_new_train == None:
                        route_for_new_train = self.train_routes[0][c.train_route_flags[i+4]]
                        self.train_counter += 1
                        new_train = Train(carts, route_for_new_train, c.train_state_flags[1], i, self.train_counter)

                    self.trains.append(new_train)

    def draw(self, surface, base_offset):
        for i in self.trains:
            i.draw(surface, base_offset)
