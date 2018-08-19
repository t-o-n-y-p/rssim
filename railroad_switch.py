import logging
import configparser
import os

from game_object import GameObject


class RailroadSwitch(GameObject):
    def __init__(self, straight_track, side_track, direction):
        super().__init__()
        self.logger = logging.getLogger('game.switch_{}_{}_{}'.format(straight_track, side_track, direction))
        self.logger.debug('------- START INIT -------')
        self.straight_track = straight_track
        self.side_track = side_track
        self.direction = direction
        self.logger.debug('straight and side tracks and direction set: {} {} {}'
                          .format(self.straight_track, self.side_track, self.direction))
        self.config = configparser.RawConfigParser()
        self.logger.debug('config parser created')
        self.dependency = None
        self.busy = False
        self.force_busy = False
        self.last_entered_by = 0
        self.trail_points = {}
        self.read_state()
        self.logger.debug('------- END INIT -------')
        self.logger.warning('switch init completed')

    def read_state(self):
        self.logger.debug('------- START READING STATE -------')
        if os.path.exists('user_cfg/switches/switch_{}_{}_{}.ini'
                          .format(self.straight_track, self.side_track, self.direction)):
            self.config.read('user_cfg/switches/switch_{}_{}_{}.ini'
                             .format(self.straight_track, self.side_track, self.direction))
            self.logger.debug('config parsed from user_cfg')
        else:
            self.config.read('default_cfg/switches/switch_{}_{}_{}.ini'
                             .format(self.straight_track, self.side_track, self.direction))
            self.logger.debug('config parsed from default_cfg')

        self.busy = self.config['user_data'].getboolean('busy')
        self.logger.debug('busy: {}'.format(self.busy))
        self.force_busy = self.config['user_data'].getboolean('force_busy')
        self.logger.debug('force_busy: {}'.format(self.force_busy))
        self.last_entered_by = self.config['user_data'].getint('last_entered_by')
        self.logger.debug('last_entered_by: {}'.format(self.last_entered_by))
        self.logger.info('user-related config parsed')
        straight_trail_points_parsed \
            = self.config['switch_config']['trail_points_{}'.format(self.straight_track)].split('|')
        for i in range(len(straight_trail_points_parsed)):
            straight_trail_points_parsed[i] = straight_trail_points_parsed[i].split(',')
            straight_trail_points_parsed[i] = (int(straight_trail_points_parsed[i][0]),
                                               int(straight_trail_points_parsed[i][1]))

        self.trail_points[self.straight_track] = tuple(straight_trail_points_parsed)
        self.logger.debug('trail points for straight track parsed')
        side_trail_points_parsed = self.config['switch_config']['trail_points_{}'.format(self.side_track)].split('|')
        for i in range(len(side_trail_points_parsed)):
            side_trail_points_parsed[i] = side_trail_points_parsed[i].split(',')
            side_trail_points_parsed[i] = (int(side_trail_points_parsed[i][0]),
                                           int(side_trail_points_parsed[i][1]))

        self.trail_points[self.side_track] = tuple(side_trail_points_parsed)
        self.logger.debug('trail points for side track parsed')
        self.logger.info('solid config parsed')
        self.logger.debug('------- END READING STATE -------')
        self.logger.info('switch state initialized')

    def save_state(self):
        self.logger.debug('------- START SAVING STATE -------')
        if not os.path.exists('user_cfg'):
            os.mkdir('user_cfg')
            self.logger.debug('created user_cfg folder')

        if not os.path.exists('user_cfg/switches'):
            os.mkdir('user_cfg/switches')
            self.logger.debug('created user_cfg/switches folder')

        self.config['user_data']['busy'] = str(self.busy)
        self.logger.debug('busy: {}'.format(self.config['user_data']['busy']))
        self.config['user_data']['force_busy'] = str(self.force_busy)
        self.logger.debug('force_busy: {}'.format(self.config['user_data']['force_busy']))
        self.config['user_data']['last_entered_by'] = str(self.last_entered_by)
        self.logger.debug('last_entered_by: {}'.format(self.config['user_data']['last_entered_by']))

        with open('user_cfg/switches/switch_{}_{}_{}.ini'
                  .format(self.straight_track, self.side_track, self.direction), 'w') as configfile:
            self.config.write(configfile)

        self.logger.debug('------- END SAVING STATE -------')
        self.logger.info('switch state saved to file user_cfg/switches/switch_{}_{}_{}.ini'
                         .format(self.straight_track, self.side_track, self.direction))

    def update(self, game_paused):
        if not game_paused:
            self.logger.debug('------- SWITCH UPDATE START -------')
            self.busy = self.force_busy or self.dependency.force_busy
            self.logger.debug('force_busy: {}'.format(self.force_busy))
            self.logger.debug('busy: {}'.format(self.busy))
            self.logger.debug('------- SWITCH UPDATE END -------')
            self.logger.info('switch updated')
