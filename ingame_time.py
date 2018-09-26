import logging
import configparser
import os

import pyglet

from game_object import GameObject


def _game_is_not_paused(fn):
    def _update_if_game_is_not_paused(*args, **kwargs):
        if not args[1]:
            fn(*args, **kwargs)

    return _update_if_game_is_not_paused


class InGameTime(GameObject):
    def __init__(self, batch, day_text_group):
        super().__init__()
        self.logger = logging.getLogger('game.in-game_time')
        self.logger.debug('------- START INIT -------')
        self.config = configparser.RawConfigParser()
        self.logger.debug('config parser created')
        self.epoch_timestamp = None
        self.day = None
        self.hour = None
        self.hour_string = ''
        self.minute = None
        self.minute_string = ''
        self.second = None
        self.second_string = ''
        self.logger.debug('created text object for days counter')
        self.read_state()
        self.day_text = pyglet.text.Label('DAY {}'.format(self.day),
                                          font_name='Courier New', bold=True,
                                          font_size=self.c['graphics']['day_font_size'],
                                          color=self.c['graphics']['day_text_color'],
                                          x=self.c['graphics']['screen_resolution'][0] - 141, y=85,
                                          anchor_x='center', anchor_y='center',
                                          batch=batch, group=day_text_group)
        self.time_text = pyglet.text.Label('0',
                                           font_name='Courier New', bold=True,
                                           font_size=self.c['graphics']['day_font_size'],
                                           color=self.c['graphics']['day_text_color'],
                                           x=self.c['graphics']['screen_resolution'][0] - 141, y=45,
                                           anchor_x='center', anchor_y='center',
                                           batch=batch, group=day_text_group)
        self.logger.debug('------- END INIT -------')
        self.logger.warning('time init completed')

    def read_state(self):
        self.logger.debug('------- START READING STATE -------')
        if os.path.exists('user_cfg/epoch_time.ini'):
            self.config.read('user_cfg/epoch_time.ini')
            self.logger.debug('config parsed from user_cfg')
        else:
            self.config.read('default_cfg/epoch_time.ini')
            self.logger.debug('config parsed from default_cfg')

        self.epoch_timestamp = self.config['user_data'].getint('epoch_timestamp')
        self.logger.debug('epoch_timestamp: {}'.format(self.epoch_timestamp))
        self.day = 1 + self.epoch_timestamp // 345600
        self.logger.debug('day: {}'.format(self.day))
        self.hour = 12 + (self.epoch_timestamp % 345600) // 14400
        self.logger.debug('hour: {}'.format(self.hour))
        self.minute = ((self.epoch_timestamp % 345600) % 14400) // 240
        self.logger.debug('minute: {}'.format(self.minute))
        self.second = (((self.epoch_timestamp % 345600) % 14400) % 240) // 4
        if self.second < 10:
            self.second_string = '0' + str(self.second)
        else:
            self.second_string = str(self.second)

        if self.minute < 10:
            self.minute_string = '0' + str(self.minute)
        else:
            self.minute_string = str(self.minute)

        if self.hour < 10:
            self.hour_string = '0' + str(self.hour)
        else:
            self.hour_string = str(self.hour)

        self.logger.debug('------- END READING STATE -------')
        self.logger.info('time state initialized')

    def save_state(self):
        self.logger.debug('------- START SAVING STATE -------')
        if not os.path.exists('user_cfg'):
            os.mkdir('user_cfg')
            self.logger.debug('created user_cfg folder')

        self.config['user_data']['epoch_timestamp'] = str(self.epoch_timestamp)
        self.logger.debug('epoch_timestamp: {}'.format(self.config['user_data']['epoch_timestamp']))
        with open('user_cfg/epoch_time.ini', 'w') as configfile:
            self.config.write(configfile)

        self.logger.debug('------- END SAVING STATE -------')
        self.logger.info('time state saved to file user_cfg/epoch_time.ini')

    def update_sprite(self, base_offset):
        self.time_text.text = self.hour_string + ':' + self.minute_string + ':' + self.second_string

    @_game_is_not_paused
    def update(self, game_paused):
        self.logger.debug('------- TIME UPDATE START -------')
        self.epoch_timestamp += 1
        self.second = (self.epoch_timestamp // 4) % 60
        if self.second < 10:
            self.second_string = '0' + str(self.second)
        else:
            self.second_string = str(self.second)

        if self.epoch_timestamp % 240 == 0:
            self.minute += 1
            if self.minute % 60 == 0:
                self.minute = 0

            if self.minute < 10:
                self.minute_string = '0' + str(self.minute)
            else:
                self.minute_string = str(self.minute)

        if self.epoch_timestamp % 14400 == 0:
            self.hour += 1
            if self.hour % 24 == 0:
                self.hour = 0

            if self.hour < 10:
                self.hour_string = '0' + str(self.hour)
            else:
                self.hour_string = str(self.hour)

        if self.epoch_timestamp % 345600 == 0:
            self.day += 1
            self.day_text.text = 'DAY {}'.format(self.day)

        self.logger.debug('------- TIME UPDATE END -------')
        self.logger.info('time updated')
