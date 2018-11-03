from configparser import RawConfigParser
from logging import getLogger
from os import path, mkdir

from game_object import GameObject


def _game_is_not_paused(fn):
    def _update_if_game_is_not_paused(*args, **kwargs):
        if not args[1]:
            fn(*args, **kwargs)

    return _update_if_game_is_not_paused


def _more_trains_needed(fn):
    def _generate_more_trains_if_needed(*args, **kwargs):
        if args[0].game_time.epoch_timestamp + args[0].c.schedule_cycle_length[args[0].game_progress.level] \
                >= args[0].next_cycle_start_time:
            fn(*args, **kwargs)

    return _generate_more_trains_if_needed


class Scheduler(GameObject):
    def __init__(self, game_config):
        super().__init__(game_config)
        self.logger = getLogger('game.scheduler')
        self.config = RawConfigParser()
        self.base_schedule = []
        self.game_time = None
        self.game_progress = None
        self.next_cycle_start_time = 0
        self.read_state()

    def read_state(self):
        if path.exists('user_cfg/scheduler.ini'):
            self.config.read('user_cfg/scheduler.ini')
            self.logger.debug('config parsed from user_cfg')
        else:
            self.config.read('default_cfg/scheduler.ini')
            self.logger.debug('config parsed from default_cfg')
