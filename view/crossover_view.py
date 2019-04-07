from logging import getLogger

from pyglet.sprite import Sprite

from view import *
from textures import SWITCHES_STRAIGHT, SWITCHES_DIVERGING


class CrossoverView(View):
    """
    Implements Crossover view.
    Crossover object is responsible for properties, UI and events related to the crossover.
    """
    def __init__(self, user_db_cursor, config_db_cursor,
                 track_param_1, track_param_2, crossover_type):
        """
        Properties:
            position                            position of the crossover on the map
            crossover_region                    region to cut from crossovers texture
            current_position_1                  current position crossover is switched to: track 1
            current_position_2                  current position crossover is switched to: track 2
            images                              straight and diverging images for the crossover
            sprite                              sprite from straight or diverging image for the crossover
            locked                              indicates if crossover is available for player

        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        :param track_param_1:                   number of the first track of two being connected by the crossover
        :param track_param_2:                   number of the second track of two being connected by the crossover
        :param crossover_type:                  crossover location: left/right side of the map
        """
        self.map_id = None
        self.on_update_map_id()
        super().__init__(
            user_db_cursor, config_db_cursor,
            logger=getLogger(
                f'root.app.game.map.crossover.{track_param_1}.{track_param_2}.{crossover_type}.view'
            )
        )
        self.config_db_cursor.execute('''SELECT offset_x, offset_y FROM crossovers_config
                                         WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? 
                                         AND map_id = ?''',
                                      (track_param_1, track_param_2, crossover_type, self.map_id))
        self.position = self.config_db_cursor.fetchone()
        self.config_db_cursor.execute('''SELECT region_x, region_y, region_w, region_h FROM crossovers_config
                                         WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? 
                                         AND map_id = ?''',
                                      (track_param_1, track_param_2, crossover_type, self.map_id))
        self.switch_region = self.config_db_cursor.fetchone()
        self.user_db_cursor.execute('''SELECT current_position_1, current_position_2 FROM crossovers 
                                       WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? 
                                       AND map_id = ?''',
                                    (track_param_1, track_param_2, crossover_type, self.map_id))
        self.current_position_1, self.current_position_2 = self.user_db_cursor.fetchone()
        self.images = {track_param_1:
                           {track_param_1: SWITCHES_STRAIGHT.get_region(self.switch_region[0], self.switch_region[1],
                                                                        self.switch_region[2], self.switch_region[3]),
                            track_param_2: SWITCHES_DIVERGING.get_region(self.switch_region[0], self.switch_region[1],
                                                                         self.switch_region[2], self.switch_region[3])},
                       track_param_2:
                           {track_param_1: SWITCHES_DIVERGING.get_region(self.switch_region[0], self.switch_region[1],
                                                                         self.switch_region[2], self.switch_region[3]),
                            track_param_2: SWITCHES_STRAIGHT.get_region(self.switch_region[0], self.switch_region[1],
                                                                        self.switch_region[2], self.switch_region[3])}}
        self.user_db_cursor.execute('''SELECT locked FROM crossovers 
                                       WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? 
                                       AND map_id = ?''',
                                    (track_param_1, track_param_2, crossover_type, self.map_id))
        self.locked = bool(self.user_db_cursor.fetchone()[0])
        self.sprite = None

    def on_update(self):
        """
        Updates fade-in/fade-out animations.
        """
        if self.is_activated and self.sprite is not None:
            if self.sprite.opacity < 255:
                self.sprite.opacity += 15

        if not self.is_activated and self.sprite is not None:
            if self.sprite.opacity > 0:
                self.sprite.opacity -= 15
                if self.sprite.opacity <= 0:
                    self.sprite.delete()
                    self.sprite = None

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates all sprites and labels (nothing at the moment).
        """
        self.is_activated = True
        if self.sprite is None and not self.locked:
            self.sprite = Sprite(self.images[self.current_position_1][self.current_position_2],
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
        Deactivates the view and destroys all labels and buttons.
        """
        self.is_activated = False

    def on_change_base_offset(self, new_base_offset):
        """
        Updates base offset and moves all labels and sprites to its new positions (nothing at the moment).

        :param new_base_offset:         new base offset
        """
        self.base_offset = new_base_offset
        if self.zoom_out_activated:
            x = self.base_offset[0] + self.position[0] // 2
            y = self.base_offset[1] + self.position[1] // 2
        else:
            x = self.base_offset[0] + self.position[0]
            y = self.base_offset[1] + self.position[1]

        if x not in range(-10 - self.images[self.current_position_1][self.current_position_2].width,
                          self.screen_resolution[0] + 10) \
                or y not in range(-10 - self.images[self.current_position_1][self.current_position_2].height,
                                  self.screen_resolution[1] + 10):
            if self.sprite is not None:
                self.sprite.delete()
                self.sprite = None
        else:
            if self.sprite is None:
                if not self.locked:
                    self.sprite = Sprite(self.images[self.current_position_1][self.current_position_2],
                                         x=x, y=y, batch=self.batches['main_batch'],
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

    def on_change_current_position(self, current_position_1, current_position_2):
        """
        Updates current switch position and sprite.

        :param current_position_1:                current position crossover is switched to: track 1
        :param current_position_2:                current position crossover is switched to: track 2
        :return:
        """
        self.current_position_1 = current_position_1
        self.current_position_2 = current_position_2
        if self.sprite is not None:
            self.sprite.image = self.images[self.current_position_1][self.current_position_2]

    def on_unlock(self):
        """
        Unlocks the crossover along with the associated track.
        """
        self.locked = False
        # this workaround is needed for crossover to be displayed immediately on the map
        self.on_change_base_offset(self.base_offset)

    def on_update_map_id(self):
        self.map_id = 0
