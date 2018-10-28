import logging
import configparser
import os

import pyglet

from game_object import GameObject
from tip import Tip
from button import Button


def _game_is_not_paused(fn):
    def _update_if_game_is_not_paused(*args, **kwargs):
        if not args[1]:
            fn(*args, **kwargs)

    return _update_if_game_is_not_paused


class Track(GameObject):
    def __init__(self, track_number, base_routes_in_track, batch, tip_group, button_group, text_group, borders_group,
                 game_config):
        def start_track_construction(button):
            self.game_progress.money_target = 0
            self.game_progress.erase_money_progress()
            self.game_progress.add_money((-1)*self.price)
            button.on_button_is_not_visible()
            self.unlock_available = False
            self.not_enough_money_tip.condition_met = False
            self.under_construction = True

        super().__init__(game_config)
        self.logger = logging.getLogger('game.track_{}'.format(track_number))
        self.logger.debug('------- START INIT -------')
        self.config = configparser.RawConfigParser()
        self.logger.debug('config parser created')
        self.track_number = track_number
        self.base_routes = base_routes_in_track
        self.logger.debug('track number and base routes set')
        self.locked = False
        self.under_construction = False
        self.construction_time = 0
        self.busy = False
        self.last_entered_by = 0
        self.override = False
        self.price = 0
        self.supported_carts = None
        self.unlock_condition_from_level = None
        self.unlock_condition_from_previous_track = None
        self.unlock_available = False
        self.game_progress = None
        self.read_state()
        self.unlock_button = Button(position=(195, 81), button_size=(250, 30),
                                    text=['Unlock track {}                     '.format(self.track_number), ],
                                    font_size=self.c.unlock_tip_font_size, on_click=[start_track_construction, ],
                                    is_visible=False, batch=batch,
                                    button_group=button_group, text_group=text_group, borders_group=borders_group,
                                    game_config=self.c, logs_description='track{}_unlock'.format(self.track_number))
        self.not_enough_money_tip = Tip(pyglet.image.load('img/track_tip.png'), x=195, y=81,
                                        tip_type='not_enough_money', batch=batch, group=tip_group,
                                        viewport_border_group=text_group, game_config=self.c,
                                        primary_text='Get                    to unlock track {}'
                                        .format(self.track_number),
                                        price_text='  {} ¤                        '.format(self.price))
        self.under_construction_tip = Tip(pyglet.image.load('img/track_tip.png'), x=195, y=81,
                                          tip_type='track_under_construction', batch=batch, group=tip_group,
                                          viewport_border_group=text_group, game_config=self.c,
                                          primary_text='Building track {}, some time left'.format(self.track_number))
        self.logger.debug('------- END INIT -------')
        self.logger.warning('track init completed')

    def read_state(self):
        self.logger.debug('------- START READING STATE -------')
        if os.path.exists('user_cfg/tracks/track{}.ini'.format(self.track_number)):
            self.config.read('user_cfg/tracks/track{}.ini'.format(self.track_number))
            self.logger.debug('config parsed from user_cfg')
        else:
            self.config.read('default_cfg/tracks/track{}.ini'.format(self.track_number))
            self.logger.debug('config parsed from default_cfg')

        self.locked = self.config['user_data'].getboolean('locked')
        self.under_construction = self.config['user_data'].getboolean('under_construction')
        self.construction_time = self.config['user_data'].getint('construction_time')
        self.construction_time //= 100
        self.busy = self.config['user_data'].getboolean('busy')
        self.logger.debug('busy: {}'.format(self.busy))
        self.last_entered_by = self.config['user_data'].getint('last_entered_by')
        self.logger.debug('last_entered_by: {}'.format(self.last_entered_by))
        self.override = self.config['user_data'].getboolean('override')
        self.logger.debug('override: {}'.format(self.override))
        supported_carts_parsed = self.config['track_config']['supported_carts'].split(',')
        self.supported_carts = (int(supported_carts_parsed[0]), int(supported_carts_parsed[1]))
        self.unlock_condition_from_level = self.config['user_data'].getboolean('unlock_condition_from_level')
        self.unlock_condition_from_previous_track \
            = self.config['user_data'].getboolean('unlock_condition_from_previous_track')
        self.unlock_available = self.config['user_data'].getboolean('unlock_available')
        self.price = self.config['track_config'].getint('price')

        self.logger.debug('------- END READING STATE -------')
        self.logger.info('track state initialized')

    def save_state(self):
        self.logger.debug('------- START SAVING STATE -------')
        if not os.path.exists('user_cfg'):
            os.mkdir('user_cfg')
            self.logger.debug('created user_cfg folder')

        if not os.path.exists('user_cfg/tracks'):
            os.mkdir('user_cfg/tracks')
            self.logger.debug('created user_cfg/tracks folder')

        self.config['user_data']['locked'] = str(self.locked)
        self.config['user_data']['under_construction'] = str(self.under_construction)
        self.config['user_data']['construction_time'] = str(self.construction_time)
        self.config['user_data']['busy'] = str(self.busy)
        self.logger.debug('busy: {}'.format(self.config['user_data']['busy']))
        self.config['user_data']['last_entered_by'] = str(self.last_entered_by)
        self.logger.debug('last_entered_by: {}'.format(self.config['user_data']['last_entered_by']))
        self.config['user_data']['override'] = str(self.override)
        self.logger.debug('override: {}'.format(self.config['user_data']['override']))
        self.config['user_data']['unlock_condition_from_level'] = str(self.unlock_condition_from_level)
        self.config['user_data']['unlock_condition_from_previous_track'] \
            = str(self.unlock_condition_from_previous_track)
        self.config['user_data']['unlock_available'] = str(self.unlock_available)

        with open('user_cfg/tracks/track{}.ini'.format(self.track_number), 'w') as configfile:
            self.config.write(configfile)

        self.logger.debug('------- END SAVING STATE -------')
        self.logger.info('track state saved to file user_cfg/tracks/track{}.ini'.format(self.track_number))

    @_game_is_not_paused
    def update(self, game_paused):
        # if game is paused, track status should not be updated
        # if track settings are overridden, we do nothing too
        self.logger.debug('------- TRACK UPDATE START -------')
        if not self.override:
            busy_1 = False
            # if any of 4 base routes are busy, all track will become busy
            for i in self.base_routes:
                busy_1 = busy_1 or i.route_config['busy']
                self.logger.debug('base route {} busy: {}'.format(i, i.route_config['busy']))
                if i.route_config['busy']:
                    self.last_entered_by = i.route_config['last_entered_by']

            self.busy = busy_1
            self.logger.debug('busy: {}'.format(self.busy))

        if self.unlock_available:
            if self.game_progress.money < self.price:
                if self.unlock_button.is_visible:
                    self.unlock_button.on_button_is_not_visible()
                    self.not_enough_money_tip.primary_text_label.text = 'Get                    to unlock track {}'\
                                                                        .format(self.track_number),
                    self.not_enough_money_tip.price_text_label.text = '  {} ¤                        '\
                                                                      .format(self.price)
            else:
                if not self.unlock_button.is_visible:
                    self.unlock_button.on_button_is_visible()
                    self.not_enough_money_tip.primary_text_label.text = ''
                    self.not_enough_money_tip.price_text_label.text = '                      {} ¤'.format(self.price)

        if self.under_construction:
            if not self.under_construction_tip.condition_met:
                self.under_construction_tip.condition_met = True

            self.logger.info('base route is under construction')
            self.construction_time -= 1
            self.logger.info('construction_time left: {}'.format(self.construction_time))
            if self.construction_time <= 0:
                self.locked = False
                self.under_construction = False
                self.under_construction_tip.condition_met = False
                self.game_progress.on_track_unlock(self.track_number)
                self.logger.info('route unlocked and is no longer under construction')

        self.logger.debug('------- TRACK UPDATE END -------')
        self.logger.info('track updated')

    def on_unlock_condition_from_previous_track(self):
        self.unlock_condition_from_previous_track = True
        if self.unlock_condition_from_level and self.unlock_condition_from_previous_track:
            self.unlock_condition_from_level = False
            self.unlock_condition_from_previous_track = False
            self.unlock_available = True
            self.not_enough_money_tip.condition_met = True
            self.game_progress.money_target = self.price
            self.game_progress.update_money_progress_sprite()

    def on_unlock_condition_from_level(self):
        self.unlock_condition_from_level = True
        if self.unlock_condition_from_level and self.unlock_condition_from_previous_track:
            self.unlock_condition_from_level = False
            self.unlock_condition_from_previous_track = False
            self.unlock_available = True
            self.not_enough_money_tip.condition_met = True
            self.game_progress.money_target = self.price
            self.game_progress.update_money_progress_sprite()
