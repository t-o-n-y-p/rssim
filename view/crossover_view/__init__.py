from logging import getLogger
from ctypes import windll

from database import CONFIG_DB_CURSOR
from view import *
from textures import SWITCHES_STRAIGHT, SWITCHES_DIVERGING
from ui.sprite.crossover_sprite import CrossoverSprite


class CrossoverView(View):
    def __init__(self, map_id, track_param_1, track_param_2, crossover_type):
        super().__init__(
            logger=getLogger(
                f'root.app.game.map.{map_id}.crossover.{track_param_1}.{track_param_2}.{crossover_type}.view'
            )
        )
        self.map_id = map_id
        CONFIG_DB_CURSOR.execute('''SELECT region_x, region_y, region_w, region_h FROM crossovers_config
                                    WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? 
                                    AND map_id = ?''',
                                 (track_param_1, track_param_2, crossover_type, self.map_id))
        self.crossover_region = CONFIG_DB_CURSOR.fetchone()
        USER_DB_CURSOR.execute('''SELECT current_position_1, current_position_2 FROM crossovers 
                                  WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? 
                                  AND map_id = ?''',
                               (track_param_1, track_param_2, crossover_type, self.map_id))
        self.current_position_1, self.current_position_2 = USER_DB_CURSOR.fetchone()
        self.images = {track_param_1:
                           {track_param_1: SWITCHES_STRAIGHT.get_region(*self.crossover_region),
                            track_param_2: SWITCHES_DIVERGING.get_region(*self.crossover_region)},
                       track_param_2:
                           {track_param_1: SWITCHES_DIVERGING.get_region(*self.crossover_region),
                            track_param_2: SWITCHES_STRAIGHT.get_region(*self.crossover_region)}
                       }
        USER_DB_CURSOR.execute('''SELECT locked FROM crossovers 
                                  WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? 
                                  AND map_id = ?''',
                               (track_param_1, track_param_2, crossover_type, self.map_id))
        self.locked = bool(USER_DB_CURSOR.fetchone()[0])
        self.sprite = CrossoverSprite(map_id, track_param_1, track_param_2, crossover_type,
                                      parent_viewport=self.viewport)
        self.sprite.on_update_texture(self.images[self.current_position_1][self.current_position_2])

    def on_init_content(self):
        CONFIG_DB_CURSOR.execute('SELECT app_width, app_height FROM screen_resolution_config')
        screen_resolution_config = CONFIG_DB_CURSOR.fetchall()
        monitor_resolution_config = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
        USER_DB_CURSOR.execute('SELECT fullscreen FROM graphics')
        if bool(USER_DB_CURSOR.fetchone()[0]) and monitor_resolution_config in screen_resolution_config:
            self.on_change_screen_resolution(monitor_resolution_config)
        else:
            USER_DB_CURSOR.execute('SELECT app_width, app_height FROM graphics')
            self.on_change_screen_resolution(USER_DB_CURSOR.fetchone())

    @view_is_not_active
    def on_activate(self):
        self.is_activated = True
        if not self.sprite.is_located_outside_viewport() and not self.locked:
            self.sprite.create()

    @view_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_change_base_offset(self, new_base_offset):
        self.base_offset = new_base_offset
        self.sprite.on_change_base_offset(self.base_offset)
        if self.sprite.is_located_outside_viewport():
            self.sprite.delete()
        elif not self.locked:
            self.sprite.create()

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.viewport.x1, self.viewport.y1 = 0, 0
        self.viewport.x2, self.viewport.y2 = self.screen_resolution

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.sprite.on_update_opacity(self.opacity)

    def on_change_zoom_factor(self, zoom_factor, zoom_out_activated):
        self.zoom_factor = zoom_factor
        self.zoom_out_activated = zoom_out_activated
        self.sprite.on_change_scale(self.zoom_factor)

    def on_change_current_position(self, current_position_1, current_position_2):
        self.current_position_1 = current_position_1
        self.current_position_2 = current_position_2
        self.sprite.on_update_texture(self.images[self.current_position_1][self.current_position_2])

    def on_unlock(self):
        self.locked = False
        # this workaround is needed for crossover to be displayed immediately on the map
        self.on_change_base_offset(self.base_offset)
