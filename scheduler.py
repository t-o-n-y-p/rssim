from configparser import RawConfigParser
from logging import getLogger
from os import path, mkdir
from random import seed, choice

from pyglet.image import load
from pyglet.sprite import Sprite
from pyglet.text import Label
from pyglet.resource import add_font

from game_object import GameObject
from button import Button


def _game_is_not_paused(fn):
    def _update_if_game_is_not_paused(*args, **kwargs):
        if not args[1]:
            fn(*args, **kwargs)

    return _update_if_game_is_not_paused


def _schedule_board_is_activated(fn):
    def _update_sprite_if_schedule_board_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _update_sprite_if_schedule_board_is_activated


class Scheduler(GameObject):
    def __init__(self, game_config, batch, group, text_group):
        super().__init__(game_config)
        self.logger = getLogger('game.scheduler')
        self.config = RawConfigParser()
        self.base_schedule = []
        self.base_schedule_sprites = []
        self.game_time = None
        self.game_progress = None
        self.dispatcher = None
        self.next_cycle_start_time = 0
        self.train_counter = 0
        seed()
        self.batch = batch
        self.group = group
        self.text_group = text_group
        self.is_activated = False
        add_font('perfo-bold.ttf')
        self.background_sprite = Sprite(load('img/main_frame/schedule_{}_{}.png'
                                             .format(self.c.screen_resolution[0], self.c.screen_resolution[1])),
                                        x=0, y=0, batch=self.batch, group=self.group)
        self.background_sprite.opacity = 0
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

    def update_sprite(self, base_offset):
        if self.is_activated:
            if self.background_sprite.opacity < 255:
                self.background_sprite.opacity += 15
        else:
            if self.background_sprite.opacity > 0:
                self.background_sprite.opacity -= 15

    def on_board_activate(self):
        self.is_activated = True
        counter = 0
        departure = ''
        self.base_schedule_sprites = []
        while self.base_schedule[counter][1] < self.game_time.epoch_timestamp + 14400 \
                and counter < len(self.base_schedule) and counter < 26:
            self.base_schedule_sprites.append(Label('{0:0>6}'.format(self.base_schedule[counter][0]),
                                                    font_name='Perfo', bold=True, font_size=18,
                                                    color=self.c.day_text_color, x=94 + 640 * (counter // 13),
                                                    y=501 - counter * 27, anchor_x='center', anchor_y='center',
                                                    batch=self.batch, group=self.text_group))
            self.base_schedule_sprites.append(Label('{0:0>2} : {1:0>2}'
                                                    .format((self.base_schedule[counter][1] // 14400 + 12) % 24,
                                                            (self.base_schedule[counter][1] // 240) % 60),
                                                    font_name='Perfo', bold=True, font_size=18,
                                                    color=self.c.day_text_color, x=200 + 640 * (counter // 13),
                                                    y=501 - counter * 27, anchor_x='center', anchor_y='center',
                                                    batch=self.batch, group=self.text_group))
            if self.base_schedule[counter][2] == 0:
                departure = 'West City'
            elif self.base_schedule[counter][2] == 1:
                departure = 'East City'
            elif self.base_schedule[counter][2] == 2:
                departure = 'North-West City'
            elif self.base_schedule[counter][2] == 3:
                departure = 'South-East City'

            self.base_schedule_sprites.append(Label(departure,
                                                    font_name='Perfo', bold=True, font_size=18,
                                                    color=self.c.day_text_color, x=346 + 640 * (counter // 13),
                                                    y=501 - counter * 27, anchor_x='center', anchor_y='center',
                                                    batch=self.batch, group=self.text_group))
            self.base_schedule_sprites.append(Label('{0:0>2}'.format(self.base_schedule[counter][4]),
                                                    font_name='Perfo', bold=True, font_size=18,
                                                    color=self.c.day_text_color, x=470 + 640 * (counter // 13),
                                                    y=501 - counter * 27, anchor_x='center', anchor_y='center',
                                                    batch=self.batch, group=self.text_group))
            self.base_schedule_sprites.append(Label('{0:0>2} : {1:0>2}'
                                                    .format(self.base_schedule[counter][5] // 240,
                                                            (self.base_schedule[counter][5] // 4) % 60),
                                                    font_name='Perfo', bold=True, font_size=18,
                                                    color=self.c.day_text_color, x=550 + 640 * (counter // 13),
                                                    y=501 - counter * 27, anchor_x='center', anchor_y='center',
                                                    batch=self.batch, group=self.text_group))
            counter += 1

    def on_board_deactivate(self):
        self.is_activated = False
        for i in self.base_schedule_sprites:
            i.delete()

        self.base_schedule_sprites.clear()
