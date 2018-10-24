import logging
import configparser
import os

import pyglet

from game_object import GameObject


class GameProgress(GameObject):
    def __init__(self, main_map, mini_map, game_config, batch, inactive_group, active_group):
        super().__init__(game_config)
        self.logger = logging.getLogger('game.game_progress')
        self.config = configparser.RawConfigParser()
        self.unlocked_tracks = 4
        self.level = 0
        self.exp = 0
        self.accumulated_exp = 0
        self.main_map = main_map
        self.mini_map = mini_map
        self.progress_bar_inactive_image = pyglet.image.load('img/progress_bar_inactive.png')
        self.progress_bar_inactive = pyglet.sprite.Sprite(self.progress_bar_inactive_image,
                                                          x=10, y=10, batch=batch, group=inactive_group)
        self.progress_bar_active_image = pyglet.image.load('img/progress_bar_active.png')
        self.progress_bar_active = pyglet.sprite.Sprite(self.progress_bar_active_image,
                                                        x=10, y=10, batch=batch, group=active_group)
        self.progress_bar_active.image = self.progress_bar_active_image.get_region(0, 0, 1, 10)
        self.read_state()
        self.level_text = pyglet.text.Label('Level {}'.format(self.level), font_name=self.c.font_name,
                                            font_size=self.c.level_font_size, x=110, y=40, anchor_x='center',
                                            anchor_y='center', batch=batch, group=active_group)

    def read_state(self):
        if os.path.exists('user_cfg/game_progress.ini'):
            self.config.read('user_cfg/game_progress.ini')
            self.logger.debug('config parsed from user_cfg')
        else:
            self.config.read('default_cfg/game_progress.ini')
            self.logger.debug('config parsed from default_cfg')

        self.unlocked_tracks = self.config['user_data'].getint('unlocked_tracks')
        self.level = self.config['user_data'].getint('level')
        self.exp = self.config['user_data'].getint('exp')
        self.accumulated_exp = self.config['user_data'].getint('accumulated_exp')
        self.update_exp_progress()
        self.update_exp_progress_sprite()

    def save_state(self):
        self.config['user_data']['unlocked_tracks'] = str(self.unlocked_tracks)
        self.config['user_data']['level'] = str(self.level)
        self.config['user_data']['exp'] = str(self.exp)
        self.config['user_data']['accumulated_exp'] = str(self.accumulated_exp)

        with open('user_cfg/game_progress.ini', 'w') as configfile:
            self.config.write(configfile)

    def on_track_unlock(self, track):
        self.main_map.on_track_unlock(track)
        self.mini_map.on_track_unlock(track)
        self.unlocked_tracks = track

    def add_exp(self, exp):
        self.exp += exp
        self.accumulated_exp += exp
        self.update_exp_progress()
        self.update_exp_progress_sprite()

    def update_exp_progress(self):
        if self.accumulated_exp >= self.c.accumulated_player_progress[self.level]:
            self.exp = self.accumulated_exp - self.c.accumulated_player_progress[self.level]
            self.level += 1
            self.level_text.text = 'Level {}'.format(self.level)

    def update_exp_progress_sprite(self):
        percent = int(self.exp / self.c.player_progress[self.level] * 100)
        if percent == 0:
            image_region = self.progress_bar_active_image.get_region(0, 0, 1, 10)
        else:
            image_region = self.progress_bar_active_image.get_region(0, 0, percent * 2, 60)

        self.progress_bar_active.image = image_region
        image_region = self.progress_bar_inactive_image.get_region(percent * 2, 0, 200 - percent * 2, 60)
        self.progress_bar_inactive.image = image_region
        self.progress_bar_inactive.position = (10 + percent * 2, 10)
