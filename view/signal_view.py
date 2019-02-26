from logging import getLogger

from pyglet.sprite import Sprite

from view import *


class SignalView(View):
    """
    Implements Signal view.
    Signal object is responsible for properties, UI and events related to the signal state.
    """
    def __init__(self, user_db_cursor, config_db_cursor, surface, batches, groups, track, base_route,
                 red_signal_image, green_signal_image):
        """
        Properties:
            red_signal_image                    texture for red signal state
            green_signal_image                  texture for green signal state
            signal_sprite                       sprite from the signal image
            state                               signal state: red or green
            locked                              indicates if signal is locked and should not be displayed on map
            flip_needed                         indicates if signal image should be rotated
            position                            signal position on the map

        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        :param surface:                         surface to draw all UI objects on
        :param batches:                         batches to group all labels and sprites
        :param groups:                          defines drawing layers (some labels and sprites behind others)
        :param track:                           signal track number
        :param base_route:                      base route (train route part) which signal belongs to
        :param red_signal_image                 texture for red signal state
        :param green_signal_image               texture for green signal state
        """
        super().__init__(user_db_cursor, config_db_cursor, surface, batches, groups,
                         logger=getLogger(f'root.app.game.map.signal.{track}.{base_route}.view'))
        self.logger.info('START INIT')
        self.red_signal_image = red_signal_image
        self.green_signal_image = green_signal_image
        self.logger.debug('textures set successfully')
        self.signal_sprite = None
        self.state = None
        self.locked = None
        self.config_db_cursor.execute('SELECT x, y, flip_needed FROM signal_config WHERE track = ? AND base_route = ?',
                                      (track, base_route))
        x, y, self.flip_needed = self.config_db_cursor.fetchone()
        self.position = (x, y)
        self.logger.debug(f'position: {self.position}')
        self.flip_needed = bool(self.flip_needed)
        self.logger.debug(f'flip_needed: {self.flip_needed}')
        self.logger.info('END INIT')

    @signal_is_displayed_on_map
    def on_update(self):
        """
        Updates fade-in/fade-out animations.
        """
        self.logger.info('START ON_UPDATE')
        self.logger.debug(f'is activated: {self.is_activated}')
        self.logger.debug(f'signal_sprite opacity: {self.signal_sprite.opacity}')
        if self.is_activated and self.signal_sprite.opacity < 255:
            self.signal_sprite.opacity += 15
            self.logger.debug(f'signal_sprite opacity: {self.signal_sprite.opacity}')

        if not self.is_activated and self.signal_sprite.opacity > 0:
            self.signal_sprite.opacity -= 15
            self.logger.debug(f'signal_sprite opacity: {self.signal_sprite.opacity}')
            if self.signal_sprite.opacity <= 0:
                self.signal_sprite.delete()
                self.signal_sprite = None
                self.logger.debug(f'signal_sprite: {self.signal_sprite}')

        self.logger.info('END ON_UPDATE')

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
        self.logger.debug(f'signal_sprite: {self.signal_sprite}')
        self.logger.debug(f'locked: {self.locked}')
        if self.signal_sprite is None and not self.locked:
            self.logger.debug(f'state: {self.state}')
            if self.state == 'red_signal':
                self.signal_sprite = Sprite(self.red_signal_image, x=self.base_offset[0] + self.position[0],
                                            y=self.base_offset[1] + self.position[1], batch=self.batches['main_batch'],
                                            group=self.groups['signal'])
            else:
                self.signal_sprite = Sprite(self.green_signal_image, x=self.base_offset[0] + self.position[0],
                                            y=self.base_offset[1] + self.position[1], batch=self.batches['main_batch'],
                                            group=self.groups['signal'])

            self.logger.debug(f'zoom_out_activated: {self.zoom_out_activated}')
            if self.zoom_out_activated:
                self.signal_sprite.position = (self.base_offset[0] + self.position[0] // 2,
                                               self.base_offset[1] + self.position[1] // 2)

            self.logger.debug(f'signal_sprite position: {self.signal_sprite.position}')
            self.signal_sprite.scale = self.zoom_factor
            self.logger.debug(f'signal_sprite scale: {self.signal_sprite.scale}')
            self.logger.debug(f'flip_needed: {self.flip_needed}')
            if self.flip_needed:
                self.signal_sprite.rotation = 180.0

            self.logger.debug(f'signal_sprite rotation: {self.signal_sprite.rotation}')

        self.logger.info('END ON_ACTIVATE')

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
        self.logger.info('END ON_DEACTIVATE')

    def on_unlock(self):
        """
        Unlocks the signal along with the associated track.
        """
        self.logger.info('START ON_UNLOCK')
        self.locked = False
        self.logger.debug(f'locked: {self.locked}')
        # this workaround is needed for signal to be displayed immediately on the map
        self.on_change_base_offset(self.base_offset)
        self.logger.info('END ON_UNLOCK')

    def on_change_base_offset(self, new_base_offset):
        """
        Updates base offset and moves all labels and sprites to its new positions.

        :param new_base_offset:         new base offset
        """
        self.logger.info('START ON_CHANGE_BASE_OFFSET')
        self.base_offset = new_base_offset
        self.logger.debug(f'base_offset: {self.base_offset}')
        self.logger.debug(f'zoom_out_activated: {self.zoom_out_activated}')
        if self.zoom_out_activated:
            x = self.base_offset[0] + self.position[0] // 2
            y = self.base_offset[1] + self.position[1] // 2
        else:
            x = self.base_offset[0] + self.position[0]
            y = self.base_offset[1] + self.position[1]

        self.logger.debug(f'x, y: {(x, y)}')
        self.logger.debug(f'screen_resolution: {self.screen_resolution}')
        if x not in range(-10, self.screen_resolution[0] + 10) or y not in range(-10, self.screen_resolution[1] + 10):
            self.logger.debug('signal is outside of the screen, delete sprite')
            self.logger.debug(f'signal_sprite: {self.signal_sprite}')
            if self.signal_sprite is not None:
                self.signal_sprite.delete()
                self.signal_sprite = None
                self.logger.debug(f'signal_sprite: {self.signal_sprite}')
        else:
            self.logger.debug('signal is inside the screen, create sprite if needed')
            self.logger.debug(f'is activated: {self.is_activated}')
            self.logger.debug(f'is locked: {self.locked}')
            if self.is_activated and not self.locked:
                self.logger.debug(f'signal_sprite: {self.signal_sprite}')
                if self.signal_sprite is None:
                    self.logger.debug(f'state: {self.state}')
                    if self.state == 'red_signal':
                        self.signal_sprite = Sprite(self.red_signal_image, x=x, y=y,
                                                    batch=self.batches['main_batch'], group=self.groups['signal'])
                    else:
                        self.signal_sprite = Sprite(self.green_signal_image, x=x, y=y,
                                                    batch=self.batches['main_batch'], group=self.groups['signal'])

                    self.logger.debug(f'signal_sprite position: {self.signal_sprite.position}')
                    self.signal_sprite.scale = self.zoom_factor
                    self.logger.debug(f'signal_sprite scale: {self.signal_sprite.scale}')
                    self.logger.debug(f'flip_needed: {self.flip_needed}')
                    if self.flip_needed:
                        self.signal_sprite.rotation = 180.0

                    self.logger.debug(f'signal_sprite rotation: {self.signal_sprite.rotation}')
                else:
                    self.signal_sprite.position = (x, y)
                    self.logger.debug(f'signal_sprite position: {self.signal_sprite.position}')

        self.logger.info('END ON_CHANGE_BASE_OFFSET')

    def on_change_zoom_factor(self, zoom_factor, zoom_out_activated):
        """
        Zooms in/out all sprites.
        Note that adjusting base offset is made by on_change_base_offset handler,
        this function only changes scale.

        :param zoom_factor                      sprite scale coefficient
        :param zoom_out_activated               indicates if zoom out mode is activated
        """
        self.logger.info('START ON_CHANGE_ZOOM_FACTOR')
        self.zoom_factor = zoom_factor
        self.logger.debug(f'zoom_factor: {self.zoom_factor}')
        self.zoom_out_activated = zoom_out_activated
        self.logger.debug(f'zoom_out_activated: {self.zoom_out_activated}')
        self.logger.debug(f'is activated: {self.is_activated}')
        if self.is_activated:
            self.signal_sprite.scale = self.zoom_factor
            self.logger.debug(f'signal_sprite scale: {self.signal_sprite.scale}')

        self.logger.info('END ON_CHANGE_ZOOM_FACTOR')

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution.

        :param screen_resolution:       new screen resolution
        """
        self.logger.info('START ON_CHANGE_SCREEN_RESOLUTION')
        self.on_recalculate_ui_properties(screen_resolution)
        self.logger.info('END ON_CHANGE_SCREEN_RESOLUTION')

    def on_change_state(self, state):
        """
        Updates signal state and sprite.

        :param state:                   new signal state
        """
        self.logger.info('START ON_CHANGE_STATE')
        self.state = state
        self.logger.debug(f'state: {self.state}')
        self.logger.debug(f'is activated: {self.is_activated}')
        if self.is_activated:
            if self.state == 'red_signal':
                self.signal_sprite.image = self.red_signal_image
                self.logger.debug('red signal image set successfully')
            else:
                self.signal_sprite.image = self.green_signal_image
                self.logger.debug('green signal image set successfully')

        self.logger.info('END ON_CHANGE_STATE')
