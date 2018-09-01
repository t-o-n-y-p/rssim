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
    def __init__(self, batch, clock_face_group, day_text_group, minute_hand_group, hour_hand_group):
        super().__init__()
        self.logger = logging.getLogger('game.in-game_time')
        self.logger.debug('------- START INIT -------')
        self.config = configparser.RawConfigParser()
        self.logger.debug('config parser created')
        self.clock_face_image = pyglet.image.load('img/clock_face.png')
        self.clock_face_image.anchor_x = self.clock_face_image.width // 2 + 1
        self.clock_face_image.anchor_y = self.clock_face_image.height // 2 + 1
        self.clock_face_sprite = pyglet.sprite.Sprite(self.clock_face_image,
                                                      x=self.c['graphics']['screen_resolution'][0] - 101,
                                                      y=101, batch=batch, group=clock_face_group)
        self.logger.debug('loaded clock face image: img/clock_face.png')
        self.minute_hand_image = pyglet.image.load('img/minute_hand.png')
        self.minute_hand_image.anchor_x = self.minute_hand_image.width // 2 + 1
        self.minute_hand_image.anchor_y = self.minute_hand_image.height // 2 + 1
        self.minute_hand_sprite = pyglet.sprite.Sprite(self.minute_hand_image,
                                                       x=self.c['graphics']['screen_resolution'][0] - 101,
                                                       y=101, batch=batch, group=minute_hand_group)
        self.logger.debug('loaded minute hand image: img/minute_hand.png')
        self.hour_hand_image = pyglet.image.load('img/hour_hand.png')
        self.hour_hand_image.anchor_x = self.hour_hand_image.width // 2 + 1
        self.hour_hand_image.anchor_y = self.hour_hand_image.height // 2 + 1
        self.hour_hand_sprite = pyglet.sprite.Sprite(self.hour_hand_image,
                                                     x=self.c['graphics']['screen_resolution'][0] - 101,
                                                     y=101, batch=batch, group=hour_hand_group)
        self.logger.debug('loaded hour hand image: img/hour_hand.png')
        self.epoch_timestamp = None
        self.day = None
        self.hour = None
        self.minute = None
        self.logger.debug('created text object for days counter')
        self.read_state()
        self.day_text = pyglet.text.Label('Day {}'.format(self.day),
                                          font_name=self.c['graphics']['font_name'],
                                          font_size=self.c['graphics']['day_font_size'],
                                          color=self.c['graphics']['day_text_color'],
                                          x=self.c['graphics']['screen_resolution'][0] - 101, y=70,
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
        self.hour = float(self.epoch_timestamp % 345600) / float(14400)
        self.logger.debug('hour: {}'.format(self.hour))
        self.minute = float(self.hour % 14400) / float(240)
        self.logger.debug('minute: {}'.format(self.minute))
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
        self.day_text.text = 'Day {}'.format(self.day)
        minute_hand_rotate_angle = self.minute / float(60) * float(360)
        self.minute_hand_sprite.rotation = minute_hand_rotate_angle
        hour_hand_rotate_angle = self.hour / float(12) * float(360)
        self.hour_hand_sprite.rotation = hour_hand_rotate_angle

    @_game_is_not_paused
    def update(self, game_paused):
        self.logger.debug('------- TIME UPDATE START -------')
        self.epoch_timestamp += 1
        self.logger.debug('epoch_timestamp: {}'.format(self.epoch_timestamp))
        self.day = 1 + self.epoch_timestamp // 345600
        self.logger.debug('day: {}'.format(self.day))
        self.hour = float(self.epoch_timestamp % 345600) / float(14400)
        self.logger.debug('hour: {}'.format(self.hour))
        self.minute = float((self.epoch_timestamp % 345600) % 14400) / float(240)
        self.logger.debug('minute: {}'.format(self.minute))
        self.logger.debug('------- TIME UPDATE END -------')
        self.logger.info('time updated')
