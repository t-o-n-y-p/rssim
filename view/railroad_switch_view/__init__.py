from logging import getLogger

from pyglet.sprite import Sprite

from view import *
from textures import SWITCHES_STRAIGHT, SWITCHES_DIVERGING


class RailroadSwitchView(View):
    """
    Implements Railroad switch view.
    Railroad switch object is responsible for properties, UI and events related to the railroad switch.
    """
    def __init__(self, track_param_1, track_param_2, switch_type):
        """
        Properties:
            position                            position of the switch on the map
            switch_region                       region to cut from switches texture
            current_position                    current switch position
            images                              straight and diverging images for the switch
            sprite                              sprite from straight or diverging image for the switch
            locked                              indicates if switch is available for player

        :param track_param_1:                   number of the straight track
        :param track_param_2:                   number of the diverging track
        :param switch_type:                     railroad switch location: left/right side of the map
        """
        self.map_id = None
        self.on_update_map_id()
        super().__init__(
            logger=getLogger(
                f'root.app.game.map.{self.map_id}.railroad_switch.{track_param_1}.{track_param_2}.{switch_type}.view'
            )
        )
        self.config_db_cursor.execute('''SELECT offset_x, offset_y FROM switches_config
                                         WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ? 
                                         AND map_id = ?''',
                                      (track_param_1, track_param_2, switch_type, self.map_id))
        self.position = self.config_db_cursor.fetchone()
        self.config_db_cursor.execute('''SELECT region_x, region_y, region_w, region_h FROM switches_config
                                         WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ? 
                                         AND map_id = ?''',
                                      (track_param_1, track_param_2, switch_type, self.map_id))
        self.switch_region = self.config_db_cursor.fetchone()
        self.user_db_cursor.execute('''SELECT current_position FROM switches 
                                       WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ? 
                                       AND map_id = ?''',
                                    (track_param_1, track_param_2, switch_type, self.map_id))
        self.current_position = self.user_db_cursor.fetchone()[0]
        self.images = {track_param_1: SWITCHES_STRAIGHT.get_region(self.switch_region[0], self.switch_region[1],
                                                                   self.switch_region[2], self.switch_region[3]),
                       track_param_2: SWITCHES_DIVERGING.get_region(self.switch_region[0], self.switch_region[1],
                                                                    self.switch_region[2], self.switch_region[3])}
        self.user_db_cursor.execute('''SELECT locked FROM switches 
                                       WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ? 
                                       AND map_id = ?''',
                                    (track_param_1, track_param_2, switch_type, self.map_id))
        self.locked = bool(self.user_db_cursor.fetchone()[0])
        self.sprite = None
        self.on_init_graphics()

    def on_update(self):
        pass

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.on_update_sprite_opacity()

    def on_update_sprite_opacity(self):
        if self.opacity <= 0:
            if self.sprite is not None:
                self.sprite.delete()
                self.sprite = None
        else:
            if self.sprite is not None:
                self.sprite.opacity = self.opacity

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates all sprites and labels.
        """
        self.on_init_graphics()
        self.is_activated = True
        if self.sprite is None and not self.locked:
            self.sprite = Sprite(self.images[self.current_position],
                                 x=self.base_offset[0] + self.position[0],
                                 y=self.base_offset[1] + self.position[1], batch=self.batches['main_batch'],
                                 group=self.groups['main_map'])
            if self.zoom_out_activated:
                self.sprite.position = (self.base_offset[0] + self.position[0] // 2,
                                        self.base_offset[1] + self.position[1] // 2)

            self.sprite.scale = self.zoom_factor

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all sprites and labels.
        """
        self.is_activated = False

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

            if x not in range(-10 - self.images[self.current_position].width, self.screen_resolution[0] + 10) \
                    or y not in range(-10 - self.images[self.current_position].height, self.screen_resolution[1] + 10):
                if self.sprite is not None:
                    self.sprite.delete()
                    self.sprite = None
            else:
                if self.sprite is None:
                    if not self.locked:
                        self.sprite = Sprite(self.images[self.current_position], x=x, y=y, batch=self.batches['main_batch'],
                                             group=self.groups['main_map'])
                        self.sprite.scale = self.zoom_factor

                else:
                    self.sprite.position = (x, y)

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions (nothing at the moment).

        :param screen_resolution:       new screen resolution
        """
        self.on_recalculate_ui_properties(screen_resolution)

    def on_change_zoom_factor(self, zoom_factor, zoom_out_activated):
        """
        Zooms in/out all sprites (nothing at the moment).
        Note that adjusting base offset is made by on_change_base_offset handler,
        this function only changes scale.

        :param zoom_factor                      sprite scale coefficient
        :param zoom_out_activated               indicates if zoom out mode is activated
        """
        self.zoom_factor = zoom_factor
        self.zoom_out_activated = zoom_out_activated
        if self.sprite is not None:
            self.sprite.scale = self.zoom_factor

    def on_change_current_position(self, current_position):
        """
        Updates current switch position and sprite.

        :param current_position:                new switch position
        :return:
        """
        self.current_position = current_position
        if self.sprite is not None:
            self.sprite.image = self.images[self.current_position]

    def on_unlock(self):
        """
        Unlocks the switch along with the associated track.
        """
        self.locked = False
        # this workaround is needed for switch to be displayed immediately on the map
        self.on_change_base_offset(self.base_offset)

    def on_update_map_id(self):
        pass

    def on_init_graphics(self):
        self.on_change_screen_resolution(self.screen_resolution)
