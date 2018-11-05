from sys import exit
from os import path, listdir, remove, rmdir

from win32api import MessageBoxEx
import win32con

from base_route import BaseRoute
from main_map import MainMap
from exceptions import VideoAdapterNotSupportedException
from dispatcher import Dispatcher
from game import Game
from signal import Signal
from track import Track
from train_route import TrainRoute
from button import Button
from main_frame import MainFrame
from game_time import GameTime
from railroad_switch import RailroadSwitch
from crossover import Crossover
from game_progress import GameProgress
from scheduler import Scheduler


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
        self.scheduler = None
        self.game_progress = None
        self.game_time = None
        # we create background image object first to be drawn first
        self.create_main_map()
        # we create routes, signals and dispatcher and link them to each other correctly
        self.create_infrastructure()
        self.saved_onboarding_tip = None
        self.create_onboarding_tips()
        self.pause_button = None
        self.resume_button = None
        self.close_button = None
        self.iconify_button = None
        self.open_schedule_button = None
        self.close_schedule_button = None
        self.create_buttons()
        self.logger.debug('map drag event appended')
        self.logger.debug('------- END INIT -------')
        self.logger.warning('rssim game init completed')

    def create_main_map(self):
        self.logger.debug('------- START CREATING BG IMAGE -------')
        self.main_map = MainMap(batch=self.batch, group=self.map_ordered_group, game_config=self.c)
        self.game_progress = GameProgress(main_map=self.main_map, mini_map=self.mini_map_tip, game_config=self.c,
                                          batch=self.batch,
                                          inactive_group=self.buttons_general_borders_day_text_ordered_group,
                                          active_group=self.buttons_text_and_borders_ordered_group)
        self.game_time = GameTime(batch=self.batch, day_text_group=self.buttons_general_borders_day_text_ordered_group,
                                  game_config=self.c)
        self.logger.info('main map object created')
        self.logger.debug('main map object appended')
        self.logger.debug('------- END CREATING BG IMAGE -------')

    def create_infrastructure(self):
        self.logger.debug('------- START CREATING INFRASTRUCTURE -------')
        # ------ BASE ROUTES AND SIGNALS ------
        # create main entry and main exit base routes and signals for them
        for j in ('left_entry_base_route', 'left_exit_base_route', 'right_entry_base_route', 'right_exit_base_route'):
            self.base_routes[0][j] = BaseRoute(track_number=0, route_type=j, game_config=self.c)
            placement = self.base_routes[0][j].route_config['exit_signal_placement']
            self.logger.debug('placement = {}'.format(placement))
            flip_needed = self.base_routes[0][j].route_config['flip_needed']
            self.logger.debug('flip_needed = {}'.format(flip_needed))
            if placement is not None:
                self.signals[0][j] = Signal(placement=placement, flip_needed=flip_needed,
                                            track_number=0, route_type=j,
                                            batch=self.batch, signal_group=self.signals_and_trains_ordered_group,
                                            game_config=self.c)

        self.logger.info('track 0 base routes and signals created')
        for j in ('left_entry_base_route', 'right_entry_base_route'):
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
        for i in range(1, 33):
            self.base_routes.append({})
            self.signals.append({})
            if i <= 20:
                for k in ('left_entry_base_route', 'left_exit_base_route',
                          'right_entry_base_route', 'right_exit_base_route'):
                    self.base_routes[i][k] = BaseRoute(track_number=i, route_type=k, game_config=self.c)

            if i in (21, 23):
                for k in ('left_entry_base_route', 'left_exit_base_route',
                          'left_side_entry_base_route', 'left_side_exit_base_route',
                          'right_entry_base_route', 'right_exit_base_route'):
                    self.base_routes[i][k] = BaseRoute(track_number=i, route_type=k, game_config=self.c)

            if i in (22, 24):
                for k in ('left_entry_base_route', 'left_exit_base_route',
                          'right_side_entry_base_route', 'right_side_exit_base_route',
                          'right_entry_base_route', 'right_exit_base_route'):
                    self.base_routes[i][k] = BaseRoute(track_number=i, route_type=k, game_config=self.c)

            if i >= 25:
                if i % 2 == 1:
                    for k in ('left_side_entry_base_route', 'left_side_exit_base_route',
                              'right_entry_base_route', 'right_exit_base_route'):
                        self.base_routes[i][k] = BaseRoute(track_number=i, route_type=k, game_config=self.c)
                else:
                    for k in ('left_entry_base_route', 'left_exit_base_route',
                              'right_side_entry_base_route', 'right_side_exit_base_route'):
                        self.base_routes[i][k] = BaseRoute(track_number=i, route_type=k, game_config=self.c)

            for k in ('left_entry_platform_base_route', 'left_exit_platform_base_route',
                      'right_entry_platform_base_route', 'right_exit_platform_base_route'):
                self.base_routes[i][k] = BaseRoute(track_number=i, route_type=k, game_config=self.c)
                placement = self.base_routes[i][k].route_config['exit_signal_placement']
                self.logger.debug('placement = {}'.format(placement))
                flip_needed = self.base_routes[i][k].route_config['flip_needed']
                self.logger.debug('flip_needed = {}'.format(flip_needed))
                if placement is not None:
                    self.signals[i][k] = Signal(placement=placement, flip_needed=flip_needed,
                                                track_number=i, route_type=k, batch=self.batch,
                                                signal_group=self.signals_and_trains_ordered_group, game_config=self.c)

            self.logger.debug('track {} base routes and signals created'.format(i))

        for i in range(100):
            self.base_routes.append({})
            self.signals.append({})

        for j in ('left_side_entry_base_route', 'left_side_exit_base_route',
                  'right_side_entry_base_route', 'right_side_exit_base_route'):
            self.base_routes[100][j] = BaseRoute(track_number=100, route_type=j, game_config=self.c)
            placement = self.base_routes[100][j].route_config['exit_signal_placement']
            self.logger.debug('placement = {}'.format(placement))
            flip_needed = self.base_routes[100][j].route_config['flip_needed']
            self.logger.debug('flip_needed = {}'.format(flip_needed))
            if placement is not None:
                self.signals[100][j] = Signal(placement=placement, flip_needed=flip_needed,
                                              track_number=100, route_type=j,
                                              batch=self.batch, signal_group=self.signals_and_trains_ordered_group,
                                              game_config=self.c)

        for j in ('left_side_entry_base_route', 'right_side_entry_base_route'):
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

        self.construct_base_routes()

        for i in range(1, 33):
            # associate platform base route with its signal
            self.base_routes[i]['right_exit_platform_base_route'].route_config['exit_signal'] \
                = self.signals[i]['right_exit_platform_base_route']
            self.base_routes[i]['left_exit_platform_base_route'].route_config['exit_signal'] \
                = self.signals[i]['left_exit_platform_base_route']
            # for every signal, exit route is the route which ends with this signal
            self.signals[i]['right_exit_platform_base_route'].base_route_exit \
                = self.base_routes[i]['right_exit_platform_base_route']
            self.signals[i]['left_exit_platform_base_route'].base_route_exit \
                = self.base_routes[i]['left_exit_platform_base_route']
            self.logger.debug('track {} base routes and signals associated'.format(i))

        self.logger.info('all base routes and signals associated')
        # fill opened and busy route lists for signals
        for i in range(1, 33):
            # for every platform signal, opened list includes exit base route
            # which begins behind the signal
            # for main entry signals, opened list includes all entry base routes
            if i <= 24 or i in (26, 28, 30, 32):
                self.signals[i]['left_exit_platform_base_route'].base_route_opened_list \
                    .append(self.base_routes[i]['left_exit_base_route'])
                self.signals[0]['left_entry_base_route'].base_route_opened_list \
                    .append(self.base_routes[i]['left_entry_base_route'])

            if i <= 24 or i in (25, 27, 29, 31):
                self.signals[i]['right_exit_platform_base_route'].base_route_opened_list \
                    .append(self.base_routes[i]['right_exit_base_route'])
                self.signals[0]['right_entry_base_route'].base_route_opened_list \
                    .append(self.base_routes[i]['right_entry_base_route'])

            if i in (21, 23, 25, 27, 29, 31):
                self.signals[i]['left_exit_platform_base_route'].base_route_opened_list\
                    .append(self.base_routes[i]['left_side_exit_base_route'])
                self.signals[100]['left_side_entry_base_route'].base_route_opened_list \
                    .append(self.base_routes[i]['left_side_entry_base_route'])

            if i in (22, 24, 26, 28, 30, 32):
                self.signals[i]['right_exit_platform_base_route'].base_route_opened_list \
                    .append(self.base_routes[i]['right_side_exit_base_route'])
                self.signals[100]['right_side_entry_base_route'].base_route_opened_list \
                    .append(self.base_routes[i]['right_side_entry_base_route'])

        self.logger.debug('opened list set up for track 0 signals')
        self.logger.info('opened list set up for all signals')

        # ------ TRAIN ROUTES AND TRACKS ------
        # create basic entry train routes for trains which cannot find available track
        train_route_sections \
            = [self.base_routes[0][
                   '{}_base_route'
                   .format(self.c.entry_train_route[self.c.direction_from_left_to_right])], ]
        train_route_sections_positions = [0, ]
        self.train_routes[0][self.c.approaching_train_route[self.c.direction_from_left_to_right]] \
            = TrainRoute(track_number=0,
                         route_type=self.c.approaching_train_route[self.c.direction_from_left_to_right],
                         supported_carts=[0, 20], train_route_sections=train_route_sections,
                         train_route_sections_positions=train_route_sections_positions, game_config=self.c)
        train_route_sections \
            = [self.base_routes[0][
                   '{}_base_route'
                   .format(self.c.entry_train_route[self.c.direction_from_right_to_left])], ]
        train_route_sections_positions = [0, ]
        self.train_routes[0][self.c.approaching_train_route[self.c.direction_from_right_to_left]] \
            = TrainRoute(track_number=0,
                         route_type=self.c.approaching_train_route[self.c.direction_from_right_to_left],
                         supported_carts=[0, 20], train_route_sections=train_route_sections,
                         train_route_sections_positions=train_route_sections_positions, game_config=self.c)
        self.logger.info('approaching train routes created')

        for i in range(1, 33):
            self.train_routes.append({})
            # create track object
            # it includes all 4 base routes
            base_routes_in_track = [self.base_routes[i]['left_entry_platform_base_route'],
                                    self.base_routes[i]['right_entry_platform_base_route'],
                                    self.base_routes[i]['left_exit_platform_base_route'],
                                    self.base_routes[i]['right_exit_platform_base_route']]
            new_track = Track(track_number=i, base_routes_in_track=base_routes_in_track,
                              batch=self.batch, tip_group=self.top_bottom_bars_ordered_group,
                              button_group=self.buttons_general_borders_day_text_ordered_group,
                              text_group=self.buttons_text_and_borders_ordered_group,
                              borders_group=self.buttons_text_and_borders_ordered_group, game_config=self.c,
                              map_move_mode=self.map_move_mode, game_progress=self.game_progress)
            if i == 1:
                new_track.signals_to_unlock.append(self.signals[0]['right_entry_base_route'])
            elif i == 2:
                new_track.signals_to_unlock.append(self.signals[0]['left_entry_base_route'])
            elif i == 21:
                new_track.signals_to_unlock.append(self.signals[100]['left_side_entry_base_route'])
            elif i == 22:
                new_track.signals_to_unlock.append(self.signals[100]['right_side_entry_base_route'])

            for j in self.signals[i]:
                new_track.signals_to_unlock.append(self.signals[i][j])

            for a in new_track.signals_to_unlock:
                a.locked = new_track.locked

            self.tracks.append(new_track)
            self.logger.info('track {} created'.format(i))
            # create entry train route
            # it includes main entry base route, specific entry base route and platform base route
            if i <= 24:
                for k in (self.c.direction_from_left_to_right, self.c.direction_from_right_to_left):
                    train_route_sections = [
                        self.base_routes[0]['{}_base_route'
                                            .format(self.c.entry_train_route[k])], ]
                    train_route_sections.extend(
                        self.base_routes[i]['{}_base_route'
                                            .format(self.c.entry_train_route[k])].junctions)
                    train_route_sections.extend([
                        self.base_routes[i]['{}_base_route'
                                            .format(self.c.entry_train_route[k])],
                        self.base_routes[i]['{}_platform_base_route'
                                            .format(self.c.entry_train_route[k])]])
                    train_route_sections_positions = [0, ]
                    train_route_sections_positions.extend(
                        self.base_routes[i]['{}_base_route'.format(self.c.entry_train_route[k])].junction_position)
                    train_route_sections_positions.extend([0, 0])
                    self.train_routes[i][self.c.entry_train_route[k]] \
                        = TrainRoute(track_number=i, route_type=self.c.entry_train_route[k],
                                     supported_carts=self.tracks[i - 1].supported_carts,
                                     train_route_sections=train_route_sections,
                                     train_route_sections_positions=train_route_sections_positions, game_config=self.c)
                    self.logger.info('track {} {} train route created'.format(i, k))

                # create exit train route
                # it includes platform base route, specific exit base route and main exit base route
                for m in (self.c.direction_from_left_to_right, self.c.direction_from_right_to_left):
                    train_route_sections = [
                        self.base_routes[i]['{}_platform_base_route'
                                            .format(self.c.exit_train_route[m])], ]
                    train_route_sections.extend(
                        self.base_routes[i]['{}_base_route'
                                            .format(self.c.exit_train_route[m])].junctions)
                    train_route_sections.extend([
                        self.base_routes[i]['{}_base_route'
                                            .format(self.c.exit_train_route[m])],
                        self.base_routes[0]['{}_base_route'
                                            .format(self.c.exit_train_route[m])]])
                    train_route_sections_positions = [0, ]
                    train_route_sections_positions.extend(
                        self.base_routes[i]['{}_base_route'.format(self.c.exit_train_route[m])].junction_position)
                    train_route_sections_positions.extend([0, 0])

                    self.train_routes[i][self.c.exit_train_route[m]] \
                        = TrainRoute(track_number=i, route_type=self.c.exit_train_route[m],
                                     supported_carts=self.tracks[i - 1].supported_carts,
                                     train_route_sections=train_route_sections,
                                     train_route_sections_positions=train_route_sections_positions, game_config=self.c)
                    self.logger.info('track {} {} train route created'.format(i, m))

            if i in (21, 23, 25, 27, 29, 31):
                train_route_sections = [
                    self.base_routes[100]['{}_base_route'
                        .format(self.c.entry_train_route[self.c.direction_from_left_to_right_side])], ]
                train_route_sections.extend(
                    self.base_routes[i]['{}_base_route'
                        .format(self.c.entry_train_route[self.c.direction_from_left_to_right_side])]
                        .junctions)
                train_route_sections.extend([
                    self.base_routes[i]['{}_base_route'
                        .format(self.c.entry_train_route[self.c.direction_from_left_to_right_side])],
                    self.base_routes[i]['{}_platform_base_route'
                        .format(self.c.entry_train_route[self.c.direction_from_left_to_right])]])
                train_route_sections_positions = [0, ]
                train_route_sections_positions.extend(
                    self.base_routes[i]['{}_base_route'
                        .format(self.c.entry_train_route[self.c.direction_from_left_to_right_side])]
                        .junction_position)
                train_route_sections_positions.extend([0, 0])

                self.train_routes[i][self.c.entry_train_route[self.c.direction_from_left_to_right_side]] \
                    = TrainRoute(track_number=i,
                                 route_type=self.c.entry_train_route[self.c.direction_from_left_to_right_side],
                                 supported_carts=self.tracks[i - 1].supported_carts,
                                 train_route_sections=train_route_sections,
                                 train_route_sections_positions=train_route_sections_positions, game_config=self.c)
                self.logger.info('track {} {} train route created'.format(i, self.c.direction_from_left_to_right_side))

                train_route_sections = [
                    self.base_routes[i]['{}_platform_base_route'
                        .format(self.c.exit_train_route[self.c.direction_from_right_to_left])], ]
                train_route_sections.extend(
                    self.base_routes[i]['{}_base_route'
                        .format(self.c.exit_train_route[self.c.direction_from_right_to_left_side])].junctions)
                train_route_sections.extend([
                    self.base_routes[i]['{}_base_route'
                        .format(self.c.exit_train_route[self.c.direction_from_right_to_left_side])],
                    self.base_routes[100]['{}_base_route'
                        .format(self.c.exit_train_route[self.c.direction_from_right_to_left_side])]])
                train_route_sections_positions = [0, ]
                train_route_sections_positions.extend(
                    self.base_routes[i]['{}_base_route'
                        .format(self.c.exit_train_route[self.c.direction_from_right_to_left_side])].junction_position)
                train_route_sections_positions.extend([0, 0])

                self.train_routes[i][self.c.exit_train_route[self.c.direction_from_right_to_left_side]] \
                    = TrainRoute(track_number=i,
                                 route_type=self.c.exit_train_route[self.c.direction_from_right_to_left_side],
                                 supported_carts=self.tracks[i - 1].supported_carts,
                                 train_route_sections=train_route_sections,
                                 train_route_sections_positions=train_route_sections_positions, game_config=self.c)
                self.logger.info('track {} {} train route created'.format(i, self.c.direction_from_right_to_left_side))
                if i >= 25:
                    train_route_sections = [
                        self.base_routes[0]['{}_base_route'
                            .format(self.c.entry_train_route[self.c.direction_from_right_to_left])], ]
                    train_route_sections.extend(
                        self.base_routes[i]['{}_base_route'
                            .format(self.c.entry_train_route[self.c.direction_from_right_to_left])]
                            .junctions)
                    train_route_sections.extend([
                        self.base_routes[i]['{}_base_route'
                            .format(self.c.entry_train_route[self.c.direction_from_right_to_left])],
                        self.base_routes[i]['{}_platform_base_route'
                            .format(self.c.entry_train_route[self.c.direction_from_right_to_left])]])
                    train_route_sections_positions = [0, ]
                    train_route_sections_positions.extend(
                        self.base_routes[i]['{}_base_route'
                            .format(self.c.entry_train_route[self.c.direction_from_right_to_left])]
                            .junction_position)
                    train_route_sections_positions.extend([0, 0])

                    self.train_routes[i][self.c.entry_train_route[self.c.direction_from_right_to_left]] \
                        = TrainRoute(track_number=i,
                                     route_type=self.c.entry_train_route[self.c.direction_from_right_to_left],
                                     supported_carts=self.tracks[i - 1].supported_carts,
                                     train_route_sections=train_route_sections,
                                     train_route_sections_positions=train_route_sections_positions, game_config=self.c)
                    self.logger.info('track {} {} train route created'.format(i, self.c.direction_from_right_to_left))

                    train_route_sections = [
                        self.base_routes[i]['{}_platform_base_route'
                            .format(self.c.exit_train_route[self.c.direction_from_left_to_right])], ]
                    train_route_sections.extend(
                        self.base_routes[i]['{}_base_route'
                            .format(self.c.exit_train_route[self.c.direction_from_left_to_right])]
                            .junctions)
                    train_route_sections.extend([
                        self.base_routes[i]['{}_base_route'
                            .format(self.c.exit_train_route[self.c.direction_from_left_to_right])],
                        self.base_routes[0]['{}_base_route'
                            .format(self.c.exit_train_route[self.c.direction_from_left_to_right])]])
                    train_route_sections_positions = [0, ]
                    train_route_sections_positions.extend(
                        self.base_routes[i]['{}_base_route'
                            .format(self.c.exit_train_route[self.c.direction_from_left_to_right])]
                            .junction_position)
                    train_route_sections_positions.extend([0, 0])

                    self.train_routes[i][self.c.exit_train_route[self.c.direction_from_left_to_right]] \
                        = TrainRoute(track_number=i,
                                     route_type=self.c.exit_train_route[self.c.direction_from_left_to_right],
                                     supported_carts=self.tracks[i - 1].supported_carts,
                                     train_route_sections=train_route_sections,
                                     train_route_sections_positions=train_route_sections_positions, game_config=self.c)
                    self.logger.info('track {} {} train route created'.format(i, self.c.direction_from_left_to_right))

            if i in (22, 24, 26, 28, 30, 32):
                train_route_sections = [
                    self.base_routes[100]['{}_base_route'
                        .format(self.c.entry_train_route[self.c.direction_from_right_to_left_side])], ]
                train_route_sections.extend(
                    self.base_routes[i]['{}_base_route'
                        .format(self.c.entry_train_route[self.c.direction_from_right_to_left_side])].junctions)
                train_route_sections.extend([
                    self.base_routes[i]['{}_base_route'
                        .format(self.c.entry_train_route[self.c.direction_from_right_to_left_side])],
                    self.base_routes[i]['{}_platform_base_route'
                        .format(self.c.entry_train_route[self.c.direction_from_right_to_left])]])
                train_route_sections_positions = [0, ]
                train_route_sections_positions.extend(
                    self.base_routes[i]['{}_base_route'
                        .format(self.c.entry_train_route[self.c.direction_from_right_to_left_side])].junction_position)
                train_route_sections_positions.extend([0, 0])

                self.train_routes[i][self.c.entry_train_route[self.c.direction_from_right_to_left_side]] \
                    = TrainRoute(track_number=i,
                                 route_type=self.c.entry_train_route[self.c.direction_from_right_to_left_side],
                                 supported_carts=self.tracks[i - 1].supported_carts,
                                 train_route_sections=train_route_sections,
                                 train_route_sections_positions=train_route_sections_positions, game_config=self.c)
                self.logger.info('track {} {} train route created'.format(i, self.c.direction_from_right_to_left_side))

                train_route_sections = [
                    self.base_routes[i]['{}_platform_base_route'
                        .format(self.c.exit_train_route[self.c.direction_from_left_to_right])], ]
                train_route_sections.extend(
                    self.base_routes[i]['{}_base_route'
                        .format(self.c.exit_train_route[self.c.direction_from_left_to_right_side])].junctions)
                train_route_sections.extend([
                    self.base_routes[i]['{}_base_route'
                        .format(self.c.exit_train_route[self.c.direction_from_left_to_right_side])],
                    self.base_routes[100]['{}_base_route'
                        .format(self.c.exit_train_route[self.c.direction_from_left_to_right_side])]])
                train_route_sections_positions = [0, ]
                train_route_sections_positions.extend(
                    self.base_routes[i]['{}_base_route'
                        .format(self.c.exit_train_route[self.c.direction_from_left_to_right_side])].junction_position)
                train_route_sections_positions.extend([0, 0])

                self.train_routes[i][self.c.exit_train_route[self.c.direction_from_left_to_right_side]] \
                    = TrainRoute(track_number=i,
                                 route_type=self.c.exit_train_route[self.c.direction_from_left_to_right_side],
                                 supported_carts=self.tracks[i - 1].supported_carts,
                                 train_route_sections=train_route_sections,
                                 train_route_sections_positions=train_route_sections_positions, game_config=self.c)
                self.logger.info('track {} {} train route created'.format(i, self.c.direction_from_left_to_right_side))
                if i >= 26:
                    train_route_sections = [
                        self.base_routes[0]['{}_base_route'
                            .format(self.c.entry_train_route[self.c.direction_from_left_to_right])], ]
                    train_route_sections.extend(
                        self.base_routes[i]['{}_base_route'
                            .format(self.c.entry_train_route[self.c.direction_from_left_to_right])].junctions)
                    train_route_sections.extend([
                        self.base_routes[i]['{}_base_route'
                            .format(self.c.entry_train_route[self.c.direction_from_left_to_right])],
                        self.base_routes[i]['{}_platform_base_route'
                            .format(self.c.entry_train_route[self.c.direction_from_left_to_right])]])
                    train_route_sections_positions = [0, ]
                    train_route_sections_positions.extend(
                        self.base_routes[i]['{}_base_route'
                            .format(self.c.entry_train_route[self.c.direction_from_left_to_right])].junction_position)
                    train_route_sections_positions.extend([0, 0])

                    self.train_routes[i][self.c.entry_train_route[self.c.direction_from_left_to_right]] \
                        = TrainRoute(track_number=i,
                                     route_type=self.c.entry_train_route[self.c.direction_from_left_to_right],
                                     supported_carts=self.tracks[i - 1].supported_carts,
                                     train_route_sections=train_route_sections,
                                     train_route_sections_positions=train_route_sections_positions, game_config=self.c)
                    self.logger.info('track {} {} train route created'.format(i, self.c.direction_from_left_to_right))

                    train_route_sections = [
                        self.base_routes[i]['{}_platform_base_route'
                            .format(self.c.exit_train_route[self.c.direction_from_right_to_left])], ]
                    train_route_sections.extend(
                        self.base_routes[i]['{}_base_route'
                            .format(self.c.exit_train_route[self.c.direction_from_right_to_left])].junctions)
                    train_route_sections.extend([
                        self.base_routes[i]['{}_base_route'
                            .format(self.c.exit_train_route[self.c.direction_from_right_to_left])],
                        self.base_routes[0]['{}_base_route'
                            .format(self.c.exit_train_route[self.c.direction_from_right_to_left])]])
                    train_route_sections_positions = [0, ]
                    train_route_sections_positions.extend(
                        self.base_routes[i]['{}_base_route'
                            .format(self.c.exit_train_route[self.c.direction_from_right_to_left])].junction_position)
                    train_route_sections_positions.extend([0, 0])

                    self.train_routes[i][self.c.exit_train_route[self.c.direction_from_right_to_left]] \
                        = TrainRoute(track_number=i,
                                     route_type=self.c.exit_train_route[self.c.direction_from_right_to_left],
                                     supported_carts=self.tracks[i - 1].supported_carts,
                                     train_route_sections=train_route_sections,
                                     train_route_sections_positions=train_route_sections_positions, game_config=self.c)
                    self.logger.info('track {} {} train route created'.format(i, self.c.direction_from_right_to_left))

        for i in range(100):
            self.train_routes.append({})

        train_route_sections \
            = [self.base_routes[100][
                '{}_base_route'
                .format(self.c.entry_train_route[self.c.direction_from_left_to_right_side])], ]
        train_route_sections_positions = [0, ]
        self.train_routes[100][self.c.approaching_train_route[self.c.direction_from_left_to_right_side]] \
            = TrainRoute(track_number=100,
                         route_type=self.c.approaching_train_route[self.c.direction_from_left_to_right_side],
                         supported_carts=[0, 20], train_route_sections=train_route_sections,
                         train_route_sections_positions=train_route_sections_positions, game_config=self.c)

        train_route_sections \
            = [self.base_routes[100][
                   '{}_base_route'
                   .format(self.c.entry_train_route[self.c.direction_from_right_to_left_side])], ]
        train_route_sections_positions = [0, ]
        self.train_routes[100][self.c.approaching_train_route[self.c.direction_from_right_to_left_side]] \
            = TrainRoute(track_number=100,
                         route_type=self.c.approaching_train_route[self.c.direction_from_right_to_left_side],
                         supported_carts=[0, 20], train_route_sections=train_route_sections,
                         train_route_sections_positions=train_route_sections_positions, game_config=self.c)

        self.logger.info('tracks and train routes created')
        # ------ SORT THIS OUT ------
        # train routes and tracks are added to dispatcher which we create right now
        self.scheduler = Scheduler(game_config=self.c, batch=self.batch, group=self.top_bottom_bars_ordered_group,
                                   text_group=self.buttons_general_borders_day_text_ordered_group)
        self.dispatcher = Dispatcher(batch=self.batch, group=self.signals_and_trains_ordered_group,
                                     boarding_lights_group=self.boarding_lights_ordered_group, game_config=self.c)
        for i in range(33):
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
        for i in range(32):
            self.dispatcher.tracks.append(self.tracks[i])
            self.logger.debug('track {} appended to dispatcher'.format(i + 1))

        for i in range(33):
            for n in self.signals[i]:
                self.dispatcher.signals.append(self.signals[i][n])
                self.logger.debug('signal {} {} appended to dispatcher'.format(i, n))

        for n in self.signals[100]:
            self.dispatcher.signals.append(self.signals[100][n])
            self.logger.debug('signal {} {} appended to dispatcher'.format(100, n))

        self.logger.info('all tracks appended to dispatcher')
        # now we add dispatcher itself to generic objects list
        self.dispatcher.read_state()
        self.game_progress.tracks = self.tracks
        for i in self.tracks:
            i.game_progress = self.game_progress

        self.dispatcher.game_progress = self.game_progress
        self.scheduler.game_progress = self.game_progress
        self.scheduler.game_time = self.game_time
        self.scheduler.dispatcher = self.dispatcher
        self.objects.append(self.scheduler)
        self.objects.append(self.dispatcher)
        self.objects.append(self.game_progress)
        self.logger.info('dispatcher appended to global objects list')
        self.logger.debug('------- START CREATING INFRASTRUCTURE -------')
        self.logger.warning('all infrastructure created')

    def create_junctions(self):
        self.junctions[1] = {}
        self.junctions[1][2] = {}
        self.junctions[1][2]['right_entry_crossover'] = Crossover(1, 2, 'right_entry_crossover', game_config=self.c)
        self.junctions[1][2]['right_exit_crossover'] = Crossover(1, 2, 'right_exit_crossover', game_config=self.c)
        self.junctions[1][21] = {}
        self.junctions[1][21]['left_entry_railroad_switch'] = RailroadSwitch(1, 21, 'left_entry_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[1][21]['left_exit_railroad_switch'] = RailroadSwitch(1, 21, 'left_exit_railroad_switch',
                                                                            game_config=self.c)
        self.junctions[1][29] = {}
        self.junctions[1][29]['right_entry_railroad_switch'] = RailroadSwitch(1, 29, 'right_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[1][29]['right_exit_railroad_switch'] = RailroadSwitch(1, 29, 'right_exit_railroad_switch',
                                                                             game_config=self.c)
        self.logger.debug('junctions for track 1 created')

        self.junctions[2] = {}
        self.junctions[2][1] = {}
        self.junctions[2][1]['left_entry_crossover'] = Crossover(2, 1, 'left_entry_crossover', game_config=self.c)
        self.junctions[2][1]['left_exit_crossover'] = Crossover(2, 1, 'left_exit_crossover', game_config=self.c)
        self.junctions[2][22] = {}
        self.junctions[2][22]['right_entry_railroad_switch'] = RailroadSwitch(2, 22, 'right_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[2][22]['right_exit_railroad_switch'] = RailroadSwitch(2, 22, 'right_exit_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[2][30] = {}
        self.junctions[2][30]['left_entry_railroad_switch'] = RailroadSwitch(2, 30, 'left_entry_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[2][30]['left_exit_railroad_switch'] = RailroadSwitch(2, 30, 'left_exit_railroad_switch',
                                                                            game_config=self.c)
        self.logger.debug('junctions for track 2 created')

        self.junctions[5] = {}
        self.junctions[5][7] = {}
        self.junctions[5][7]['left_entry_railroad_switch'] = RailroadSwitch(5, 7, 'left_entry_railroad_switch',
                                                                            game_config=self.c)
        self.junctions[5][7]['left_exit_railroad_switch'] = RailroadSwitch(5, 7, 'left_exit_railroad_switch',
                                                                           game_config=self.c)
        self.junctions[5][7]['right_entry_railroad_switch'] = RailroadSwitch(5, 7, 'right_entry_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[5][7]['right_exit_railroad_switch'] = RailroadSwitch(5, 7, 'right_exit_railroad_switch',
                                                                            game_config=self.c)

        self.junctions[6] = {}
        self.junctions[6][8] = {}
        self.junctions[6][8]['left_entry_railroad_switch'] = RailroadSwitch(6, 8, 'left_entry_railroad_switch',
                                                                            game_config=self.c)
        self.junctions[6][8]['left_exit_railroad_switch'] = RailroadSwitch(6, 8, 'left_exit_railroad_switch',
                                                                           game_config=self.c)
        self.junctions[6][8]['right_entry_railroad_switch'] = RailroadSwitch(6, 8, 'right_entry_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[6][8]['right_exit_railroad_switch'] = RailroadSwitch(6, 8, 'right_exit_railroad_switch',
                                                                            game_config=self.c)

        self.junctions[9] = {}
        self.junctions[9][11] = {}
        self.junctions[9][11]['left_entry_railroad_switch'] = RailroadSwitch(9, 11, 'left_entry_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[9][11]['left_exit_railroad_switch'] = RailroadSwitch(9, 11, 'left_exit_railroad_switch',
                                                                            game_config=self.c)
        self.junctions[9][11]['right_entry_railroad_switch'] = RailroadSwitch(9, 11, 'right_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[9][11]['right_exit_railroad_switch'] = RailroadSwitch(9, 11, 'right_exit_railroad_switch',
                                                                             game_config=self.c)

        self.junctions[10] = {}
        self.junctions[10][12] = {}
        self.junctions[10][12]['left_entry_railroad_switch'] = RailroadSwitch(10, 12, 'left_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[10][12]['left_exit_railroad_switch'] = RailroadSwitch(10, 12, 'left_exit_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[10][12]['right_entry_railroad_switch'] = RailroadSwitch(10, 12, 'right_entry_railroad_switch',
                                                                               game_config=self.c)
        self.junctions[10][12]['right_exit_railroad_switch'] = RailroadSwitch(10, 12, 'right_exit_railroad_switch',
                                                                              game_config=self.c)

        self.junctions[13] = {}
        self.junctions[13][15] = {}
        self.junctions[13][15]['left_entry_railroad_switch'] = RailroadSwitch(13, 15, 'left_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[13][15]['left_exit_railroad_switch'] = RailroadSwitch(13, 15, 'left_exit_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[13][15]['right_entry_railroad_switch'] = RailroadSwitch(13, 15, 'right_entry_railroad_switch',
                                                                               game_config=self.c)
        self.junctions[13][15]['right_exit_railroad_switch'] = RailroadSwitch(13, 15, 'right_exit_railroad_switch',
                                                                              game_config=self.c)

        self.junctions[14] = {}
        self.junctions[14][16] = {}
        self.junctions[14][16]['left_entry_railroad_switch'] = RailroadSwitch(14, 16, 'left_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[14][16]['left_exit_railroad_switch'] = RailroadSwitch(14, 16, 'left_exit_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[14][16]['right_entry_railroad_switch'] = RailroadSwitch(14, 16, 'right_entry_railroad_switch',
                                                                               game_config=self.c)
        self.junctions[14][16]['right_exit_railroad_switch'] = RailroadSwitch(14, 16, 'right_exit_railroad_switch',
                                                                              game_config=self.c)

        self.junctions[17] = {}
        self.junctions[17][19] = {}
        self.junctions[17][19]['left_entry_railroad_switch'] = RailroadSwitch(17, 19, 'left_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[17][19]['left_exit_railroad_switch'] = RailroadSwitch(17, 19, 'left_exit_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[17][19]['right_entry_railroad_switch'] = RailroadSwitch(17, 19, 'right_entry_railroad_switch',
                                                                               game_config=self.c)
        self.junctions[17][19]['right_exit_railroad_switch'] = RailroadSwitch(17, 19, 'right_exit_railroad_switch',
                                                                              game_config=self.c)

        self.junctions[18] = {}
        self.junctions[18][20] = {}
        self.junctions[18][20]['left_entry_railroad_switch'] = RailroadSwitch(18, 20, 'left_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[18][20]['left_exit_railroad_switch'] = RailroadSwitch(18, 20, 'left_exit_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[18][20]['right_entry_railroad_switch'] = RailroadSwitch(18, 20, 'right_entry_railroad_switch',
                                                                               game_config=self.c)
        self.junctions[18][20]['right_exit_railroad_switch'] = RailroadSwitch(18, 20, 'right_exit_railroad_switch',
                                                                              game_config=self.c)

        self.junctions[21] = {}
        self.junctions[21][3] = {}
        self.junctions[21][3]['left_entry_railroad_switch'] = RailroadSwitch(21, 3, 'left_entry_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[21][3]['left_exit_railroad_switch'] = RailroadSwitch(21, 3, 'left_exit_railroad_switch',
                                                                            game_config=self.c)
        self.junctions[21][5] = {}
        self.junctions[21][5]['left_entry_railroad_switch'] = RailroadSwitch(21, 5, 'left_entry_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[21][5]['left_exit_railroad_switch'] = RailroadSwitch(21, 5, 'left_exit_railroad_switch',
                                                                            game_config=self.c)
        self.junctions[21][9] = {}
        self.junctions[21][9]['left_entry_railroad_switch'] = RailroadSwitch(21, 9, 'left_entry_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[21][9]['left_exit_railroad_switch'] = RailroadSwitch(21, 9, 'left_exit_railroad_switch',
                                                                            game_config=self.c)
        self.junctions[21][13] = {}
        self.junctions[21][13]['left_entry_railroad_switch'] = RailroadSwitch(21, 13, 'left_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[21][13]['left_exit_railroad_switch'] = RailroadSwitch(21, 13, 'left_exit_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[21][17] = {}
        self.junctions[21][17]['left_entry_railroad_switch'] = RailroadSwitch(21, 17, 'left_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[21][17]['left_exit_railroad_switch'] = RailroadSwitch(21, 17, 'left_exit_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[21][23] = {}
        self.junctions[21][23]['right_entry_railroad_switch'] = RailroadSwitch(21, 23, 'right_entry_railroad_switch',
                                                                               game_config=self.c)
        self.junctions[21][23]['right_exit_railroad_switch'] = RailroadSwitch(21, 23, 'right_exit_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[21][23]['left_entry_crossover'] = Crossover(21, 23, 'left_entry_crossover', game_config=self.c)

        self.junctions[22] = {}
        self.junctions[22][4] = {}
        self.junctions[22][4]['right_entry_railroad_switch'] = RailroadSwitch(22, 4, 'right_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[22][4]['right_exit_railroad_switch'] = RailroadSwitch(22, 4, 'right_exit_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[22][6] = {}
        self.junctions[22][6]['right_entry_railroad_switch'] = RailroadSwitch(22, 6, 'right_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[22][6]['right_exit_railroad_switch'] = RailroadSwitch(22, 6, 'right_exit_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[22][10] = {}
        self.junctions[22][10]['right_entry_railroad_switch'] = RailroadSwitch(22, 10, 'right_entry_railroad_switch',
                                                                               game_config=self.c)
        self.junctions[22][10]['right_exit_railroad_switch'] = RailroadSwitch(22, 10, 'right_exit_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[22][14] = {}
        self.junctions[22][14]['right_entry_railroad_switch'] = RailroadSwitch(22, 14, 'right_entry_railroad_switch',
                                                                               game_config=self.c)
        self.junctions[22][14]['right_exit_railroad_switch'] = RailroadSwitch(22, 14, 'right_exit_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[22][18] = {}
        self.junctions[22][18]['right_entry_railroad_switch'] = RailroadSwitch(22, 18, 'right_entry_railroad_switch',
                                                                               game_config=self.c)
        self.junctions[22][18]['right_exit_railroad_switch'] = RailroadSwitch(22, 18, 'right_exit_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[22][24] = {}
        self.junctions[22][24]['left_entry_railroad_switch'] = RailroadSwitch(22, 24, 'left_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[22][24]['left_exit_railroad_switch'] = RailroadSwitch(22, 24, 'left_exit_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[22][24]['right_entry_crossover'] = Crossover(22, 24, 'right_entry_crossover', game_config=self.c)

        self.junctions[23] = {}
        self.junctions[23][21] = {}
        self.junctions[23][21]['left_exit_crossover'] = Crossover(23, 21, 'left_exit_crossover', game_config=self.c)

        self.junctions[24] = {}
        self.junctions[24][22] = {}
        self.junctions[24][22]['right_exit_crossover'] = Crossover(24, 22, 'right_exit_crossover', game_config=self.c)

        self.junctions[25] = {}
        self.junctions[25][27] = {}
        self.junctions[25][27]['right_entry_railroad_switch'] = RailroadSwitch(25, 27, 'right_entry_railroad_switch',
                                                                               game_config=self.c)
        self.junctions[25][27]['right_exit_railroad_switch'] = RailroadSwitch(25, 27, 'right_exit_railroad_switch',
                                                                              game_config=self.c)

        self.junctions[26] = {}
        self.junctions[26][28] = {}
        self.junctions[26][28]['left_entry_railroad_switch'] = RailroadSwitch(26, 28, 'left_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[26][28]['left_exit_railroad_switch'] = RailroadSwitch(26, 28, 'left_exit_railroad_switch',
                                                                             game_config=self.c)

        self.junctions[27] = {}
        self.junctions[27][25] = {}
        self.junctions[27][25]['left_entry_railroad_switch'] = RailroadSwitch(27, 25, 'left_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[27][25]['left_exit_railroad_switch'] = RailroadSwitch(27, 25, 'left_exit_railroad_switch',
                                                                             game_config=self.c)

        self.junctions[28] = {}
        self.junctions[28][26] = {}
        self.junctions[28][26]['right_entry_railroad_switch'] = RailroadSwitch(28, 26, 'right_entry_railroad_switch',
                                                                               game_config=self.c)
        self.junctions[28][26]['right_exit_railroad_switch'] = RailroadSwitch(28, 26, 'right_exit_railroad_switch',
                                                                              game_config=self.c)

        self.junctions[29] = {}
        self.junctions[29][3] = {}
        self.junctions[29][3]['right_entry_railroad_switch'] = RailroadSwitch(29, 3, 'right_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[29][3]['right_exit_railroad_switch'] = RailroadSwitch(29, 3, 'right_exit_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[29][5] = {}
        self.junctions[29][5]['right_entry_railroad_switch'] = RailroadSwitch(29, 5, 'right_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[29][5]['right_exit_railroad_switch'] = RailroadSwitch(29, 5, 'right_exit_railroad_switch',
                                                                             game_config=self.c)
        self.logger.debug('junctions for track 3 created')
        self.junctions[29][9] = {}
        self.junctions[29][9]['right_entry_railroad_switch'] = RailroadSwitch(29, 9, 'right_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[29][9]['right_exit_railroad_switch'] = RailroadSwitch(29, 9, 'right_exit_railroad_switch',
                                                                             game_config=self.c)
        self.logger.debug('junctions for track 3 created')
        self.junctions[29][13] = {}
        self.junctions[29][13]['right_entry_railroad_switch'] = RailroadSwitch(29, 13, 'right_entry_railroad_switch',
                                                                               game_config=self.c)
        self.junctions[29][13]['right_exit_railroad_switch'] = RailroadSwitch(29, 13, 'right_exit_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[29][17] = {}
        self.junctions[29][17]['right_entry_railroad_switch'] = RailroadSwitch(29, 17, 'right_entry_railroad_switch',
                                                                               game_config=self.c)
        self.junctions[29][17]['right_exit_railroad_switch'] = RailroadSwitch(29, 17, 'right_exit_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[29][21] = {}
        self.junctions[29][21]['right_entry_railroad_switch'] = RailroadSwitch(29, 21, 'right_entry_railroad_switch',
                                                                               game_config=self.c)
        self.junctions[29][21]['right_exit_railroad_switch'] = RailroadSwitch(29, 21, 'right_exit_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[29][25] = {}
        self.junctions[29][25]['right_entry_railroad_switch'] = RailroadSwitch(29, 25, 'right_entry_railroad_switch',
                                                                               game_config=self.c)
        self.junctions[29][25]['right_exit_railroad_switch'] = RailroadSwitch(29, 25, 'right_exit_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[29][27] = {}
        self.junctions[29][27]['left_entry_railroad_switch'] = RailroadSwitch(29, 27, 'left_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[29][27]['left_exit_railroad_switch'] = RailroadSwitch(29, 27, 'left_exit_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[29][31] = {}
        self.junctions[29][31]['left_entry_railroad_switch'] = RailroadSwitch(29, 31, 'left_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[29][31]['left_exit_railroad_switch'] = RailroadSwitch(29, 31, 'left_exit_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[29][31]['right_entry_railroad_switch'] = RailroadSwitch(29, 31, 'right_entry_railroad_switch',
                                                                               game_config=self.c)
        self.junctions[29][31]['right_exit_railroad_switch'] = RailroadSwitch(29, 31, 'right_exit_railroad_switch',
                                                                              game_config=self.c)
        self.logger.debug('junctions for track 3 created')

        self.junctions[30] = {}
        self.junctions[30][4] = {}
        self.junctions[30][4]['left_entry_railroad_switch'] = RailroadSwitch(30, 4, 'left_entry_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[30][4]['left_exit_railroad_switch'] = RailroadSwitch(30, 4, 'left_exit_railroad_switch',
                                                                            game_config=self.c)
        self.junctions[30][6] = {}
        self.junctions[30][6]['left_entry_railroad_switch'] = RailroadSwitch(30, 6, 'left_entry_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[30][6]['left_exit_railroad_switch'] = RailroadSwitch(30, 6, 'left_exit_railroad_switch',
                                                                            game_config=self.c)
        self.junctions[30][10] = {}
        self.junctions[30][10]['left_entry_railroad_switch'] = RailroadSwitch(30, 10, 'left_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[30][10]['left_exit_railroad_switch'] = RailroadSwitch(30, 10, 'left_exit_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[30][14] = {}
        self.junctions[30][14]['left_entry_railroad_switch'] = RailroadSwitch(30, 14, 'left_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[30][14]['left_exit_railroad_switch'] = RailroadSwitch(30, 14, 'left_exit_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[30][18] = {}
        self.junctions[30][18]['left_entry_railroad_switch'] = RailroadSwitch(30, 18, 'left_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[30][18]['left_exit_railroad_switch'] = RailroadSwitch(30, 18, 'left_exit_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[30][22] = {}
        self.junctions[30][22]['left_entry_railroad_switch'] = RailroadSwitch(30, 22, 'left_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[30][22]['left_exit_railroad_switch'] = RailroadSwitch(30, 22, 'left_exit_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[30][26] = {}
        self.junctions[30][26]['left_entry_railroad_switch'] = RailroadSwitch(30, 26, 'left_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[30][26]['left_exit_railroad_switch'] = RailroadSwitch(30, 26, 'left_exit_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[30][28] = {}
        self.junctions[30][28]['right_entry_railroad_switch'] = RailroadSwitch(30, 28, 'right_entry_railroad_switch',
                                                                               game_config=self.c)
        self.junctions[30][28]['right_exit_railroad_switch'] = RailroadSwitch(30, 28, 'right_exit_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[30][32] = {}
        self.junctions[30][32]['left_entry_railroad_switch'] = RailroadSwitch(30, 32, 'left_entry_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[30][32]['left_exit_railroad_switch'] = RailroadSwitch(30, 32, 'left_exit_railroad_switch',
                                                                             game_config=self.c)
        self.junctions[30][32]['right_entry_railroad_switch'] = RailroadSwitch(30, 32, 'right_entry_railroad_switch',
                                                                               game_config=self.c)
        self.junctions[30][32]['right_exit_railroad_switch'] = RailroadSwitch(30, 32, 'right_exit_railroad_switch',
                                                                              game_config=self.c)
        self.logger.debug('junctions for track 4 created')

        self.junctions[101] = {}
        self.junctions[101][21] = {}
        self.junctions[101][21]['left_entry_railroad_switch'] = RailroadSwitch(101, 21, 'left_entry_railroad_switch',
                                                                               game_config=self.c)
        self.junctions[101][21]['left_exit_railroad_switch'] = RailroadSwitch(101, 21, 'left_exit_railroad_switch',
                                                                              game_config=self.c)
        self.junctions[101][103] = {}
        self.junctions[101][103]['left_entry_crossover'] = Crossover(101, 103, 'left_entry_crossover',
                                                                     game_config=self.c)
        self.junctions[101][103]['left_exit_crossover'] = Crossover(101, 103, 'left_exit_crossover', game_config=self.c)

        self.junctions[102] = {}
        self.junctions[102][22] = {}
        self.junctions[102][22]['right_entry_railroad_switch'] = RailroadSwitch(102, 22, 'right_entry_railroad_switch',
                                                                                game_config=self.c)
        self.junctions[102][22]['right_exit_railroad_switch'] = RailroadSwitch(102, 22, 'right_exit_railroad_switch',
                                                                               game_config=self.c)
        self.junctions[102][104] = {}
        self.junctions[102][104]['right_entry_crossover'] = Crossover(102, 104, 'right_entry_crossover',
                                                                      game_config=self.c)
        self.junctions[102][104]['right_exit_crossover'] = Crossover(102, 104, 'right_exit_crossover',
                                                                     game_config=self.c)

        self.junctions[103] = {}
        self.junctions[103][29] = {}
        self.junctions[103][29]['left_entry_railroad_switch'] = RailroadSwitch(103, 29, 'left_entry_railroad_switch',
                                                                               game_config=self.c)
        self.junctions[103][29]['left_exit_railroad_switch'] = RailroadSwitch(103, 29, 'left_exit_railroad_switch',
                                                                              game_config=self.c)

        self.junctions[104] = {}
        self.junctions[104][30] = {}
        self.junctions[104][30]['right_entry_railroad_switch'] = RailroadSwitch(104, 30, 'right_entry_railroad_switch',
                                                                                game_config=self.c)
        self.junctions[104][30]['right_exit_railroad_switch'] = RailroadSwitch(104, 30, 'right_exit_railroad_switch',
                                                                               game_config=self.c)
        self.logger.info('all junctions created')

        self.junctions[21][23]['left_entry_crossover'].dependency = self.junctions[23][21]['left_exit_crossover']
        self.junctions[23][21]['left_exit_crossover'].dependency = self.junctions[21][23]['left_entry_crossover']
        self.junctions[22][24]['right_entry_crossover'].dependency = self.junctions[24][22]['right_exit_crossover']
        self.junctions[24][22]['right_exit_crossover'].dependency = self.junctions[22][24]['right_entry_crossover']

        for i in self.junctions:
            for j in self.junctions[i]:
                for k in self.junctions[i][j]:
                    if k == 'left_entry_railroad_switch':
                        self.junctions[i][j][k].dependency = self.junctions[i][j]['left_exit_railroad_switch']
                    elif k == 'left_exit_railroad_switch':
                        self.junctions[i][j][k].dependency = self.junctions[i][j]['left_entry_railroad_switch']
                    elif k == 'right_entry_railroad_switch':
                        self.junctions[i][j][k].dependency = self.junctions[i][j]['right_exit_railroad_switch']
                    elif k == 'right_exit_railroad_switch':
                        self.junctions[i][j][k].dependency = self.junctions[i][j]['right_entry_railroad_switch']
                    elif k == 'left_entry_crossover' and i in (1, 2, 101, 102):
                        self.junctions[i][j][k].dependency = self.junctions[i][j]['left_exit_crossover']
                    elif k == 'left_exit_crossover' and i in (1, 2, 101, 102):
                        self.junctions[i][j][k].dependency = self.junctions[i][j]['left_entry_crossover']
                    elif k == 'right_entry_crossover' and i in (1, 2, 101, 102):
                        self.junctions[i][j][k].dependency = self.junctions[i][j]['right_exit_crossover']
                    elif k == 'right_exit_crossover' and i in (1, 2, 101, 102):
                        self.junctions[i][j][k].dependency = self.junctions[i][j]['right_entry_crossover']

        self.logger.info('all junctions associated')

    def construct_base_routes(self):
        self.base_routes[1]['left_entry_base_route'].junctions\
            .append(self.junctions[2][1]['left_entry_crossover'])
        self.base_routes[1]['left_entry_base_route'].junction_position.append([2, 1])
        self.base_routes[1]['left_entry_base_route'].junctions \
            .append(self.junctions[1][21]['left_entry_railroad_switch'])
        self.base_routes[1]['left_entry_base_route'].junction_position.append(1)

        self.base_routes[1]['right_entry_base_route'].junctions\
            .append(self.junctions[1][2]['right_entry_crossover'])
        self.base_routes[1]['right_entry_base_route'].junction_position.append([1, 1])
        self.base_routes[1]['right_entry_base_route'].junctions \
            .append(self.junctions[1][29]['right_entry_railroad_switch'])
        self.base_routes[1]['right_entry_base_route'].junction_position.append(1)

        self.base_routes[1]['left_exit_base_route'].junctions\
            .append(self.junctions[1][21]['left_exit_railroad_switch'])
        self.base_routes[1]['left_exit_base_route'].junction_position.append(1)
        self.base_routes[1]['left_exit_base_route'].junctions\
            .append(self.junctions[2][1]['left_exit_crossover'])
        self.base_routes[1]['left_exit_base_route'].junction_position.append([1, 1])

        self.base_routes[1]['right_exit_base_route'].junctions \
            .append(self.junctions[1][29]['right_exit_railroad_switch'])
        self.base_routes[1]['right_exit_base_route'].junction_position.append(1)
        self.base_routes[1]['right_exit_base_route'].junctions\
            .append(self.junctions[1][2]['right_exit_crossover'])
        self.base_routes[1]['right_exit_base_route'].junction_position.append([1, 2])

        self.base_routes[3]['left_entry_base_route'].junctions\
            .append(self.junctions[2][1]['left_entry_crossover'])
        self.base_routes[3]['left_entry_base_route'].junction_position.append([2, 1])
        self.base_routes[3]['left_entry_base_route'].junctions \
            .append(self.junctions[1][21]['left_entry_railroad_switch'])
        self.base_routes[3]['left_entry_base_route'].junction_position.append(21)
        self.base_routes[3]['left_entry_base_route'].junctions \
            .append(self.junctions[21][3]['left_entry_railroad_switch'])
        self.base_routes[3]['left_entry_base_route'].junction_position.append(3)

        self.base_routes[3]['right_entry_base_route'].junctions\
            .append(self.junctions[1][2]['right_entry_crossover'])
        self.base_routes[3]['right_entry_base_route'].junction_position.append([1, 1])
        self.base_routes[3]['right_entry_base_route'].junctions \
            .append(self.junctions[1][29]['right_entry_railroad_switch'])
        self.base_routes[3]['right_entry_base_route'].junction_position.append(29)
        self.base_routes[3]['right_entry_base_route'].junctions \
            .append(self.junctions[29][3]['right_entry_railroad_switch'])
        self.base_routes[3]['right_entry_base_route'].junction_position.append(3)

        self.base_routes[3]['left_exit_base_route'].junctions \
            .append(self.junctions[21][3]['left_exit_railroad_switch'])
        self.base_routes[3]['left_exit_base_route'].junction_position.append(3)
        self.base_routes[3]['left_exit_base_route'].junctions \
            .append(self.junctions[1][21]['left_exit_railroad_switch'])
        self.base_routes[3]['left_exit_base_route'].junction_position.append(21)
        self.base_routes[3]['left_exit_base_route'].junctions\
            .append(self.junctions[2][1]['left_exit_crossover'])
        self.base_routes[3]['left_exit_base_route'].junction_position.append([1, 1])

        self.base_routes[3]['right_exit_base_route'].junctions \
            .append(self.junctions[29][3]['right_exit_railroad_switch'])
        self.base_routes[3]['right_exit_base_route'].junction_position.append(3)
        self.base_routes[3]['right_exit_base_route'].junctions \
            .append(self.junctions[1][29]['right_exit_railroad_switch'])
        self.base_routes[3]['right_exit_base_route'].junction_position.append(29)
        self.base_routes[3]['right_exit_base_route'].junctions\
            .append(self.junctions[1][2]['right_exit_crossover'])
        self.base_routes[3]['right_exit_base_route'].junction_position.append([1, 2])

        for i in range(5, 20, 4):
            # ----------- left entry ---------------
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[2][1]['left_entry_crossover'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append([2, 1])
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[1][21]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(21)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[21][3]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(21)
            for j in range(5, i, 4):
                self.base_routes[i]['left_entry_base_route'].junctions \
                    .append(self.junctions[21][j]['left_entry_railroad_switch'])
                self.base_routes[i]['left_entry_base_route'].junction_position.append(21)

            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[21][i]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(i)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[i][i + 2]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(i)

            # ---------------- right entry --------------
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[1][2]['right_entry_crossover'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append([1, 1])
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[1][29]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][3]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            for j in range(5, i, 4):
                self.base_routes[i]['right_entry_base_route'].junctions \
                    .append(self.junctions[29][j]['right_entry_railroad_switch'])
                self.base_routes[i]['right_entry_base_route'].junction_position.append(29)

            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][i]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(i)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[i][i + 2]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(i)

            # ------------------ left exit ---------------
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[i][i + 2]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(i)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[21][i]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(i)
            for j in range(i - 4, 4, -4):
                self.base_routes[i]['left_exit_base_route'].junctions \
                    .append(self.junctions[21][j]['left_exit_railroad_switch'])
                self.base_routes[i]['left_exit_base_route'].junction_position.append(21)

            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[21][3]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(21)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[1][21]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(21)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[2][1]['left_exit_crossover'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append([1, 1])

            # --------------- right exit --------------
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[i][i + 2]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(i)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][i]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(i)
            for j in range(i - 4, 4, -4):
                self.base_routes[i]['right_exit_base_route'].junctions \
                    .append(self.junctions[29][j]['right_exit_railroad_switch'])
                self.base_routes[i]['right_exit_base_route'].junction_position.append(29)

            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][3]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[1][29]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[1][2]['right_exit_crossover'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append([1, 2])

        for i in range(7, 20, 4):
            # ----------------- left entry ------------
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[2][1]['left_entry_crossover'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append([2, 1])
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[1][21]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(21)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[21][3]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(21)
            for j in range(5, i - 2, 4):
                self.base_routes[i]['left_entry_base_route'].junctions \
                    .append(self.junctions[21][j]['left_entry_railroad_switch'])
                self.base_routes[i]['left_entry_base_route'].junction_position.append(21)

            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[21][i - 2]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(i - 2)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[i - 2][i]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(i)

            # ---------------- right entry --------------
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[1][2]['right_entry_crossover'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append([1, 1])
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[1][29]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][3]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            for j in range(5, i - 2, 4):
                self.base_routes[i]['right_entry_base_route'].junctions \
                    .append(self.junctions[29][j]['right_entry_railroad_switch'])
                self.base_routes[i]['right_entry_base_route'].junction_position.append(29)

            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][i - 2]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(i - 2)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[i - 2][i]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(i)

            # ------------------ left exit ---------------
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[i - 2][i]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(i)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[21][i - 2]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(i - 2)
            for j in range(i - 6, 4, -4):
                self.base_routes[i]['left_exit_base_route'].junctions \
                    .append(self.junctions[21][j]['left_exit_railroad_switch'])
                self.base_routes[i]['left_exit_base_route'].junction_position.append(21)

            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[21][3]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(21)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[1][21]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(21)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[2][1]['left_exit_crossover'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append([1, 1])

            # --------------- right exit --------------
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[i - 2][i]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(i)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][i - 2]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(i - 2)
            for j in range(i - 6, 4, -4):
                self.base_routes[i]['right_exit_base_route'].junctions \
                    .append(self.junctions[29][j]['right_exit_railroad_switch'])
                self.base_routes[i]['right_exit_base_route'].junction_position.append(29)

            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][3]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[1][29]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[1][2]['right_exit_crossover'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append([1, 2])

        for i in (21, 23):
            # ------------- left entry ---------------
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[2][1]['left_entry_crossover'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append([2, 1])
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[1][21]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(21)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[21][3]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(21)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[21][5]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(21)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[21][9]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(21)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[21][13]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(21)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[21][17]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(21)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[101][21]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(21)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[21][23]['left_entry_crossover'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append([21, i])

            # ------------- left side entry ---------------
            self.base_routes[i]['left_side_entry_base_route'].junctions \
                .append(self.junctions[101][103]['left_entry_crossover'])
            self.base_routes[i]['left_side_entry_base_route'].junction_position \
                .append([101, 101])
            self.base_routes[i]['left_side_entry_base_route'].junctions \
                .append(self.junctions[101][21]['left_entry_railroad_switch'])
            self.base_routes[i]['left_side_entry_base_route'].junction_position.append(101)
            self.base_routes[i]['left_side_entry_base_route'].junctions \
                .append(self.junctions[21][23]['left_entry_crossover'])
            self.base_routes[i]['left_side_entry_base_route'].junction_position \
                .append([21, i])

            # ------------- right entry ---------------
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[1][2]['right_entry_crossover'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append([1, 1])
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[1][29]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][3]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][5]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][9]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][13]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][17]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][21]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(21)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[21][23]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(i)

            # ------------- left exit ---------------
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[23][21]['left_exit_crossover'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append([i, 21])
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[101][21]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(21)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[21][17]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(21)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[21][13]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(21)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[21][9]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(21)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[21][5]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(21)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[21][3]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(21)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[1][21]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(21)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[2][1]['left_exit_crossover'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append([1, 1])

            # ------------- right exit ---------------
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[21][23]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(i)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][21]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(21)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][17]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][13]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][9]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][5]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][3]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[1][29]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[1][2]['right_exit_crossover'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append([1, 2])

        # ------------- left side exit ---------------
        self.base_routes[21]['left_side_exit_base_route'].junctions \
            .append(self.junctions[23][21]['left_exit_crossover'])
        self.base_routes[21]['left_side_exit_base_route'].junction_position \
            .append([21, 21])
        self.base_routes[21]['left_side_exit_base_route'].junctions \
            .append(self.junctions[101][21]['left_exit_railroad_switch'])
        self.base_routes[21]['left_side_exit_base_route'].junction_position.append(101)
        self.base_routes[21]['left_side_exit_base_route'].junctions \
            .append(self.junctions[101][103]['left_exit_crossover'])
        self.base_routes[21]['left_side_exit_base_route'].junction_position \
            .append([101, 103])
        # ------------- left side exit ---------------
        self.base_routes[23]['left_side_exit_base_route'].junctions \
            .append(self.junctions[23][21]['left_exit_crossover'])
        self.base_routes[23]['left_side_exit_base_route'].junction_position \
            .append([23, 23])
        self.base_routes[23]['left_side_exit_base_route'].junctions \
            .append(self.junctions[103][29]['left_exit_railroad_switch'])
        self.base_routes[23]['left_side_exit_base_route'].junction_position.append(103)
        self.base_routes[23]['left_side_exit_base_route'].junctions \
            .append(self.junctions[101][103]['left_exit_crossover'])
        self.base_routes[23]['left_side_exit_base_route'].junction_position \
            .append([103, 103])

        for i in (25, 27):
            # ------------- left side entry ---------------
            self.base_routes[i]['left_side_entry_base_route'].junctions \
                .append(self.junctions[101][103]['left_entry_crossover'])
            self.base_routes[i]['left_side_entry_base_route'].junction_position \
                .append([101, 103])
            self.base_routes[i]['left_side_entry_base_route'].junctions \
                .append(self.junctions[103][29]['left_entry_railroad_switch'])
            self.base_routes[i]['left_side_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['left_side_entry_base_route'].junctions \
                .append(self.junctions[29][27]['left_entry_railroad_switch'])
            self.base_routes[i]['left_side_entry_base_route'].junction_position.append(27)
            self.base_routes[i]['left_side_entry_base_route'].junctions \
                .append(self.junctions[27][25]['left_entry_railroad_switch'])
            self.base_routes[i]['left_side_entry_base_route'].junction_position.append(i)

            # ------------- left side exit ---------------
            self.base_routes[i]['left_side_exit_base_route'].junctions \
                .append(self.junctions[27][25]['left_exit_railroad_switch'])
            self.base_routes[i]['left_side_exit_base_route'].junction_position.append(i)
            self.base_routes[i]['left_side_exit_base_route'].junctions \
                .append(self.junctions[29][27]['left_exit_railroad_switch'])
            self.base_routes[i]['left_side_exit_base_route'].junction_position.append(27)
            self.base_routes[i]['left_side_exit_base_route'].junctions \
                .append(self.junctions[103][29]['left_exit_railroad_switch'])
            self.base_routes[i]['left_side_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['left_side_exit_base_route'].junctions \
                .append(self.junctions[101][103]['left_exit_crossover'])
            self.base_routes[i]['left_side_exit_base_route'].junction_position \
                .append([103, 103])

            # -------------- right entry --------------
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[1][2]['right_entry_crossover'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append([1, 1])
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[1][29]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][3]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][5]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][9]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][13]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][17]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][21]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][25]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(25)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[25][27]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(i)

            # -------------- right exit --------------
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[25][27]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(i)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][25]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(25)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][21]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][17]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][13]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][9]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][5]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][3]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[1][29]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[1][2]['right_exit_crossover'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append([1, 2])

        for i in (29, 31):
            # ------------- left side entry ---------------
            self.base_routes[i]['left_side_entry_base_route'].junctions \
                .append(self.junctions[101][103]['left_entry_crossover'])
            self.base_routes[i]['left_side_entry_base_route'].junction_position \
                .append([101, 103])
            self.base_routes[i]['left_side_entry_base_route'].junctions \
                .append(self.junctions[103][29]['left_entry_railroad_switch'])
            self.base_routes[i]['left_side_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['left_side_entry_base_route'].junctions \
                .append(self.junctions[29][27]['left_entry_railroad_switch'])
            self.base_routes[i]['left_side_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['left_side_entry_base_route'].junctions \
                .append(self.junctions[29][31]['left_entry_railroad_switch'])
            self.base_routes[i]['left_side_entry_base_route'].junction_position.append(i)

            # ------------- left side exit ---------------
            self.base_routes[i]['left_side_exit_base_route'].junctions \
                .append(self.junctions[29][31]['left_exit_railroad_switch'])
            self.base_routes[i]['left_side_exit_base_route'].junction_position.append(i)
            self.base_routes[i]['left_side_exit_base_route'].junctions \
                .append(self.junctions[29][27]['left_exit_railroad_switch'])
            self.base_routes[i]['left_side_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['left_side_exit_base_route'].junctions \
                .append(self.junctions[103][29]['left_exit_railroad_switch'])
            self.base_routes[i]['left_side_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['left_side_exit_base_route'].junctions \
                .append(self.junctions[101][103]['left_exit_crossover'])
            self.base_routes[i]['left_side_exit_base_route'].junction_position \
                .append([103, 103])

            # -------------- right entry --------------
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[1][2]['right_entry_crossover'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append([1, 1])
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[1][29]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][3]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][5]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][9]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][13]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][17]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][21]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][25]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(29)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[29][31]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(i)

            # -------------- right exit --------------
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][31]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(i)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][25]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][21]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][17]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][13]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][9]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][5]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[29][3]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[1][29]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(29)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[1][2]['right_exit_crossover'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append([1, 2])

        self.logger.info('trail points initialized for odd tracks')

        self.base_routes[2]['left_entry_base_route'].junctions\
            .append(self.junctions[2][1]['left_entry_crossover'])
        self.base_routes[2]['left_entry_base_route'].junction_position.append([2, 2])
        self.base_routes[2]['left_entry_base_route'].junctions \
            .append(self.junctions[2][30]['left_entry_railroad_switch'])
        self.base_routes[2]['left_entry_base_route'].junction_position.append(2)

        self.base_routes[2]['right_entry_base_route'].junctions\
            .append(self.junctions[1][2]['right_entry_crossover'])
        self.base_routes[2]['right_entry_base_route'].junction_position.append([1, 2])
        self.base_routes[2]['right_entry_base_route'].junctions \
            .append(self.junctions[2][22]['right_entry_railroad_switch'])
        self.base_routes[2]['right_entry_base_route'].junction_position.append(2)

        self.base_routes[2]['left_exit_base_route'].junctions \
            .append(self.junctions[2][30]['left_exit_railroad_switch'])
        self.base_routes[2]['left_exit_base_route'].junction_position.append(2)
        self.base_routes[2]['left_exit_base_route'].junctions\
            .append(self.junctions[2][1]['left_exit_crossover'])
        self.base_routes[2]['left_exit_base_route'].junction_position.append([2, 1])

        self.base_routes[2]['right_exit_base_route'].junctions \
            .append(self.junctions[2][22]['right_exit_railroad_switch'])
        self.base_routes[2]['right_exit_base_route'].junction_position.append(2)
        self.base_routes[2]['right_exit_base_route'].junctions\
            .append(self.junctions[1][2]['right_exit_crossover'])
        self.base_routes[2]['right_exit_base_route'].junction_position.append([2, 2])

        self.base_routes[4]['left_entry_base_route'].junctions\
            .append(self.junctions[2][1]['left_entry_crossover'])
        self.base_routes[4]['left_entry_base_route'].junction_position.append([2, 2])
        self.base_routes[4]['left_entry_base_route'].junctions \
            .append(self.junctions[2][30]['left_entry_railroad_switch'])
        self.base_routes[4]['left_entry_base_route'].junction_position.append(30)
        self.base_routes[4]['left_entry_base_route'].junctions \
            .append(self.junctions[30][4]['left_entry_railroad_switch'])
        self.base_routes[4]['left_entry_base_route'].junction_position.append(4)

        self.base_routes[4]['right_entry_base_route'].junctions\
            .append(self.junctions[1][2]['right_entry_crossover'])
        self.base_routes[4]['right_entry_base_route'].junction_position.append([1, 2])
        self.base_routes[4]['right_entry_base_route'].junctions \
            .append(self.junctions[2][22]['right_entry_railroad_switch'])
        self.base_routes[4]['right_entry_base_route'].junction_position.append(22)
        self.base_routes[4]['right_entry_base_route'].junctions \
            .append(self.junctions[22][4]['right_entry_railroad_switch'])
        self.base_routes[4]['right_entry_base_route'].junction_position.append(4)

        self.base_routes[4]['left_exit_base_route'].junctions \
            .append(self.junctions[30][4]['left_exit_railroad_switch'])
        self.base_routes[4]['left_exit_base_route'].junction_position.append(4)
        self.base_routes[4]['left_exit_base_route'].junctions \
            .append(self.junctions[2][30]['left_exit_railroad_switch'])
        self.base_routes[4]['left_exit_base_route'].junction_position.append(30)
        self.base_routes[4]['left_exit_base_route'].junctions\
            .append(self.junctions[2][1]['left_exit_crossover'])
        self.base_routes[4]['left_exit_base_route'].junction_position.append([2, 1])

        self.base_routes[4]['right_exit_base_route'].junctions \
            .append(self.junctions[22][4]['right_exit_railroad_switch'])
        self.base_routes[4]['right_exit_base_route'].junction_position.append(4)
        self.base_routes[4]['right_exit_base_route'].junctions \
            .append(self.junctions[2][22]['right_exit_railroad_switch'])
        self.base_routes[4]['right_exit_base_route'].junction_position.append(22)
        self.base_routes[4]['right_exit_base_route'].junctions\
            .append(self.junctions[1][2]['right_exit_crossover'])
        self.base_routes[4]['right_exit_base_route'].junction_position.append([2, 2])

        for i in range(6, 21, 4):
            # --------------- left entry -----------------
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[2][1]['left_entry_crossover'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append([2, 2])
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[2][30]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][4]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            for j in range(6, i, 4):
                self.base_routes[i]['left_entry_base_route'].junctions \
                    .append(self.junctions[30][j]['left_entry_railroad_switch'])
                self.base_routes[i]['left_entry_base_route'].junction_position.append(30)

            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][i]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(i)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[i][i + 2]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(i)

            # --------------------- right entry ---------------
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[1][2]['right_entry_crossover'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append([1, 2])
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[2][22]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(22)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[22][4]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(22)
            for j in range(6, i, 4):
                self.base_routes[i]['right_entry_base_route'].junctions \
                    .append(self.junctions[22][j]['right_entry_railroad_switch'])
                self.base_routes[i]['right_entry_base_route'].junction_position.append(22)

            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[22][i]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(i)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[i][i + 2]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(i)

            # ----------------- left exit ---------------
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[i][i + 2]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(i)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][i]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(i)
            if i > 6:
                for j in range(i - 4, 5, -4):
                    self.base_routes[i]['left_exit_base_route'].junctions \
                        .append(self.junctions[30][j]['left_exit_railroad_switch'])
                    self.base_routes[i]['left_exit_base_route'].junction_position.append(30)

            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][4]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[2][30]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[2][1]['left_exit_crossover'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append([2, 1])

            # ---------------- right exit ------------------
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[i][i + 2]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(i)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[22][i]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(i)
            if i > 6:
                for j in range(i - 4, 5, -4):
                    self.base_routes[i]['right_exit_base_route'].junctions \
                        .append(self.junctions[22][j]['right_exit_railroad_switch'])
                    self.base_routes[i]['right_exit_base_route'].junction_position.append(22)

            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[22][4]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(22)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[2][22]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(22)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[1][2]['right_exit_crossover'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append([2, 2])

        for i in range(8, 21, 4):
            # --------------- left entry -----------------
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[2][1]['left_entry_crossover'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append([2, 2])
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[2][30]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][4]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            for j in range(6, i - 2, 4):
                self.base_routes[i]['left_entry_base_route'].junctions \
                    .append(self.junctions[30][j]['left_entry_railroad_switch'])
                self.base_routes[i]['left_entry_base_route'].junction_position.append(30)

            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][i - 2]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(i - 2)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[i - 2][i]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(i)

            # --------------------- right entry ---------------
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[1][2]['right_entry_crossover'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append([1, 2])
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[2][22]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(22)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[22][4]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(22)
            for j in range(6, i - 2, 4):
                self.base_routes[i]['right_entry_base_route'].junctions \
                    .append(self.junctions[22][j]['right_entry_railroad_switch'])
                self.base_routes[i]['right_entry_base_route'].junction_position.append(22)

            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[22][i - 2]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(i - 2)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[i - 2][i]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(i)

            # ----------------- left exit ---------------
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[i - 2][i]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(i)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][i - 2]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(i - 2)
            if i > 8:
                for j in range(i - 6, 5, -4):
                    self.base_routes[i]['left_exit_base_route'].junctions \
                        .append(self.junctions[30][j]['left_exit_railroad_switch'])
                    self.base_routes[i]['left_exit_base_route'].junction_position.append(30)

            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][4]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[2][30]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[2][1]['left_exit_crossover'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append([2, 1])

            # ---------------- right exit ------------------
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[i - 2][i]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(i)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[22][i - 2]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(i - 2)
            if i > 8:
                for j in range(i - 6, 5, -4):
                    self.base_routes[i]['right_exit_base_route'].junctions \
                        .append(self.junctions[22][j]['right_exit_railroad_switch'])
                    self.base_routes[i]['right_exit_base_route'].junction_position\
                        .append(22)

            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[22][4]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(22)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[2][22]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(22)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[1][2]['right_exit_crossover'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append([2, 2])

        for i in (22, 24):
            # --------------- left entry -----------------
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[2][1]['left_entry_crossover'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append([2, 2])
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[2][30]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][4]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][6]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][10]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][14]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][18]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][22]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(22)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[22][24]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(i)

            # --------------------- right entry ---------------
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[1][2]['right_entry_crossover'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append([1, 2])
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[2][22]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(22)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[22][4]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(22)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[22][6]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(22)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[22][10]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(22)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[22][14]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(22)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[22][18]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(22)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[102][22]['right_entry_railroad_switch'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append(22)
            self.base_routes[i]['right_entry_base_route'].junctions \
                .append(self.junctions[22][24]['right_entry_crossover'])
            self.base_routes[i]['right_entry_base_route'].junction_position.append([22, i])

            # ------------------ right side entry ----------------
            self.base_routes[i]['right_side_entry_base_route'].junctions \
                .append(self.junctions[102][104]['right_entry_crossover'])
            self.base_routes[i]['right_side_entry_base_route'].junction_position \
                .append([102, 102])
            self.base_routes[i]['right_side_entry_base_route'].junctions \
                .append(self.junctions[102][22]['right_entry_railroad_switch'])
            self.base_routes[i]['right_side_entry_base_route'].junction_position.append(102)
            self.base_routes[i]['right_side_entry_base_route'].junctions \
                .append(self.junctions[22][24]['right_entry_crossover'])
            self.base_routes[i]['right_side_entry_base_route'].junction_position \
                .append([22, i])

            # ----------------- left exit ---------------
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[22][24]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(i)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][22]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(22)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][18]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][14]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][10]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][6]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][4]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[2][30]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[2][1]['left_exit_crossover'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append([2, 1])

            # ---------------- right exit ------------------
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[24][22]['right_exit_crossover'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append([i, 22])
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[102][22]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(22)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[22][18]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(22)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[22][14]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(22)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[22][10]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(22)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[22][6]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(22)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[22][4]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(22)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[2][22]['right_exit_railroad_switch'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append(22)
            self.base_routes[i]['right_exit_base_route'].junctions \
                .append(self.junctions[1][2]['right_exit_crossover'])
            self.base_routes[i]['right_exit_base_route'].junction_position.append([2, 2])

        # ------------ right side exit ------------
        self.base_routes[22]['right_side_exit_base_route'].junctions \
            .append(self.junctions[24][22]['right_exit_crossover'])
        self.base_routes[22]['right_side_exit_base_route'].junction_position \
            .append([22, 22])
        self.base_routes[22]['right_side_exit_base_route'].junctions \
            .append(self.junctions[102][22]['right_exit_railroad_switch'])
        self.base_routes[22]['right_side_exit_base_route'].junction_position.append(102)
        self.base_routes[22]['right_side_exit_base_route'].junctions \
            .append(self.junctions[102][104]['right_exit_crossover'])
        self.base_routes[22]['right_side_exit_base_route'].junction_position \
            .append([102, 104])

        # ------------ right side exit ------------
        self.base_routes[24]['right_side_exit_base_route'].junctions \
            .append(self.junctions[24][22]['right_exit_crossover'])
        self.base_routes[24]['right_side_exit_base_route'].junction_position \
            .append([24, 24])
        self.base_routes[24]['right_side_exit_base_route'].junctions \
            .append(self.junctions[104][30]['right_exit_railroad_switch'])
        self.base_routes[24]['right_side_exit_base_route'].junction_position.append(104)
        self.base_routes[24]['right_side_exit_base_route'].junctions \
            .append(self.junctions[102][104]['right_exit_crossover'])
        self.base_routes[24]['right_side_exit_base_route'].junction_position \
            .append([104, 104])

        for i in (26, 28):
            # --------------- left entry -----------------
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[2][1]['left_entry_crossover'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append([2, 2])
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[2][30]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][4]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][6]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][10]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][14]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][18]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][22]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][26]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(26)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[26][28]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(i)

            # ------------------ right side entry ----------------
            self.base_routes[i]['right_side_entry_base_route'].junctions \
                .append(self.junctions[102][104]['right_entry_crossover'])
            self.base_routes[i]['right_side_entry_base_route'].junction_position \
                .append([102, 104])
            self.base_routes[i]['right_side_entry_base_route'].junctions \
                .append(self.junctions[104][30]['right_entry_railroad_switch'])
            self.base_routes[i]['right_side_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['right_side_entry_base_route'].junctions \
                .append(self.junctions[30][28]['right_entry_railroad_switch'])
            self.base_routes[i]['right_side_entry_base_route'].junction_position.append(28)
            self.base_routes[i]['right_side_entry_base_route'].junctions \
                .append(self.junctions[28][26]['right_entry_railroad_switch'])
            self.base_routes[i]['right_side_entry_base_route'].junction_position.append(i)

            # ----------------- left exit ---------------
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[26][28]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(i)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][26]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(26)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][22]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][18]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][14]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][10]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][6]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][4]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[2][30]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[2][1]['left_exit_crossover'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append([2, 1])

            # ------------ right side exit ------------
            self.base_routes[i]['right_side_exit_base_route'].junctions \
                .append(self.junctions[28][26]['right_exit_railroad_switch'])
            self.base_routes[i]['right_side_exit_base_route'].junction_position.append(i)
            self.base_routes[i]['right_side_exit_base_route'].junctions \
                .append(self.junctions[30][28]['right_exit_railroad_switch'])
            self.base_routes[i]['right_side_exit_base_route'].junction_position.append(28)
            self.base_routes[i]['right_side_exit_base_route'].junctions \
                .append(self.junctions[104][30]['right_exit_railroad_switch'])
            self.base_routes[i]['right_side_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['right_side_exit_base_route'].junctions \
                .append(self.junctions[102][104]['right_exit_crossover'])
            self.base_routes[i]['right_side_exit_base_route'].junction_position \
                .append([104, 104])

        for i in (30, 32):
            # --------------- left entry -----------------
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[2][1]['left_entry_crossover'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append([2, 2])
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[2][30]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][4]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][6]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][10]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][14]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][18]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][22]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][26]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['left_entry_base_route'].junctions \
                .append(self.junctions[30][32]['left_entry_railroad_switch'])
            self.base_routes[i]['left_entry_base_route'].junction_position.append(i)

            # ------------------ right side entry ----------------
            self.base_routes[i]['right_side_entry_base_route'].junctions \
                .append(self.junctions[102][104]['right_entry_crossover'])
            self.base_routes[i]['right_side_entry_base_route'].junction_position \
                .append([102, 104])
            self.base_routes[i]['right_side_entry_base_route'].junctions \
                .append(self.junctions[104][30]['right_entry_railroad_switch'])
            self.base_routes[i]['right_side_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['right_side_entry_base_route'].junctions \
                .append(self.junctions[30][28]['right_entry_railroad_switch'])
            self.base_routes[i]['right_side_entry_base_route'].junction_position.append(30)
            self.base_routes[i]['right_side_entry_base_route'].junctions \
                .append(self.junctions[30][32]['right_entry_railroad_switch'])
            self.base_routes[i]['right_side_entry_base_route'].junction_position.append(i)

            # ----------------- left exit ---------------
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][32]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(i)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][26]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][22]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][18]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][14]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][10]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][6]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[30][4]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[2][30]['left_exit_railroad_switch'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['left_exit_base_route'].junctions \
                .append(self.junctions[2][1]['left_exit_crossover'])
            self.base_routes[i]['left_exit_base_route'].junction_position.append([2, 1])

            # ------------ right side exit ------------
            self.base_routes[i]['right_side_exit_base_route'].junctions \
                .append(self.junctions[30][32]['right_exit_railroad_switch'])
            self.base_routes[i]['right_side_exit_base_route'].junction_position.append(i)
            self.base_routes[i]['right_side_exit_base_route'].junctions \
                .append(self.junctions[30][28]['right_exit_railroad_switch'])
            self.base_routes[i]['right_side_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['right_side_exit_base_route'].junctions \
                .append(self.junctions[104][30]['right_exit_railroad_switch'])
            self.base_routes[i]['right_side_exit_base_route'].junction_position.append(30)
            self.base_routes[i]['right_side_exit_base_route'].junctions \
                .append(self.junctions[102][104]['right_exit_crossover'])
            self.base_routes[i]['right_side_exit_base_route'].junction_position \
                .append([104, 104])

        self.logger.info('trail points initialized for even tracks')

    def create_onboarding_tips(self):
        self.dispatcher.mini_map_tip = self.mini_map_tip
        self.objects.append(self.mini_map_tip)
        for i in self.tracks:
            self.objects.append(i.not_enough_money_tip)
            self.objects.append(i.under_construction_tip)

        self.logger.debug('saved_onboarding_tip appended to global objects list')
        self.logger.info('all tips appended to global objects list')

    def create_buttons(self):
        self.logger.debug('------- START CREATING BUTTONS -------')

        def pause_game(button):
            button.on_button_is_deactivated()
            self.game_paused = True
            self.resume_button.on_button_is_activated()
            self.logger.critical('------- GAME IS PAUSED -------')

        def resume_game(button):
            button.on_button_is_deactivated()
            self.game_paused = False
            self.pause_button.on_button_is_activated()
            self.logger.critical('------- GAME IS RESUMED -------')

        def open_schedule(button):
            button.on_button_is_deactivated()
            self.mini_map_tip.on_condition_not_met()
            self.scheduler.on_board_activate()
            self.close_schedule_button.on_button_is_activated()

        def close_schedule(button):
            button.on_button_is_deactivated()
            self.scheduler.on_board_deactivate()
            self.open_schedule_button.on_button_is_activated()

        def close_game(button):
            if path.exists('user_cfg/trains'):
                for j in listdir('user_cfg/trains'):
                    remove('user_cfg/trains/' + j)

                rmdir('user_cfg/trains')

            for i in self.objects:
                i.save_state()

            for x in range(len(self.base_routes)):
                for y in self.base_routes[x]:
                    if self.base_routes[x][y] is not None:
                        self.base_routes[x][y].save_state()

            for u in self.junctions:
                for v in self.junctions[u]:
                    for w in self.junctions[u][v]:
                        self.junctions[u][v][w].save_state()

            self.surface.close()
            exit()

        def iconify_game(button):
            self.surface.minimize()

        def save_game(button):
            self.logger.critical('------- GAME SAVE START -------')
            if path.exists('user_cfg/trains'):
                for j in listdir('user_cfg/trains'):
                    remove('user_cfg/trains/' + j)

                rmdir('user_cfg/trains')

            for i in self.objects:
                i.save_state()

            for x in range(len(self.base_routes)):
                for y in self.base_routes[x]:
                    if self.base_routes[x][y] is not None:
                        self.base_routes[x][y].save_state()

            for u in self.junctions:
                for v in self.junctions[u]:
                    for w in self.junctions[u][v]:
                        self.junctions[u][v][w].save_state()

            self.logger.critical('------- GAME SAVE END -------')

        self.logger.debug('time appended to global objects list')
        self.objects.append(MainFrame(batch=self.batch,
                                      main_frame_group=self.top_bottom_bars_ordered_group, game_config=self.c))
        self.logger.debug('bottom bar appended to global objects list')
        self.pause_button = Button(position=(self.c.screen_resolution[0] - 80, 0), button_size=(80, 80),
                                   text='‖', font_size=self.c.play_pause_button_font_size,
                                   on_click=pause_game, is_activated=True,
                                   batch=self.batch, button_group=self.buttons_general_borders_day_text_ordered_group,
                                   text_group=self.buttons_text_and_borders_ordered_group,
                                   borders_group=self.buttons_text_and_borders_ordered_group, game_config=self.c,
                                   logs_description='pause/resume', map_move_mode=self.map_move_mode)
        self.resume_button = Button(position=(self.c.screen_resolution[0] - 80, 0), button_size=(80, 80),
                                    text='►', font_size=self.c.play_pause_button_font_size,
                                    on_click=resume_game, is_activated=False,
                                    batch=self.batch, button_group=self.buttons_general_borders_day_text_ordered_group,
                                    text_group=self.buttons_text_and_borders_ordered_group,
                                    borders_group=self.buttons_text_and_borders_ordered_group, game_config=self.c,
                                    logs_description='pause/resume', map_move_mode=self.map_move_mode)
        self.close_button = Button(position=(self.c.screen_resolution[0] - 34, self.c.screen_resolution[1] - 34),
                                   button_size=(34, 34), text='X', font_size=self.c.iconify_close_button_font_size,
                                   on_click=close_game, is_activated=True,
                                   batch=self.batch, button_group=self.buttons_general_borders_day_text_ordered_group,
                                   text_group=self.buttons_text_and_borders_ordered_group,
                                   borders_group=self.buttons_text_and_borders_ordered_group, game_config=self.c,
                                   logs_description='close', map_move_mode=self.map_move_mode)
        self.iconify_button = Button(position=(self.c.screen_resolution[0] - 66, self.c.screen_resolution[1] - 34),
                                     button_size=(34, 34), text='_',
                                     font_size=self.c.iconify_close_button_font_size,
                                     on_click=iconify_game, is_activated=True,
                                     batch=self.batch, button_group=self.buttons_general_borders_day_text_ordered_group,
                                     text_group=self.buttons_text_and_borders_ordered_group,
                                     borders_group=self.buttons_text_and_borders_ordered_group, game_config=self.c,
                                     logs_description='iconify', map_move_mode=self.map_move_mode)
        self.open_schedule_button = Button(position=(self.c.screen_resolution[0] - 480, 0), button_size=(200, 80),
                                           text='Open Schedule', font_size=self.c.iconify_close_button_font_size,
                                           on_click=open_schedule, is_activated=True,
                                           batch=self.batch,
                                           button_group=self.buttons_general_borders_day_text_ordered_group,
                                           text_group=self.buttons_text_and_borders_ordered_group,
                                           borders_group=self.buttons_text_and_borders_ordered_group,
                                           game_config=self.c, logs_description='open_schedule',
                                           map_move_mode=self.map_move_mode)
        self.close_schedule_button = Button(position=(self.c.screen_resolution[0] - 480, 0), button_size=(200, 80),
                                            text='Close Schedule', font_size=self.c.iconify_close_button_font_size,
                                            on_click=close_schedule, is_activated=False,
                                            batch=self.batch,
                                            button_group=self.buttons_general_borders_day_text_ordered_group,
                                            text_group=self.buttons_text_and_borders_ordered_group,
                                            borders_group=self.buttons_text_and_borders_ordered_group,
                                            game_config=self.c, logs_description='close_schedule',
                                            map_move_mode=self.map_move_mode)

        self.on_mouse_press_handlers.append(self.handle_mouse_press)
        self.on_mouse_press_handlers.append(self.pause_button.handle_mouse_press)
        self.on_mouse_press_handlers.append(self.resume_button.handle_mouse_press)
        self.on_mouse_press_handlers.append(self.close_button.handle_mouse_press)
        self.on_mouse_press_handlers.append(self.iconify_button.handle_mouse_press)
        self.on_mouse_press_handlers.append(self.open_schedule_button.handle_mouse_press)
        self.on_mouse_press_handlers.append(self.close_schedule_button.handle_mouse_press)

        self.on_mouse_release_handlers.append(self.handle_mouse_release)
        self.on_mouse_release_handlers.append(self.pause_button.handle_mouse_release)
        self.on_mouse_release_handlers.append(self.resume_button.handle_mouse_release)
        self.on_mouse_release_handlers.append(self.close_button.handle_mouse_release)
        self.on_mouse_release_handlers.append(self.iconify_button.handle_mouse_release)
        self.on_mouse_release_handlers.append(self.open_schedule_button.handle_mouse_release)
        self.on_mouse_release_handlers.append(self.close_schedule_button.handle_mouse_release)

        self.on_mouse_motion_handlers.append(self.pause_button.handle_mouse_motion)
        self.on_mouse_motion_handlers.append(self.resume_button.handle_mouse_motion)
        self.on_mouse_motion_handlers.append(self.close_button.handle_mouse_motion)
        self.on_mouse_motion_handlers.append(self.iconify_button.handle_mouse_motion)
        self.on_mouse_motion_handlers.append(self.open_schedule_button.handle_mouse_motion)
        self.on_mouse_motion_handlers.append(self.close_schedule_button.handle_mouse_motion)

        self.on_mouse_leave_handlers.append(self.pause_button.handle_mouse_leave)
        self.on_mouse_leave_handlers.append(self.resume_button.handle_mouse_leave)
        self.on_mouse_leave_handlers.append(self.close_button.handle_mouse_leave)
        self.on_mouse_leave_handlers.append(self.iconify_button.handle_mouse_leave)
        self.on_mouse_leave_handlers.append(self.open_schedule_button.handle_mouse_leave)
        self.on_mouse_leave_handlers.append(self.close_schedule_button.handle_mouse_leave)

        self.on_mouse_drag_handlers.append(self.handle_mouse_drag)
        self.logger.debug('save button button handler appended to global mouse handlers list')
        self.objects.append(self.pause_button)
        self.objects.append(self.resume_button)
        self.logger.debug('pause/resume button appended to global objects list')
        self.objects.append(self.close_button)
        self.objects.append(self.iconify_button)
        self.objects.append(self.open_schedule_button)
        self.objects.append(self.close_schedule_button)
        for i in self.tracks:
            self.on_mouse_press_handlers.append(i.unlock_button.handle_mouse_press)
            self.on_mouse_release_handlers.append(i.unlock_button.handle_mouse_release)
            self.on_mouse_motion_handlers.append(i.unlock_button.handle_mouse_motion)
            self.on_mouse_leave_handlers.append(i.unlock_button.handle_mouse_leave)
            self.objects.append(i.unlock_button)

        self.logger.debug('save button appended to global objects list')
        self.game_time.auto_save_function = save_game
        self.objects.append(self.game_time)
        self.logger.debug('------- END CREATING BUTTONS -------')
        self.logger.warning('all buttons created')


def main():
    try:
        RSSim().run()
    except VideoAdapterNotSupportedException as e:
        MessageBoxEx(win32con.NULL, e.text, e.caption,
                     win32con.MB_OK | win32con.MB_ICONERROR | win32con.MB_DEFBUTTON1
                     | win32con.MB_SYSTEMMODAL | win32con.MB_SETFOREGROUND, 0)
        exit()


if __name__ == '__main__':
    main()
