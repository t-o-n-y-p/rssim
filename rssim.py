import sys

import pygame

import config as c
from base_route import BaseRoute
from bgimg import BgImg
from dispatcher import Dispatcher
from game import Game
from signal import Signal
from track import Track
from train_route import TrainRoute


class RSSim(Game):
    def __init__(self):
        super().__init__('Railway Station Simulator', c.screen_resolution, c.frame_rate, c.base_offset)
        self.base_routes = [{}]
        self.signals = [{}]
        self.train_routes = [{}]
        self.tracks = []
        self.dispatcher = None
        # we create background image object first to be drawn first
        self.create_bg_img()
        # we create routes, signals and dispatcher and link them to each other correctly
        self.create_infrastructure()
        # this allows user to drag map
        self.mouse_handlers.append(self.handle_mouse_drag)

    def create_bg_img(self):
        background_image = BgImg(c.background_image)
        self.objects.append(background_image)

    def create_infrastructure(self):
        # allow base routes to have access to its config files
        sys.path.append('./base_route_cfg')
        # ------ BASE ROUTES AND SIGNALS ------
        # create main entry and main exit base routes and signals for them
        for j in (c.LEFT_ENTRY_BASE_ROUTE, c.LEFT_EXIT_BASE_ROUTE, c.RIGHT_ENTRY_BASE_ROUTE, c.RIGHT_EXIT_BASE_ROUTE):
            self.base_routes[0][j] = BaseRoute(0, j)
            placement = self.base_routes[0][j].route_config.exit_signal_placement
            flip_needed = self.base_routes[0][j].route_config.flip_needed
            if placement is not None:
                self.signals[0][j] = Signal(placement, flip_needed)

        for j in (c.LEFT_ENTRY_BASE_ROUTE, c.LEFT_EXIT_BASE_ROUTE, c.RIGHT_ENTRY_BASE_ROUTE, c.RIGHT_EXIT_BASE_ROUTE):
            # associate main entry/exit base route with its signal
            self.base_routes[0][j].route_config.exit_signal = self.signals[0][j]
            # for every signal, exit route is the route which ends with this signal
            self.signals[0][j].base_route_exit = self.base_routes[0][j]

        # create all other base routes and signals for platform routes
        for i in range(1, c.tracks_ready + 1):
            self.base_routes.append({})
            self.signals.append({})
            for k in (c.LEFT_ENTRY_BASE_ROUTE, c.LEFT_EXIT_BASE_ROUTE,
                      c.RIGHT_ENTRY_BASE_ROUTE, c.RIGHT_EXIT_BASE_ROUTE,
                      c.LEFT_ENTRY_PLATFORM_BASE_ROUTE, c.RIGHT_ENTRY_PLATFORM_BASE_ROUTE,
                      c.RIGHT_EXIT_PLATFORM_BASE_ROUTE, c.LEFT_EXIT_PLATFORM_BASE_ROUTE):
                self.base_routes[i][k] = BaseRoute(i, k)
                placement = self.base_routes[i][k].route_config.exit_signal_placement
                flip_needed = self.base_routes[i][k].route_config.flip_needed
                if placement is not None and k in (c.RIGHT_EXIT_PLATFORM_BASE_ROUTE, c.LEFT_EXIT_PLATFORM_BASE_ROUTE):
                    self.signals[i][k] = Signal(placement, flip_needed)

        for i in range(1, c.tracks_ready + 1):
            # associate platform base route with its signal
            self.base_routes[i][c.RIGHT_EXIT_PLATFORM_BASE_ROUTE].route_config.exit_signal = \
                self.signals[i][c.RIGHT_EXIT_PLATFORM_BASE_ROUTE]
            self.base_routes[i][c.LEFT_ENTRY_PLATFORM_BASE_ROUTE].route_config.exit_signal = \
                self.signals[i][c.RIGHT_EXIT_PLATFORM_BASE_ROUTE]
            self.base_routes[i][c.LEFT_EXIT_PLATFORM_BASE_ROUTE].route_config.exit_signal = \
                self.signals[i][c.LEFT_EXIT_PLATFORM_BASE_ROUTE]
            self.base_routes[i][c.RIGHT_ENTRY_PLATFORM_BASE_ROUTE].route_config.exit_signal = \
                self.signals[i][c.LEFT_EXIT_PLATFORM_BASE_ROUTE]
            # for every signal, exit route is the route which ends with this signal
            self.signals[i][c.RIGHT_EXIT_PLATFORM_BASE_ROUTE].base_route_exit = \
                self.base_routes[i][c.RIGHT_EXIT_PLATFORM_BASE_ROUTE]
            self.signals[i][c.LEFT_EXIT_PLATFORM_BASE_ROUTE].base_route_exit = \
                self.base_routes[i][c.LEFT_EXIT_PLATFORM_BASE_ROUTE]

        # fill opened and busy route lists for signals
        for i in range(1, c.tracks_ready + 1):
            # for every platform signal, opened list includes exit base route
            # which begins behind the signal
            self.signals[i][c.RIGHT_EXIT_PLATFORM_BASE_ROUTE].base_route_opened_list \
                .append(self.base_routes[i][c.RIGHT_EXIT_BASE_ROUTE])
            self.signals[i][c.LEFT_EXIT_PLATFORM_BASE_ROUTE].base_route_opened_list \
                .append(self.base_routes[i][c.LEFT_EXIT_BASE_ROUTE])
            # for every platform signal, busy list includes all exit base routes
            # located on the same side
            for q in range(1, c.tracks_ready + 1):
                self.signals[i][c.RIGHT_EXIT_PLATFORM_BASE_ROUTE].base_route_busy_list \
                    .append(self.base_routes[q][c.RIGHT_EXIT_BASE_ROUTE])
                self.signals[i][c.LEFT_EXIT_PLATFORM_BASE_ROUTE].base_route_busy_list \
                    .append(self.base_routes[q][c.LEFT_EXIT_BASE_ROUTE])

            # for main entry signals, opened list includes all entry base routes
            self.signals[0][c.LEFT_ENTRY_BASE_ROUTE].base_route_opened_list \
                .append(self.base_routes[i][c.LEFT_ENTRY_BASE_ROUTE])
            self.signals[0][c.RIGHT_ENTRY_BASE_ROUTE].base_route_opened_list \
                .append(self.base_routes[i][c.RIGHT_ENTRY_BASE_ROUTE])
            # for main entry signals, busy list includes all entry base routes too
            self.signals[0][c.LEFT_ENTRY_BASE_ROUTE].base_route_busy_list \
                .append(self.base_routes[i][c.LEFT_ENTRY_BASE_ROUTE])
            self.signals[0][c.RIGHT_ENTRY_BASE_ROUTE].base_route_busy_list \
                .append(self.base_routes[i][c.RIGHT_ENTRY_BASE_ROUTE])
            # so far odd and even routes block each other,
            # it is a known limitation for now and should not be removed
            self.signals[0][c.RIGHT_ENTRY_BASE_ROUTE].base_route_busy_list \
                .append(self.base_routes[i][c.RIGHT_EXIT_BASE_ROUTE])
            self.signals[0][c.LEFT_ENTRY_BASE_ROUTE].base_route_busy_list \
                .append(self.base_routes[i][c.LEFT_EXIT_BASE_ROUTE])

        # ------ TRAIN ROUTES AND TRACKS ------
        # create basic entry train routes for trains which cannot find available track
        base_routes_in_train_route = [self.base_routes[0]['{}_base_route'.format(c.ENTRY_TRAIN_ROUTE[c.LEFT])]]
        self.train_routes[0][c.APPROACHING_TRAIN_ROUTE[c.LEFT]] = \
            TrainRoute(base_routes_in_train_route, 0, c.APPROACHING_TRAIN_ROUTE[c.LEFT])
        base_routes_in_train_route = [self.base_routes[0]['{}_base_route'.format(c.ENTRY_TRAIN_ROUTE[c.RIGHT])]]
        self.train_routes[0][c.APPROACHING_TRAIN_ROUTE[c.RIGHT]] = \
            TrainRoute(base_routes_in_train_route, 0, c.APPROACHING_TRAIN_ROUTE[c.RIGHT])

        for i in range(1, c.tracks_ready + 1):
            self.train_routes.append({})
            # create track object
            # it includes all 4 base routes
            base_routes_in_track = [self.base_routes[i][c.LEFT_ENTRY_PLATFORM_BASE_ROUTE],
                                    self.base_routes[i][c.RIGHT_ENTRY_PLATFORM_BASE_ROUTE],
                                    self.base_routes[i][c.LEFT_EXIT_PLATFORM_BASE_ROUTE],
                                    self.base_routes[i][c.RIGHT_EXIT_PLATFORM_BASE_ROUTE]]
            new_track = Track()
            new_track.base_routes = base_routes_in_track
            self.tracks.append(new_track)
            # create entry train route
            # it includes main entry base route, specific entry base route and platform base route
            for k in c.ENTRY_TRAIN_ROUTE:
                base_routes_in_train_route = [
                    self.base_routes[0]['{}_base_route'.format(c.ENTRY_TRAIN_ROUTE[k])],
                    self.base_routes[i]['{}_base_route'.format(c.ENTRY_TRAIN_ROUTE[k])],
                    self.base_routes[i]['{}_platform_base_route'.format(c.ENTRY_TRAIN_ROUTE[k])]]

                self.train_routes[i][c.ENTRY_TRAIN_ROUTE[k]] = \
                    TrainRoute(base_routes_in_train_route, i, c.ENTRY_TRAIN_ROUTE[k])

            # create exit train route
            # it includes platform base route, specific exit base route and main exit base route
            for m in c.EXIT_TRAIN_ROUTE:
                base_routes_in_train_route = [
                    self.base_routes[i]['{}_platform_base_route'.format(c.EXIT_TRAIN_ROUTE[m])],
                    self.base_routes[i]['{}_base_route'.format(c.EXIT_TRAIN_ROUTE[m])],
                    self.base_routes[0]['{}_base_route'.format(c.EXIT_TRAIN_ROUTE[m])]]

                self.train_routes[i][c.EXIT_TRAIN_ROUTE[m]] = \
                    TrainRoute(base_routes_in_train_route, i, c.EXIT_TRAIN_ROUTE[m])

        # ------ SORT THIS OUT ------
        # base routes and signals are added to generic objects list
        for i in range(c.tracks_ready + 1):
            for n in self.base_routes[i].keys():
                self.objects.append(self.base_routes[i][n])

            for n in self.signals[i].keys():
                self.objects.append(self.signals[i][n])

        # train routes and tracks are added to dispatcher which we create right now
        train_dispatcher = Dispatcher()
        for i in range(c.tracks_ready + 1):
            train_dispatcher.train_routes.append({})
            for p in self.train_routes[i].keys():
                train_dispatcher.train_routes[i].update({p: self.train_routes[i][p]})

        for i in range(c.tracks_ready):
            train_dispatcher.tracks.append(self.tracks[i])

        # now we add dispatcher itself to generic objects list
        self.objects.append(train_dispatcher)

    def handle_mouse_drag(self, event_type, pos):
        movement = pygame.mouse.get_rel()
        if event_type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            # if left mouse button is pressed and user moves mouse, we move entire map with all its content
            self.base_offset = (self.base_offset[0] + movement[0], self.base_offset[1] + movement[1])
            # but not beyond limits
            if self.base_offset[0] > c.base_offset_lower_right_limit[0]:
                self.base_offset = (c.base_offset_lower_right_limit[0], self.base_offset[1])
            if self.base_offset[0] < c.base_offset_upper_left_limit[0]:
                self.base_offset = (c.base_offset_upper_left_limit[0], self.base_offset[1])
            if self.base_offset[1] > c.base_offset_lower_right_limit[1]:
                self.base_offset = (self.base_offset[0], c.base_offset_lower_right_limit[1])
            if self.base_offset[1] < c.base_offset_upper_left_limit[1]:
                self.base_offset = (self.base_offset[0], c.base_offset_upper_left_limit[1])


def main():
    RSSim().run()


if __name__ == '__main__':
    main()
