import random

import config as c
from game_object import GameObject
from train import Train


class Dispatcher(GameObject):
    def __init__(self):
        super().__init__()
        # timer since main entry was left by previous train before creating new one
        self.train_timer = [0, 0]
        self.trains = []
        self.train_routes = []
        self.tracks = []
        # next train ID, used by signals to distinguish trains
        self.train_counter = 1

    def update(self, game_paused):
        # if game is paused, dispatcher does not work
        if not game_paused:
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

                    # when boarding time is about to expire, we open exit route,
                    # and now it is up to exit signal to decide if train moves or not
                    if i.boarding_time in range(11) and i.train_route is None:
                        i.assign_new_train_route(self.train_routes[i.track_number][c.EXIT_TRAIN_ROUTE[i.direction]],
                                                 i.train_id)

                if len(i.carts_position) > 0:
                    if i.carts_position[0][0] == i.train_route.destination_point:
                        # if train arrives to the track, boarding begins
                        if i.state == c.PENDING_BOARDING:
                            i.state = c.BOARDING_IN_PROGRESS
                            i.complete_train_route()

                        # if train arrives to the end of exit route, it just goes away
                        if i.state == c.BOARDING_COMPLETE:
                            i.complete_train_route()
                            self.trains.remove(i)

                # train is in approaching state if all tracks are busy,
                # so we wait for any compatible track to be available for this train
                if i.state == c.APPROACHING:
                    route_for_new_train = None
                    for j in range(c.first_priority_tracks[i.direction][0],
                                   c.first_priority_tracks[i.direction][1],
                                   c.first_priority_tracks[i.direction][2]):
                        r = self.train_routes[j][c.ENTRY_TRAIN_ROUTE[i.direction]]
                        # if compatible track is finally available,
                        # we open entry route for our train and leave loop
                        if i.carts in range(r.supported_carts[0], r.supported_carts[1] + 1) and not r.opened and not \
                                self.tracks[j - 1].busy:
                            route_for_new_train = self.train_routes[j][c.ENTRY_TRAIN_ROUTE[i.direction]]
                            self.tracks[j - 1].busy = True
                            self.tracks[j - 1].last_entered_by = i.train_id
                            i.state = c.PENDING_BOARDING
                            i.complete_train_route()
                            i.assign_new_train_route(route_for_new_train, i.train_id)
                            break

                    if route_for_new_train is None:
                        for j in range(c.second_priority_tracks[i.direction][0],
                                       c.second_priority_tracks[i.direction][1],
                                       c.second_priority_tracks[i.direction][2]):
                            r = self.train_routes[j][c.ENTRY_TRAIN_ROUTE[i.direction]]
                            # if compatible track is finally available,
                            # we open entry route for our train and leave loop
                            if i.carts in range(r.supported_carts[0], r.supported_carts[1] + 1) and not r.opened and not \
                                    self.tracks[j - 1].busy:
                                route_for_new_train = self.train_routes[j][c.ENTRY_TRAIN_ROUTE[i.direction]]
                                self.tracks[j - 1].busy = True
                                self.tracks[j - 1].last_entered_by = i.train_id
                                i.state = c.PENDING_BOARDING
                                i.complete_train_route()
                                i.assign_new_train_route(route_for_new_train, i.train_id)
                                break

            # it's time to check if we can spawn more trains
            self.create_new_trains()

            # dispatcher's logic iteration is done, now we update trains, routes and tracks
            for q4 in self.trains:
                q4.update(game_paused)
                if q4.train_route:
                    q4.train_route.update(game_paused)
                for q3 in self.tracks:
                    q3.update(game_paused)

    def create_new_trains(self):
        for i in (c.LEFT, c.RIGHT):
            entry_busy = self.train_routes[0][c.APPROACHING_TRAIN_ROUTE[i]].base_routes[0].route_config.busy
            # we wait until main entry is free
            if not entry_busy:
                self.train_timer[i] += 1
                if self.train_timer[i] >= c.train_creation_timeout[i]:
                    self.train_timer[i] = 0
                    new_train = None
                    # randomly choose number of carts for train
                    random.seed()
                    carts = random.choice(range(12, 21))
                    # if i == c.LEFT:
                    #     carts = random.choice(range(19, 21))
                    # else:
                    #     carts = random.choice(range(12, 14))
                    # if some compatible track is available, we open route for new train
                    route_for_new_train = None
                    for j in range(c.first_priority_tracks[i][0],
                                   c.first_priority_tracks[i][1],
                                   c.first_priority_tracks[i][2]):
                        r = self.train_routes[j][c.ENTRY_TRAIN_ROUTE[i]]
                        if carts in range(r.supported_carts[0], r.supported_carts[1] + 1) and not r.opened and not \
                                self.tracks[j - 1].busy:
                            route_for_new_train = self.train_routes[j][c.ENTRY_TRAIN_ROUTE[i]]
                            new_train = Train(carts, route_for_new_train, c.PENDING_BOARDING, i, self.train_counter)
                            self.train_counter += 1
                            break

                    if route_for_new_train is None:
                        for j in range(c.second_priority_tracks[i][0],
                                       c.second_priority_tracks[i][1],
                                       c.second_priority_tracks[i][2]):
                            r = self.train_routes[j][c.ENTRY_TRAIN_ROUTE[i]]
                            if carts in range(r.supported_carts[0], r.supported_carts[1] + 1) and not r.opened and not \
                                    self.tracks[j - 1].busy:
                                route_for_new_train = self.train_routes[j][c.ENTRY_TRAIN_ROUTE[i]]
                                new_train = Train(carts, route_for_new_train, c.PENDING_BOARDING, i, self.train_counter)
                                self.train_counter += 1
                                break

                    # if compatible route is not available, we open basic entry route
                    # so our train can wait for some track to be available
                    if route_for_new_train is None:
                        route_for_new_train = self.train_routes[0][c.APPROACHING_TRAIN_ROUTE[i]]
                        new_train = Train(carts, route_for_new_train, c.APPROACHING, i, self.train_counter)
                        self.train_counter += 1

                    self.trains.append(new_train)

    def draw(self, surface, base_offset):
        for i in self.trains:
            i.draw(surface, base_offset)
