from logging import getLogger

from pyglet.sprite import Sprite

from view import *
from textures import RED_SIGNAL_IMAGE, GREEN_SIGNAL_IMAGE


class SignalView(View):
    """
    Implements Signal view.
    Signal object is responsible for properties, UI and events related to the signal state.
    """
    def __init__(self, map_id, track, base_route):
        """
        Properties:
            map_id                              ID of the map which this signal belongs to
            red_signal_image                    texture for red signal state
            green_signal_image                  texture for green signal state
            signal_sprite                       sprite from the signal image
            state                               signal state: red or green
            locked                              indicates if signal is locked and should not be displayed on map
            flip_needed                         indicates if signal image should be rotated
            position                            signal position on the map

        :param map_id:                          ID of the map which this signal belongs to
        :param track:                           signal track number
        :param base_route:                      base route (train route part) which signal belongs to
        """
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.signal.{track}.{base_route}.view'))
        self.map_id = map_id
        self.red_signal_image = RED_SIGNAL_IMAGE
        self.green_signal_image = GREEN_SIGNAL_IMAGE
        self.signal_sprite = None
        self.state = None
        self.locked = None
        self.config_db_cursor.execute('''SELECT x, y, flip_needed FROM signal_config 
                                         WHERE track = ? AND base_route = ? AND map_id = ?''',
                                      (track, base_route, self.map_id))
        x, y, self.flip_needed = self.config_db_cursor.fetchone()
        self.position = (x, y)
        self.flip_needed = bool(self.flip_needed)
        self.on_init_graphics()

    def on_update_opacity(self, new_opacity):
        """
        Updates view opacity with given value.

        :param new_opacity:                     new opacity value
        """
        self.opacity = new_opacity
        self.on_update_sprite_opacity()

    def on_update_sprite_opacity(self):
        """
        Applies new opacity value to all sprites and labels.
        """
        if self.opacity <= 0:
            if self.signal_sprite is not None:
                self.signal_sprite.delete()
                self.signal_sprite = None
        else:
            if self.signal_sprite is not None:
                self.signal_sprite.opacity = self.opacity

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.on_init_graphics()
        self.is_activated = True
        if self.signal_sprite is None and not self.locked:
            if self.state == 'red_signal':
                self.signal_sprite = Sprite(self.red_signal_image, x=self.base_offset[0] + self.position[0],
                                            y=self.base_offset[1] + self.position[1], batch=self.batches['main_batch'],
                                            group=self.groups['signal'])
            else:
                self.signal_sprite = Sprite(self.green_signal_image, x=self.base_offset[0] + self.position[0],
                                            y=self.base_offset[1] + self.position[1], batch=self.batches['main_batch'],
                                            group=self.groups['signal'])

            self.signal_sprite.opacity = self.opacity
            if self.zoom_out_activated:
                self.signal_sprite.position = (self.base_offset[0] + self.position[0] // 2,
                                               self.base_offset[1] + self.position[1] // 2)

            self.signal_sprite.scale = self.zoom_factor
            if self.flip_needed:
                self.signal_sprite.rotation = 180.0

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
        """
        self.is_activated = False

    def on_unlock(self):
        """
        Unlocks the signal along with the associated track.
        """
        self.locked = False
        # this workaround is needed for signal to be displayed immediately on the map
        self.on_change_base_offset(self.base_offset)

    def on_change_base_offset(self, new_base_offset):
        """
        Updates base offset and moves all labels and sprites to its new positions.

        :param new_base_offset:         new base offset
        """
        self.base_offset = new_base_offset
        if self.is_activated:
            if self.zoom_out_activated:
                x = self.base_offset[0] + self.position[0] // 2
                y = self.base_offset[1] + self.position[1] // 2
            else:
                x = self.base_offset[0] + self.position[0]
                y = self.base_offset[1] + self.position[1]

            if x not in range(-10, self.screen_resolution[0] + 10) \
                    or y not in range(-10, self.screen_resolution[1] + 10):
                if self.signal_sprite is not None:
                    self.signal_sprite.delete()
                    self.signal_sprite = None
            else:
                if self.signal_sprite is None:
                    if not self.locked:
                        if self.state == 'red_signal':
                            self.signal_sprite = Sprite(self.red_signal_image, x=x, y=y,
                                                        batch=self.batches['main_batch'], group=self.groups['signal'])
                        else:
                            self.signal_sprite = Sprite(self.green_signal_image, x=x, y=y,
                                                        batch=self.batches['main_batch'], group=self.groups['signal'])

                        self.signal_sprite.scale = self.zoom_factor
                        if self.flip_needed:
                            self.signal_sprite.rotation = 180.0

                else:
                    self.signal_sprite.position = (x, y)

    def on_change_zoom_factor(self, zoom_factor, zoom_out_activated):
        """
        Zooms in/out all sprites.
        Note that adjusting base offset is made by on_change_base_offset handler,
        this function only changes scale.

        :param zoom_factor                      sprite scale coefficient
        :param zoom_out_activated               indicates if zoom out mode is activated
        """
        self.zoom_factor = zoom_factor
        self.zoom_out_activated = zoom_out_activated
        if self.signal_sprite is not None:
            self.signal_sprite.scale = self.zoom_factor

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution.

        :param screen_resolution:       new screen resolution
        """
        self.on_recalculate_ui_properties(screen_resolution)

    def on_change_state(self, state):
        """
        Updates signal state and sprite.

        :param state:                   new signal state
        """
        self.state = state
        if self.signal_sprite is not None:
            if self.state == 'red_signal':
                self.signal_sprite.image = self.red_signal_image
            else:
                self.signal_sprite.image = self.green_signal_image

    def on_init_graphics(self):
        """
        Initializes the view based on saved screen resolution and base offset.
        """
        self.on_change_screen_resolution(self.screen_resolution)
