import win32api
import win32con
import win32gui
import sys

import pygame

from base_route import BaseRoute
from bgimg import BgImg
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
        self.game_window_handler = win32gui.GetActiveWindow()
        self.game_window_position = win32gui.GetWindowRect(self.game_window_handler)
        self.absolute_mouse_pos = win32api.GetCursorPos()
        pygame.mouse.set_pos([0, 0])
        temp_absolute_mouse_pos = win32api.GetCursorPos()
        self.system_borders = (temp_absolute_mouse_pos[0] - self.game_window_position[0],
                               temp_absolute_mouse_pos[1] - self.game_window_position[1])
        win32api.SetCursorPos(self.absolute_mouse_pos)
        self.logger.critical('rssim game created')
        self.logger.debug('------- START INIT -------')
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
        self.app_window_move_mode = False
        self.app_window_move_offset = ()
        self.mouse_handlers.append(self.handle_app_window_drag)
        self.mouse_handlers.append(self.handle_map_drag)
        self.logger.debug('map drag event appended')
        self.logger.debug('------- END INIT -------')
        self.logger.warning('rssim game init completed')

    def create_bg_img(self):
        self.logger.debug('------- START CREATING BG IMAGE -------')
        background_image = BgImg(self.c['graphics']['background_image'])
        self.logger.info('background image object created')
        self.objects.append(background_image)
        self.logger.debug('background image object appended')
        self.logger.debug('------- END CREATING BG IMAGE -------')

    def create_infrastructure(self):
        self.logger.debug('------- START CREATING INFRASTRUCTURE -------')
        # ------ BASE ROUTES AND SIGNALS ------
        # create main entry and main exit base routes and signals for them
        for j in (self.c['base_route_types']['left_entry_base_route'],
                  self.c['base_route_types']['left_exit_base_route'],
                  self.c['base_route_types']['right_entry_base_route'],
                  self.c['base_route_types']['right_exit_base_route']):
            self.base_routes[0][j] = BaseRoute(0, j)
            self.base_routes[0][j].read_trail_points()
            placement = self.base_routes[0][j].route_config['exit_signal_placement']
            self.logger.debug('placement = {}'.format(placement))
            flip_needed = self.base_routes[0][j].route_config['flip_needed']
            self.logger.debug('flip_needed = {}'.format(flip_needed))
            invisible = self.base_routes[0][j].route_config['invisible_signal']
            self.logger.debug('invisible = {}'.format(invisible))
            if placement is not None:
                self.signals[0][j] = Signal(placement, flip_needed, invisible, 0, j)

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
            for k in (self.c['base_route_types']['left_entry_base_route'],
                      self.c['base_route_types']['left_exit_base_route'],
                      self.c['base_route_types']['right_entry_base_route'],
                      self.c['base_route_types']['right_exit_base_route'],
                      self.c['base_route_types']['left_entry_platform_base_route'],
                      self.c['base_route_types']['left_exit_platform_base_route'],
                      self.c['base_route_types']['right_entry_platform_base_route'],
                      self.c['base_route_types']['right_exit_platform_base_route']):
                self.base_routes[i][k] = BaseRoute(i, k)
                if k in (self.c['base_route_types']['left_entry_platform_base_route'],
                         self.c['base_route_types']['left_exit_platform_base_route'],
                         self.c['base_route_types']['right_entry_platform_base_route'],
                         self.c['base_route_types']['right_exit_platform_base_route']):
                    self.base_routes[i][k].read_trail_points()

                placement = self.base_routes[i][k].route_config['exit_signal_placement']
                self.logger.debug('placement = {}'.format(placement))
                flip_needed = self.base_routes[i][k].route_config['flip_needed']
                self.logger.debug('flip_needed = {}'.format(flip_needed))
                invisible = self.base_routes[i][k].route_config['invisible_signal']
                self.logger.debug('invisible = {}'.format(invisible))
                if placement is not None and k in (self.c['base_route_types']['right_exit_platform_base_route'],
                                                   self.c['base_route_types']['left_exit_platform_base_route']):
                    self.signals[i][k] = Signal(placement, flip_needed, invisible, i, k)

            self.logger.debug('track {} base routes and signals created'.format(i))

        self.logger.info('base routes and signals created for all tracks')

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

        self.junctions[21] = {}
        self.junctions[21][3] = {}
        self.junctions[21][3][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(21, 3, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[21][3][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(21, 3, self.c['switch_types']['left_exit_railroad_switch'])

        self.junctions[22] = {}
        self.junctions[22][4] = {}
        self.junctions[22][4][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(22, 4, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[22][4][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(22, 4, self.c['switch_types']['right_exit_railroad_switch'])

        self.junctions[29] = {}
        self.junctions[29][3] = {}
        self.junctions[29][3][self.c['switch_types']['right_entry_railroad_switch']] \
            = RailroadSwitch(29, 3, self.c['switch_types']['right_entry_railroad_switch'])
        self.junctions[29][3][self.c['switch_types']['right_exit_railroad_switch']] \
            = RailroadSwitch(29, 3, self.c['switch_types']['right_exit_railroad_switch'])
        self.logger.debug('junctions for track 3 created')

        self.junctions[30] = {}
        self.junctions[30][4] = {}
        self.junctions[30][4][self.c['switch_types']['left_entry_railroad_switch']] \
            = RailroadSwitch(30, 4, self.c['switch_types']['left_entry_railroad_switch'])
        self.junctions[30][4][self.c['switch_types']['left_exit_railroad_switch']] \
            = RailroadSwitch(30, 4, self.c['switch_types']['left_exit_railroad_switch'])
        self.logger.debug('junctions for track 4 created')
        self.logger.info('all junctions created')

        self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']].dependency \
            = self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']]
        self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']].dependency \
            = self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']]
        self.logger.debug('main left crossovers associated')
        self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']].dependency \
            = self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']]
        self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']].dependency \
            = self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']]
        self.logger.debug('main right crossovers associated')

        for i in self.junctions:
            for j in self.junctions[i]:
                for k in self.junctions[i][j]:
                    if k == self.c['switch_types']['left_entry_railroad_switch']:
                        self.junctions[i][j][k].dependency \
                            = self.junctions[i][j][self.c['switch_types']['left_exit_railroad_switch']]
                        self.logger.debug('{} {} {} and {} associated'
                                          .format(i, j, k, self.c['switch_types']['left_exit_railroad_switch']))
                    elif k == self.c['switch_types']['left_exit_railroad_switch']:
                        self.junctions[i][j][k].dependency \
                            = self.junctions[i][j][self.c['switch_types']['left_entry_railroad_switch']]
                        self.logger.debug('{} {} {} and {} associated'
                                          .format(i, j, k, self.c['switch_types']['left_entry_railroad_switch']))
                    elif k == self.c['switch_types']['right_entry_railroad_switch']:
                        self.junctions[i][j][k].dependency \
                            = self.junctions[i][j][self.c['switch_types']['right_exit_railroad_switch']]
                        self.logger.debug('{} {} {} and {} associated'
                                          .format(i, j, k, self.c['switch_types']['right_exit_railroad_switch']))
                    elif k == self.c['switch_types']['right_exit_railroad_switch']:
                        self.junctions[i][j][k].dependency \
                            = self.junctions[i][j][self.c['switch_types']['right_entry_railroad_switch']]
                        self.logger.debug('{} {} {} and {} associated'
                                          .format(i, j, k, self.c['switch_types']['right_entry_railroad_switch']))

        self.logger.info('all junctions associated')

        self.base_routes[1][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[1][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 1])
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(2, 1, self.c['crossover_types']['left_entry_crossover'], [2, 1], 1,
                                  self.c['base_route_types']['left_entry_base_route']))
        self.base_routes[1][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[1][self.c['base_route_types']['left_entry_base_route']].junction_position.append(1)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(1, 21, self.c['switch_types']['left_entry_railroad_switch'], 1, 1,
                                  self.c['base_route_types']['left_entry_base_route']))
        self.logger.debug('junctions appended to base route {} {}'
                          .format(1, self.c['base_route_types']['left_entry_base_route']))

        self.base_routes[1][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[1][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 1])
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(1, 2, self.c['crossover_types']['right_entry_crossover'], [1, 1], 1,
                                  self.c['base_route_types']['right_entry_base_route']))
        self.base_routes[1][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[1][self.c['base_route_types']['right_entry_base_route']].junction_position.append(1)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(1, 29, self.c['crossover_types']['right_entry_crossover'], 1, 1,
                                  self.c['base_route_types']['right_entry_base_route']))
        self.logger.debug('junctions appended to base route {} {}'
                          .format(1, self.c['base_route_types']['right_entry_base_route']))

        self.base_routes[1][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[1][21][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[1][self.c['base_route_types']['left_exit_base_route']].junction_position.append(1)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(1, 21, self.c['switch_types']['left_exit_railroad_switch'], 1, 1,
                                  self.c['base_route_types']['left_exit_base_route']))
        self.base_routes[1][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[1][self.c['base_route_types']['left_exit_base_route']].junction_position.append([1, 1])
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(2, 1, self.c['crossover_types']['left_exit_crossover'], [1, 1], 1,
                                  self.c['base_route_types']['left_exit_base_route']))
        self.logger.debug('junctions appended to base route {} {}'
                          .format(1, self.c['base_route_types']['left_exit_base_route']))

        self.base_routes[1][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[1][self.c['base_route_types']['right_exit_base_route']].junction_position.append(1)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(1, 29, self.c['switch_types']['right_exit_railroad_switch'], 1, 1,
                                  self.c['base_route_types']['right_exit_base_route']))
        self.base_routes[1][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[1][self.c['base_route_types']['right_exit_base_route']].junction_position.append([1, 2])
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(1, 2, self.c['crossover_types']['right_exit_crossover'], [1, 2], 1,
                                  self.c['base_route_types']['right_exit_base_route']))
        self.logger.debug('junctions appended to base route {} {}'
                          .format(1, self.c['base_route_types']['right_exit_base_route']))

        self.base_routes[3][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[3][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 1])
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(2, 1, self.c['crossover_types']['left_entry_crossover'], [2, 1], 3,
                                  self.c['base_route_types']['left_entry_base_route']))
        self.base_routes[3][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[3][self.c['base_route_types']['left_entry_base_route']].junction_position.append(21)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(1, 21, self.c['switch_types']['left_entry_railroad_switch'], 21, 3,
                                  self.c['base_route_types']['left_entry_base_route']))
        self.base_routes[3][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[21][3][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[3][self.c['base_route_types']['left_entry_base_route']].junction_position.append(3)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(21, 3, self.c['switch_types']['left_entry_railroad_switch'], 3, 3,
                                  self.c['base_route_types']['left_entry_base_route']))
        self.logger.debug('junctions appended to base route {} {}'
                          .format(3, self.c['base_route_types']['left_entry_base_route']))

        self.base_routes[3][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[3][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 1])
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(1, 2, self.c['crossover_types']['right_entry_crossover'], [1, 1], 3,
                                  self.c['base_route_types']['right_entry_base_route']))
        self.base_routes[3][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[3][self.c['base_route_types']['right_entry_base_route']].junction_position.append(29)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(1, 29, self.c['switch_types']['right_entry_railroad_switch'], 29, 3,
                                  self.c['base_route_types']['right_entry_base_route']))
        self.base_routes[3][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[29][3][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[3][self.c['base_route_types']['right_entry_base_route']].junction_position.append(3)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(29, 3, self.c['switch_types']['right_entry_railroad_switch'], 3, 3,
                                  self.c['base_route_types']['right_entry_base_route']))
        self.logger.debug('junctions appended to base route {} {}'
                          .format(3, self.c['base_route_types']['right_entry_base_route']))

        self.base_routes[3][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[21][3][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[3][self.c['base_route_types']['left_exit_base_route']].junction_position.append(3)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(21, 3, self.c['switch_types']['left_exit_railroad_switch'], 3, 3,
                                  self.c['base_route_types']['left_exit_base_route']))
        self.base_routes[3][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[1][21][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[3][self.c['base_route_types']['left_exit_base_route']].junction_position.append(21)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(1, 21, self.c['switch_types']['left_exit_railroad_switch'], 21, 3,
                                  self.c['base_route_types']['left_exit_base_route']))
        self.base_routes[3][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[3][self.c['base_route_types']['left_exit_base_route']].junction_position.append([1, 1])
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(2, 1, self.c['crossover_types']['left_exit_crossover'], [1, 1], 3,
                                  self.c['base_route_types']['left_exit_base_route']))
        self.logger.debug('junctions appended to base route {} {}'
                          .format(3, self.c['base_route_types']['left_exit_base_route']))

        self.base_routes[3][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[29][3][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[3][self.c['base_route_types']['right_exit_base_route']].junction_position.append(3)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(29, 3, self.c['switch_types']['right_exit_railroad_switch'], 3, 3,
                                  self.c['base_route_types']['right_exit_base_route']))
        self.base_routes[3][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[1][29][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[3][self.c['base_route_types']['right_exit_base_route']].junction_position.append(29)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(1, 29, self.c['switch_types']['right_exit_railroad_switch'], 29, 3,
                                  self.c['base_route_types']['right_exit_base_route']))
        self.base_routes[3][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[3][self.c['base_route_types']['right_exit_base_route']].junction_position.append([1, 2])
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(1, 2, self.c['crossover_types']['right_exit_crossover'], [1, 2], 3,
                                  self.c['base_route_types']['right_exit_base_route']))
        self.logger.debug('junctions appended to base route {} {}'
                          .format(3, self.c['base_route_types']['right_exit_base_route']))

        for i in range(1, self.c['dispatcher_config']['tracks_ready'] + 1, 2):
            self.base_routes[i][self.c['base_route_types']['left_entry_base_route']].read_trail_points()
            self.base_routes[i][self.c['base_route_types']['left_exit_base_route']].read_trail_points()
            self.base_routes[i][self.c['base_route_types']['right_entry_base_route']].read_trail_points()
            self.base_routes[i][self.c['base_route_types']['right_exit_base_route']].read_trail_points()

        self.logger.info('trail points initialized for odd tracks')

        self.base_routes[2][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[2][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 2])
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(2, 1, self.c['crossover_types']['left_entry_crossover'], [2, 2], 2,
                                  self.c['base_route_types']['left_entry_base_route']))
        self.base_routes[2][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[2][self.c['base_route_types']['left_entry_base_route']].junction_position.append(2)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(2, 30, self.c['crossover_types']['left_entry_crossover'], 2, 2,
                                  self.c['base_route_types']['left_entry_base_route']))
        self.logger.debug('junctions appended to base route {} {}'
                          .format(2, self.c['base_route_types']['left_entry_base_route']))

        self.base_routes[2][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[2][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 2])
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(1, 2, self.c['crossover_types']['right_entry_crossover'], [1, 2], 2,
                                  self.c['base_route_types']['right_entry_base_route']))
        self.base_routes[2][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[2][self.c['base_route_types']['right_entry_base_route']].junction_position.append(2)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(2, 22, self.c['switch_types']['right_entry_railroad_switch'], 2, 2,
                                  self.c['base_route_types']['right_entry_base_route']))
        self.logger.debug('junctions appended to base route {} {}'
                          .format(2, self.c['base_route_types']['right_entry_base_route']))

        self.base_routes[2][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[2][self.c['base_route_types']['left_exit_base_route']].junction_position.append(2)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(2, 30, self.c['switch_types']['left_exit_railroad_switch'], 2, 2,
                                  self.c['base_route_types']['left_exit_base_route']))
        self.base_routes[2][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[2][self.c['base_route_types']['left_exit_base_route']].junction_position.append([2, 1])
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(2, 1, self.c['crossover_types']['left_exit_crossover'], [2, 1], 2,
                                  self.c['base_route_types']['left_exit_base_route']))
        self.logger.debug('junctions appended to base route {} {}'
                          .format(2, self.c['base_route_types']['left_exit_base_route']))

        self.base_routes[2][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[2][self.c['base_route_types']['right_exit_base_route']].junction_position.append(2)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(2, 22, self.c['switch_types']['right_exit_railroad_switch'], 2, 2,
                                  self.c['base_route_types']['right_exit_base_route']))
        self.base_routes[2][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[2][self.c['base_route_types']['right_exit_base_route']].junction_position.append([2, 2])
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(1, 2, self.c['crossover_types']['right_exit_crossover'], [2, 2], 2,
                                  self.c['base_route_types']['right_exit_base_route']))
        self.logger.debug('junctions appended to base route {} {}'
                          .format(2, self.c['base_route_types']['right_exit_base_route']))

        self.base_routes[4][self.c['base_route_types']['left_entry_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_entry_crossover']])
        self.base_routes[4][self.c['base_route_types']['left_entry_base_route']].junction_position.append([2, 2])
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(2, 1, self.c['crossover_types']['left_entry_crossover'], [2, 2], 4,
                                  self.c['base_route_types']['left_entry_base_route']))
        self.base_routes[4][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[4][self.c['base_route_types']['left_entry_base_route']].junction_position.append(30)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(2, 30, self.c['switch_types']['left_entry_railroad_switch'], 30, 4,
                                  self.c['base_route_types']['left_entry_base_route']))
        self.base_routes[4][self.c['base_route_types']['left_entry_base_route']].junctions \
            .append(self.junctions[30][4][self.c['switch_types']['left_entry_railroad_switch']])
        self.base_routes[4][self.c['base_route_types']['left_entry_base_route']].junction_position.append(4)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(30, 4, self.c['switch_types']['left_entry_railroad_switch'], 4, 4,
                                  self.c['base_route_types']['left_entry_base_route']))
        self.logger.debug('junctions appended to base route {} {}'
                          .format(4, self.c['base_route_types']['left_entry_base_route']))

        self.base_routes[4][self.c['base_route_types']['right_entry_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_entry_crossover']])
        self.base_routes[4][self.c['base_route_types']['right_entry_base_route']].junction_position.append([1, 2])
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(1, 2, self.c['crossover_types']['right_entry_crossover'], [1, 2], 4,
                                  self.c['base_route_types']['right_entry_base_route']))
        self.base_routes[4][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[4][self.c['base_route_types']['right_entry_base_route']].junction_position.append(22)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(2, 22, self.c['switch_types']['right_entry_railroad_switch'], 22, 4,
                                  self.c['base_route_types']['right_entry_base_route']))
        self.base_routes[4][self.c['base_route_types']['right_entry_base_route']].junctions \
            .append(self.junctions[22][4][self.c['switch_types']['right_entry_railroad_switch']])
        self.base_routes[4][self.c['base_route_types']['right_entry_base_route']].junction_position.append(4)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(22, 4, self.c['switch_types']['right_entry_railroad_switch'], 4, 4,
                                  self.c['base_route_types']['right_entry_base_route']))
        self.logger.debug('junctions appended to base route {} {}'
                          .format(4, self.c['base_route_types']['right_entry_base_route']))

        self.base_routes[4][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[30][4][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[4][self.c['base_route_types']['left_exit_base_route']].junction_position.append(4)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(30, 4, self.c['switch_types']['left_exit_railroad_switch'], 4, 4,
                                  self.c['base_route_types']['left_exit_base_route']))
        self.base_routes[4][self.c['base_route_types']['left_exit_base_route']].junctions \
            .append(self.junctions[2][30][self.c['switch_types']['left_exit_railroad_switch']])
        self.base_routes[4][self.c['base_route_types']['left_exit_base_route']].junction_position.append(30)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(2, 30, self.c['switch_types']['left_exit_railroad_switch'], 30, 4,
                                  self.c['base_route_types']['left_exit_base_route']))
        self.base_routes[4][self.c['base_route_types']['left_exit_base_route']].junctions\
            .append(self.junctions[2][1][self.c['crossover_types']['left_exit_crossover']])
        self.base_routes[4][self.c['base_route_types']['left_exit_base_route']].junction_position.append([2, 1])
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(2, 1, self.c['crossover_types']['left_exit_crossover'], [2, 1], 4,
                                  self.c['base_route_types']['left_exit_base_route']))
        self.logger.debug('junctions appended to base route {} {}'
                          .format(4, self.c['base_route_types']['left_exit_base_route']))

        self.base_routes[4][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[22][4][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[4][self.c['base_route_types']['right_exit_base_route']].junction_position.append(4)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(22, 4, self.c['switch_types']['right_exit_railroad_switch'], 4, 4,
                                  self.c['base_route_types']['right_exit_base_route']))
        self.base_routes[4][self.c['base_route_types']['right_exit_base_route']].junctions \
            .append(self.junctions[2][22][self.c['switch_types']['right_exit_railroad_switch']])
        self.base_routes[4][self.c['base_route_types']['right_exit_base_route']].junction_position.append(22)
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(2, 22, self.c['switch_types']['right_exit_railroad_switch'], 22, 4,
                                  self.c['base_route_types']['right_exit_base_route']))
        self.base_routes[4][self.c['base_route_types']['right_exit_base_route']].junctions\
            .append(self.junctions[1][2][self.c['crossover_types']['right_exit_crossover']])
        self.base_routes[4][self.c['base_route_types']['right_exit_base_route']].junction_position.append([2, 2])
        self.logger.debug('junction {} {} {} with position {} appended to base route {} {}'
                          .format(1, 2, self.c['crossover_types']['right_exit_crossover'], [2, 2], 4,
                                  self.c['base_route_types']['right_exit_base_route']))
        self.logger.debug('junctions appended to base route {} {}'
                          .format(4, self.c['base_route_types']['right_exit_base_route']))

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
            self.signals[i][self.c['base_route_types']['right_exit_platform_base_route']].base_route_opened_list \
                .append(self.base_routes[i][self.c['base_route_types']['right_exit_base_route']])
            self.logger.debug('base route {} {} appended to signal {} {} opened list'
                              .format(i, self.c['base_route_types']['right_exit_base_route'],
                                      i, self.c['base_route_types']['right_exit_platform_base_route']))
            self.signals[i][self.c['base_route_types']['left_exit_platform_base_route']].base_route_opened_list \
                .append(self.base_routes[i][self.c['base_route_types']['left_exit_base_route']])
            self.logger.debug('base route {} {} appended to signal {} {} opened list'
                              .format(i, self.c['base_route_types']['left_exit_base_route'],
                                      i, self.c['base_route_types']['left_exit_platform_base_route']))
            self.logger.debug('opened list set up for track {} signals'.format(i))

            # for main entry signals, opened list includes all entry base routes
            self.signals[0][self.c['base_route_types']['left_entry_base_route']].base_route_opened_list \
                .append(self.base_routes[i][self.c['base_route_types']['left_entry_base_route']])
            self.logger.debug('base route {} {} appended to signal {} {} opened list'
                              .format(i, self.c['base_route_types']['left_entry_base_route'],
                                      0, self.c['base_route_types']['left_entry_base_route']))
            self.signals[0][self.c['base_route_types']['right_entry_base_route']].base_route_opened_list \
                .append(self.base_routes[i][self.c['base_route_types']['right_entry_base_route']])
            self.logger.debug('base route {} {} appended to signal {} {} opened list'
                              .format(i, self.c['base_route_types']['right_entry_base_route'],
                                      0, self.c['base_route_types']['right_entry_base_route']))

        self.logger.debug('opened list set up for track 0 signals')
        self.logger.info('opened list set up for all signals')

        # ------ TRAIN ROUTES AND TRACKS ------
        # create basic entry train routes for trains which cannot find available track
        base_routes_in_train_route \
            = [self.base_routes[0][
                   '{}_base_route'
                   .format(self.c['train_route_types']['entry_train_route'][self.c['direction']['left']])], ]
        self.train_routes[0][self.c['train_route_types']['approaching_train_route'][self.c['direction']['left']]] \
            = TrainRoute(base_routes_in_train_route,
                         0, self.c['train_route_types']['approaching_train_route'][self.c['direction']['left']])
        base_routes_in_train_route \
            = [self.base_routes[0][
                   '{}_base_route'
                   .format(self.c['train_route_types']['entry_train_route'][self.c['direction']['right']])], ]
        self.train_routes[0][self.c['train_route_types']['approaching_train_route'][self.c['direction']['right']]] \
            = TrainRoute(base_routes_in_train_route,
                         0, self.c['train_route_types']['approaching_train_route'][self.c['direction']['right']])
        self.logger.info('approaching train routes created')

        for i in range(1, self.c['dispatcher_config']['tracks_ready'] + 1):
            self.train_routes.append({})
            # create track object
            # it includes all 4 base routes
            base_routes_in_track = [self.base_routes[i][self.c['base_route_types']['left_entry_platform_base_route']],
                                    self.base_routes[i][self.c['base_route_types']['right_entry_platform_base_route']],
                                    self.base_routes[i][self.c['base_route_types']['left_exit_platform_base_route']],
                                    self.base_routes[i][self.c['base_route_types']['right_exit_platform_base_route']]]
            new_track = Track(i, base_routes_in_track)
            self.tracks.append(new_track)
            self.logger.info('track {} created'.format(i))
            # create entry train route
            # it includes main entry base route, specific entry base route and platform base route
            for k in range(len(self.c['train_route_types']['entry_train_route'])):
                base_routes_in_train_route = [
                    self.base_routes[0]['{}_base_route'.format(self.c['train_route_types']['entry_train_route'][k])],
                    self.base_routes[i]['{}_base_route'.format(self.c['train_route_types']['entry_train_route'][k])],
                    self.base_routes[i]['{}_platform_base_route'
                                        .format(self.c['train_route_types']['entry_train_route'][k])]]

                self.train_routes[i][self.c['train_route_types']['entry_train_route'][k]] \
                    = TrainRoute(base_routes_in_train_route,
                                 i, self.c['train_route_types']['entry_train_route'][k])
                self.logger.info('track {} {} train route created'.format(i, k))

            # create exit train route
            # it includes platform base route, specific exit base route and main exit base route
            for m in range(len(self.c['train_route_types']['exit_train_route'])):
                base_routes_in_train_route = [
                    self.base_routes[i]['{}_platform_base_route'
                                        .format(self.c['train_route_types']['exit_train_route'][m])],
                    self.base_routes[i]['{}_base_route'.format(self.c['train_route_types']['exit_train_route'][m])],
                    self.base_routes[0]['{}_base_route'.format(self.c['train_route_types']['exit_train_route'][m])]]

                self.train_routes[i][self.c['train_route_types']['exit_train_route'][m]] \
                    = TrainRoute(base_routes_in_train_route, i, self.c['train_route_types']['exit_train_route'][m])
                self.logger.info('track {} {} train route created'.format(i, m))

        self.logger.info('tracks and train routes created')
        # ------ SORT THIS OUT ------
        # base routes and signals are added to generic objects list
        for i in self.junctions:
            for j in self.junctions[i]:
                for k in self.junctions[i][j]:
                    self.objects.append(self.junctions[i][j][k])
                    self.logger.debug('junction {} {} {} appended to global objects list'.format(i, j, k))

        for i in range(self.c['dispatcher_config']['tracks_ready'] + 1):
            for n in self.base_routes[i]:
                self.objects.append(self.base_routes[i][n])
                self.logger.debug('base route {} {} appended to global objects list'.format(i, n))

        for i in range(self.c['dispatcher_config']['tracks_ready'] + 1):
            for n in self.signals[i]:
                self.objects.append(self.signals[i][n])
                self.logger.debug('signal {} {} appended to global objects list'.format(i, n))

        self.logger.info('base routes and signals appended')
        # train routes and tracks are added to dispatcher which we create right now
        self.dispatcher = Dispatcher()
        for i in range(self.c['dispatcher_config']['tracks_ready'] + 1):
            self.dispatcher.train_routes.append({})
            for p in self.train_routes[i].keys():
                self.dispatcher.train_routes[i].update({p: self.train_routes[i][p]})
                self.logger.debug('train route {} {} appended to dispatcher'.format(i, p))

        self.logger.info('all train routes appended to dispatcher')
        for i in range(self.c['dispatcher_config']['tracks_ready']):
            self.dispatcher.tracks.append(self.tracks[i])
            self.logger.debug('track {} appended to dispatcher'.format(i + 1))

        self.logger.info('all tracks appended to dispatcher')
        # now we add dispatcher itself to generic objects list
        self.dispatcher.read_state()
        self.objects.append(self.dispatcher)
        self.logger.info('dispatcher appended to global objects list')
        self.logger.debug('------- START CREATING INFRASTRUCTURE -------')
        self.logger.warning('all infrastructure created')

    def create_onboarding_tips(self):
        self.saved_onboarding_tip = OnboardingTips('img/game_saved.png', 'game_saved')
        self.objects.append(self.saved_onboarding_tip)
        self.logger.debug('saved_onboarding_tip appended to global objects list')
        self.logger.info('all tips appended to global objects list')

    def create_buttons(self):
        self.logger.debug('------- START CREATING BUTTONS -------')

        def pause_game(button):
            self.game_paused = True
            self.logger.critical('------- GAME IS PAUSED -------')

        def resume_game(button):
            self.game_paused = False
            self.logger.critical('------- GAME IS RESUMED -------')

        def close_game(button):
            pygame.quit()
            sys.exit()

        def iconify_game(button):
            pygame.display.iconify()

        def save_game(button):
            self.logger.critical('------- GAME SAVE START -------')
            for i in self.objects:
                i.save_state()

            self.saved_onboarding_tip.condition_met = True
            self.logger.critical('------- GAME SAVE END -------')

        self.objects.append(InGameTime())
        self.logger.debug('time appended to global objects list')
        self.objects.append(TopAndBottomBar())
        self.logger.debug('bottom bar appended to global objects list')
        stop_button = Button((890, 673), (100, 40), ['Pause', 'Resume'], [pause_game, resume_game], False)
        save_button = Button((780, 673), (100, 40), ['Save', ], [save_game, ], True)
        close_button = Button((self.c['graphics']['screen_resolution'][0] - 34, 0), (34, 34),
                              ['X', ], [close_game, ], False)
        iconify_button = Button((self.c['graphics']['screen_resolution'][0] - 66, 0), (34, 34),
                                ['_', ], [iconify_game, ], False)
        self.mouse_handlers.append(stop_button.handle_mouse_event)
        self.logger.debug('pause/resume button handler appended to global mouse handlers list')
        self.mouse_handlers.append(save_button.handle_mouse_event)
        self.mouse_handlers.append(close_button.handle_mouse_event)
        self.mouse_handlers.append(iconify_button.handle_mouse_event)
        self.logger.debug('save button button handler appended to global mouse handlers list')
        self.objects.append(stop_button)
        self.logger.debug('pause/resume button appended to global objects list')
        self.objects.append(save_button)
        self.objects.append(close_button)
        self.objects.append(iconify_button)
        self.logger.debug('save button appended to global objects list')
        self.logger.debug('------- END CREATING BUTTONS -------')
        self.logger.warning('all buttons created')

    def handle_map_drag(self, event_type, pos):
        self.mouse_movement = pygame.mouse.get_rel()
        if event_type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0] \
                and pos[1] in range(self.c['graphics']['top_bar_height'],
                                    self.c['graphics']['screen_resolution'][1]
                                    - self.c['graphics']['bottom_bar_height']):
            # if left mouse button is pressed and user moves mouse, we move entire map with all its content
            self.logger.debug('user drags map')
            self.logger.debug('old offset: {}'.format(self.base_offset))
            self.base_offset = (self.base_offset[0] + self.mouse_movement[0],
                                self.base_offset[1] + self.mouse_movement[1])
            self.logger.debug('mouse movement: {}'.format(self.mouse_movement))
            self.logger.debug('new offset: {}'.format(self.base_offset))
            # but not beyond limits
            if self.base_offset[0] > self.c['graphics']['base_offset_lower_right_limit'][0]:
                self.base_offset = (self.c['graphics']['base_offset_lower_right_limit'][0], self.base_offset[1])
            if self.base_offset[0] < self.c['graphics']['base_offset_upper_left_limit'][0]:
                self.base_offset = (self.c['graphics']['base_offset_upper_left_limit'][0], self.base_offset[1])
            if self.base_offset[1] > self.c['graphics']['base_offset_lower_right_limit'][1]:
                self.base_offset = (self.base_offset[0], self.c['graphics']['base_offset_lower_right_limit'][1])
            if self.base_offset[1] < self.c['graphics']['base_offset_upper_left_limit'][1]:
                self.base_offset = (self.base_offset[0], self.c['graphics']['base_offset_upper_left_limit'][1])

            self.logger.debug('new limited offset: {}'.format(self.base_offset))

    def handle_app_window_drag(self, event_type, pos):
        if pygame.display.get_active():
            if event_type == pygame.MOUSEBUTTONDOWN \
                    and pos[0] in range(0, self.c['graphics']['screen_resolution'][0] - 70) \
                    and pos[1] in range(0, self.c['graphics']['top_bar_height']):
                self.app_window_move_mode = True
                self.app_window_move_offset = pos

            if event_type == pygame.MOUSEBUTTONUP:
                self.app_window_move_mode = False

            if self.app_window_move_mode:
                self.absolute_mouse_pos = win32api.GetCursorPos()
                self.game_window_position = win32gui.GetWindowRect(self.game_window_handler)
                win32gui.SetWindowPos(self.game_window_handler, win32con.HWND_TOP,
                                      self.absolute_mouse_pos[0] - self.app_window_move_offset[0]
                                      - self.system_borders[0],
                                      self.absolute_mouse_pos[1] - self.app_window_move_offset[1]
                                      - self.system_borders[1],
                                      self.game_window_position[2] - self.game_window_position[0],
                                      self.game_window_position[3] - self.game_window_position[1],
                                      win32con.SWP_NOREDRAW)


def main():
    RSSim().run()


if __name__ == '__main__':
    main()
