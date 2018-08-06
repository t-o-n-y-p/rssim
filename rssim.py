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
        self.create_bg_img()
        self.create_infrastructure()
        self.mouse_handlers.append(self.handle_mouse_drag)

    def create_bg_img(self):
        background_image = BgImg(c.background_image)
        self.objects.append(background_image)

    def create_infrastructure(self):
        sys.path.append('./base_route_cfg')
        for j in (c.base_route_flags[0], c.base_route_flags[1], c.base_route_flags[2], c.base_route_flags[3]):
            self.base_routes[0][j] = BaseRoute(0, j)
            placement = self.base_routes[0][j].route_config.exit_signal_placement
            flip_needed = self.base_routes[0][j].route_config.flip_needed
            if placement:
                self.signals[0][j] = Signal(placement, flip_needed)

        for j in (c.base_route_flags[0], c.base_route_flags[1], c.base_route_flags[2], c.base_route_flags[3]):
            self.base_routes[0][j].route_config.exit_signal = self.signals[0][j]
            self.signals[0][j].base_route_exit_list.append(self.base_routes[0][j])

        for i in range(1, 2):
            self.base_routes.append({})
            self.signals.append({})
            for k in c.base_route_flags:
                self.base_routes[i][k] = BaseRoute(i, k)
                placement = self.base_routes[i][k].route_config.exit_signal_placement
                flip_needed = self.base_routes[i][k].route_config.flip_needed
                if placement and k in (c.base_route_flags[6], c.base_route_flags[7]):
                    self.signals[i][k] = Signal(placement, flip_needed)

        for i in range(1, 2):
            self.base_routes[i][c.base_route_flags[6]].route_config.exit_signal = self.signals[i][c.base_route_flags[6]]
            self.base_routes[i][c.base_route_flags[4]].route_config.exit_signal = self.signals[i][c.base_route_flags[6]]
            self.base_routes[i][c.base_route_flags[7]].route_config.exit_signal = self.signals[i][c.base_route_flags[7]]
            self.base_routes[i][c.base_route_flags[5]].route_config.exit_signal = self.signals[i][c.base_route_flags[7]]
            self.signals[i][c.base_route_flags[6]].base_route_exit_list\
                .append(self.base_routes[i][c.base_route_flags[6]])
            # self.signals[i][c.base_route_flags[6]].base_route_exit_list\
            #     .append(self.base_routes[i][c.base_route_flags[4]])
            self.signals[i][c.base_route_flags[6]].base_route_opened_list \
                .append(self.base_routes[i][c.base_route_flags[3]])
            self.signals[i][c.base_route_flags[7]].base_route_exit_list\
                .append(self.base_routes[i][c.base_route_flags[7]])
            self.signals[i][c.base_route_flags[7]].base_route_exit_list\
                .append(self.base_routes[i][c.base_route_flags[5]])
            self.signals[i][c.base_route_flags[7]].base_route_opened_list\
                .append(self.base_routes[i][c.base_route_flags[1]])
            self.signals[0][c.base_route_flags[0]].base_route_opened_list\
                .append(self.base_routes[i][c.base_route_flags[0]])
            self.signals[0][c.base_route_flags[0]].base_route_opened_list\
                .append(self.base_routes[i][c.base_route_flags[4]])
            self.signals[0][c.base_route_flags[2]].base_route_opened_list\
                .append(self.base_routes[i][c.base_route_flags[2]])
            self.signals[0][c.base_route_flags[2]].base_route_opened_list\
                .append(self.base_routes[i][c.base_route_flags[5]])
            self.signals[0][c.base_route_flags[0]].base_route_busy_list\
                .append(self.base_routes[i][c.base_route_flags[0]])
            self.signals[0][c.base_route_flags[2]].base_route_busy_list\
                .append(self.base_routes[i][c.base_route_flags[2]])
            self.signals[0][c.base_route_flags[0]].base_route_busy_list\
                .append(self.base_routes[i][c.base_route_flags[1]])
            self.signals[0][c.base_route_flags[2]].base_route_busy_list\
                .append(self.base_routes[i][c.base_route_flags[3]])

        base_routes_in_train_route = [self.base_routes[0]['{}_base_route'.format(c.train_route_flags[0])]]
        self.train_routes[0][c.train_route_flags[4]] = \
            TrainRoute(base_routes_in_train_route, 0, c.train_route_flags[4])
        base_routes_in_train_route = [self.base_routes[0]['{}_base_route'.format(c.train_route_flags[2])]]
        self.train_routes[0][c.train_route_flags[5]] = \
            TrainRoute(base_routes_in_train_route, 0, c.train_route_flags[5])

        for i in range(1, 2):
            self.train_routes.append({})
            base_routes_in_track = [self.base_routes[i]['left_entry_platform_base_route'],
                                    self.base_routes[i]['right_entry_platform_base_route'],
                                    self.base_routes[i]['left_exit_platform_base_route'],
                                    self.base_routes[i]['right_exit_platform_base_route']]
            new_track = Track()
            new_track.base_routes = base_routes_in_track
            self.tracks.append(new_track)
            for k in (c.train_route_flags[0], c.train_route_flags[2]):
                base_routes_in_train_route = [self.base_routes[0]['{}_base_route'.format(k)],
                                              self.base_routes[i]['{}_base_route'.format(k)],
                                              self.base_routes[i]['{}_platform_base_route'.format(k)]]

                self.train_routes[i][k] = TrainRoute(base_routes_in_train_route, i, k)

            for m in (c.train_route_flags[1], c.train_route_flags[3]):
                base_routes_in_train_route = [self.base_routes[i]['{}_platform_base_route'.format(m)],
                                              self.base_routes[i]['{}_base_route'.format(m)],
                                              self.base_routes[0]['{}_base_route'.format(m)]]

                self.train_routes[i][m] = TrainRoute(base_routes_in_train_route, i, m)

            self.train_routes[i][c.train_route_flags[6]] = TrainRoute(
                [self.base_routes[i]['left_entry_platform_base_route']], i, c.train_route_flags[6])

        for i in range(2):
            for n in self.base_routes[i].keys():
                self.objects.append(self.base_routes[i][n])

            for n in self.signals[i].keys():
                self.objects.append(self.signals[i][n])

        train_dispatcher = Dispatcher()
        for i in range(2):
            train_dispatcher.train_routes.append({})
            for p in self.train_routes[i].keys():
                train_dispatcher.train_routes[i].update({p: self.train_routes[i][p]})

        for i in range(1, ):
            train_dispatcher.tracks.append(self.tracks[i])

        self.objects.append(train_dispatcher)

    def handle_mouse_drag(self, event_type, pos):
        movement = pygame.mouse.get_rel()
        if event_type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            self.base_offset = (self.base_offset[0] + movement[0], self.base_offset[1] + movement[1])
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
