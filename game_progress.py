import logging
import configparser
import os

import pyglet

from game_object import GameObject


def _maximum_level_not_reached(fn):
    def _add_exp_if_max_level_not_reached(*args, **kwargs):
        if args[0].level < args[0].c.maximum_level:
            fn(*args, **kwargs)

    return _add_exp_if_max_level_not_reached


def _money_target_exists(fn):
    def _update_money_progress_if_money_target_exists(*args, **kwargs):
        if args[0].money_target > 0:
            fn(*args, **kwargs)

    return _update_money_progress_if_money_target_exists


def _level_up(fn):
    def _update_exp_progress_if_level_up(*args, **kwargs):
        if args[0].accumulated_exp >= args[0].c.accumulated_player_progress[args[0].level]:
            fn(*args, **kwargs)

    return _update_exp_progress_if_level_up


class GameProgress(GameObject):
    def __init__(self, main_map, mini_map, game_config, batch, inactive_group, active_group):
        super().__init__(game_config)
        self.logger = logging.getLogger('game.game_progress')
        self.config = configparser.RawConfigParser()
        self.unlocked_tracks = 4
        self.level = 0
        self.exp = 0.0
        self.accumulated_exp = 0.0
        self.money = 0.0
        self.exp_percent = 0
        self.money_percent = 0
        self.supported_carts = None
        self.main_map = main_map
        self.mini_map = mini_map
        self.tracks = None
        pyglet.resource.add_font('perfo-bold.ttf')
        self.progress_bar_inactive_image = pyglet.image.load('img/progress_bar_inactive.png')
        self.progress_bar_exp_inactive = pyglet.sprite.Sprite(self.progress_bar_inactive_image,
                                                              x=10, y=10, batch=batch, group=inactive_group)
        self.progress_bar_money_inactive = pyglet.sprite.Sprite(self.progress_bar_inactive_image,
                                                                x=220, y=10, batch=batch, group=inactive_group)
        self.progress_bar_exp_active_image = pyglet.image.load('img/progress_bar_active.png')
        self.progress_bar_money_active_image = pyglet.image.load('img/progress_bar_money_active.png')
        self.progress_bar_exp_active = pyglet.sprite.Sprite(self.progress_bar_exp_active_image,
                                                            x=10, y=10, batch=batch, group=active_group)
        self.progress_bar_exp_active.image = self.progress_bar_exp_active_image.get_region(0, 0, 1, 10)
        self.progress_bar_money_active = pyglet.sprite.Sprite(self.progress_bar_money_active_image,
                                                              x=220, y=10, batch=batch, group=active_group)
        self.progress_bar_money_active.image = self.progress_bar_money_active_image.get_region(0, 0, 1, 10)
        self.money_target = 50000
        self.read_state()
        self.level_text = pyglet.text.Label('LEVEL {}'.format(self.level), font_name='Perfo', bold=True,
                                            font_size=self.c.level_font_size, x=110, y=40,
                                            anchor_x='center', anchor_y='center', batch=batch, group=active_group)
        self.money_text = pyglet.text.Label('{0:0>8} ¤'.format(int(self.money)), font_name='Perfo', bold=True,
                                            color=(0, 192, 0, 255), font_size=self.c.level_font_size, x=320, y=40,
                                            anchor_x='center', anchor_y='center', batch=batch, group=active_group)

    def read_state(self):
        if os.path.exists('user_cfg/game_progress.ini'):
            self.config.read('user_cfg/game_progress.ini')
            self.logger.debug('config parsed from user_cfg')
        else:
            self.config.read('default_cfg/game_progress.ini')
            self.logger.debug('config parsed from default_cfg')

        self.unlocked_tracks = self.config['user_data'].getint('unlocked_tracks')
        self.level = self.config['user_data'].getint('level')
        self.exp = self.config['user_data'].getfloat('exp')
        self.accumulated_exp = self.config['user_data'].getfloat('accumulated_exp')
        self.money = self.config['user_data'].getfloat('money')
        supported_carts_parsed = self.config['user_data']['supported_carts'].split(',')
        self.supported_carts = (int(supported_carts_parsed[0]), int(supported_carts_parsed[1]))
        self.update_exp_progress_sprite()
        self.update_money_progress_sprite()

    def save_state(self):
        self.config['user_data']['unlocked_tracks'] = str(self.unlocked_tracks)
        self.config['user_data']['level'] = str(self.level)
        self.config['user_data']['exp'] = str(self.exp)
        self.config['user_data']['accumulated_exp'] = str(self.accumulated_exp)
        self.config['user_data']['money'] = str(self.money)
        self.config['user_data']['supported_carts'] = str(self.supported_carts[0]) + ',' + str(self.supported_carts[1])

        with open('user_cfg/game_progress.ini', 'w') as configfile:
            self.config.write(configfile)

    def on_track_unlock(self, track):
        self.main_map.on_track_unlock(track)
        self.mini_map.on_track_unlock(track)
        self.unlocked_tracks = track
        self.supported_carts = self.tracks[track - 1].supported_carts
        self.tracks[track].unlock_condition_from_previous_track = True

    @_maximum_level_not_reached
    def add_exp(self, exp):
        self.exp += exp
        self.accumulated_exp += exp
        self.update_exp_progress_sprite()

    def add_money(self, money):
        self.money += money
        self.money_text.text = '{0:0>8} ¤'.format(int(self.money))
        self.update_money_progress_sprite()

    @_maximum_level_not_reached
    @_level_up
    def update(self, game_paused):
        self.exp = self.accumulated_exp - self.c.accumulated_player_progress[self.level]
        self.level += 1
        if self.level == self.c.maximum_level:
            self.exp = 0.0

        self.level_text.text = 'LEVEL {}'.format(self.level)
        for i in self.c.unlocked_tracks[self.level]:
            self.tracks[i - 1].unlock_condition_from_level = True

        self.update_exp_progress_sprite()

    def update_exp_progress_sprite(self):
        if self.level < self.c.maximum_level:
            self.exp_percent = int(self.exp / self.c.player_progress[self.level] * 100)
            if self.exp_percent > 100:
                self.exp_percent = 100
        else:
            self.exp_percent = 100

        if self.exp_percent == 0:
            image_region = self.progress_bar_exp_active_image.get_region(0, 0, 1, 10)
        else:
            image_region = self.progress_bar_exp_active_image.get_region(0, 0, self.exp_percent * 2, 60)

        self.progress_bar_exp_active.image = image_region
        if self.exp_percent < 100:
            image_region = self.progress_bar_inactive_image.get_region(self.exp_percent * 2, 0,
                                                                       200 - self.exp_percent * 2, 60)
        else:
            image_region = self.progress_bar_inactive_image.get_region(199, 0, 1, 10)

        self.progress_bar_exp_inactive.image = image_region
        self.progress_bar_exp_inactive.position = (10 + self.exp_percent * 2, 10)

    @_money_target_exists
    def update_money_progress_sprite(self):
        self.money_percent = int(self.money / self.money_target * 100)
        if self.money_percent > 100:
            self.money_percent = 100

        if self.money_percent == 0:
            image_region = self.progress_bar_money_active_image.get_region(0, 0, 1, 10)
        else:
            image_region = self.progress_bar_money_active_image.get_region(0, 0, self.money_percent * 2, 60)

        self.progress_bar_money_active.image = image_region
        if self.money_percent < 100:
            image_region = self.progress_bar_inactive_image.get_region(self.money_percent * 2, 0,
                                                                       200 - self.money_percent * 2, 60)
        else:
            image_region = self.progress_bar_inactive_image.get_region(199, 0, 1, 10)

        self.progress_bar_money_inactive.image = image_region
        self.progress_bar_money_inactive.position = (220 + self.money_percent * 2, 10)
