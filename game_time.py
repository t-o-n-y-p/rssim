from configparser import RawConfigParser
from logging import getLogger
from os import path, mkdir

from pyglet.resource import add_font
from pyglet.text import Label

from game_object import GameObject


def _game_is_not_paused(fn):
    def _update_if_game_is_not_paused(*args, **kwargs):
        if not args[1]:
            fn(*args, **kwargs)

    return _update_if_game_is_not_paused


def _one_minute_has_passed(fn):
    def _update_if_one_minute_has_passed(*args, **kwargs):
        if args[0].epoch_timestamp % 240 == 0:
            fn(*args, **kwargs)

    return _update_if_one_minute_has_passed


class GameTime(GameObject):
    def __init__(self, batch, day_text_group, game_config):
        super().__init__(game_config)
        self.logger = getLogger('game.game_time')
        self.logger.debug('------- START INIT -------')
        self.config = RawConfigParser()
        self.logger.debug('config parser created')
        self.epoch_timestamp = None
        self.day = None
        self.hour = None
        self.minute = None
        self.logger.debug('created text object for days counter')
        add_font('perfo-bold.ttf')
        self.read_state()
        self.day_text = Label('DAY  {}'.format(self.day), font_name='Perfo', bold=True, font_size=self.c.day_font_size,
                              color=self.c.day_text_color, x=self.c.screen_resolution[0] - 181, y=57,
                              anchor_x='center', anchor_y='center', batch=batch, group=day_text_group)
        self.time_text = Label('{0:0>2}'.format(self.hour) + ' : ' + '{0:0>2}'.format(self.minute),
                               font_name='Perfo', bold=True, font_size=self.c.day_font_size,
                               color=self.c.day_text_color, x=self.c.screen_resolution[0] - 181, y=26,
                               anchor_x='center', anchor_y='center', batch=batch, group=day_text_group)
        self.auto_save_function = None
        self.logger.debug('------- END INIT -------')
        self.logger.warning('time init completed')

    def read_state(self):
        self.logger.debug('------- START READING STATE -------')
        if path.exists('user_cfg/epoch_time.ini'):
            self.config.read('user_cfg/epoch_time.ini')
            self.logger.debug('config parsed from user_cfg')
        else:
            self.config.read('default_cfg/epoch_time.ini')
            self.logger.debug('config parsed from default_cfg')

        self.epoch_timestamp = self.config['user_data'].getint('epoch_timestamp')
        self.logger.debug('epoch_timestamp: {}'.format(self.epoch_timestamp))
        self.day = 1 + self.epoch_timestamp // 345600
        self.logger.debug('day: {}'.format(self.day))
        self.hour = (self.epoch_timestamp // 14400 + 12) % 24
        self.logger.debug('hour: {}'.format(self.hour))
        self.minute = (self.epoch_timestamp // 240) % 60
        self.logger.debug('minute: {}'.format(self.minute))
        self.logger.debug('------- END READING STATE -------')
        self.logger.info('time state initialized')

    def save_state(self):
        self.logger.debug('------- START SAVING STATE -------')
        if not path.exists('user_cfg'):
            mkdir('user_cfg')
            self.logger.debug('created user_cfg folder')

        self.config['user_data']['epoch_timestamp'] = str(self.epoch_timestamp)
        self.logger.debug('epoch_timestamp: {}'.format(self.config['user_data']['epoch_timestamp']))
        with open('user_cfg/epoch_time.ini', 'w') as configfile:
            self.config.write(configfile)

        self.logger.debug('------- END SAVING STATE -------')
        self.logger.info('time state saved to file user_cfg/epoch_time.ini')

    @_one_minute_has_passed
    def update_sprite(self, base_offset):
        self.time_text.text = '{0:0>2} : {1:0>2}'.format(self.hour, self.minute)

    @_game_is_not_paused
    def update(self, game_paused):
        self.logger.debug('------- TIME UPDATE START -------')
        self.epoch_timestamp += 1
        if self.epoch_timestamp % 240 == 0:
            self.minute = (self.minute + 1) % 60

        if self.epoch_timestamp % 14400 == 0:
            self.hour = (self.hour + 1) % 24

        if self.epoch_timestamp % 345600 == 0:
            self.day += 1
            self.day_text.text = 'DAY  {}'.format(self.day)

        if self.epoch_timestamp % 28800 == 0:
            self.auto_save_function(None)

        self.logger.debug('------- TIME UPDATE END -------')
        self.logger.info('time updated')
