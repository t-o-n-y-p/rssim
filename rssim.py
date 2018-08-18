import logging

import pygame

import config as c
from base_route import BaseRoute
from bgimg import BgImg
from dispatcher import Dispatcher
from game import Game
from signal import Signal
from track import Track
from train_route import TrainRoute
from button import Button
from bottom_bar import BottomBar
from ingame_time import InGameTime
from onboarding_tips import OnboardingTips
from railroad_switch import RailroadSwitch
from crossover import Crossover


class RSSim(Game):
    def __init__(self):
        super().__init__('Railway Station Simulator', c.screen_resolution, c.frame_rate, c.base_offset)
        self.base_routes = [{}]
        self.signals = [{}]
        self.train_routes = [{}]
        self.junctions = {}
        self.tracks = []
        self.dispatcher = None
        # we create background image object first to be drawn first
        self.create_bg_img()
        # we create routes, signals and dispatcher and link them to each other correctly
        self.create_infrastructure()
        self.saved_onboarding_tip = None
        self.create_onboarding_tips()
        self.create_buttons()
        # this allows user to drag map
        self.mouse_handlers.append(self.handle_mouse_drag)

    def create_bg_img(self):
        background_image = BgImg(c.background_image)
        self.logger.info('background image object created')
        self.objects.append(background_image)
        self.logger.info('background image object appended')

    def create_infrastructure(self):
        # ------ BASE ROUTES AND SIGNALS ------
        # create main entry and main exit base routes and signals for them
        for j in (c.LEFT_ENTRY_BASE_ROUTE, c.LEFT_EXIT_BASE_ROUTE, c.RIGHT_ENTRY_BASE_ROUTE, c.RIGHT_EXIT_BASE_ROUTE):
            self.base_routes[0][j] = BaseRoute(0, j)
            self.base_routes[0][j].read_trail_points()
            placement = self.base_routes[0][j].route_config['exit_signal_placement']
            flip_needed = self.base_routes[0][j].route_config['flip_needed']
            invisible = self.base_routes[0][j].route_config['invisible_signal']
            if placement is not None:
                self.signals[0][j] = Signal(placement, flip_needed, invisible, 0, j)
                self.signals[0][j].read_state()

        self.logger.info('track 0 base routes and signals created')
        for j in (c.LEFT_ENTRY_BASE_ROUTE, c.LEFT_EXIT_BASE_ROUTE, c.RIGHT_ENTRY_BASE_ROUTE, c.RIGHT_EXIT_BASE_ROUTE):
            # associate main entry/exit base route with its signal
            self.base_routes[0][j].route_config['exit_signal'] = self.signals[0][j]
            # for every signal, exit route is the route which ends with this signal
            self.signals[0][j].base_route_exit = self.base_routes[0][j]

        self.logger.info('track 0 base routes and signals associated')
        # create all other base routes and signals for platform routes
        for i in range(1, c.tracks_ready + 1):
            self.base_routes.append({})
            self.signals.append({})
            for k in (c.LEFT_ENTRY_BASE_ROUTE, c.LEFT_EXIT_BASE_ROUTE,
                      c.RIGHT_ENTRY_BASE_ROUTE, c.RIGHT_EXIT_BASE_ROUTE,
                      c.LEFT_ENTRY_PLATFORM_BASE_ROUTE, c.RIGHT_ENTRY_PLATFORM_BASE_ROUTE,
                      c.RIGHT_EXIT_PLATFORM_BASE_ROUTE, c.LEFT_EXIT_PLATFORM_BASE_ROUTE):
                self.base_routes[i][k] = BaseRoute(i, k)
                if k in (c.LEFT_ENTRY_PLATFORM_BASE_ROUTE, c.RIGHT_ENTRY_PLATFORM_BASE_ROUTE,
                         c.RIGHT_EXIT_PLATFORM_BASE_ROUTE, c.LEFT_EXIT_PLATFORM_BASE_ROUTE):
                    self.base_routes[i][k].read_trail_points()
                placement = self.base_routes[i][k].route_config['exit_signal_placement']
                flip_needed = self.base_routes[i][k].route_config['flip_needed']
                invisible = self.base_routes[i][k].route_config['invisible_signal']
                if placement is not None and k in (c.RIGHT_EXIT_PLATFORM_BASE_ROUTE, c.LEFT_EXIT_PLATFORM_BASE_ROUTE):
                    self.signals[i][k] = Signal(placement, flip_needed, invisible, i, k)
                    self.signals[i][k].read_state()

        self.junctions[1] = {}
        self.junctions[1][2] = {}
        self.junctions[1][2][c.RIGHT_ENTRY_CROSSOVER] = Crossover(1, 2, c.RIGHT_ENTRY_CROSSOVER)
        self.junctions[1][2][c.RIGHT_EXIT_CROSSOVER] = Crossover(1, 2, c.RIGHT_EXIT_CROSSOVER)
        self.junctions[1][21] = {}
        self.junctions[1][21][c.LEFT_ENTRY_RAILROAD_SWITCH] = RailroadSwitch(1, 21, c.LEFT_ENTRY_RAILROAD_SWITCH)
        self.junctions[1][21][c.LEFT_EXIT_RAILROAD_SWITCH] = RailroadSwitch(1, 21, c.LEFT_EXIT_RAILROAD_SWITCH)
        self.junctions[1][29] = {}
        self.junctions[1][29][c.RIGHT_ENTRY_RAILROAD_SWITCH] = RailroadSwitch(1, 29, c.RIGHT_ENTRY_RAILROAD_SWITCH)
        self.junctions[1][29][c.RIGHT_EXIT_RAILROAD_SWITCH] = RailroadSwitch(1, 29, c.RIGHT_EXIT_RAILROAD_SWITCH)

        self.junctions[2] = {}
        self.junctions[2][1] = {}
        self.junctions[2][1][c.LEFT_ENTRY_CROSSOVER] = Crossover(2, 1, c.LEFT_ENTRY_CROSSOVER)
        self.junctions[2][1][c.LEFT_EXIT_CROSSOVER] = Crossover(2, 1, c.LEFT_EXIT_CROSSOVER)
        self.junctions[2][22] = {}
        self.junctions[2][22][c.RIGHT_ENTRY_RAILROAD_SWITCH] = RailroadSwitch(2, 22, c.RIGHT_ENTRY_RAILROAD_SWITCH)
        self.junctions[2][22][c.RIGHT_EXIT_RAILROAD_SWITCH] = RailroadSwitch(2, 22, c.RIGHT_EXIT_RAILROAD_SWITCH)
        self.junctions[2][30] = {}
        self.junctions[2][30][c.LEFT_ENTRY_RAILROAD_SWITCH] = RailroadSwitch(2, 30, c.LEFT_ENTRY_RAILROAD_SWITCH)
        self.junctions[2][30][c.LEFT_EXIT_RAILROAD_SWITCH] = RailroadSwitch(2, 30, c.LEFT_EXIT_RAILROAD_SWITCH)

        self.junctions[21] = {}
        self.junctions[21][3] = {}
        self.junctions[21][3][c.LEFT_ENTRY_RAILROAD_SWITCH] = RailroadSwitch(21, 3, c.LEFT_ENTRY_RAILROAD_SWITCH)
        self.junctions[21][3][c.LEFT_EXIT_RAILROAD_SWITCH] = RailroadSwitch(21, 3, c.LEFT_EXIT_RAILROAD_SWITCH)

        self.junctions[22] = {}
        self.junctions[22][4] = {}
        self.junctions[22][4][c.RIGHT_ENTRY_RAILROAD_SWITCH] = RailroadSwitch(22, 4, c.RIGHT_ENTRY_RAILROAD_SWITCH)
        self.junctions[22][4][c.RIGHT_EXIT_RAILROAD_SWITCH] = RailroadSwitch(22, 4, c.RIGHT_EXIT_RAILROAD_SWITCH)

        self.junctions[29] = {}
        self.junctions[29][3] = {}
        self.junctions[29][3][c.RIGHT_ENTRY_RAILROAD_SWITCH] = RailroadSwitch(29, 3, c.RIGHT_ENTRY_RAILROAD_SWITCH)
        self.junctions[29][3][c.RIGHT_EXIT_RAILROAD_SWITCH] = RailroadSwitch(29, 3, c.RIGHT_EXIT_RAILROAD_SWITCH)

        self.junctions[30] = {}
        self.junctions[30][4] = {}
        self.junctions[30][4][c.LEFT_ENTRY_RAILROAD_SWITCH] = RailroadSwitch(30, 4, c.LEFT_ENTRY_RAILROAD_SWITCH)
        self.junctions[30][4][c.LEFT_EXIT_RAILROAD_SWITCH] = RailroadSwitch(30, 4, c.LEFT_EXIT_RAILROAD_SWITCH)

        self.junctions[1][2][c.RIGHT_ENTRY_CROSSOVER].dependency = self.junctions[1][2][c.RIGHT_EXIT_CROSSOVER]
        self.junctions[1][2][c.RIGHT_EXIT_CROSSOVER].dependency = self.junctions[1][2][c.RIGHT_ENTRY_CROSSOVER]
        self.junctions[1][21][c.LEFT_ENTRY_RAILROAD_SWITCH].dependency \
            = self.junctions[1][21][c.LEFT_EXIT_RAILROAD_SWITCH]
        self.junctions[1][21][c.LEFT_EXIT_RAILROAD_SWITCH].dependency \
            = self.junctions[1][21][c.LEFT_ENTRY_RAILROAD_SWITCH]
        self.junctions[1][29][c.RIGHT_ENTRY_RAILROAD_SWITCH].dependency \
            = self.junctions[1][29][c.RIGHT_EXIT_RAILROAD_SWITCH]
        self.junctions[1][29][c.RIGHT_EXIT_RAILROAD_SWITCH].dependency \
            = self.junctions[1][29][c.RIGHT_ENTRY_RAILROAD_SWITCH]

        self.junctions[2][1][c.LEFT_ENTRY_CROSSOVER].dependency = self.junctions[2][1][c.LEFT_EXIT_CROSSOVER]
        self.junctions[2][1][c.LEFT_EXIT_CROSSOVER].dependency = self.junctions[2][1][c.LEFT_ENTRY_CROSSOVER]

        for i in self.junctions:
            for j in self.junctions[i]:
                for k in self.junctions[i][j]:
                    if k == c.LEFT_ENTRY_RAILROAD_SWITCH:
                        self.junctions[i][j][k].dependency = self.junctions[i][j][c.LEFT_EXIT_RAILROAD_SWITCH]
                    elif k == c.LEFT_EXIT_RAILROAD_SWITCH:
                        self.junctions[i][j][k].dependency = self.junctions[i][j][c.LEFT_ENTRY_RAILROAD_SWITCH]
                    elif k == c.RIGHT_ENTRY_RAILROAD_SWITCH:
                        self.junctions[i][j][k].dependency = self.junctions[i][j][c.RIGHT_EXIT_RAILROAD_SWITCH]
                    elif k == c.RIGHT_EXIT_RAILROAD_SWITCH:
                        self.junctions[i][j][k].dependency = self.junctions[i][j][c.RIGHT_ENTRY_RAILROAD_SWITCH]

        self.base_routes[1][c.LEFT_ENTRY_BASE_ROUTE].junctions.append(self.junctions[2][1][c.LEFT_ENTRY_CROSSOVER])
        self.base_routes[1][c.LEFT_ENTRY_BASE_ROUTE].junction_position.append([2, 1])
        self.base_routes[1][c.LEFT_ENTRY_BASE_ROUTE].junctions\
            .append(self.junctions[1][21][c.LEFT_ENTRY_RAILROAD_SWITCH])
        self.base_routes[1][c.LEFT_ENTRY_BASE_ROUTE].junction_position.append(1)

        self.base_routes[1][c.RIGHT_ENTRY_BASE_ROUTE].junctions.append(self.junctions[1][2][c.RIGHT_ENTRY_CROSSOVER])
        self.base_routes[1][c.RIGHT_ENTRY_BASE_ROUTE].junction_position.append([1, 1])
        self.base_routes[1][c.RIGHT_ENTRY_BASE_ROUTE].junctions\
            .append(self.junctions[1][29][c.RIGHT_ENTRY_RAILROAD_SWITCH])
        self.base_routes[1][c.RIGHT_ENTRY_BASE_ROUTE].junction_position.append(1)

        self.base_routes[1][c.LEFT_EXIT_BASE_ROUTE].junctions.append(self.junctions[1][21][c.LEFT_EXIT_RAILROAD_SWITCH])
        self.base_routes[1][c.LEFT_EXIT_BASE_ROUTE].junction_position.append(1)
        self.base_routes[1][c.LEFT_EXIT_BASE_ROUTE].junctions.append(self.junctions[2][1][c.LEFT_EXIT_CROSSOVER])
        self.base_routes[1][c.LEFT_EXIT_BASE_ROUTE].junction_position.append([1, 1])

        self.base_routes[1][c.RIGHT_EXIT_BASE_ROUTE].junctions\
            .append(self.junctions[1][29][c.RIGHT_EXIT_RAILROAD_SWITCH])
        self.base_routes[1][c.RIGHT_EXIT_BASE_ROUTE].junction_position.append(1)
        self.base_routes[1][c.RIGHT_EXIT_BASE_ROUTE].junctions.append(self.junctions[1][2][c.RIGHT_EXIT_CROSSOVER])
        self.base_routes[1][c.RIGHT_EXIT_BASE_ROUTE].junction_position.append([1, 2])

        self.base_routes[3][c.LEFT_ENTRY_BASE_ROUTE].junctions.append(self.junctions[2][1][c.LEFT_ENTRY_CROSSOVER])
        self.base_routes[3][c.LEFT_ENTRY_BASE_ROUTE].junction_position.append([2, 1])
        self.base_routes[3][c.LEFT_ENTRY_BASE_ROUTE].junctions\
            .append(self.junctions[1][21][c.LEFT_ENTRY_RAILROAD_SWITCH])
        self.base_routes[3][c.LEFT_ENTRY_BASE_ROUTE].junction_position.append(21)
        self.base_routes[3][c.LEFT_ENTRY_BASE_ROUTE].junctions\
            .append(self.junctions[21][3][c.LEFT_ENTRY_RAILROAD_SWITCH])
        self.base_routes[3][c.LEFT_ENTRY_BASE_ROUTE].junction_position.append(3)

        self.base_routes[3][c.RIGHT_ENTRY_BASE_ROUTE].junctions.append(self.junctions[1][2][c.RIGHT_ENTRY_CROSSOVER])
        self.base_routes[3][c.RIGHT_ENTRY_BASE_ROUTE].junction_position.append([1, 1])
        self.base_routes[3][c.RIGHT_ENTRY_BASE_ROUTE].junctions\
            .append(self.junctions[1][29][c.RIGHT_ENTRY_RAILROAD_SWITCH])
        self.base_routes[3][c.RIGHT_ENTRY_BASE_ROUTE].junction_position.append(29)
        self.base_routes[3][c.RIGHT_ENTRY_BASE_ROUTE].junctions\
            .append(self.junctions[29][3][c.RIGHT_ENTRY_RAILROAD_SWITCH])
        self.base_routes[3][c.RIGHT_ENTRY_BASE_ROUTE].junction_position.append(3)

        self.base_routes[3][c.LEFT_EXIT_BASE_ROUTE].junctions\
            .append(self.junctions[21][3][c.LEFT_EXIT_RAILROAD_SWITCH])
        self.base_routes[3][c.LEFT_EXIT_BASE_ROUTE].junction_position.append(3)
        self.base_routes[3][c.LEFT_EXIT_BASE_ROUTE].junctions\
            .append(self.junctions[1][21][c.LEFT_EXIT_RAILROAD_SWITCH])
        self.base_routes[3][c.LEFT_EXIT_BASE_ROUTE].junction_position.append(21)
        self.base_routes[3][c.LEFT_EXIT_BASE_ROUTE].junctions.append(self.junctions[2][1][c.LEFT_EXIT_CROSSOVER])
        self.base_routes[3][c.LEFT_EXIT_BASE_ROUTE].junction_position.append([1, 1])

        self.base_routes[3][c.RIGHT_EXIT_BASE_ROUTE].junctions\
            .append(self.junctions[29][3][c.RIGHT_EXIT_RAILROAD_SWITCH])
        self.base_routes[3][c.RIGHT_EXIT_BASE_ROUTE].junction_position.append(3)
        self.base_routes[3][c.RIGHT_EXIT_BASE_ROUTE].junctions\
            .append(self.junctions[1][29][c.RIGHT_EXIT_RAILROAD_SWITCH])
        self.base_routes[3][c.RIGHT_EXIT_BASE_ROUTE].junction_position.append(29)
        self.base_routes[3][c.RIGHT_EXIT_BASE_ROUTE].junctions.append(self.junctions[1][2][c.RIGHT_EXIT_CROSSOVER])
        self.base_routes[3][c.RIGHT_EXIT_BASE_ROUTE].junction_position.append([1, 2])

        for i in range(1, c.tracks_ready + 1, 2):
            self.base_routes[i][c.LEFT_ENTRY_BASE_ROUTE].read_trail_points()
            self.base_routes[i][c.LEFT_EXIT_BASE_ROUTE].read_trail_points()
            self.base_routes[i][c.RIGHT_ENTRY_BASE_ROUTE].read_trail_points()
            self.base_routes[i][c.RIGHT_EXIT_BASE_ROUTE].read_trail_points()

        self.base_routes[2][c.LEFT_ENTRY_BASE_ROUTE].junctions.append(self.junctions[2][1][c.LEFT_ENTRY_CROSSOVER])
        self.base_routes[2][c.LEFT_ENTRY_BASE_ROUTE].junction_position.append([2, 2])
        self.base_routes[2][c.LEFT_ENTRY_BASE_ROUTE].junctions\
            .append(self.junctions[2][30][c.LEFT_ENTRY_RAILROAD_SWITCH])
        self.base_routes[2][c.LEFT_ENTRY_BASE_ROUTE].junction_position.append(2)

        self.base_routes[2][c.RIGHT_ENTRY_BASE_ROUTE].junctions.append(self.junctions[1][2][c.RIGHT_ENTRY_CROSSOVER])
        self.base_routes[2][c.RIGHT_ENTRY_BASE_ROUTE].junction_position.append([1, 2])
        self.base_routes[2][c.RIGHT_ENTRY_BASE_ROUTE].junctions\
            .append(self.junctions[2][22][c.RIGHT_ENTRY_RAILROAD_SWITCH])
        self.base_routes[2][c.RIGHT_ENTRY_BASE_ROUTE].junction_position.append(2)

        self.base_routes[2][c.LEFT_EXIT_BASE_ROUTE].junctions\
            .append(self.junctions[2][30][c.LEFT_EXIT_RAILROAD_SWITCH])
        self.base_routes[2][c.LEFT_EXIT_BASE_ROUTE].junction_position.append(2)
        self.base_routes[2][c.LEFT_EXIT_BASE_ROUTE].junctions.append(self.junctions[2][1][c.LEFT_EXIT_CROSSOVER])
        self.base_routes[2][c.LEFT_EXIT_BASE_ROUTE].junction_position.append([2, 1])

        self.base_routes[2][c.RIGHT_EXIT_BASE_ROUTE].junctions\
            .append(self.junctions[2][22][c.RIGHT_EXIT_RAILROAD_SWITCH])
        self.base_routes[2][c.RIGHT_EXIT_BASE_ROUTE].junction_position.append(2)
        self.base_routes[2][c.RIGHT_EXIT_BASE_ROUTE].junctions.append(self.junctions[1][2][c.RIGHT_EXIT_CROSSOVER])
        self.base_routes[2][c.RIGHT_EXIT_BASE_ROUTE].junction_position.append([2, 2])

        self.base_routes[4][c.LEFT_ENTRY_BASE_ROUTE].junctions.append(self.junctions[2][1][c.LEFT_ENTRY_CROSSOVER])
        self.base_routes[4][c.LEFT_ENTRY_BASE_ROUTE].junction_position.append([2, 2])
        self.base_routes[4][c.LEFT_ENTRY_BASE_ROUTE].junctions\
            .append(self.junctions[2][30][c.LEFT_ENTRY_RAILROAD_SWITCH])
        self.base_routes[4][c.LEFT_ENTRY_BASE_ROUTE].junction_position.append(30)
        self.base_routes[4][c.LEFT_ENTRY_BASE_ROUTE].junctions\
            .append(self.junctions[30][4][c.LEFT_ENTRY_RAILROAD_SWITCH])
        self.base_routes[4][c.LEFT_ENTRY_BASE_ROUTE].junction_position.append(4)

        self.base_routes[4][c.RIGHT_ENTRY_BASE_ROUTE].junctions.append(self.junctions[1][2][c.RIGHT_ENTRY_CROSSOVER])
        self.base_routes[4][c.RIGHT_ENTRY_BASE_ROUTE].junction_position.append([1, 2])
        self.base_routes[4][c.RIGHT_ENTRY_BASE_ROUTE].junctions\
            .append(self.junctions[2][22][c.RIGHT_ENTRY_RAILROAD_SWITCH])
        self.base_routes[4][c.RIGHT_ENTRY_BASE_ROUTE].junction_position.append(22)
        self.base_routes[4][c.RIGHT_ENTRY_BASE_ROUTE].junctions\
            .append(self.junctions[22][4][c.RIGHT_ENTRY_RAILROAD_SWITCH])
        self.base_routes[4][c.RIGHT_ENTRY_BASE_ROUTE].junction_position.append(4)

        self.base_routes[4][c.LEFT_EXIT_BASE_ROUTE].junctions\
            .append(self.junctions[30][4][c.LEFT_EXIT_RAILROAD_SWITCH])
        self.base_routes[4][c.LEFT_EXIT_BASE_ROUTE].junction_position.append(4)
        self.base_routes[4][c.LEFT_EXIT_BASE_ROUTE].junctions\
            .append(self.junctions[2][30][c.LEFT_EXIT_RAILROAD_SWITCH])
        self.base_routes[4][c.LEFT_EXIT_BASE_ROUTE].junction_position.append(30)
        self.base_routes[4][c.LEFT_EXIT_BASE_ROUTE].junctions.append(self.junctions[2][1][c.LEFT_EXIT_CROSSOVER])
        self.base_routes[4][c.LEFT_EXIT_BASE_ROUTE].junction_position.append([2, 1])

        self.base_routes[4][c.RIGHT_EXIT_BASE_ROUTE].junctions\
            .append(self.junctions[22][4][c.RIGHT_EXIT_RAILROAD_SWITCH])
        self.base_routes[4][c.RIGHT_EXIT_BASE_ROUTE].junction_position.append(4)
        self.base_routes[4][c.RIGHT_EXIT_BASE_ROUTE].junctions\
            .append(self.junctions[2][22][c.RIGHT_EXIT_RAILROAD_SWITCH])
        self.base_routes[4][c.RIGHT_EXIT_BASE_ROUTE].junction_position.append(22)
        self.base_routes[4][c.RIGHT_EXIT_BASE_ROUTE].junctions.append(self.junctions[1][2][c.RIGHT_EXIT_CROSSOVER])
        self.base_routes[4][c.RIGHT_EXIT_BASE_ROUTE].junction_position.append([2, 2])

        for i in range(2, c.tracks_ready + 1, 2):
            self.base_routes[i][c.LEFT_ENTRY_BASE_ROUTE].read_trail_points()
            self.base_routes[i][c.LEFT_EXIT_BASE_ROUTE].read_trail_points()
            self.base_routes[i][c.RIGHT_ENTRY_BASE_ROUTE].read_trail_points()
            self.base_routes[i][c.RIGHT_EXIT_BASE_ROUTE].read_trail_points()

            self.logger.info('track {} base routes and signals created'.format(i))

        for i in range(1, c.tracks_ready + 1):
            # associate platform base route with its signal
            self.base_routes[i][c.RIGHT_EXIT_PLATFORM_BASE_ROUTE].route_config['exit_signal'] = \
                self.signals[i][c.RIGHT_EXIT_PLATFORM_BASE_ROUTE]
            self.base_routes[i][c.LEFT_ENTRY_PLATFORM_BASE_ROUTE].route_config['exit_signal'] = \
                self.signals[i][c.RIGHT_EXIT_PLATFORM_BASE_ROUTE]
            self.base_routes[i][c.LEFT_EXIT_PLATFORM_BASE_ROUTE].route_config['exit_signal'] = \
                self.signals[i][c.LEFT_EXIT_PLATFORM_BASE_ROUTE]
            self.base_routes[i][c.RIGHT_ENTRY_PLATFORM_BASE_ROUTE].route_config['exit_signal'] = \
                self.signals[i][c.LEFT_EXIT_PLATFORM_BASE_ROUTE]
            # for every signal, exit route is the route which ends with this signal
            self.signals[i][c.RIGHT_EXIT_PLATFORM_BASE_ROUTE].base_route_exit = \
                self.base_routes[i][c.RIGHT_EXIT_PLATFORM_BASE_ROUTE]
            self.signals[i][c.LEFT_EXIT_PLATFORM_BASE_ROUTE].base_route_exit = \
                self.base_routes[i][c.LEFT_EXIT_PLATFORM_BASE_ROUTE]
            self.logger.info('track {} base routes and signals associated'.format(i))

        # fill opened and busy route lists for signals
        for i in range(1, c.tracks_ready + 1):
            # for every platform signal, opened list includes exit base route
            # which begins behind the signal
            self.signals[i][c.RIGHT_EXIT_PLATFORM_BASE_ROUTE].base_route_opened_list \
                .append(self.base_routes[i][c.RIGHT_EXIT_BASE_ROUTE])
            self.signals[i][c.LEFT_EXIT_PLATFORM_BASE_ROUTE].base_route_opened_list \
                .append(self.base_routes[i][c.LEFT_EXIT_BASE_ROUTE])
            self.logger.info('opened list set up for track {} signals'.format(i))

            # for main entry signals, opened list includes all entry base routes
            self.signals[0][c.LEFT_ENTRY_BASE_ROUTE].base_route_opened_list \
                .append(self.base_routes[i][c.LEFT_ENTRY_BASE_ROUTE])
            self.signals[0][c.RIGHT_ENTRY_BASE_ROUTE].base_route_opened_list \
                .append(self.base_routes[i][c.RIGHT_ENTRY_BASE_ROUTE])

        self.logger.info('opened list set up for track 0 signals')

        # ------ TRAIN ROUTES AND TRACKS ------
        # create basic entry train routes for trains which cannot find available track
        base_routes_in_train_route = [self.base_routes[0]['{}_base_route'.format(c.ENTRY_TRAIN_ROUTE[c.LEFT])]]
        self.train_routes[0][c.APPROACHING_TRAIN_ROUTE[c.LEFT]] = \
            TrainRoute(base_routes_in_train_route, 0, c.APPROACHING_TRAIN_ROUTE[c.LEFT])
        base_routes_in_train_route = [self.base_routes[0]['{}_base_route'.format(c.ENTRY_TRAIN_ROUTE[c.RIGHT])]]
        self.train_routes[0][c.APPROACHING_TRAIN_ROUTE[c.RIGHT]] = \
            TrainRoute(base_routes_in_train_route, 0, c.APPROACHING_TRAIN_ROUTE[c.RIGHT])
        self.logger.info('approaching train routes created')

        for i in range(1, c.tracks_ready + 1):
            self.train_routes.append({})
            # create track object
            # it includes all 4 base routes
            base_routes_in_track = [self.base_routes[i][c.LEFT_ENTRY_PLATFORM_BASE_ROUTE],
                                    self.base_routes[i][c.RIGHT_ENTRY_PLATFORM_BASE_ROUTE],
                                    self.base_routes[i][c.LEFT_EXIT_PLATFORM_BASE_ROUTE],
                                    self.base_routes[i][c.RIGHT_EXIT_PLATFORM_BASE_ROUTE]]
            new_track = Track(i, base_routes_in_track)
            self.tracks.append(new_track)
            self.logger.info('track {} created'.format(i))
            # create entry train route
            # it includes main entry base route, specific entry base route and platform base route
            for k in c.ENTRY_TRAIN_ROUTE:
                base_routes_in_train_route = [
                    self.base_routes[0]['{}_base_route'.format(c.ENTRY_TRAIN_ROUTE[k])],
                    self.base_routes[i]['{}_base_route'.format(c.ENTRY_TRAIN_ROUTE[k])],
                    self.base_routes[i]['{}_platform_base_route'.format(c.ENTRY_TRAIN_ROUTE[k])]]

                self.train_routes[i][c.ENTRY_TRAIN_ROUTE[k]] = \
                    TrainRoute(base_routes_in_train_route, i, c.ENTRY_TRAIN_ROUTE[k])
                self.logger.info('track {} {} train route created'.format(i, k))

            # create exit train route
            # it includes platform base route, specific exit base route and main exit base route
            for m in c.EXIT_TRAIN_ROUTE:
                base_routes_in_train_route = [
                    self.base_routes[i]['{}_platform_base_route'.format(c.EXIT_TRAIN_ROUTE[m])],
                    self.base_routes[i]['{}_base_route'.format(c.EXIT_TRAIN_ROUTE[m])],
                    self.base_routes[0]['{}_base_route'.format(c.EXIT_TRAIN_ROUTE[m])]]

                self.train_routes[i][c.EXIT_TRAIN_ROUTE[m]] = \
                    TrainRoute(base_routes_in_train_route, i, c.EXIT_TRAIN_ROUTE[m])
                self.logger.info('track {} {} train route created'.format(i, m))

        # ------ SORT THIS OUT ------
        # base routes and signals are added to generic objects list
        for i in self.junctions:
            for j in self.junctions[i]:
                for k in self.junctions[i][j]:
                    self.objects.append(self.junctions[i][j][k])

        for i in range(c.tracks_ready + 1):
            for n in self.base_routes[i]:
                self.objects.append(self.base_routes[i][n])

        for i in range(c.tracks_ready + 1):
            for n in self.signals[i]:
                self.objects.append(self.signals[i][n])

        self.logger.info('base routes and signals appended')
        # train routes and tracks are added to dispatcher which we create right now
        self.dispatcher = Dispatcher()
        self.logger.info('dispatcher created')
        for i in range(c.tracks_ready + 1):
            self.dispatcher.train_routes.append({})
            for p in self.train_routes[i].keys():
                self.dispatcher.train_routes[i].update({p: self.train_routes[i][p]})

        self.logger.info('train routes appended to dispatcher')
        for i in range(c.tracks_ready):
            self.dispatcher.tracks.append(self.tracks[i])

        self.logger.info('tracks appended to dispatcher')
        # now we add dispatcher itself to generic objects list
        self.dispatcher.read_state()
        self.objects.append(self.dispatcher)
        self.logger.info('dispatcher appended')

    def create_onboarding_tips(self):
        self.saved_onboarding_tip = OnboardingTips('img/game_saved.png')
        self.objects.append(self.saved_onboarding_tip)

    def create_buttons(self):

        def pause_game(button):
            self.game_paused = True

        def resume_game(button):
            self.game_paused = False

        def save_game(button):
            for i in self.objects:
                i.save_state()

            self.saved_onboarding_tip.condition_met = True

        self.objects.append(InGameTime())
        self.objects.append(BottomBar())
        stop_button = Button((890, 555), ['Pause', 'Resume'], [pause_game, resume_game], False)
        save_button = Button((780, 555), ['Save', ], [save_game, ], True)
        self.mouse_handlers.append(stop_button.handle_mouse_event)
        self.mouse_handlers.append(save_button.handle_mouse_event)
        self.objects.append(stop_button)
        self.objects.append(save_button)

    def handle_mouse_drag(self, event_type, pos):
        movement = pygame.mouse.get_rel()
        if event_type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0] and \
                pos[1] < c.screen_resolution[1] - c.bottom_bar_height:
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
