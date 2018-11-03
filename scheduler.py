from configparser import RawConfigParser
from logging import getLogger
from os import path, mkdir
from random import seed, choice

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
        self.dispatcher = None
        self.next_cycle_start_time = 0
        self.train_counter = 0
        seed()
        self.read_state()

    def read_state(self):
        if path.exists('user_cfg/scheduler.ini'):
            self.config.read('user_cfg/scheduler.ini')
            self.logger.debug('config parsed from user_cfg')
        else:
            self.config.read('default_cfg/scheduler.ini')
            self.logger.debug('config parsed from default_cfg')

        self.train_counter = self.config['user_data'].getint('train_counter')
        self.next_cycle_start_time = self.config['user_data'].getint('next_cycle_start_time')
        if self.config['user_data']['base_schedule'] == 'None':
            self.base_schedule = []
        else:
            base_schedule_parsed = self.config['user_data']['base_schedule'].split('|')
            for i in range(len(base_schedule_parsed)):
                base_schedule_parsed[i] = base_schedule_parsed[i].split(',')
                for j in range(6):
                    base_schedule_parsed[i][j] = int(base_schedule_parsed[i][j])
                for j in (6, 7):
                    base_schedule_parsed[i][j] = float(base_schedule_parsed[i][j])

            self.base_schedule = base_schedule_parsed

    def save_state(self):
        if not path.exists('user_cfg'):
            mkdir('user_cfg')
            self.logger.debug('created user_cfg folder')

        self.config['user_data']['train_counter'] = str(self.train_counter)
        self.config['user_data']['next_cycle_start_time'] = str(self.next_cycle_start_time)
        base_schedule_string = ''
        for i in range(len(self.base_schedule)):
            for j in self.base_schedule[i]:
                base_schedule_string += '{},'.format(j)

            base_schedule_string = base_schedule_string[0:len(base_schedule_string)-1] + '|'

        if len(base_schedule_string) > 0:
            base_schedule_string = base_schedule_string[0:len(base_schedule_string)-1]
            self.config['user_data']['base_schedule'] = base_schedule_string
        else:
            self.config['user_data']['base_schedule'] = 'None'

        with open('user_cfg/scheduler.ini', 'w') as configfile:
            self.config.write(configfile)

    @_game_is_not_paused
    def update(self, game_paused):
        if self.game_time.epoch_timestamp + self.c.schedule_cycle_length[self.game_progress.level] \
                >= self.next_cycle_start_time:
            for i in self.c.schedule_options[self.game_progress.level]:
                carts = choice(i[3])
                self.base_schedule.append(
                    (self.train_counter, self.next_cycle_start_time + choice(i[0]), i[1], choice(i[2]), carts,
                     self.c.frame_per_cart[self.game_progress.level] * carts,
                     self.c.exp_per_cart[self.game_progress.level] * carts,
                     self.c.money_per_cart[self.game_progress.level] * carts)
                )
                self.train_counter += 1

            self.next_cycle_start_time += self.c.schedule_cycle_length[self.game_progress.level]

        if self.game_time.epoch_timestamp >= self.base_schedule[0][1]:
            self.dispatcher.on_create_train(self.base_schedule.pop(0))
