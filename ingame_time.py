import logs_config as log_c
import configparser
from game_object import GameObject
import os
import pygame
import config as c
from text_object import TextObject


class IngameTime(GameObject):
    def __init__(self):
        super().__init__()
        self.clock_face_image = pygame.image.load('img/clock_face.png').convert_alpha()
        self.minute_hand_image = pygame.image.load('img/minute_hand.png').convert_alpha()
        self.hour_hand_image = pygame.image.load('img/hour_hand.png').convert_alpha()
        self.config = None
        self.epoch_timestamp = None
        self.day = None
        self.hour = None
        self.minute = None
        self.day_text = TextObject((c.screen_resolution[0] - 100, c.screen_resolution[1] - 70),
                                   'Day {}'.format(self.day),
                                   c.colors.RED3, 18)
        self.read_state()

    def read_state(self):
        self.config = configparser.RawConfigParser()
        if os.path.exists('user_cfg/epoch_time.ini'):
            self.config.read('user_cfg/epoch_time.ini')
        else:
            self.config.read('default_cfg/epoch_time.ini')

        self.epoch_timestamp = self.config['user_data'].getint('epoch_timestamp')
        self.day = 1 + self.epoch_timestamp // 345600
        self.hour = float(self.epoch_timestamp % 345600) / float(14400)
        self.minute = float(self.hour % 14400) / float(240)

    def save_state(self):
        if not os.path.exists('user_cfg'):
            os.mkdir('user_cfg')

        self.config['user_data']['epoch_timestamp'] = str(self.epoch_timestamp)
        with open('user_cfg/epoch_time.ini', 'w') as configfile:
            self.config.write(configfile)

    def draw(self, surface, base_offset):
        surface.blit(self.clock_face_image, (c.screen_resolution[0] - 200, c.screen_resolution[1] - 200))
        self.day_text.update('Day {}'.format(self.day))
        self.day_text.draw(surface)
        minute_hand_rotate_axis = float(-1)*self.minute/float(60)*float(360)
        minute_hand_rotated = pygame.transform.rotozoom(self.minute_hand_image, minute_hand_rotate_axis, 1.0)
        new_minute_hand_size = minute_hand_rotated.get_size()
        surface.blit(minute_hand_rotated, (c.screen_resolution[0] - 100 - new_minute_hand_size[0] // 2,
                                           c.screen_resolution[1] - 100 - new_minute_hand_size[1] // 2))
        hour_hand_rotate_axis = float(-1)*self.hour/float(12)*float(360)
        hour_hand_rotated = pygame.transform.rotozoom(self.hour_hand_image, hour_hand_rotate_axis, 1.0)
        new_hour_hand_size = hour_hand_rotated.get_size()
        surface.blit(hour_hand_rotated, (c.screen_resolution[0] - 100 - new_hour_hand_size[0] // 2,
                                         c.screen_resolution[1] - 100 - new_hour_hand_size[1] // 2))

    def update(self, game_paused):
        if not game_paused:
            self.epoch_timestamp += 1
            self.day = 1 + self.epoch_timestamp // 345600
            self.hour = float(self.epoch_timestamp % 345600) / float(14400)
            self.minute = float((self.epoch_timestamp % 345600) % 14400) / float(240)
