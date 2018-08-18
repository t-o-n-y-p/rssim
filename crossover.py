import configparser
import os

from game_object import GameObject


class Crossover(GameObject):
    def __init__(self, straight_track_1, straight_track_2, direction):
        super().__init__()
        self.straight_track_1 = straight_track_1
        self.straight_track_2 = straight_track_2
        self.direction = direction
        self.dependency = None
        self.busy = {self.straight_track_1: {self.straight_track_1: False,
                                             self.straight_track_2: False},
                     self.straight_track_2: {self.straight_track_2: False}}
        self.force_busy = {self.straight_track_1: {self.straight_track_1: False,
                                                   self.straight_track_2: False},
                           self.straight_track_2: {self.straight_track_2: False}}
        self.last_entered_by = {self.straight_track_1: {self.straight_track_1: 0,
                                                        self.straight_track_2: 0},
                                self.straight_track_2: {self.straight_track_2: 0}}
        self.trail_points = {self.straight_track_1: {self.straight_track_1: (),
                                                     self.straight_track_2: ()},
                             self.straight_track_2: {self.straight_track_2: ()}}
        self.config = None
        self.read_state()

    def read_state(self):
        self.config = configparser.RawConfigParser()
        if os.path.exists('user_cfg/crossovers/crossover_{}_{}_{}.ini'.format(self.straight_track_1,
                                                                              self.straight_track_2,
                                                                              self.direction)):
            self.config.read('user_cfg/crossovers/crossover_{}_{}_{}.ini'.format(self.straight_track_1,
                                                                                 self.straight_track_2,
                                                                                 self.direction))
        else:
            self.config.read('default_cfg/crossovers/crossover_{}_{}_{}.ini'.format(self.straight_track_1,
                                                                                    self.straight_track_2,
                                                                                    self.direction))

        self.busy[self.straight_track_1][self.straight_track_1] \
            = self.config['user_data'].getboolean('busy_{}_{}'.format(self.straight_track_1, self.straight_track_1))
        self.busy[self.straight_track_1][self.straight_track_2] \
            = self.config['user_data'].getboolean('busy_{}_{}'.format(self.straight_track_1, self.straight_track_2))
        self.busy[self.straight_track_2][self.straight_track_2] \
            = self.config['user_data'].getboolean('busy_{}_{}'.format(self.straight_track_2, self.straight_track_2))
        self.force_busy[self.straight_track_1][self.straight_track_1] \
            = self.config['user_data'].getboolean('force_busy_{}_{}'
                                                  .format(self.straight_track_1, self.straight_track_1))
        self.force_busy[self.straight_track_1][self.straight_track_2] \
            = self.config['user_data'].getboolean('force_busy_{}_{}'
                                                  .format(self.straight_track_1, self.straight_track_2))
        self.force_busy[self.straight_track_2][self.straight_track_2] \
            = self.config['user_data'].getboolean('force_busy_{}_{}'
                                                  .format(self.straight_track_2, self.straight_track_2))
        self.last_entered_by = self.config['user_data'].getint('last_entered_by')
        trail_points_parsed \
            = self.config['crossover_config']['trail_points_{}_{}'
                                              .format(self.straight_track_1, self.straight_track_1)].split('|')
        for i in range(len(trail_points_parsed)):
            trail_points_parsed[i] = trail_points_parsed[i].split(',')
            trail_points_parsed[i] = (int(trail_points_parsed[i][0]), int(trail_points_parsed[i][1]))

        self.trail_points[self.straight_track_1][self.straight_track_1] = tuple(trail_points_parsed)
        trail_points_parsed \
            = self.config['crossover_config']['trail_points_{}_{}'
                                              .format(self.straight_track_1, self.straight_track_2)].split('|')
        for i in range(len(trail_points_parsed)):
            trail_points_parsed[i] = trail_points_parsed[i].split(',')
            trail_points_parsed[i] = (int(trail_points_parsed[i][0]), int(trail_points_parsed[i][1]))

        self.trail_points[self.straight_track_1][self.straight_track_2] = tuple(trail_points_parsed)
        trail_points_parsed \
            = self.config['crossover_config']['trail_points_{}_{}'
                                              .format(self.straight_track_2, self.straight_track_2)].split('|')
        for i in range(len(trail_points_parsed)):
            trail_points_parsed[i] = trail_points_parsed[i].split(',')
            trail_points_parsed[i] = (int(trail_points_parsed[i][0]), int(trail_points_parsed[i][1]))

        self.trail_points[self.straight_track_2][self.straight_track_2] = tuple(trail_points_parsed)

    def save_state(self):
        if not os.path.exists('user_cfg'):
            os.mkdir('user_cfg')

        if not os.path.exists('user_cfg/crossovers'):
            os.mkdir('user_cfg/crossovers')

        self.config['user_data']['busy'] = str(self.busy[self.straight_track_1][self.straight_track_1]) + ',' \
                                           + str(self.busy[self.straight_track_1][self.straight_track_2]) + ',' \
                                           + str(self.busy[self.straight_track_2][self.straight_track_2])
        self.config['user_data']['force_busy'] = str(self.force_busy[self.straight_track_1][self.straight_track_1]) \
                                                 + ',' \
                                                 + str(self.force_busy[self.straight_track_1][self.straight_track_2]) \
                                                 + ',' \
                                                 + str(self.force_busy[self.straight_track_2][self.straight_track_2])
        self.config['user_data']['last_entered_by'] = str(self.last_entered_by)

        with open('user_cfg/crossovers/crossover_{}_{}_{}.ini'.format(self.straight_track_1,
                                                                      self.straight_track_2,
                                                                      self.direction), 'w') as configfile:
            self.config.write(configfile)

    def update(self, game_paused):
        if not game_paused:
            self.busy[self.straight_track_1][self.straight_track_1] \
                = self.force_busy[self.straight_track_1][self.straight_track_1] \
                or self.force_busy[self.straight_track_1][self.straight_track_2] \
                or self.dependency.force_busy[self.dependency.straight_track_1][self.dependency.straight_track_2] \
                or self.dependency.force_busy[self.straight_track_1][self.straight_track_1]
            self.busy[self.straight_track_1][self.straight_track_2] \
                = self.force_busy[self.straight_track_1][self.straight_track_1] \
                or self.force_busy[self.straight_track_1][self.straight_track_2] \
                or self.force_busy[self.straight_track_2][self.straight_track_2] \
                or self.dependency.force_busy[self.dependency.straight_track_1][self.dependency.straight_track_1] \
                or self.dependency.force_busy[self.dependency.straight_track_1][self.dependency.straight_track_2] \
                or self.dependency.force_busy[self.dependency.straight_track_2][self.dependency.straight_track_2]
            self.busy[self.straight_track_2][self.straight_track_2] \
                = self.force_busy[self.straight_track_2][self.straight_track_2] \
                or self.force_busy[self.straight_track_1][self.straight_track_2] \
                or self.dependency.force_busy[self.dependency.straight_track_1][self.dependency.straight_track_2] \
                or self.dependency.force_busy[self.straight_track_2][self.straight_track_2]
