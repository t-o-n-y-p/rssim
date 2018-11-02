import configparser
import os
import logging

import pyglet

from game_object import GameObject


def _game_is_not_paused(fn):
    def _update_if_game_is_not_paused(*args, **kwargs):
        if not args[1]:
            fn(*args, **kwargs)

    return _update_if_game_is_not_paused


def _signal_is_not_locked(fn):
    def _update_sprite_if_signal_is_not_locked(*args, **kwargs):
        if not args[0].locked:
            fn(*args, **kwargs)

    return _update_sprite_if_signal_is_not_locked


class Signal(GameObject):
    def __init__(self, placement, flip_needed, track_number, route_type, batch, signal_group, game_config):
        super().__init__(game_config)
        self.logger = logging.getLogger('game.signal_{}_{}'.format(route_type, track_number))
        self.logger.debug('------- START INIT -------')
        self.config = configparser.RawConfigParser()
        self.logger.debug('config parser created')
        self.track_number = track_number
        self.route_type = route_type
        # where to place signal on map
        self.placement = placement
        self.priority = 0
        self.batch = batch
        self.signal_group = signal_group
        # for left-directed routes we need to flip signal (its default image is for right-directed routes)
        self.flip_needed = flip_needed
        self.logger.debug('params set: track number {}, route type {}, placement {}, flip_needed {}'
                          .format(self.track_number, self.route_type, self.placement, self.flip_needed))
        # initialize signal state
        self.state = 'red_signal'
        self.image = {'red_signal': pyglet.image.load('img/signals/signal_red.png'),
                      'green_signal': pyglet.image.load('img/signals/signal_green.png')}
        self.image['red_signal'].anchor_x = 5
        self.image['red_signal'].anchor_y = 5
        self.image['green_signal'].anchor_x = 5
        self.image['green_signal'].anchor_y = 5

        self.base_route_opened_list = []
        self.base_route_exit = None
        self.base_route_opened = None
        self.locked = None
        self.read_state()
        self.sprite = None
        self.logger.debug('------- END INIT -------')
        self.logger.warning('signal init completed')

    def read_state(self):
        self.logger.debug('------- START READING STATE -------')
        if os.path.exists('user_cfg/signals/track{}/track{}_{}.ini'
                          .format(self.track_number, self.track_number, self.route_type)):
            self.config.read('user_cfg/signals/track{}/track{}_{}.ini'
                             .format(self.track_number, self.track_number, self.route_type))
            self.logger.debug('config parsed from user_cfg')
        else:
            self.config.read('default_cfg/signals/track{}/track{}_{}.ini'
                             .format(self.track_number, self.track_number, self.route_type))
            self.logger.debug('config parsed from default_cfg')

        self.state = self.config['user_data']['state']
        self.logger.debug('state: {}'.format(self.state))
        self.logger.debug('------- END READING STATE -------')
        self.logger.info('signal state initialized')

    def save_state(self):
        self.logger.debug('------- START SAVING STATE -------')
        if not os.path.exists('user_cfg'):
            os.mkdir('user_cfg')
            self.logger.debug('created user_cfg folder')

        if not os.path.exists('user_cfg/signals'):
            os.mkdir('user_cfg/signals')
            self.logger.debug('created user_cfg/signals folder')

        if not os.path.exists('user_cfg/signals/track{}'.format(self.track_number)):
            os.mkdir('user_cfg/signals/track{}'.format(self.track_number))
            self.logger.debug('created user_cfg/signals/track{} folder'.format(self.track_number))

        self.config['user_data']['state'] = self.state
        self.logger.debug('state: {}'.format(self.config['user_data']['state']))

        with open('user_cfg/signals/track{}/track{}_{}.ini'
                  .format(self.track_number, self.track_number, self.route_type), 'w') as configfile:
            self.config.write(configfile)

        self.logger.debug('------- END SAVING STATE -------')
        self.logger.info('signal state saved to file user_cfg/signals/track{}/track{}_{}.ini'
                         .format(self.track_number, self.track_number, self.route_type))

    def update_sprite(self, base_offset):
        self.logger.debug('------- START DRAWING -------')
        self.logger.debug('signal is not invisible, drawing')
        signal_position = (base_offset[0] + self.placement[0], base_offset[1] + self.placement[1])
        if signal_position[0] not in range(-15, self.c.screen_resolution[0] + 15) \
                or signal_position[1] not in range(-15, self.c.screen_resolution[1] + 15):
            if self.sprite is not None:
                self.sprite.delete()
                self.sprite = None

        else:
            if self.sprite is None:
                self.sprite = pyglet.sprite.Sprite(self.image[self.state],
                                                   x=signal_position[0], y=signal_position[1],
                                                   batch=self.batch, group=self.signal_group)
                self.sprite.visible = not self.locked
                if self.flip_needed:
                    self.sprite.rotation = 180.0

            else:
                self.sprite.position = signal_position

        self.logger.info('signal image is in place')
        self.logger.debug('------- END DRAWING -------')

    @_game_is_not_paused
    @_signal_is_not_locked
    def update(self, game_paused):
        self.logger.debug('-------UPDATE START-------')
        if not self.base_route_exit.route_config['opened']:
            self.priority = 0
            if self.state == 'green_signal':
                self.state = 'red_signal'
                if self.sprite is not None:
                    self.sprite.image = self.image[self.state]
                    if self.flip_needed:
                        self.sprite.rotation = 180.0

                self.base_route_opened = None

            self.logger.debug('no train approaching, signal is RED')
        else:
            self.priority = self.base_route_exit.priority
            for i in self.base_route_opened_list:
                if i.route_config['opened'] and i.route_config['last_opened_by'] \
                        == self.base_route_exit.route_config['last_opened_by']:
                    self.base_route_opened = i

            if self.base_route_opened is None:
                if self.state == 'green_signal':
                    self.state = 'red_signal'
                    if self.sprite is not None:
                        self.sprite.image = self.image[self.state]
                        if self.flip_needed:
                            self.sprite.rotation = 180.0

                self.logger.debug('route through signal is not opened, signal is RED')
            else:
                self.base_route_opened.update_base_route_state()

                self.logger.debug('approaching train: {}'.format(self.base_route_exit.route_config['last_opened_by']))
                self.logger.debug('its route is busy by train: {}'
                                  .format(self.base_route_opened.route_config['last_entered_by']))
                if self.base_route_opened.route_config['busy'] and self.base_route_exit.route_config['last_opened_by'] \
                        != self.base_route_opened.route_config['last_entered_by']:
                    if self.state == 'green_signal':
                        self.state = 'red_signal'
                        if self.sprite is not None:
                            self.sprite.image = self.image[self.state]
                            if self.flip_needed:
                                self.sprite.rotation = 180.0

                    self.logger.debug('route through signal is opened but busy by another train, signal is RED')
                else:
                    if self.state == 'red_signal':
                        self.state = 'green_signal'
                        if self.sprite is not None:
                            self.sprite.image = self.image[self.state]
                            if self.flip_needed:
                                self.sprite.rotation = 180.0

                        self.base_route_opened.enter_base_route(self.base_route_exit.route_config['last_opened_by'])
                        self.logger.debug('train {} is allowed to pass'
                                          .format(self.base_route_exit.route_config['last_opened_by']))

        self.logger.debug('-------UPDATE END-------')
        self.logger.info('signal updated')

    def on_unlock(self):
        self.locked = False
        if self.sprite is not None:
            self.sprite.visible = True
