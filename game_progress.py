import logging
import configparser
import os

from game_object import GameObject


def _game_is_not_paused(fn):
    def _update_if_game_is_not_paused(*args, **kwargs):
        if not args[1]:
            fn(*args, **kwargs)

    return _update_if_game_is_not_paused


class GameProgress(GameObject):
    def __init__(self, main_map, mini_map, game_config):
        super().__init__(game_config)
        self.logger = logging.getLogger('game.game_progress')
        self.config = configparser.RawConfigParser()
        self.unlocked_tracks = 4
        self.level = 0
        self.exp = 0
        self.accumulated_exp = 0
        self.main_map = main_map
        self.mini_map = mini_map
        self.read_state()

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

    @_game_is_not_paused
    def update(self, game_paused):
        if self.accumulated_exp >= self.c.player_progress[self.level]:
            self.exp = self.accumulated_exp - self.c.player_progress[self.level]
            self.level += 1
