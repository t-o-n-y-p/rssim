import logging
import configparser
import os

from game_object import GameObject


class Track(GameObject):
    def __init__(self, track_number, base_routes_in_track):
        super().__init__()
        self.logger = logging.getLogger('game.track()'.format(track_number))
        self.logger.debug('------- START INIT -------')
        self.config = configparser.RawConfigParser()
        self.logger.debug('config parser created')
        self.track_number = track_number
        self.base_routes = base_routes_in_track
        self.logger.debug('track number and base routes set')
        self.busy = False
        self.last_entered_by = 0
        self.override = False
        self.read_state()
        self.logger.debug('------- END INIT -------')
        self.logger.warning('track init completed')

    def read_state(self):
        self.logger.debug('------- START READING STATE -------')
        if os.path.exists('user_cfg/tracks/track{}.ini'.format(self.track_number)):
            self.config.read('user_cfg/tracks/track{}.ini'.format(self.track_number))
            self.logger.debug('config parsed from user_cfg')
        else:
            self.config.read('default_cfg/tracks/track{}.ini'.format(self.track_number))
            self.logger.debug('config parsed from default_cfg')

        self.busy = self.config['user_data'].getboolean('busy')
        self.logger.debug('busy: {}'.format(self.busy))
        self.last_entered_by = self.config['user_data'].getint('last_entered_by')
        self.logger.debug('last_entered_by: {}'.format(self.last_entered_by))
        self.override = self.config['user_data'].getboolean('override')
        self.logger.debug('override: {}'.format(self.override))
        self.logger.debug('------- END READING STATE -------')
        self.logger.info('track state initialized')

    def save_state(self):
        self.logger.debug('------- START SAVING STATE -------')
        if not os.path.exists('user_cfg'):
            os.mkdir('user_cfg')
            self.logger.debug('created user_cfg folder')

        if not os.path.exists('user_cfg/tracks'):
            os.mkdir('user_cfg/tracks')
            self.logger.debug('created user_cfg/tracks folder')

        self.config['user_data']['busy'] = str(self.busy)
        self.logger.debug('busy: {}'.format(self.config['user_data']['busy']))
        self.config['user_data']['last_entered_by'] = str(self.last_entered_by)
        self.logger.debug('last_entered_by: {}'.format(self.config['user_data']['last_entered_by']))
        self.config['user_data']['override'] = str(self.override)
        self.logger.debug('override: {}'.format(self.config['user_data']['override']))

        with open('user_cfg/tracks/track{}.ini'.format(self.track_number), 'w') as configfile:
            self.config.write(configfile)

        self.logger.debug('------- END SAVING STATE -------')
        self.logger.info('track state saved to file user_cfg/tracks/track{}.ini'.format(self.track_number))

    def update(self, game_paused):
        # if game is paused, track status should not be updated
        # if track settings are overridden, we do nothing too
        self.logger.debug('------- TRACK UPDATE START -------')
        self.logger.debug('override: {}'.format(self.override))
        if not game_paused and not self.override:
            busy_1 = False
            # if any of 4 base routes are busy, all track will become busy
            for i in self.base_routes:
                busy_1 = busy_1 or i.route_config['busy']
                self.logger.debug('base route {} busy: {}'.format(i, i.route_config['busy']))
                if i.route_config['busy']:
                    self.last_entered_by = i.route_config['last_entered_by']

            self.busy = busy_1
            self.logger.debug('busy: {}'.format(self.busy))
            self.logger.debug('------- TRACK UPDATE END -------')
            self.logger.info('track updated')
