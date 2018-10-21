import configparser
import os
import logging

from game_object import GameObject


def _game_is_not_paused(fn):
    def _update_if_game_is_not_paused(*args, **kwargs):
        if not args[1]:
            fn(*args, **kwargs)

    return _update_if_game_is_not_paused


class Crossover(GameObject):
    def __init__(self, straight_track_1, straight_track_2, direction, game_config):
        super().__init__(game_config)
        self.logger = logging.getLogger('game.crossover_{}_{}_{}'.format(straight_track_1, straight_track_2, direction))
        self.logger.debug('------- START INIT -------')
        self.config = configparser.RawConfigParser()
        self.logger.debug('config parser created')
        self.straight_track_1 = straight_track_1
        self.straight_track_2 = straight_track_2
        self.direction = direction
        self.logger.debug('straight tracks and direction set: {} {} {}'
                          .format(self.straight_track_1, self.straight_track_2, self.direction))
        self.dependency = None
        self.busy = {}
        self.force_busy = {}
        self.last_entered_by = {}
        self.length = {}
        self.read_state()
        self.logger.debug('------- END INIT -------')
        self.logger.warning('crossover init completed')

    def read_state(self):
        self.logger.debug('------- START READING STATE -------')
        if os.path.exists('user_cfg/crossovers/crossover_{}_{}_{}.ini'
                          .format(self.straight_track_1, self.straight_track_2, self.direction)):
            self.config.read('user_cfg/crossovers/crossover_{}_{}_{}.ini'
                             .format(self.straight_track_1, self.straight_track_2, self.direction))
            self.logger.debug('config parsed from user_cfg')
        else:
            self.config.read('default_cfg/crossovers/crossover_{}_{}_{}.ini'
                             .format(self.straight_track_1, self.straight_track_2, self.direction))
            self.logger.debug('config parsed from default_cfg')

        self.busy[self.straight_track_1] = {}
        self.busy[self.straight_track_2] = {}
        self.busy[self.straight_track_1][self.straight_track_1] \
            = self.config['user_data'].getboolean('busy_{}_{}'.format(self.straight_track_1, self.straight_track_1))
        self.logger.debug('busy {}->{}: {}'.format(self.straight_track_1, self.straight_track_1,
                                                   self.busy[self.straight_track_1][self.straight_track_1]))
        self.busy[self.straight_track_1][self.straight_track_2] \
            = self.config['user_data'].getboolean('busy_{}_{}'.format(self.straight_track_1, self.straight_track_2))
        self.logger.debug('busy {}->{}: {}'.format(self.straight_track_1, self.straight_track_2,
                                                   self.busy[self.straight_track_1][self.straight_track_2]))
        self.busy[self.straight_track_2][self.straight_track_2] \
            = self.config['user_data'].getboolean('busy_{}_{}'.format(self.straight_track_2, self.straight_track_2))
        self.logger.debug('busy {}->{}: {}'.format(self.straight_track_2, self.straight_track_2,
                                                   self.busy[self.straight_track_2][self.straight_track_2]))
        self.force_busy[self.straight_track_1] = {}
        self.force_busy[self.straight_track_2] = {}
        self.force_busy[self.straight_track_1][self.straight_track_1] \
            = self.config['user_data'].getboolean('force_busy_{}_{}'
                                                  .format(self.straight_track_1, self.straight_track_1))
        self.logger.debug('force busy {}->{}: {}'.format(self.straight_track_1, self.straight_track_1,
                                                         self.force_busy[self.straight_track_1][self.straight_track_1]))
        self.force_busy[self.straight_track_1][self.straight_track_2] \
            = self.config['user_data'].getboolean('force_busy_{}_{}'
                                                  .format(self.straight_track_1, self.straight_track_2))
        self.logger.debug('force busy {}->{}: {}'.format(self.straight_track_1, self.straight_track_2,
                                                         self.force_busy[self.straight_track_1][self.straight_track_2]))
        self.force_busy[self.straight_track_2][self.straight_track_2] \
            = self.config['user_data'].getboolean('force_busy_{}_{}'
                                                  .format(self.straight_track_2, self.straight_track_2))
        self.logger.debug('force busy {}->{}: {}'.format(self.straight_track_2, self.straight_track_2,
                                                         self.force_busy[self.straight_track_2][self.straight_track_2]))
        self.last_entered_by[self.straight_track_1] = {}
        self.last_entered_by[self.straight_track_2] = {}
        self.last_entered_by[self.straight_track_1][self.straight_track_1] \
            = self.config['user_data'].getint('last_entered_by_{}_{}'
                                              .format(self.straight_track_1, self.straight_track_1))
        self.logger.debug('last_entered_by {}->{}: {}'
                          .format(self.straight_track_1, self.straight_track_1,
                                  self.last_entered_by[self.straight_track_1][self.straight_track_1]))
        self.last_entered_by[self.straight_track_1][self.straight_track_2] \
            = self.config['user_data'].getint('last_entered_by_{}_{}'
                                              .format(self.straight_track_1, self.straight_track_2))
        self.logger.debug('last_entered_by {}->{}: {}'
                          .format(self.straight_track_1, self.straight_track_2,
                                  self.last_entered_by[self.straight_track_1][self.straight_track_2]))
        self.last_entered_by[self.straight_track_2][self.straight_track_2] \
            = self.config['user_data'].getint('last_entered_by_{}_{}'
                                              .format(self.straight_track_2, self.straight_track_2))
        self.logger.debug('last_entered_by {}->{}: {}'
                          .format(self.straight_track_2, self.straight_track_2,
                                  self.last_entered_by[self.straight_track_2][self.straight_track_2]))
        self.logger.info('user-related config parsed')

        self.length[self.straight_track_1] = {}
        self.length[self.straight_track_2] = {}
        self.length[self.straight_track_1][self.straight_track_1] \
            = self.config['crossover_config'].getint('length_{}_{}'
                                                     .format(self.straight_track_1, self.straight_track_1))
        self.length[self.straight_track_1][self.straight_track_2] \
            = self.config['crossover_config'].getint('length_{}_{}'
                                                     .format(self.straight_track_1, self.straight_track_2))
        self.length[self.straight_track_2][self.straight_track_2] \
            = self.config['crossover_config'].getint('length_{}_{}'
                                                     .format(self.straight_track_2, self.straight_track_2))

        self.logger.info('solid config parsed')
        self.logger.debug('------- END READING STATE -------')
        self.logger.info('crossover state initialized')

    def save_state(self):
        self.logger.debug('------- START SAVING STATE -------')
        if not os.path.exists('user_cfg'):
            os.mkdir('user_cfg')
            self.logger.debug('created user_cfg folder')

        if not os.path.exists('user_cfg/crossovers'):
            os.mkdir('user_cfg/crossovers')
            self.logger.debug('created user_cfg/crossovers folder')

        self.config['user_data']['busy_{}_{}'.format(self.straight_track_1, self.straight_track_1)] \
            = str(self.busy[self.straight_track_1][self.straight_track_1])
        self.logger.debug('busy {}->{} value to save: {}'
                          .format(self.straight_track_1, self.straight_track_1,
                                  self.config['user_data'][
                                      'busy_{}_{}'.format(self.straight_track_1, self.straight_track_1)]))
        self.config['user_data']['busy_{}_{}'.format(self.straight_track_1, self.straight_track_2)] \
            = str(self.busy[self.straight_track_1][self.straight_track_2])
        self.logger.debug('busy {}->{} value to save: {}'
                          .format(self.straight_track_1, self.straight_track_2,
                                  self.config['user_data'][
                                      'busy_{}_{}'.format(self.straight_track_1, self.straight_track_2)]))
        self.config['user_data']['busy_{}_{}'.format(self.straight_track_2, self.straight_track_2)] \
            = str(self.busy[self.straight_track_2][self.straight_track_2])
        self.logger.debug('busy {}->{} value to save: {}'
                          .format(self.straight_track_2, self.straight_track_2,
                                  self.config['user_data'][
                                      'busy_{}_{}'.format(self.straight_track_2, self.straight_track_2)]))

        self.config['user_data']['force_busy_{}_{}'.format(self.straight_track_1, self.straight_track_1)] \
            = str(self.force_busy[self.straight_track_1][self.straight_track_1])
        self.logger.debug('force_busy {}->{} value to save: {}'
                          .format(self.straight_track_1, self.straight_track_1,
                                  self.config['user_data'][
                                      'force_busy_{}_{}'.format(self.straight_track_1, self.straight_track_1)]))
        self.config['user_data']['force_busy_{}_{}'.format(self.straight_track_1, self.straight_track_2)] \
            = str(self.force_busy[self.straight_track_1][self.straight_track_2])
        self.logger.debug('force_busy {}->{} value to save: {}'
                          .format(self.straight_track_1, self.straight_track_2,
                                  self.config['user_data'][
                                      'force_busy_{}_{}'.format(self.straight_track_1, self.straight_track_2)]))
        self.config['user_data']['force_busy_{}_{}'.format(self.straight_track_2, self.straight_track_2)] \
            = str(self.force_busy[self.straight_track_2][self.straight_track_2])
        self.logger.debug('force_busy {}->{} value to save: {}'
                          .format(self.straight_track_2, self.straight_track_2,
                                  self.config['user_data'][
                                      'force_busy_{}_{}'.format(self.straight_track_2, self.straight_track_2)]))

        self.config['user_data']['last_entered_by_{}_{}'.format(self.straight_track_1, self.straight_track_1)] \
            = str(self.last_entered_by[self.straight_track_1][self.straight_track_1])
        self.logger.debug('last_entered_by {}->{} value to save: {}'
                          .format(self.straight_track_1, self.straight_track_1,
                                  self.config['user_data'][
                                      'last_entered_by_{}_{}'.format(self.straight_track_1, self.straight_track_1)]))
        self.config['user_data']['last_entered_by_{}_{}'.format(self.straight_track_1, self.straight_track_2)] \
            = str(self.last_entered_by[self.straight_track_1][self.straight_track_2])
        self.logger.debug('last_entered_by {}->{} value to save: {}'
                          .format(self.straight_track_1, self.straight_track_2,
                                  self.config['user_data'][
                                      'last_entered_by_{}_{}'.format(self.straight_track_1, self.straight_track_2)]))
        self.config['user_data']['last_entered_by_{}_{}'.format(self.straight_track_2, self.straight_track_2)] \
            = str(self.last_entered_by[self.straight_track_2][self.straight_track_2])
        self.logger.debug('last_entered_by {}->{} value to save: {}'
                          .format(self.straight_track_2, self.straight_track_2,
                                  self.config['user_data'][
                                      'last_entered_by_{}_{}'.format(self.straight_track_2, self.straight_track_2)]))

        with open('user_cfg/crossovers/crossover_{}_{}_{}.ini'
                  .format(self.straight_track_1, self.straight_track_2, self.direction), 'w') as configfile:
            self.config.write(configfile)

        self.logger.debug('------- END SAVING STATE -------')
        self.logger.info('crossover state saved to file user_cfg/crossovers/crossover_{}_{}_{}.ini'
                         .format(self.straight_track_1, self.straight_track_2, self.direction))

    @_game_is_not_paused
    def update(self, game_paused):
        self.logger.debug('------- CROSSOVER UPDATE START -------')
        self.busy[self.straight_track_1][self.straight_track_1] \
            = self.force_busy[self.straight_track_1][self.straight_track_1] \
            or self.force_busy[self.straight_track_1][self.straight_track_2] \
            or self.dependency.force_busy[self.dependency.straight_track_1][self.dependency.straight_track_2] \
            or self.dependency.force_busy[self.straight_track_1][self.straight_track_1]
        self.logger.debug('track {}->{} force busy = {}'
                          .format(self.straight_track_1, self.straight_track_1,
                                  self.force_busy[self.straight_track_1][self.straight_track_1]))
        self.logger.debug('track {}->{} busy = {}'.format(self.straight_track_1, self.straight_track_1,
                                                          self.busy[self.straight_track_1][self.straight_track_1]))
        self.busy[self.straight_track_1][self.straight_track_2] \
            = self.force_busy[self.straight_track_1][self.straight_track_1] \
            or self.force_busy[self.straight_track_1][self.straight_track_2] \
            or self.force_busy[self.straight_track_2][self.straight_track_2] \
            or self.dependency.force_busy[self.dependency.straight_track_1][self.dependency.straight_track_1] \
            or self.dependency.force_busy[self.dependency.straight_track_1][self.dependency.straight_track_2] \
            or self.dependency.force_busy[self.dependency.straight_track_2][self.dependency.straight_track_2]
        self.logger.debug('track {}->{} force busy = {}'
                          .format(self.straight_track_1, self.straight_track_2,
                                  self.force_busy[self.straight_track_1][self.straight_track_2]))
        self.logger.debug('track {}->{} busy = {}'.format(self.straight_track_1, self.straight_track_2,
                                                          self.busy[self.straight_track_1][self.straight_track_2]))
        self.busy[self.straight_track_2][self.straight_track_2] \
            = self.force_busy[self.straight_track_2][self.straight_track_2] \
            or self.force_busy[self.straight_track_1][self.straight_track_2] \
            or self.dependency.force_busy[self.dependency.straight_track_1][self.dependency.straight_track_2] \
            or self.dependency.force_busy[self.straight_track_2][self.straight_track_2]
        self.logger.debug('track {}->{} force busy = {}'
                          .format(self.straight_track_2, self.straight_track_2,
                                  self.force_busy[self.straight_track_2][self.straight_track_2]))
        self.logger.debug('track {}->{} busy = {}'.format(self.straight_track_2, self.straight_track_2,
                                                          self.busy[self.straight_track_2][self.straight_track_2]))
        self.logger.debug('------- CROSSOVER UPDATE END -------')
        self.logger.info('crossover updated')
