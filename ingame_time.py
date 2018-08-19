import logging
import configparser
import os

import pygame

import config as c
from text_object import TextObject
from game_object import GameObject


class InGameTime(GameObject):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('game.in-game_time')
        self.logger.debug('------- START INIT -------')
        self.config = configparser.RawConfigParser()
        self.logger.debug('config parser created')
        self.clock_face_image = pygame.image.load('img/clock_face.png').convert_alpha()
        self.logger.debug('loaded clock face image: img/clock_face.png')
        self.minute_hand_image = pygame.image.load('img/minute_hand.png').convert_alpha()
        self.logger.debug('loaded minute hand image: img/minute_hand.png')
        self.hour_hand_image = pygame.image.load('img/hour_hand.png').convert_alpha()
        self.logger.debug('loaded hour hand image: img/hour_hand.png')
        self.epoch_timestamp = None
        self.day = None
        self.hour = None
        self.minute = None
        self.day_text = TextObject((c.SCREEN_RESOLUTION[0] - 100, c.SCREEN_RESOLUTION[1] - 70),
                                   'Day {}'.format(self.day),
                                   c.DAY_FONT_COLOR, c.DAY_FONT_SIZE)
        self.logger.debug('created text object for days counter')
        self.read_state()
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

    def draw(self, surface, base_offset):
        self.logger.debug('------- START DRAWING -------')
        surface.blit(self.clock_face_image, (c.SCREEN_RESOLUTION[0] - 200, c.SCREEN_RESOLUTION[1] - 200))
        self.logger.debug('clock face image is in place')
        self.day_text.update('Day {}'.format(self.day))
        self.day_text.draw(surface)
        self.logger.debug('days counter is in place')
        minute_hand_rotate_angle = float(-1)*self.minute/float(60)*float(360)
        self.logger.debug('minute_hand_rotate_axis: {}'.format(minute_hand_rotate_angle))
        minute_hand_rotated = pygame.transform.rotozoom(self.minute_hand_image, minute_hand_rotate_angle, 1.0)
        new_minute_hand_size = minute_hand_rotated.get_size()
        surface.blit(minute_hand_rotated, (c.SCREEN_RESOLUTION[0] - 100 - new_minute_hand_size[0] // 2,
                                           c.SCREEN_RESOLUTION[1] - 100 - new_minute_hand_size[1] // 2))
        self.logger.debug('minute hand is in place')
        hour_hand_rotate_angle = float(-1)*self.hour/float(12)*float(360)
        self.logger.debug('hour_hand_rotate_axis: {}'.format(hour_hand_rotate_angle))
        hour_hand_rotated = pygame.transform.rotozoom(self.hour_hand_image, hour_hand_rotate_angle, 1.0)
        new_hour_hand_size = hour_hand_rotated.get_size()
        surface.blit(hour_hand_rotated, (c.SCREEN_RESOLUTION[0] - 100 - new_hour_hand_size[0] // 2,
                                         c.SCREEN_RESOLUTION[1] - 100 - new_hour_hand_size[1] // 2))
        self.logger.debug('hour hand is in place')
        self.logger.debug('------- END DRAWING -------')
        self.logger.info('time is in place')

    def update(self, game_paused):
        if not game_paused:
            self.logger.debug('------- TIME UPDATE START -------')
            self.epoch_timestamp += 1
            self.logger.debug('epoch_timestamp: {}'.format(self.epoch_timestamp))
            self.day = 1 + self.epoch_timestamp // 345600
            self.logger.debug('day: {}'.format(self.day))
            self.hour = float(self.epoch_timestamp % 345600) / float(14400)
            self.logger.debug('hour: {}'.format(self.hour))
            self.minute = float((self.epoch_timestamp % 345600) % 14400) / float(240)
            self.logger.debug('minute: {}'.format(self.minute))
            self.logger.debug('------- CROSSOVER UPDATE END -------')
            self.logger.info('time updated')
