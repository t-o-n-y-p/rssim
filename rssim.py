import sys

import win32api
import win32con
import pyglet

from base_route import BaseRoute
from main_map import MainMap
from exceptions import VideoAdapterNotSupportedException
from dispatcher import Dispatcher
from game import Game
from signal import Signal
from track import Track
from train_route import TrainRoute
from button import Button
from top_and_bottom_bar import TopAndBottomBar
from ingame_time import InGameTime
from onboarding_tips import OnboardingTips
from railroad_switch import RailroadSwitch
from crossover import Crossover


class RSSim(Game):
    def __init__(self):
        super().__init__('Railway Station Simulator')
        self.logger.critical('rssim game created')
        self.logger.debug('------- START INIT -------')
        self.base_routes = [{}]
        self.signals = [{}]
        self.train_routes = [{}]
        self.junctions = {}
        self.tracks = []
        self.dispatcher = None
        # we create background image object first to be drawn first
        try:
            self.create_main_map()
        except VideoAdapterNotSupportedException as e:
            e.surface = self.surface
            raise e
        # we create routes, signals and dispatcher and link them to each other correctly
        self.create_infrastructure()
        self.saved_onboarding_tip = None
        self.create_onboarding_tips()
        self.create_buttons()
        self.logger.debug('map drag event appended')
        self.logger.debug('------- END INIT -------')
        self.logger.warning('rssim game init completed')

    def create_main_map(self):
        self.logger.debug('------- START CREATING BG IMAGE -------')
        try:
            self.main_map_tiles = MainMap(batch=self.batch, group=self.map_ordered_group)
        except VideoAdapterNotSupportedException:
            raise VideoAdapterNotSupportedException
        self.logger.info('main map object created')
        self.logger.debug('main map object appended')
        self.logger.debug('------- END CREATING BG IMAGE -------')

    def create_infrastructure(self):
        self.logger.debug('------- START CREATING INFRASTRUCTURE -------')
        # ------ BASE ROUTES AND SIGNALS ------
        # create main entry and main exit base routes and signals for them
        for j in (self.c['base_route_types']['left_entry_base_route'],
                  self.c['base_route_types']['left_exit_base_route'],
                  self.c['base_route_types']['right_entry_base_route'],
                  self.c['base_route_types']['right_exit_base_route']):
            self.base_routes[0][j] = BaseRoute(track_number=0, route_type=j)
            self.base_routes[0][j].read_trail_points()
            placement = self.base_routes[0][j].route_config['exit_signal_placement']
            self.logger.debug('placement = {}'.format(placement))
            flip_needed = self.base_routes[0][j].route_config['flip_needed']
            self.logger.debug('flip_needed = {}'.format(flip_needed))
            invisible = self.base_routes[0][j].route_config['invisible_signal']
            self.logger.debug('invisible = {}'.format(invisible))
            if placement is not None:
                self.signals[0][j] = Signal(placement=placement, flip_needed=flip_needed, invisible=invisible,
                                            track_number=0, route_type=j,
                                            batch=self.batch, signal_group=self.signals_and_trains_ordered_group)

        self.logger.info('track 0 base routes and signals created')
        for j in (self.c['base_route_types']['left_entry_base_route'],
                  self.c['base_route_types']['left_exit_base_route'],
                  self.c['base_route_types']['right_entry_base_route'],
                  self.c['base_route_types']['right_exit_base_route']):
            # associate main entry/exit base route with its signal
            self.base_routes[0][j].route_config['exit_signal'] = self.signals[0][j]
            self.logger.debug('base route {} {} exit signal now is signal {} {}'
                              .format(0, j, 0, j))
            # for every signal, exit route is the route which ends with this signal
            self.signals[0][j].base_route_exit = self.base_routes[0][j]
            self.logger.debug('signal {} {} exit route now is base route {} {}'
                              .format(0, j, 0, j))

        self.logger.info('track 0 base routes and signals associated')
        # create all other base routes and signals for platform routes
        for i in range(1, self.c['dispatcher_config']['tracks_ready'] + 1):
            self.base_routes.append({})
            self.signals.append({})
            if i <= 24:
                for k in (self.c['base_route_types']['left_entry_base_route'],
                          self.c['base_route_types']['left_exit_base_route'],
                          self.c['base_route_types']['right_entry_base_route'],
                          self.c['base_route_types']['right_exit_base_route']):
                    self.base_routes[i][k] = BaseRoute(track_number=i, route_type=k)

            if i >= 21:
                if i % 2 == 1:
                    for k in (self.c['base_route_types']['left_side_entry_base_route'],
                              self.c['base_route_types']['left_side_exit_base_route']):
                        self.base_routes[i][k] = BaseRoute(track_number=i, route_type=k)
                else:
                    for k in (self.c['base_route_types']['right_side_entry_base_route'],
                              self.c['base_route_types']['right_side_exit_base_route']):
                        self.base_routes[i][k] = BaseRoute(track_number=i, route_type=k)

            for k in (self.c['base_route_types']['left_entry_platform_base_route'],
                      self.c['base_route_types']['left_exit_platform_base_route'],
                      self.c['base_route_types']['right_entry_platform_base_route'],
                      self.c['base_route_types']['right_exit_platform_base_route']):
                self.base_routes[i][k] = BaseRoute(track_number=i, route_type=k)
                self.base_routes[i][k].read_trail_points()
                placement = self.base_routes[i][k].route_config['exit_signal_placement']
                self.logger.debug('placement = {}'.format(placement))
                flip_needed = self.base_routes[i][k].route_config['flip_needed']
                self.logger.debug('flip_needed = {}'.format(flip_needed))
                invisible = self.base_routes[i][k].route_config['invisible_signal']
                self.logger.debug('invisible = {}'.format(invisible))
                if placement is not None and k in (self.c['base_route_types']['right_exit_platform_base_route'],
                                                   self.c['base_route_types']['left_exit_platform_base_route']):
                    self.signals[i][k] = Signal(placement=placement, flip_needed=flip_needed, invisible=invisible,
                                                track_number=i, route_type=k, batch=self.batch,
                                                signal_group=self.signals_and_trains_ordered_group)

            self.logger.debug('track {} base routes and signals created'.format(i))

        for i in range(100):
            self.base_routes.append({})
            self.signals.append({})

        for j in (self.c['base_route_types']['left_side_entry_base_route'],
                  self.c['base_route_types']['left_side_exit_base_route'],
                  self.c['base_route_types']['right_side_entry_base_route'],
                  self.c['base_route_types']['right_side_exit_base_route']):
            self.base_routes[100][j] = BaseRoute(track_number=100, route_type=j)
            self.base_routes[100][j].read_trail_points()
            placement = self.base_routes[100][j].route_config['exit_signal_placement']
            self.logger.debug('placement = {}'.format(placement))
            flip_needed = self.base_routes[100][j].route_config['flip_needed']
            self.logger.debug('flip_needed = {}'.format(flip_needed))
            invisible = self.base_routes[100][j].route_config['invisible_signal']
            self.logger.debug('invisible = {}'.format(invisible))
            if placement is not None:
                self.signals[100][j] = Signal(placement=placement, flip_needed=flip_needed, invisible=invisible,
                                              track_number=100, route_type=j,
                                              batch=self.batch, signal_group=self.signals_and_trains_ordered_group)

        for j in (self.c['base_route_types']['left_side_entry_base_route'],
                  self.c['base_route_types']['left_side_exit_base_route'],
                  self.c['base_route_types']['right_side_entry_base_route'],
                  self.c['base_route_types']['right_side_exit_base_route']):
            # associate main entry/exit base route with its signal
            self.base_routes[100][j].route_config['exit_signal'] = self.signals[100][j]
            self.logger.debug('base route {} {} exit signal now is signal {} {}'
                              .format(100, j, 100, j))
            # for every signal, exit route is the route which ends with this signal
            self.signals[100][j].base_route_exit = self.base_routes[100][j]
            self.logger.debug('signal {} {} exit route now is base route {} {}'
                              .format(100, j, 100, j))

        self.logger.info('base routes and signals created for all tracks')

        self.create_junctions()

        self.base_routes[1][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[1][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 1])
        self.base_routes[1][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[1][self.c['base_route_types']['left_entry_base_route']].junction_position.append(1)

        self.base_routes[1][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[1][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 1])
        self.base_routes[1][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[1][self.c['base_route_types']['right_entry_base_route']].junction_position.append(1)

        self.base_routes[1][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[1][21][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[1][self.c['base_route_types']['left_exit_base_route']].junction_position.append(1)
        self.base_routes[1][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[1][self.c['base_route_types']['left_exit_base_route']].junction_position.append([1, 1])

        self.base_routes[1][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[1][self.c['base_route_types']['right_exit_base_route']].junction_position.append(1)
        self.base_routes[1][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[1][self.c['base_route_types']['right_exit_base_route']].junction_position.append([1, 2])

        self.base_routes[3][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[3][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 1])
        self.base_routes[3][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[3][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[3][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][3][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[3][self.c['base_route_types']['left_entry_base_route']].junction_position.append(3)

        self.base_routes[3][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[3][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 1])
        self.base_routes[3][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[3][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[3][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][3][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[3][self.c['base_route_types']['right_entry_base_route']].junction_position.append(3)

        self.base_routes[3][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][3][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[3][self.c['base_route_types']['left_exit_base_route']].junction_position.append(3)
        self.base_routes[3][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[3][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[3][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[3][self.c['base_route_types']['left_exit_base_route']].junction_position.append([1, 1])

        self.base_routes[3][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][3][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[3][self.c['base_route_types']['right_exit_base_route']].junction_position.append(3)
        self.base_routes[3][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[3][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[3][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[3][self.c['base_route_types']['right_exit_base_route']].junction_position.append([1, 2])

        self.base_routes[5][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[5][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 1])
        self.base_routes[5][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[5][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[5][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][3][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[5][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[5][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][5][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[5][self.c['base_route_types']['left_entry_base_route']].junction_position.append(5)
        self.base_routes[5][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[5][7][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[5][self.c['base_route_types']['left_entry_base_route']].junction_position.append(5)

        self.base_routes[5][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[5][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 1])
        self.base_routes[5][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[5][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[5][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][3][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[5][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[5][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][5][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[5][self.c['base_route_types']['right_entry_base_route']].junction_position.append(5)
        self.base_routes[5][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[5][7][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[5][self.c['base_route_types']['right_entry_base_route']].junction_position.append(5)

        self.base_routes[5][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[5][7][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[5][self.c['base_route_types']['left_exit_base_route']].junction_position.append(5)
        self.base_routes[5][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][5][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[5][self.c['base_route_types']['left_exit_base_route']].junction_position.append(5)
        self.base_routes[5][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][3][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[5][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[5][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[5][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[5][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[5][self.c['base_route_types']['left_exit_base_route']].junction_position.append([1, 1])

        self.base_routes[5][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[5][7][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[5][self.c['base_route_types']['right_exit_base_route']].junction_position.append(5)
        self.base_routes[5][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][5][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[5][self.c['base_route_types']['right_exit_base_route']].junction_position.append(5)
        self.base_routes[5][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][3][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[5][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[5][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[5][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[5][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[5][self.c['base_route_types']['right_exit_base_route']].junction_position.append([1, 2])

        # ------------------ track 7 ----------------------
        self.base_routes[7][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[7][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 1])
        self.base_routes[7][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[7][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[7][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][3][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[7][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[7][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][5][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[7][self.c['base_route_types']['left_entry_base_route']].junction_position.append(5)
        self.base_routes[7][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[5][7][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[7][self.c['base_route_types']['left_entry_base_route']].junction_position.append(7)

        self.base_routes[7][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[7][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 1])
        self.base_routes[7][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[7][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[7][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][3][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[7][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[7][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][5][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[7][self.c['base_route_types']['right_entry_base_route']].junction_position.append(5)
        self.base_routes[7][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[5][7][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[7][self.c['base_route_types']['right_entry_base_route']].junction_position.append(7)

        self.base_routes[7][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[5][7][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[7][self.c['base_route_types']['left_exit_base_route']].junction_position.append(7)
        self.base_routes[7][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][5][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[7][self.c['base_route_types']['left_exit_base_route']].junction_position.append(5)
        self.base_routes[7][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][3][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[7][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[7][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[7][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[7][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[7][self.c['base_route_types']['left_exit_base_route']].junction_position.append([1, 1])

        self.base_routes[7][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[5][7][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[7][self.c['base_route_types']['right_exit_base_route']].junction_position.append(7)
        self.base_routes[7][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][5][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[7][self.c['base_route_types']['right_exit_base_route']].junction_position.append(5)
        self.base_routes[7][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][3][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[7][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[7][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[7][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[7][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[7][self.c['base_route_types']['right_exit_base_route']].junction_position.append([1, 2])

        # ----------------------- track 9 -------------------
        self.base_routes[9][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[9][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 1])
        self.base_routes[9][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[9][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[9][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][3][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[9][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[9][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][5][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[9][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[9][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][9][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[9][self.c['base_route_types']['left_entry_base_route']].junction_position.append(9)
        self.base_routes[9][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[9][11][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[9][self.c['base_route_types']['left_entry_base_route']].junction_position.append(9)

        self.base_routes[9][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[9][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 1])
        self.base_routes[9][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[9][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[9][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][3][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[9][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[9][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][5][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[9][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[9][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][9][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[9][self.c['base_route_types']['right_entry_base_route']].junction_position.append(9)
        self.base_routes[9][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[9][11][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[9][self.c['base_route_types']['right_entry_base_route']].junction_position.append(9)

        self.base_routes[9][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[9][11][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[9][self.c['base_route_types']['left_exit_base_route']].junction_position.append(9)
        self.base_routes[9][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][9][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[9][self.c['base_route_types']['left_exit_base_route']].junction_position.append(9)
        self.base_routes[9][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][5][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[9][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[9][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][3][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[9][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[9][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[9][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[9][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[9][self.c['base_route_types']['left_exit_base_route']].junction_position.append([1, 1])

        self.base_routes[9][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[9][11][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[9][self.c['base_route_types']['right_exit_base_route']].junction_position.append(9)
        self.base_routes[9][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][9][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[9][self.c['base_route_types']['right_exit_base_route']].junction_position.append(9)
        self.base_routes[9][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][5][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[9][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[9][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][3][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[9][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[9][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[9][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[9][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[9][self.c['base_route_types']['right_exit_base_route']].junction_position.append([1, 2])

        # ------------------ track 11 ------------------
        self.base_routes[11][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[11][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 1])
        self.base_routes[11][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[11][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[11][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][3][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[11][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[11][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][5][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[11][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[11][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][9][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[11][self.c['base_route_types']['left_entry_base_route']].junction_position.append(9)
        self.base_routes[11][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[9][11][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[11][self.c['base_route_types']['left_entry_base_route']].junction_position.append(11)

        self.base_routes[11][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[11][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 1])
        self.base_routes[11][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[11][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[11][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][3][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[11][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[11][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][5][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[11][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[11][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][9][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[11][self.c['base_route_types']['right_entry_base_route']].junction_position.append(9)
        self.base_routes[11][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[9][11][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[11][self.c['base_route_types']['right_entry_base_route']].junction_position.append(11)

        self.base_routes[11][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[9][11][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[11][self.c['base_route_types']['left_exit_base_route']].junction_position.append(11)
        self.base_routes[11][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][9][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[11][self.c['base_route_types']['left_exit_base_route']].junction_position.append(9)
        self.base_routes[11][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][5][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[11][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[11][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][3][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[11][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[11][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[11][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[11][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[11][self.c['base_route_types']['left_exit_base_route']].junction_position.append([1, 1])

        self.base_routes[11][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[9][11][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[11][self.c['base_route_types']['right_exit_base_route']].junction_position.append(11)
        self.base_routes[11][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][9][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[11][self.c['base_route_types']['right_exit_base_route']].junction_position.append(9)
        self.base_routes[11][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][5][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[11][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[11][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][3][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[11][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[11][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[11][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[11][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[11][self.c['base_route_types']['right_exit_base_route']].junction_position.append([1, 2])

        # ------------------------ track 13 ---------------------------
        self.base_routes[13][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[13][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 1])
        self.base_routes[13][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[13][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][3][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[13][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][5][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[13][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][9][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[13][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][13][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['left_entry_base_route']].junction_position.append(13)
        self.base_routes[13][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[13][15][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['left_entry_base_route']].junction_position.append(13)

        self.base_routes[13][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[13][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 1])
        self.base_routes[13][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[13][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][3][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[13][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][5][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[13][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][9][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[13][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][13][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['right_entry_base_route']].junction_position.append(13)
        self.base_routes[13][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[13][15][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['right_entry_base_route']].junction_position.append(13)

        self.base_routes[13][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[13][15][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['left_exit_base_route']].junction_position.append(13)
        self.base_routes[13][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][13][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['left_exit_base_route']].junction_position.append(13)
        self.base_routes[13][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][9][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[13][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][5][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[13][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][3][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[13][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[13][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[13][self.c['base_route_types']['left_exit_base_route']].junction_position.append([1, 1])

        self.base_routes[13][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[13][15][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['right_exit_base_route']].junction_position.append(13)
        self.base_routes[13][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][13][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['right_exit_base_route']].junction_position.append(13)
        self.base_routes[13][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][9][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[13][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][5][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[13][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][3][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[13][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[13][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[13][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[13][self.c['base_route_types']['right_exit_base_route']].junction_position.append([1, 2])

        # ------------------ track 15 ----------------------
        self.base_routes[15][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[15][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 1])
        self.base_routes[15][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[15][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][3][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[15][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][5][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[15][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][9][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[15][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][13][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['left_entry_base_route']].junction_position.append(13)
        self.base_routes[15][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[13][15][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['left_entry_base_route']].junction_position.append(15)

        self.base_routes[15][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[15][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 1])
        self.base_routes[15][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[15][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][3][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[15][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][5][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[15][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][9][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[15][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][13][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['right_entry_base_route']].junction_position.append(13)
        self.base_routes[15][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[13][15][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['right_entry_base_route']].junction_position.append(15)

        self.base_routes[15][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[13][15][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['left_exit_base_route']].junction_position.append(15)
        self.base_routes[15][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][13][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['left_exit_base_route']].junction_position.append(13)
        self.base_routes[15][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][9][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[15][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][5][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[15][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][3][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[15][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[15][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[15][self.c['base_route_types']['left_exit_base_route']].junction_position.append([1, 1])

        self.base_routes[15][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[13][15][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['right_exit_base_route']].junction_position.append(15)
        self.base_routes[15][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][13][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['right_exit_base_route']].junction_position.append(13)
        self.base_routes[15][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][9][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[15][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][5][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[15][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][3][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[15][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[15][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[15][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[15][self.c['base_route_types']['right_exit_base_route']].junction_position.append([1, 2])

        # ------------------ track 17 ----------------------
        self.base_routes[17][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[17][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 1])
        self.base_routes[17][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[17][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][3][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[17][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][5][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[17][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][9][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[17][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][13][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[17][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][17][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['left_entry_base_route']].junction_position.append(17)
        self.base_routes[17][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[17][19][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['left_entry_base_route']].junction_position.append(17)

        self.base_routes[17][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[17][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 1])
        self.base_routes[17][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[17][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][3][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[17][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][5][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[17][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][9][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[17][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][13][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[17][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][17][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['right_entry_base_route']].junction_position.append(17)
        self.base_routes[17][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[17][19][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['right_entry_base_route']].junction_position.append(17)

        self.base_routes[17][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[17][19][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['left_exit_base_route']].junction_position.append(17)
        self.base_routes[17][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][17][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['left_exit_base_route']].junction_position.append(17)
        self.base_routes[17][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][13][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[17][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][9][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[17][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][5][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[17][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][3][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[17][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[17][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[17][self.c['base_route_types']['left_exit_base_route']].junction_position.append([1, 1])

        self.base_routes[17][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[17][19][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['right_exit_base_route']].junction_position.append(17)
        self.base_routes[17][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][17][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['right_exit_base_route']].junction_position.append(17)
        self.base_routes[17][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][13][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[17][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][9][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[17][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][5][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[17][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][3][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[17][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[17][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[17][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[17][self.c['base_route_types']['right_exit_base_route']].junction_position.append([1, 2])

        # ------------------ track 19 ----------------------
        self.base_routes[19][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[19][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 1])
        self.base_routes[19][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[19][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][3][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[19][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][5][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[19][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][9][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[19][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][13][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[19][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][17][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['left_entry_base_route']].junction_position.append(17)
        self.base_routes[19][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[17][19][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['left_entry_base_route']].junction_position.append(19)

        self.base_routes[19][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[19][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 1])
        self.base_routes[19][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[19][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][3][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[19][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][5][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[19][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][9][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[19][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][13][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[19][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][17][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['right_entry_base_route']].junction_position.append(17)
        self.base_routes[19][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[17][19][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['right_entry_base_route']].junction_position.append(19)

        self.base_routes[19][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[17][19][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['left_exit_base_route']].junction_position.append(19)
        self.base_routes[19][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][17][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['left_exit_base_route']].junction_position.append(17)
        self.base_routes[19][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][13][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[19][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][9][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[19][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][5][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[19][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][3][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[19][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[19][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[19][self.c['base_route_types']['left_exit_base_route']].junction_position.append([1, 1])

        self.base_routes[19][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[17][19][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['right_exit_base_route']].junction_position.append(19)
        self.base_routes[19][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][17][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['right_exit_base_route']].junction_position.append(17)
        self.base_routes[19][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][13][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[19][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][9][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[19][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][5][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[19][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][3][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[19][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[19][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[19][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[19][self.c['base_route_types']['right_exit_base_route']].junction_position.append([1, 2])

        # ------------------ track 21 ----------------------
        self.base_routes[21][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[21][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 1])
        self.base_routes[21][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[21][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][3][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[21][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][5][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[21][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][9][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[21][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][13][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[21][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][17][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[21][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[101][21][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.base_routes[21][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[21][23][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[21][self.c['base_route_types']['left_entry_base_route']].junction_position.append([21, 21])

        self.base_routes[21][self.c['base_route_types']['left_side_entry_base_route']].junctions\
            .append(self.junctions[101][103][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[21][self.c['base_route_types']['left_side_entry_base_route']].junction_position\
            .append([101, 101])
        self.base_routes[21][self.c['base_route_types']['left_side_entry_base_route']].junctions \
            .append(self.junctions[101][21][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['left_side_entry_base_route']].junction_position.append(101)
        self.base_routes[21][self.c['base_route_types']['left_side_entry_base_route']].junctions\
            .append(self.junctions[21][23][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[21][self.c['base_route_types']['left_side_entry_base_route']].junction_position\
            .append([21, 21])

        self.base_routes[21][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[21][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 1])
        self.base_routes[21][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[21][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][3][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[21][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][5][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[21][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][9][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[21][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][13][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[21][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][17][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.base_routes[21][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][21][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['right_entry_base_route']].junction_position.append(21)
        self.base_routes[21][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[21][23][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['right_entry_base_route']].junction_position.append(21)

        self.base_routes[21][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[23][21][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[21][self.c['base_route_types']['left_exit_base_route']].junction_position.append([21, 21])
        self.base_routes[21][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[101][21][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[21][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][17][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[21][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][13][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[21][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][9][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[21][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][5][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[21][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][3][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[21][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.base_routes[21][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[21][self.c['base_route_types']['left_exit_base_route']].junction_position.append([1, 1])

        self.base_routes[21][self.c['base_route_types']['left_side_exit_base_route']].junctions\
            .append(self.junctions[23][21][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[21][self.c['base_route_types']['left_side_exit_base_route']].junction_position\
            .append([21, 21])
        self.base_routes[21][self.c['base_route_types']['left_side_exit_base_route']].junctions \
            .append(self.junctions[101][21][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['left_side_exit_base_route']].junction_position.append(101)
        self.base_routes[21][self.c['base_route_types']['left_side_exit_base_route']].junctions\
            .append(self.junctions[101][103][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[21][self.c['base_route_types']['left_side_exit_base_route']].junction_position\
            .append([101, 103])

        self.base_routes[21][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[21][23][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['right_exit_base_route']].junction_position.append(21)
        self.base_routes[21][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][21][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['right_exit_base_route']].junction_position.append(21)
        self.base_routes[21][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][17][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[21][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][13][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[21][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][9][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[21][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][5][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[21][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][3][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[21][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[21][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.base_routes[21][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[21][self.c['base_route_types']['right_exit_base_route']].junction_position.append([1, 2])

        for i in range(1, self.c['dispatcher_config']['tracks_ready'] + 1, 2):
            if i <= 24:
                self.base_routes[i][self.c['base_route_types']['left_entry_base_route']].read_trail_points()
                self.base_routes[i][self.c['base_route_types']['left_exit_base_route']].read_trail_points()

            if i >= 21:
                self.base_routes[i][self.c['base_route_types']['left_side_entry_base_route']].read_trail_points()
                self.base_routes[i][self.c['base_route_types']['left_side_exit_base_route']].read_trail_points()

            self.base_routes[i][self.c['base_route_types']['right_entry_base_route']].read_trail_points()
            self.base_routes[i][self.c['base_route_types']['right_exit_base_route']].read_trail_points()

        self.logger.info('trail points initialized for odd tracks')

        self.base_routes[2][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[2][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 2])
        self.base_routes[2][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[2][self.c['base_route_types']['left_entry_base_route']].junction_position.append(2)

        self.base_routes[2][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[2][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 2])
        self.base_routes[2][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[2][self.c['base_route_types']['right_entry_base_route']].junction_position.append(2)

        self.base_routes[2][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[2][self.c['base_route_types']['left_exit_base_route']].junction_position.append(2)
        self.base_routes[2][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[2][self.c['base_route_types']['left_exit_base_route']].junction_position.append([2, 1])

        self.base_routes[2][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[2][self.c['base_route_types']['right_exit_base_route']].junction_position.append(2)
        self.base_routes[2][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[2][self.c['base_route_types']['right_exit_base_route']].junction_position.append([2, 2])

        self.base_routes[4][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[4][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 2])
        self.base_routes[4][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[4][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[4][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][4][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[4][self.c['base_route_types']['left_entry_base_route']].junction_position.append(4)

        self.base_routes[4][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[4][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 2])
        self.base_routes[4][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[4][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[4][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][4][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[4][self.c['base_route_types']['right_entry_base_route']].junction_position.append(4)

        self.base_routes[4][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][4][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[4][self.c['base_route_types']['left_exit_base_route']].junction_position.append(4)
        self.base_routes[4][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[4][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[4][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[4][self.c['base_route_types']['left_exit_base_route']].junction_position.append([2, 1])

        self.base_routes[4][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][4][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[4][self.c['base_route_types']['right_exit_base_route']].junction_position.append(4)
        self.base_routes[4][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[4][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[4][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[4][self.c['base_route_types']['right_exit_base_route']].junction_position.append([2, 2])

        self.base_routes[6][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[6][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 2])
        self.base_routes[6][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[6][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[6][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][4][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[6][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[6][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][6][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[6][self.c['base_route_types']['left_entry_base_route']].junction_position.append(6)
        self.base_routes[6][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[6][8][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[6][self.c['base_route_types']['left_entry_base_route']].junction_position.append(6)

        self.base_routes[6][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[6][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 2])
        self.base_routes[6][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[6][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[6][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][4][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[6][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[6][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][6][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[6][self.c['base_route_types']['right_entry_base_route']].junction_position.append(6)
        self.base_routes[6][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[6][8][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[6][self.c['base_route_types']['right_entry_base_route']].junction_position.append(6)

        self.base_routes[6][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[6][8][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[6][self.c['base_route_types']['left_exit_base_route']].junction_position.append(6)
        self.base_routes[6][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][6][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[6][self.c['base_route_types']['left_exit_base_route']].junction_position.append(6)
        self.base_routes[6][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][4][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[6][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[6][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[6][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[6][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[6][self.c['base_route_types']['left_exit_base_route']].junction_position.append([2, 1])

        self.base_routes[6][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[6][8][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[6][self.c['base_route_types']['right_exit_base_route']].junction_position.append(6)
        self.base_routes[6][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][6][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[6][self.c['base_route_types']['right_exit_base_route']].junction_position.append(6)
        self.base_routes[6][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][4][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[6][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[6][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[6][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[6][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[6][self.c['base_route_types']['right_exit_base_route']].junction_position.append([2, 2])

        # ---------------------- track 8 --------------------------
        self.base_routes[8][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[8][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 2])
        self.base_routes[8][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[8][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[8][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][4][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[8][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[8][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][6][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[8][self.c['base_route_types']['left_entry_base_route']].junction_position.append(6)
        self.base_routes[8][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[6][8][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[8][self.c['base_route_types']['left_entry_base_route']].junction_position.append(8)

        self.base_routes[8][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[8][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 2])
        self.base_routes[8][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[8][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[8][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][4][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[8][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[8][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][6][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[8][self.c['base_route_types']['right_entry_base_route']].junction_position.append(6)
        self.base_routes[8][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[6][8][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[8][self.c['base_route_types']['right_entry_base_route']].junction_position.append(8)

        self.base_routes[8][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[6][8][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[8][self.c['base_route_types']['left_exit_base_route']].junction_position.append(8)
        self.base_routes[8][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][6][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[8][self.c['base_route_types']['left_exit_base_route']].junction_position.append(6)
        self.base_routes[8][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][4][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[8][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[8][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[8][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[8][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[8][self.c['base_route_types']['left_exit_base_route']].junction_position.append([2, 1])

        self.base_routes[8][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[6][8][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[8][self.c['base_route_types']['right_exit_base_route']].junction_position.append(8)
        self.base_routes[8][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][6][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[8][self.c['base_route_types']['right_exit_base_route']].junction_position.append(6)
        self.base_routes[8][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][4][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[8][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[8][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[8][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[8][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[8][self.c['base_route_types']['right_exit_base_route']].junction_position.append([2, 2])

        # -------------------- track 10 ----------------------
        self.base_routes[10][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[10][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 2])
        self.base_routes[10][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[10][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[10][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][4][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[10][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[10][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][6][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[10][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[10][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][10][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[10][self.c['base_route_types']['left_entry_base_route']].junction_position.append(10)
        self.base_routes[10][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[10][12][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[10][self.c['base_route_types']['left_entry_base_route']].junction_position.append(10)

        self.base_routes[10][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[10][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 2])
        self.base_routes[10][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[10][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[10][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][4][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[10][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[10][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][6][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[10][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[10][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][10][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[10][self.c['base_route_types']['right_entry_base_route']].junction_position.append(10)
        self.base_routes[10][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[10][12][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[10][self.c['base_route_types']['right_entry_base_route']].junction_position.append(10)

        self.base_routes[10][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[10][12][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[10][self.c['base_route_types']['left_exit_base_route']].junction_position.append(10)
        self.base_routes[10][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][10][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[10][self.c['base_route_types']['left_exit_base_route']].junction_position.append(10)
        self.base_routes[10][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][6][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[10][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[10][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][4][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[10][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[10][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[10][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[10][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[10][self.c['base_route_types']['left_exit_base_route']].junction_position.append([2, 1])

        self.base_routes[10][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[10][12][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[10][self.c['base_route_types']['right_exit_base_route']].junction_position.append(10)
        self.base_routes[10][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][10][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[10][self.c['base_route_types']['right_exit_base_route']].junction_position.append(10)
        self.base_routes[10][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][6][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[10][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[10][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][4][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[10][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[10][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[10][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[10][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[10][self.c['base_route_types']['right_exit_base_route']].junction_position.append([2, 2])

        # --------------------- track 12 -------------------
        self.base_routes[12][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[12][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 2])
        self.base_routes[12][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[12][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[12][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][4][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[12][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[12][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][6][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[12][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[12][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][10][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[12][self.c['base_route_types']['left_entry_base_route']].junction_position.append(10)
        self.base_routes[12][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[10][12][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[12][self.c['base_route_types']['left_entry_base_route']].junction_position.append(12)

        self.base_routes[12][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[12][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 2])
        self.base_routes[12][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[12][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[12][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][4][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[12][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[12][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][6][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[12][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[12][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][10][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[12][self.c['base_route_types']['right_entry_base_route']].junction_position.append(10)
        self.base_routes[12][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[10][12][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[12][self.c['base_route_types']['right_entry_base_route']].junction_position.append(12)

        self.base_routes[12][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[10][12][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[12][self.c['base_route_types']['left_exit_base_route']].junction_position.append(12)
        self.base_routes[12][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][10][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[12][self.c['base_route_types']['left_exit_base_route']].junction_position.append(10)
        self.base_routes[12][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][6][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[12][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[12][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][4][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[12][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[12][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[12][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[12][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[12][self.c['base_route_types']['left_exit_base_route']].junction_position.append([2, 1])

        self.base_routes[12][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[10][12][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[12][self.c['base_route_types']['right_exit_base_route']].junction_position.append(12)
        self.base_routes[12][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][10][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[12][self.c['base_route_types']['right_exit_base_route']].junction_position.append(10)
        self.base_routes[12][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][6][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[12][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[12][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][4][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[12][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[12][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[12][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[12][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[12][self.c['base_route_types']['right_exit_base_route']].junction_position.append([2, 2])

        # ------------------- track 14 -----------------------
        self.base_routes[14][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[14][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 2])
        self.base_routes[14][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[14][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][4][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[14][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][6][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[14][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][10][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[14][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][14][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['left_entry_base_route']].junction_position.append(14)
        self.base_routes[14][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[14][16][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['left_entry_base_route']].junction_position.append(14)

        self.base_routes[14][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[14][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 2])
        self.base_routes[14][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[14][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][4][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[14][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][6][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[14][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][10][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[14][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][14][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['right_entry_base_route']].junction_position.append(14)
        self.base_routes[14][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[14][16][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['right_entry_base_route']].junction_position.append(14)

        self.base_routes[14][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[14][16][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['left_exit_base_route']].junction_position.append(14)
        self.base_routes[14][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][14][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['left_exit_base_route']].junction_position.append(14)
        self.base_routes[14][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][10][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[14][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][6][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[14][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][4][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[14][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[14][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[14][self.c['base_route_types']['left_exit_base_route']].junction_position.append([2, 1])

        self.base_routes[14][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[14][16][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['right_exit_base_route']].junction_position.append(14)
        self.base_routes[14][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][14][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['right_exit_base_route']].junction_position.append(14)
        self.base_routes[14][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][10][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[14][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][6][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[14][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][4][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[14][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[14][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[14][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[14][self.c['base_route_types']['right_exit_base_route']].junction_position.append([2, 2])

        # ------------------- track 16 -----------------------
        self.base_routes[16][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[16][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 2])
        self.base_routes[16][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[16][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][4][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[16][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][6][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[16][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][10][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[16][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][14][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['left_entry_base_route']].junction_position.append(14)
        self.base_routes[16][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[14][16][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['left_entry_base_route']].junction_position.append(16)

        self.base_routes[16][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[16][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 2])
        self.base_routes[16][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[16][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][4][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[16][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][6][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[16][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][10][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[16][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][14][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['right_entry_base_route']].junction_position.append(14)
        self.base_routes[16][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[14][16][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['right_entry_base_route']].junction_position.append(16)

        self.base_routes[16][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[14][16][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['left_exit_base_route']].junction_position.append(16)
        self.base_routes[16][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][14][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['left_exit_base_route']].junction_position.append(14)
        self.base_routes[16][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][10][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[16][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][6][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[16][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][4][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[16][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[16][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[16][self.c['base_route_types']['left_exit_base_route']].junction_position.append([2, 1])

        self.base_routes[16][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[14][16][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['right_exit_base_route']].junction_position.append(16)
        self.base_routes[16][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][14][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['right_exit_base_route']].junction_position.append(14)
        self.base_routes[16][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][10][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[16][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][6][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[16][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][4][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[16][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[16][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[16][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[16][self.c['base_route_types']['right_exit_base_route']].junction_position.append([2, 2])

        # ------------------- track 18 -----------------------
        self.base_routes[18][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[18][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 2])
        self.base_routes[18][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[18][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][4][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[18][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][6][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[18][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][10][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[18][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][14][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[18][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][18][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['left_entry_base_route']].junction_position.append(18)
        self.base_routes[18][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[18][20][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['left_entry_base_route']].junction_position.append(18)

        self.base_routes[18][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[18][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 2])
        self.base_routes[18][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[18][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][4][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[18][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][6][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[18][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][10][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[18][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][14][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[18][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][18][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['right_entry_base_route']].junction_position.append(18)
        self.base_routes[18][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[18][20][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['right_entry_base_route']].junction_position.append(18)

        self.base_routes[18][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[18][20][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['left_exit_base_route']].junction_position.append(18)
        self.base_routes[18][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][18][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['left_exit_base_route']].junction_position.append(18)
        self.base_routes[18][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][14][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[18][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][10][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[18][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][6][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[18][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][4][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[18][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[18][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[18][self.c['base_route_types']['left_exit_base_route']].junction_position.append([2, 1])

        self.base_routes[18][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[18][20][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['right_exit_base_route']].junction_position.append(18)
        self.base_routes[18][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][18][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['right_exit_base_route']].junction_position.append(18)
        self.base_routes[18][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][14][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[18][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][10][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[18][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][6][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[18][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][4][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[18][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[18][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[18][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[18][self.c['base_route_types']['right_exit_base_route']].junction_position.append([2, 2])

        # ------------------- track 20 -----------------------
        self.base_routes[20][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[20][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 2])
        self.base_routes[20][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[20][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][4][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[20][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][6][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[20][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][10][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[20][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][14][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.base_routes[20][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][18][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['left_entry_base_route']].junction_position.append(18)
        self.base_routes[20][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[18][20][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['left_entry_base_route']].junction_position.append(20)

        self.base_routes[20][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[20][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 2])
        self.base_routes[20][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[20][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][4][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[20][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][6][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[20][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][10][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[20][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][14][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.base_routes[20][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][18][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['right_entry_base_route']].junction_position.append(18)
        self.base_routes[20][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[18][20][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['right_entry_base_route']].junction_position.append(20)

        self.base_routes[20][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[18][20][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['left_exit_base_route']].junction_position.append(20)
        self.base_routes[20][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][18][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['left_exit_base_route']].junction_position.append(18)
        self.base_routes[20][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][14][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[20][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][10][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[20][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][6][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[20][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][4][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[20][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.base_routes[20][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[20][self.c['base_route_types']['left_exit_base_route']].junction_position.append([2, 1])

        self.base_routes[20][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[18][20][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['right_exit_base_route']].junction_position.append(20)
        self.base_routes[20][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][18][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['right_exit_base_route']].junction_position.append(18)
        self.base_routes[20][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][14][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[20][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][10][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[20][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][6][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[20][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][4][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[20][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[20][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.base_routes[20][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[20][self.c['base_route_types']['right_exit_base_route']].junction_position.append([2, 2])

        for i in range(2, self.c['dispatcher_config']['tracks_ready'] + 1, 2):
            self.base_routes[i][self.c['base_route_types']['left_entry_base_route']].read_trail_points()
            self.base_routes[i][self.c['base_route_types']['left_exit_base_route']].read_trail_points()
            self.base_routes[i][self.c['base_route_types']['right_entry_base_route']].read_trail_points()
            self.base_routes[i][self.c['base_route_types']['right_exit_base_route']].read_trail_points()

        self.logger.info('trail points initialized for even tracks')

        for i in range(1, self.c['dispatcher_config']['tracks_ready'] + 1):
            # associate platform base route with its signal
            self.base_routes[i][
                self.c['base_route_types']['right_exit_platform_base_route']
            ].route_config['exit_signal'] \
                = self.signals[i][self.c['base_route_types']['right_exit_platform_base_route']]
            self.logger.debug('base route {} {} signal is signal {} {}'
                              .format(i, self.c['base_route_types']['right_exit_platform_base_route'],
                                      i, self.c['base_route_types']['right_exit_platform_base_route']))
            self.base_routes[i][
                self.c['base_route_types']['left_entry_platform_base_route']
            ].route_config['exit_signal'] \
                = self.signals[i][self.c['base_route_types']['right_exit_platform_base_route']]
            self.logger.debug('base route {} {} signal is signal {} {}'
                              .format(i, self.c['base_route_types']['left_entry_platform_base_route'],
                                      i, self.c['base_route_types']['right_exit_platform_base_route']))
            self.base_routes[i][
                self.c['base_route_types']['left_exit_platform_base_route']
            ].route_config['exit_signal'] \
                = self.signals[i][self.c['base_route_types']['left_exit_platform_base_route']]
            self.logger.debug('base route {} {} signal is signal {} {}'
                              .format(i, self.c['base_route_types']['left_exit_platform_base_route'],
                                      i, self.c['base_route_types']['left_exit_platform_base_route']))
            self.base_routes[i][
                self.c['base_route_types']['right_entry_platform_base_route']
            ].route_config['exit_signal'] \
                = self.signals[i][self.c['base_route_types']['left_exit_platform_base_route']]
            self.logger.debug('base route {} {} signal is signal {} {}'
                              .format(i, self.c['base_route_types']['right_entry_platform_base_route'],
                                      i, self.c['base_route_types']['left_exit_platform_base_route']))
            # for every signal, exit route is the route which ends with this signal
            self.signals[i][self.c['base_route_types']['right_exit_platform_base_route']].base_route_exit \
                = self.base_routes[i][self.c['base_route_types']['right_exit_platform_base_route']]
            self.logger.debug('signal {} {} exit route is base route {} {}'
                              .format(i, self.c['base_route_types']['right_exit_platform_base_route'],
                                      i, self.c['base_route_types']['right_exit_platform_base_route']))
            self.signals[i][self.c['base_route_types']['left_exit_platform_base_route']].base_route_exit \
                = self.base_routes[i][self.c['base_route_types']['left_exit_platform_base_route']]
            self.logger.debug('signal {} {} exit route is base route {} {}'
                              .format(i, self.c['base_route_types']['left_exit_platform_base_route'],
                                      i, self.c['base_route_types']['left_exit_platform_base_route']))
            self.logger.debug('track {} base routes and signals associated'.format(i))

        self.logger.info('all base routes and signals associated')
        # fill opened and busy route lists for signals
        for i in range(1, self.c['dispatcher_config']['tracks_ready'] + 1):
            # for every platform signal, opened list includes exit base route
            # which begins behind the signal
            # for main entry signals, opened list includes all entry base routes
            if i <= 24 or i in (26, 28, 30, 32):
                self.signals[i][self.c['base_route_types']['left_exit_platform_base_route']].base_route_opened_list \
                    .append(self.base_routes[i][self.c['base_route_types']['left_exit_base_route']])
                self.logger.debug('base route {} {} appended to signal {} {} opened list'
                                  .format(i, self.c['base_route_types']['left_exit_base_route'],
                                          i, self.c['base_route_types']['left_exit_platform_base_route']))
                self.signals[0][self.c['base_route_types']['left_entry_base_route']].base_route_opened_list \
                    .append(self.base_routes[i][self.c['base_route_types']['left_entry_base_route']])
                self.logger.debug('base route {} {} appended to signal {} {} opened list'
                                  .format(i, self.c['base_route_types']['left_entry_base_route'],
                                          0, self.c['base_route_types']['left_entry_base_route']))

            if i <= 24 or i in (25, 27, 29, 31):
                self.signals[i][self.c['base_route_types']['right_exit_platform_base_route']].base_route_opened_list \
                    .append(self.base_routes[i][self.c['base_route_types']['right_exit_base_route']])
                self.logger.debug('base route {} {} appended to signal {} {} opened list'
                                  .format(i, self.c['base_route_types']['right_exit_base_route'],
                                          i, self.c['base_route_types']['right_exit_platform_base_route']))
                self.signals[0][self.c['base_route_types']['right_entry_base_route']].base_route_opened_list \
                    .append(self.base_routes[i][self.c['base_route_types']['right_entry_base_route']])
                self.logger.debug('base route {} {} appended to signal {} {} opened list'
                                  .format(i, self.c['base_route_types']['right_entry_base_route'],
                                          0, self.c['base_route_types']['right_entry_base_route']))

            if i in (21, 23, 25, 27, 29, 31):
                self.signals[i][self.c['base_route_types']['left_exit_platform_base_route']]\
                    .base_route_opened_list\
                    .append(self.base_routes[i][self.c['base_route_types']['left_side_exit_base_route']])
                self.logger.debug('base route {} {} appended to signal {} {} opened list'
                                  .format(i, self.c['base_route_types']['left_side_exit_base_route'],
                                          i, self.c['base_route_types']['left_exit_platform_base_route']))
                self.signals[100][self.c['base_route_types']['left_side_entry_base_route']].base_route_opened_list \
                    .append(self.base_routes[i][self.c['base_route_types']['left_side_entry_base_route']])
                self.logger.debug('base route {} {} appended to signal {} {} opened list'
                                  .format(i, self.c['base_route_types']['left_side_entry_base_route'],
                                          100, self.c['base_route_types']['left_side_entry_base_route']))

            if i in (22, 24, 26, 28, 30, 32):
                self.signals[i][self.c['base_route_types']['right_exit_platform_base_route']].base_route_opened_list \
                    .append(self.base_routes[i][self.c['base_route_types']['right_side_exit_base_route']])
                self.logger.debug('base route {} {} appended to signal {} {} opened list'
                                  .format(i, self.c['base_route_types']['right_side_exit_base_route'],
                                          i, self.c['base_route_types']['right_exit_platform_base_route']))
                self.signals[100][self.c['base_route_types']['right_side_entry_base_route']].base_route_opened_list \
                    .append(self.base_routes[i][self.c['base_route_types']['right_side_entry_base_route']])
                self.logger.debug('base route {} {} appended to signal {} {} opened list'
                                  .format(i, self.c['base_route_types']['right_side_entry_base_route'],
                                          100, self.c['base_route_types']['right_side_entry_base_route']))

        self.logger.debug('opened list set up for track 0 signals')
        self.logger.info('opened list set up for all signals')

        # ------ TRAIN ROUTES AND TRACKS ------
        # create basic entry train routes for trains which cannot find available track
        base_routes_in_train_route \
            = [self.base_routes[0][
                   '{}_base_route'
                   .format(self.c['train_route_types']['entry_train_route'][self.c['direction']['left']])], ]
        self.train_routes[0][self.c['train_route_types']['approaching_train_route'][self.c['direction']['left']]] \
            = TrainRoute(base_routes=base_routes_in_train_route,
                         track_number=0,
                         route_type=self.c['train_route_types']['approaching_train_route'][self.c['direction']['left']],
                         supported_carts=[0, 20])
        base_routes_in_train_route \
            = [self.base_routes[0][
                   '{}_base_route'
                   .format(self.c['train_route_types']['entry_train_route'][self.c['direction']['right']])], ]
        self.train_routes[0][self.c['train_route_types']['approaching_train_route'][self.c['direction']['right']]] \
            = TrainRoute(base_routes=base_routes_in_train_route,
                         track_number=0,
                         route_type=self.c['train_route_types']['approaching_train_route'][
                             self.c['direction']['right']],
                         supported_carts=[0, 20])
        self.logger.info('approaching train routes created')

        for i in range(1, self.c['dispatcher_config']['tracks_ready'] + 1):
            self.train_routes.append({})
            # create track object
            # it includes all 4 base routes
            base_routes_in_track = [self.base_routes[i][self.c['base_route_types']['left_entry_platform_base_route']],
                                    self.base_routes[i][self.c['base_route_types']['right_entry_platform_base_route']],
                                    self.base_routes[i][self.c['base_route_types']['left_exit_platform_base_route']],
                                    self.base_routes[i][self.c['base_route_types']['right_exit_platform_base_route']]]
            new_track = Track(track_number=i, base_routes_in_track=base_routes_in_track)
            self.tracks.append(new_track)
            self.logger.info('track {} created'.format(i))
            # create entry train route
            # it includes main entry base route, specific entry base route and platform base route
            if i <= 24:
                for k in (self.c['direction']['left'], self.c['direction']['right']):
                    base_routes_in_train_route = [
                        self.base_routes[0]['{}_base_route'
                                            .format(self.c['train_route_types']['entry_train_route'][k])],
                        self.base_routes[i]['{}_base_route'
                                            .format(self.c['train_route_types']['entry_train_route'][k])],
                        self.base_routes[i]['{}_platform_base_route'
                                            .format(self.c['train_route_types']['entry_train_route'][k])]]

                    self.train_routes[i][self.c['train_route_types']['entry_train_route'][k]] \
                        = TrainRoute(base_routes=base_routes_in_train_route,
                                     track_number=i,
                                     route_type=self.c['train_route_types']['entry_train_route'][k],
                                     supported_carts=self.tracks[i - 1].supported_carts)
                    self.logger.info('track {} {} train route created'.format(i, k))

                # create exit train route
                # it includes platform base route, specific exit base route and main exit base route
                for m in (self.c['direction']['left'], self.c['direction']['right']):
                    base_routes_in_train_route = [
                        self.base_routes[i]['{}_platform_base_route'
                                            .format(self.c['train_route_types']['exit_train_route'][m])],
                        self.base_routes[i]['{}_base_route'
                                            .format(self.c['train_route_types']['exit_train_route'][m])],
                        self.base_routes[0]['{}_base_route'
                                            .format(self.c['train_route_types']['exit_train_route'][m])]]

                    self.train_routes[i][self.c['train_route_types']['exit_train_route'][m]] \
                        = TrainRoute(base_routes=base_routes_in_train_route,
                                     track_number=i,
                                     route_type=self.c['train_route_types']['exit_train_route'][m],
                                     supported_carts=self.tracks[i - 1].supported_carts)
                    self.logger.info('track {} {} train route created'.format(i, m))

            if i in (21, 23, 25, 27, 29, 31):
                base_routes_in_train_route = [
                    self.base_routes[100]['{}_base_route'
                        .format(self.c['train_route_types']['entry_train_route'][self.c['direction']['left_side']])],
                    self.base_routes[i]['{}_base_route'
                        .format(self.c['train_route_types']['entry_train_route'][self.c['direction']['left_side']])],
                    self.base_routes[i]['{}_platform_base_route'
                        .format(self.c['train_route_types']['entry_train_route'][self.c['direction']['left']])]]

                self.train_routes[i][self.c['train_route_types']['entry_train_route'][
                    self.c['direction']['left_side']]] \
                    = TrainRoute(base_routes=base_routes_in_train_route,
                                 track_number=i,
                                 route_type=self.c['train_route_types']['entry_train_route'][
                                     self.c['direction']['left_side']],
                                 supported_carts=self.tracks[i - 1].supported_carts)
                self.logger.info('track {} {} train route created'.format(i, self.c['direction']['left_side']))

                base_routes_in_train_route = [
                    self.base_routes[i]['{}_platform_base_route'
                        .format(self.c['train_route_types']['exit_train_route'][self.c['direction']['right']])],
                    self.base_routes[i]['{}_base_route'
                        .format(self.c['train_route_types']['exit_train_route'][self.c['direction']['right_side']])],
                    self.base_routes[100]['{}_base_route'
                        .format(self.c['train_route_types']['exit_train_route'][self.c['direction']['right_side']])]]

                self.train_routes[i][self.c['train_route_types']['exit_train_route'][
                    self.c['direction']['right_side']]] \
                    = TrainRoute(base_routes=base_routes_in_train_route,
                                 track_number=i,
                                 route_type=self.c['train_route_types']['exit_train_route'][
                                     self.c['direction']['right_side']],
                                 supported_carts=self.tracks[i - 1].supported_carts)
                self.logger.info('track {} {} train route created'.format(i, self.c['direction']['right_side']))
                if i >= 25:
                    base_routes_in_train_route = [
                        self.base_routes[0]['{}_base_route'
                            .format(self.c['train_route_types']['entry_train_route'][self.c['direction']['right']])],
                        self.base_routes[i]['{}_base_route'
                            .format(self.c['train_route_types']['entry_train_route'][self.c['direction']['right']])],
                        self.base_routes[i]['{}_platform_base_route'
                            .format(self.c['train_route_types']['entry_train_route'][self.c['direction']['right']])]]

                    self.train_routes[i][self.c['train_route_types']['entry_train_route'][
                        self.c['direction']['right']]] \
                        = TrainRoute(base_routes=base_routes_in_train_route,
                                     track_number=i,
                                     route_type=self.c['train_route_types']['entry_train_route'][
                                         self.c['direction']['right']],
                                     supported_carts=self.tracks[i - 1].supported_carts)
                    self.logger.info('track {} {} train route created'.format(i, self.c['direction']['right']))

                    base_routes_in_train_route = [
                        self.base_routes[i]['{}_platform_base_route'
                            .format(self.c['train_route_types']['exit_train_route'][self.c['direction']['left']])],
                        self.base_routes[i]['{}_base_route'
                            .format(self.c['train_route_types']['exit_train_route'][self.c['direction']['left']])],
                        self.base_routes[0]['{}_base_route'
                            .format(self.c['train_route_types']['exit_train_route'][self.c['direction']['left']])]]

                    self.train_routes[i][self.c['train_route_types']['exit_train_route'][
                        self.c['direction']['left']]] \
                        = TrainRoute(base_routes=base_routes_in_train_route,
                                     track_number=i,
                                     route_type=self.c['train_route_types']['exit_train_route'][
                                         self.c['direction']['left']],
                                     supported_carts=self.tracks[i - 1].supported_carts)
                    self.logger.info('track {} {} train route created'.format(i, self.c['direction']['left']))

            if i in (22, 24, 26, 28, 30, 32):
                base_routes_in_train_route = [
                    self.base_routes[100]['{}_base_route'
                        .format(self.c['train_route_types']['entry_train_route'][self.c['direction']['right_side']])],
                    self.base_routes[i]['{}_base_route'
                        .format(self.c['train_route_types']['entry_train_route'][self.c['direction']['right_side']])],
                    self.base_routes[i]['{}_platform_base_route'
                        .format(self.c['train_route_types']['entry_train_route'][self.c['direction']['right']])]]

                self.train_routes[i][self.c['train_route_types']['entry_train_route'][
                    self.c['direction']['right_side']]] \
                    = TrainRoute(base_routes=base_routes_in_train_route,
                                 track_number=i,
                                 route_type=self.c['train_route_types']['entry_train_route'][
                                     self.c['direction']['right_side']],
                                 supported_carts=self.tracks[i - 1].supported_carts)
                self.logger.info('track {} {} train route created'.format(i, self.c['direction']['right_side']))

                base_routes_in_train_route = [
                    self.base_routes[i]['{}_platform_base_route'
                        .format(self.c['train_route_types']['exit_train_route'][self.c['direction']['left']])],
                    self.base_routes[i]['{}_base_route'
                        .format(self.c['train_route_types']['exit_train_route'][self.c['direction']['left_side']])],
                    self.base_routes[100]['{}_base_route'
                        .format(self.c['train_route_types']['exit_train_route'][self.c['direction']['left_side']])]]

                self.train_routes[i][self.c['train_route_types']['exit_train_route'][
                    self.c['direction']['left_side']]] \
                    = TrainRoute(base_routes=base_routes_in_train_route,
                                 track_number=i,
                                 route_type=self.c['train_route_types']['exit_train_route'][
                                     self.c['direction']['left_side']],
                                 supported_carts=self.tracks[i - 1].supported_carts)
                self.logger.info('track {} {} train route created'.format(i, self.c['direction']['left_side']))
                if i >= 26:
                    base_routes_in_train_route = [
                        self.base_routes[0]['{}_base_route'
                            .format(self.c['train_route_types']['entry_train_route'][self.c['direction']['left']])],
                        self.base_routes[i]['{}_base_route'
                            .format(self.c['train_route_types']['entry_train_route'][self.c['direction']['left']])],
                        self.base_routes[i]['{}_platform_base_route'
                            .format(self.c['train_route_types']['entry_train_route'][self.c['direction']['left']])]]

                    self.train_routes[i][self.c['train_route_types']['entry_train_route'][
                        self.c['direction']['left']]] \
                        = TrainRoute(base_routes=base_routes_in_train_route,
                                     track_number=i,
                                     route_type=self.c['train_route_types']['entry_train_route'][
                                         self.c['direction']['left']],
                                     supported_carts=self.tracks[i - 1].supported_carts)
                    self.logger.info('track {} {} train route created'.format(i, self.c['direction']['left']))

                    base_routes_in_train_route = [
                        self.base_routes[i]['{}_platform_base_route'
                            .format(self.c['train_route_types']['exit_train_route'][self.c['direction']['right']])],
                        self.base_routes[i]['{}_base_route'
                            .format(self.c['train_route_types']['exit_train_route'][self.c['direction']['right']])],
                        self.base_routes[0]['{}_base_route'
                            .format(self.c['train_route_types']['exit_train_route'][self.c['direction']['right']])]]

                    self.train_routes[i][self.c['train_route_types']['exit_train_route'][
                        self.c['direction']['right']]] \
                        = TrainRoute(base_routes=base_routes_in_train_route,
                                     track_number=i,
                                     route_type=self.c['train_route_types']['exit_train_route'][
                                         self.c['direction']['right']],
                                     supported_carts=self.tracks[i - 1].supported_carts)
                    self.logger.info('track {} {} train route created'.format(i, self.c['direction']['right']))

        for i in range(100):
            self.train_routes.append({})

        base_routes_in_train_route \
            = [self.base_routes[100][
                   '{}_base_route'
                   .format(self.c['train_route_types']['entry_train_route'][self.c['direction']['left_side']])], ]
        self.train_routes[100][self.c['train_route_types']['approaching_train_route'][
            self.c['direction']['left_side']]] \
            = TrainRoute(base_routes=base_routes_in_train_route,
                         track_number=100,
                         route_type=self.c['train_route_types']['approaching_train_route'][
                             self.c['direction']['left_side']],
                         supported_carts=[0, 20]
                         )
        base_routes_in_train_route \
            = [self.base_routes[100][
                   '{}_base_route'
                   .format(self.c['train_route_types']['entry_train_route'][self.c['direction']['right_side']])], ]
        self.train_routes[100][self.c['train_route_types']['approaching_train_route'][
            self.c['direction']['right_side']]] \
            = TrainRoute(base_routes=base_routes_in_train_route,
                         track_number=100,
                         route_type=self.c['train_route_types']['approaching_train_route'][
                             self.c['direction']['right_side']],
                         supported_carts=[0, 20]
                         )

        self.logger.info('tracks and train routes created')
        # ------ SORT THIS OUT ------
        # base routes and signals are added to generic objects list
        for i in range(self.c['dispatcher_config']['tracks_ready'] + 1):
            for n in self.base_routes[i]:
                self.objects.append(self.base_routes[i][n])
                self.logger.debug('base route {} {} appended to global objects list'.format(i, n))

        for n in self.base_routes[100]:
            self.objects.append(self.base_routes[100][n])
            self.logger.debug('base route {} {} appended to global objects list'.format(100, n))

        self.logger.info('base routes and signals appended')
        # train routes and tracks are added to dispatcher which we create right now
        self.dispatcher = Dispatcher(batch=self.batch, group=self.signals_and_trains_ordered_group,
                                     boarding_lights_group=self.boarding_lights_ordered_group)
        for i in range(self.c['dispatcher_config']['tracks_ready'] + 1):
            self.dispatcher.train_routes.append({})
            for p in self.train_routes[i]:
                self.dispatcher.train_routes[i].update({p: self.train_routes[i][p]})
                self.logger.debug('train route {} {} appended to dispatcher'.format(i, p))

        for i in range(100):
            self.dispatcher.train_routes.append({})

        self.dispatcher.train_routes.append({})
        for p in self.train_routes[100]:
            self.dispatcher.train_routes[100].update({p: self.train_routes[100][p]})
            self.logger.debug('train route {} {} appended to dispatcher'.format(100, p))

        self.logger.info('all train routes appended to dispatcher')
        for i in range(self.c['dispatcher_config']['tracks_ready']):
            self.dispatcher.tracks.append(self.tracks[i])
            self.logger.debug('track {} appended to dispatcher'.format(i + 1))

        for i in range(self.c['dispatcher_config']['tracks_ready'] + 1):
            for n in self.signals[i]:
                self.dispatcher.signals.append(self.signals[i][n])
                self.logger.debug('signal {} {} appended to dispatcher'.format(i, n))

        for n in self.signals[100]:
            self.dispatcher.signals.append(self.signals[100][n])
            self.logger.debug('signal {} {} appended to dispatcher'.format(100, n))

        self.logger.info('all tracks appended to dispatcher')
        # now we add dispatcher itself to generic objects list
        self.dispatcher.read_state()
        self.objects.append(self.dispatcher)
        self.logger.info('dispatcher appended to global objects list')
        self.logger.debug('------- START CREATING INFRASTRUCTURE -------')
        self.logger.warning('all infrastructure created')

    def create_junctions(self):
        self.junctions[1] = {}
        self.junctions[1][2] = {}
        self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']] \
            = Crossover(1, 2, self.c['crossover_types']['right_entry_crossover'])
        self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']] \
            = Crossover(1, 2, self.c['crossover_types']['right_exit_crossover'])
        self.junctions[1][21] = {}
        self.junctions[1][21][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(1, 21, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[1][21][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(1, 21, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[1][29] = {}
        self.junctions[1][29][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(1, 29, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[1][29][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(1, 29, self.c['switch_types']['right_exit_railroad_switch'])
        self.logger.debug('junctions for track 1 created')

        self.junctions[2] = {}
        self.junctions[2][1] = {}
        self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']] \
            = Crossover(2, 1, self.c['crossover_types']['left_entry_crossover'])
        self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']] \
            = Crossover(2, 1, self.c['crossover_types']['left_exit_crossover'])
        self.junctions[2][22] = {}
        self.junctions[2][22][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(2, 22, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[2][22][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(2, 22, self.c['switch_types']['right_exit_railroad_switch'])
        self.junctions[2][30] = {}
        self.junctions[2][30][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(2, 30, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[2][30][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(2, 30, self.c['switch_types']['left_exit_railroad_switch'])
        self.logger.debug('junctions for track 2 created')

        self.junctions[5] = {}
        self.junctions[5][7] = {}
        self.junctions[5][7][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(5, 7, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[5][7][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(5, 7, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[5][7][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(5, 7, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[5][7][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(5, 7, self.c['switch_types']['right_exit_railroad_switch'])

        self.junctions[6] = {}
        self.junctions[6][8] = {}
        self.junctions[6][8][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(6, 8, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[6][8][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(6, 8, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[6][8][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(6, 8, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[6][8][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(6, 8, self.c['switch_types']['right_exit_railroad_switch'])

        self.junctions[9] = {}
        self.junctions[9][11] = {}
        self.junctions[9][11][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(9, 11, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[9][11][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(9, 11, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[9][11][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(9, 11, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[9][11][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(9, 11, self.c['switch_types']['right_exit_railroad_switch'])

        self.junctions[10] = {}
        self.junctions[10][12] = {}
        self.junctions[10][12][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(10, 12, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[10][12][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(10, 12, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[10][12][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(10, 12, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[10][12][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(10, 12, self.c['switch_types']['right_exit_railroad_switch'])

        self.junctions[13] = {}
        self.junctions[13][15] = {}
        self.junctions[13][15][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(13, 15, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[13][15][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(13, 15, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[13][15][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(13, 15, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[13][15][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(13, 15, self.c['switch_types']['right_exit_railroad_switch'])

        self.junctions[14] = {}
        self.junctions[14][16] = {}
        self.junctions[14][16][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(14, 16, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[14][16][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(14, 16, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[14][16][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(14, 16, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[14][16][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(14, 16, self.c['switch_types']['right_exit_railroad_switch'])

        self.junctions[17] = {}
        self.junctions[17][19] = {}
        self.junctions[17][19][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(17, 19, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[17][19][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(17, 19, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[17][19][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(17, 19, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[17][19][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(17, 19, self.c['switch_types']['right_exit_railroad_switch'])

        self.junctions[18] = {}
        self.junctions[18][20] = {}
        self.junctions[18][20][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(18, 20, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[18][20][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(18, 20, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[18][20][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(18, 20, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[18][20][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(18, 20, self.c['switch_types']['right_exit_railroad_switch'])

        self.junctions[21] = {}
        self.junctions[21][3] = {}
        self.junctions[21][3][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(21, 3, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[21][3][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(21, 3, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[21][5] = {}
        self.junctions[21][5][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(21, 5, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[21][5][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(21, 5, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[21][9] = {}
        self.junctions[21][9][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(21, 9, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[21][9][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(21, 9, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[21][13] = {}
        self.junctions[21][13][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(21, 13, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[21][13][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(21, 13, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[21][17] = {}
        self.junctions[21][17][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(21, 17, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[21][17][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(21, 17, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[21][23] = {}
        self.junctions[21][23][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(21, 23, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[21][23][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(21, 23, self.c['switch_types']['right_exit_railroad_switch'])
        self.junctions[21][23][self.c['crossover_types']['left_entry_crossover']] \
            = Crossover(21, 23, self.c['crossover_types']['left_entry_crossover'])

        self.junctions[22] = {}
        self.junctions[22][4] = {}
        self.junctions[22][4][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(22, 4, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[22][4][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(22, 4, self.c['switch_types']['right_exit_railroad_switch'])
        self.junctions[22][6] = {}
        self.junctions[22][6][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(22, 6, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[22][6][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(22, 6, self.c['switch_types']['right_exit_railroad_switch'])
        self.junctions[22][10] = {}
        self.junctions[22][10][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(22, 10, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[22][10][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(22, 10, self.c['switch_types']['right_exit_railroad_switch'])
        self.junctions[22][14] = {}
        self.junctions[22][14][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(22, 14, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[22][14][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(22, 14, self.c['switch_types']['right_exit_railroad_switch'])
        self.junctions[22][18] = {}
        self.junctions[22][18][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(22, 18, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[22][18][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(22, 18, self.c['switch_types']['right_exit_railroad_switch'])
        self.junctions[22][24] = {}
        self.junctions[22][24][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(22, 24, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[22][24][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(22, 24, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[22][24][self.c['crossover_types']['right_entry_crossover']] \
            = Crossover(22, 24, self.c['crossover_types']['right_entry_crossover'])

        self.junctions[23] = {}
        self.junctions[23][21] = {}
        self.junctions[23][21][self.c['crossover_types']['left_exit_crossover']] \
            = Crossover(23, 21, self.c['crossover_types']['left_exit_crossover'])

        self.junctions[24] = {}
        self.junctions[24][22] = {}
        self.junctions[24][22][self.c['crossover_types']['right_exit_crossover']] \
            = Crossover(24, 22, self.c['crossover_types']['right_exit_crossover'])

        self.junctions[25] = {}
        self.junctions[25][27] = {}
        self.junctions[25][27][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(25, 27, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[25][27][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(25, 27, self.c['switch_types']['right_exit_railroad_switch'])

        self.junctions[26] = {}
        self.junctions[26][28] = {}
        self.junctions[26][28][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(26, 28, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[26][28][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(26, 28, self.c['switch_types']['left_exit_railroad_switch'])

        self.junctions[27] = {}
        self.junctions[27][25] = {}
        self.junctions[27][25][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(27, 25, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[27][25][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(27, 25, self.c['switch_types']['left_exit_railroad_switch'])

        self.junctions[28] = {}
        self.junctions[28][26] = {}
        self.junctions[28][26][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(28, 26, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[28][26][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(28, 26, self.c['switch_types']['right_exit_railroad_switch'])

        self.junctions[29] = {}
        self.junctions[29][3] = {}
        self.junctions[29][3][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(29, 3, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[29][3][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(29, 3, self.c['switch_types']['right_exit_railroad_switch'])
        self.junctions[29][5] = {}
        self.junctions[29][5][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(29, 5, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[29][5][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(29, 5, self.c['switch_types']['right_exit_railroad_switch'])
        self.logger.debug('junctions for track 3 created')
        self.junctions[29][9] = {}
        self.junctions[29][9][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(29, 9, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[29][9][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(29, 9, self.c['switch_types']['right_exit_railroad_switch'])
        self.logger.debug('junctions for track 3 created')
        self.junctions[29][13] = {}
        self.junctions[29][13][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(29, 13, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[29][13][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(29, 13, self.c['switch_types']['right_exit_railroad_switch'])
        self.junctions[29][17] = {}
        self.junctions[29][17][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(29, 17, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[29][17][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(29, 17, self.c['switch_types']['right_exit_railroad_switch'])
        self.junctions[29][21] = {}
        self.junctions[29][21][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(29, 21, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[29][21][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(29, 21, self.c['switch_types']['right_exit_railroad_switch'])
        self.junctions[29][25] = {}
        self.junctions[29][25][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(29, 25, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[29][25][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(29, 25, self.c['switch_types']['right_exit_railroad_switch'])
        self.junctions[29][27] = {}
        self.junctions[29][27][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(29, 27, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[29][27][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(29, 27, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[29][31] = {}
        self.junctions[29][31][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(29, 31, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[29][31][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(29, 31, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[29][31][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(29, 31, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[29][31][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(29, 31, self.c['switch_types']['right_exit_railroad_switch'])
        self.logger.debug('junctions for track 3 created')

        self.junctions[30] = {}
        self.junctions[30][4] = {}
        self.junctions[30][4][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(30, 4, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[30][4][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(30, 4, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[30][6] = {}
        self.junctions[30][6][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(30, 6, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[30][6][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(30, 6, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[30][10] = {}
        self.junctions[30][10][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(30, 10, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[30][10][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(30, 10, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[30][14] = {}
        self.junctions[30][14][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(30, 14, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[30][14][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(30, 14, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[30][18] = {}
        self.junctions[30][18][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(30, 18, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[30][18][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(30, 18, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[30][22] = {}
        self.junctions[30][22][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(30, 22, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[30][22][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(30, 22, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[30][26] = {}
        self.junctions[30][26][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(30, 26, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[30][26][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(30, 26, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[30][28] = {}
        self.junctions[30][28][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(30, 28, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[30][28][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(30, 28, self.c['switch_types']['right_exit_railroad_switch'])
        self.junctions[30][32] = {}
        self.junctions[30][32][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(30, 32, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[30][32][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(30, 32, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[30][32][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(30, 32, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[30][32][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(30, 32, self.c['switch_types']['right_exit_railroad_switch'])
        self.logger.debug('junctions for track 4 created')

        self.junctions[101] = {}
        self.junctions[101][21] = {}
        self.junctions[101][21][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(101, 21, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[101][21][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(101, 21, self.c['switch_types']['left_exit_railroad_switch'])
        self.junctions[101][103] = {}
        self.junctions[101][103][self.c['crossover_types']['left_entry_crossover']] \
            = Crossover(101, 103, self.c['crossover_types']['left_entry_crossover'])
        self.junctions[101][103][self.c['crossover_types']['left_exit_crossover']] \
            = Crossover(101, 103, self.c['crossover_types']['left_exit_crossover'])
        self.logger.info('all junctions created')

        self.junctions[21][23][self.c['crossover_types']['left_entry_crossover']].dependency \
            = self.junctions[23][21][self.c['crossover_types']['left_exit_crossover']]
        self.junctions[23][21][self.c['crossover_types']['left_exit_crossover']].dependency \
            = self.junctions[21][23][self.c['crossover_types']['left_entry_crossover']]
        self.junctions[22][24][self.c['crossover_types']['right_entry_crossover']].dependency \
            = self.junctions[24][22][self.c['crossover_types']['right_exit_crossover']]
        self.junctions[24][22][self.c['crossover_types']['right_exit_crossover']].dependency \
            = self.junctions[22][24][self.c['crossover_types']['right_entry_crossover']]

        for i in self.junctions:
            for j in self.junctions[i]:
                for k in self.junctions[i][j]:
                    if k == self.c['switch_types']['left_entry_railroad_switch']:
                        self.junctions[i][j][k].dependency \
                            = self.junctions[i][j][self.c['switch_types']['left_exit_railroad_switch']]
                    elif k == self.c['switch_types']['left_exit_railroad_switch']:
                        self.junctions[i][j][k].dependency \
                            = self.junctions[i][j][self.c['switch_types']['left_entry_railroad_switch']]
                    elif k == self.c['switch_types']['right_entry_railroad_switch']:
                        self.junctions[i][j][k].dependency \
                            = self.junctions[i][j][self.c['switch_types']['right_exit_railroad_switch']]
                    elif k == self.c['switch_types']['right_exit_railroad_switch']:
                        self.junctions[i][j][k].dependency \
                            = self.junctions[i][j][self.c['switch_types']['right_entry_railroad_switch']]
                    elif k == self.c['crossover_types']['left_entry_crossover'] and i in (1, 2, 101, 102):
                        self.junctions[i][j][k].dependency \
                            = self.junctions[i][j][self.c['crossover_types']['left_exit_crossover']]
                    elif k == self.c['crossover_types']['left_exit_crossover'] and i in (1, 2, 101, 102):
                        self.junctions[i][j][k].dependency \
                            = self.junctions[i][j][self.c['crossover_types']['left_entry_crossover']]
                    elif k == self.c['crossover_types']['right_entry_crossover'] and i in (1, 2, 101, 102):
                        self.junctions[i][j][k].dependency \
                            = self.junctions[i][j][self.c['crossover_types']['right_exit_crossover']]
                    elif k == self.c['crossover_types']['right_exit_crossover'] and i in (1, 2, 101, 102):
                        self.junctions[i][j][k].dependency \
                            = self.junctions[i][j][self.c['crossover_types']['right_entry_crossover']]

        self.logger.info('all junctions associated')

    def create_onboarding_tips(self):
        saved_onboarding_image = pyglet.image.load('img/game_saved.png')
        self.saved_onboarding_tip \
            = OnboardingTips(image=saved_onboarding_image,
                             x=self.c['graphics']['screen_resolution'][0] // 2 - saved_onboarding_image.width // 2,
                             y=self.c['graphics']['screen_resolution'][1] // 2 - saved_onboarding_image.height // 2,
                             tip_type='game_saved', batch=self.batch,
                             group=self.top_bottom_bars_clock_face_ordered_group,
                             viewport_border_group=self.buttons_general_borders_day_text_ordered_group)
        self.objects.append(self.saved_onboarding_tip)
        self.mini_map_tip.update_image(pyglet.image.load('img/mini_map/{}/mini_map.png'
                                                         .format(self.dispatcher.unlocked_tracks)))
        self.dispatcher.mini_map_tip = self.mini_map_tip
        self.objects.append(self.mini_map_tip)
        self.logger.debug('saved_onboarding_tip appended to global objects list')
        self.logger.info('all tips appended to global objects list')

    def create_buttons(self):
        self.logger.debug('------- START CREATING BUTTONS -------')

        def pause_game(button):
            self.game_paused = True
            self.logger.critical('------- GAME IS PAUSED -------')

        def resume_game(button):
            self.game_paused = False
            self.saved_onboarding_tip.condition_met = False
            self.saved_onboarding_tip.return_rect_area = True
            self.logger.critical('------- GAME IS RESUMED -------')

        def close_game(button):
            self.surface.close()
            sys.exit()

        def iconify_game(button):
            self.surface.minimize()

        def save_game(button):
            self.logger.critical('------- GAME SAVE START -------')
            for i in self.objects:
                i.save_state()

            self.saved_onboarding_tip.condition_met = True
            self.logger.critical('------- GAME SAVE END -------')

        self.objects.append(InGameTime(batch=self.batch,
                                       clock_face_group=self.top_bottom_bars_clock_face_ordered_group,
                                       day_text_group=self.buttons_general_borders_day_text_ordered_group,
                                       minute_hand_group=self.buttons_text_minute_hand_ordered_group,
                                       hour_hand_group=self.buttons_borders_hour_hand_ordered_group))
        self.logger.debug('time appended to global objects list')
        self.objects.append(TopAndBottomBar(batch=self.batch,
                                            bar_group=self.top_bottom_bars_clock_face_ordered_group,
                                            border_group=self.buttons_general_borders_day_text_ordered_group))
        self.logger.debug('bottom bar appended to global objects list')
        stop_button = Button(position=(890, 7), button_size=(100, 40), text=['Pause', 'Resume'],
                             on_click=[pause_game, resume_game], draw_only_if_game_paused=False,
                             batch=self.batch, button_group=self.buttons_general_borders_day_text_ordered_group,
                             text_group=self.buttons_text_minute_hand_ordered_group,
                             borders_group=self.buttons_borders_hour_hand_ordered_group)
        save_button = Button(position=(780, 7), button_size=(100, 40), text=['Save', ], on_click=[save_game, ],
                             draw_only_if_game_paused=True,
                             batch=self.batch, button_group=self.buttons_general_borders_day_text_ordered_group,
                             text_group=self.buttons_text_minute_hand_ordered_group,
                             borders_group=self.buttons_borders_hour_hand_ordered_group)
        close_button = Button(position=(self.c['graphics']['screen_resolution'][0] - 34,
                                        self.c['graphics']['screen_resolution'][1] - 34), button_size=(34, 34),
                              text=['X', ], on_click=[close_game, ], draw_only_if_game_paused=False,
                              batch=self.batch, button_group=self.buttons_general_borders_day_text_ordered_group,
                              text_group=self.buttons_text_minute_hand_ordered_group,
                              borders_group=self.buttons_borders_hour_hand_ordered_group)
        iconify_button = Button(position=(self.c['graphics']['screen_resolution'][0] - 66,
                                          self.c['graphics']['screen_resolution'][1] - 34), button_size=(34, 34),
                                text=['_', ], on_click=[iconify_game, ], draw_only_if_game_paused=False,
                                batch=self.batch, button_group=self.buttons_general_borders_day_text_ordered_group,
                                text_group=self.buttons_text_minute_hand_ordered_group,
                                borders_group=self.buttons_borders_hour_hand_ordered_group)
        self.on_mouse_press_handlers.append(stop_button.handle_mouse_press)
        self.on_mouse_press_handlers.append(save_button.handle_mouse_press)
        self.on_mouse_press_handlers.append(close_button.handle_mouse_press)
        self.on_mouse_press_handlers.append(iconify_button.handle_mouse_press)
        self.on_mouse_press_handlers.append(self.handle_mouse_press)

        self.on_mouse_release_handlers.append(stop_button.handle_mouse_release)
        self.on_mouse_release_handlers.append(save_button.handle_mouse_release)
        self.on_mouse_release_handlers.append(close_button.handle_mouse_release)
        self.on_mouse_release_handlers.append(iconify_button.handle_mouse_release)
        self.on_mouse_release_handlers.append(self.handle_mouse_release)

        self.on_mouse_motion_handlers.append(stop_button.handle_mouse_motion)
        self.on_mouse_motion_handlers.append(save_button.handle_mouse_motion)
        self.on_mouse_motion_handlers.append(close_button.handle_mouse_motion)
        self.on_mouse_motion_handlers.append(iconify_button.handle_mouse_motion)

        self.on_mouse_drag_handlers.append(self.handle_mouse_drag)
        self.logger.debug('save button button handler appended to global mouse handlers list')
        self.objects.append(stop_button)
        self.logger.debug('pause/resume button appended to global objects list')
        self.objects.append(save_button)
        self.objects.append(close_button)
        self.objects.append(iconify_button)
        self.logger.debug('save button appended to global objects list')
        self.logger.debug('------- END CREATING BUTTONS -------')
        self.logger.warning('all buttons created')


def main():
    try:
        RSSim().run()
    except VideoAdapterNotSupportedException as e:
        if e.surface is not None:
            e.surface.close()

        win32api.MessageBoxEx(win32con.NULL, e.text, e.caption,
                              win32con.MB_OK | win32con.MB_ICONERROR | win32con.MB_DEFBUTTON1
                              | win32con.MB_SYSTEMMODAL | win32con.MB_SETFOREGROUND, 0)
        sys.exit()


if __name__ == '__main__':
    main()
