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


def _signal_is_not_invisible(fn):
    def _draw_if_signal_is_not_invisible(*args, **kwargs):
        if not args[0].invisible:
            return fn(*args, **kwargs)
        else:
            return []

    return _draw_if_signal_is_not_invisible


class Signal(GameObject):
    def __init__(self, placement, flip_needed, invisible, track_number, route_type, batch, group):
        super().__init__()
        self.logger = logging.getLogger('game.signal_{}_{}'.format(route_type, track_number))
        self.logger.debug('------- START INIT -------')
        self.config = configparser.RawConfigParser()
        self.logger.debug('config parser created')
        self.track_number = track_number
        self.route_type = route_type
        self.invisible = invisible
        # where to place signal on map
        self.placement = placement
        self.batch = batch
        self.group = group
        # for left-directed routes we need to flip signal (its default image is for right-directed routes)
        self.flip_needed = flip_needed
        self.logger.debug('params set: track number {}, route type {}, invisible {}, placement {}, flip_needed {}'
                          .format(self.track_number, self.route_type, self.invisible, self.placement, self.flip_needed))
        # initialize signal state
        self.state = None
        self.base_image = pyglet.image.load(self.c['signal_config']['signal_image_base_path'])
        self.base_sprite = pyglet.sprite.Sprite(self.base_image,
                                                x=placement[0], y=placement[1], batch=self.batch, group=self.group)
        self.logger.debug('base image loaded: {}'.format(self.c['signal_config']['signal_image_base_path']))
        self.image = {self.c['signal_config']['red_signal']:
                      pyglet.image.load(self.c['signal_image_path'][self.c['signal_config']['red_signal']]),
                      self.c['signal_config']['green_signal']:
                      pyglet.image.load(self.c['signal_image_path'][self.c['signal_config']['green_signal']])}
        if self.flip_needed:
            self.base_sprite.rotation = 180.0
            self.logger.debug('base image flipped')

        self.base_route_opened_list = []
        self.base_route_exit = None
        self.read_state()
        self.sprite = pyglet.sprite.Sprite(self.image[self.state],
                                           x=placement[0], y=placement[1], batch=self.batch, group=self.group)
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

    @_signal_is_not_invisible
    def update_sprite(self, base_offset):
        self.logger.debug('------- START DRAWING -------')
        self.logger.debug('signal is not invisible, drawing')
        signal_position = (base_offset[0] + self.placement[0],
                           self.c['graphics']['screen_resolution'][1] - self.base_image.height
                           - (base_offset[1] + self.placement[1]))
        # reserved for future transition between states,
        # for now there are only 2 states: pure red and pure green
        self.base_sprite.position = signal_position
        self.logger.debug('signal base image is in place')
        if self.sprite is not None:
            self.sprite.delete()
            self.sprite = None

        self.sprite = pyglet.sprite.Sprite(self.image[self.state],
                                           batch=self.batch, group=self.group)
        self.sprite.position = signal_position
        self.logger.debug('signal light image is in place')
        self.logger.info('signal image is in place')
        self.logger.debug('------- END DRAWING -------')

    @_game_is_not_paused
    def update(self, game_paused):
        self.logger.debug('-------UPDATE START-------')
        busy_logical = False
        opened_by = []
        entered_by = []

        if not self.base_route_exit.route_config['opened']:
            self.state = self.c['signal_config']['red_signal']
            self.logger.debug('no train approaching, signal is RED')
        else:
            for i in self.base_route_opened_list:
                if i.route_config['opened']:
                    opened_by.append(i.route_config['last_opened_by'])

            if self.base_route_exit.route_config['last_opened_by'] not in opened_by:
                self.state = self.c['signal_config']['red_signal']
                self.logger.debug('route through signal is not opened, signal is RED')
            else:
                for i in self.base_route_opened_list:
                    if i.route_config['opened'] and i.route_config['last_opened_by'] \
                            == self.base_route_exit.route_config['last_opened_by']:
                        i.update_base_route_state(game_paused)
                        busy_logical = busy_logical or i.route_config['busy']
                        entered_by.append(i.route_config['last_entered_by'])

                if busy_logical and self.base_route_exit.route_config['last_opened_by'] not in entered_by:
                    self.state = self.c['signal_config']['red_signal']
                    self.logger.debug('route through signal is opened but busy by another train, signal is RED')
                else:
                    self.state = self.c['signal_config']['green_signal']
                    self.logger.debug('route through signal is opened and free, signal is GREEN')
                    for i in self.base_route_opened_list:
                        if i.route_config['opened'] and i.route_config['last_opened_by'] \
                                == self.base_route_exit.route_config['last_opened_by'] \
                                and not i.route_config['busy']:
                            i.enter_base_route(self.base_route_exit.route_config['last_opened_by'], game_paused)
                            self.logger.debug('train {} is allowed to pass'
                                              .format(self.base_route_exit.route_config['last_opened_by']))

        self.logger.debug('-------UPDATE END-------')
        self.logger.info('signal updated')
