from logging import getLogger
from ctypes import windll

from database import CONFIG_DB_CURSOR
from view import *
from textures import SWITCHES_STRAIGHT, SWITCHES_DIVERGING
from ui.sprite.railroad_switch_sprite import RailroadSwitchSprite


class RailroadSwitchView(View):
    def __init__(self, map_id, track_param_1, track_param_2, switch_type):
        super().__init__(
            logger=getLogger(
                f'root.app.game.map.{map_id}.railroad_switch.{track_param_1}.{track_param_2}.{switch_type}.view'
            )
        )
        self.map_id = map_id
        CONFIG_DB_CURSOR.execute('''SELECT region_x, region_y, region_w, region_h FROM switches_config
                                    WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ? 
                                    AND map_id = ?''',
                                 (track_param_1, track_param_2, switch_type, self.map_id))
        self.switch_region = CONFIG_DB_CURSOR.fetchone()
        USER_DB_CURSOR.execute('''SELECT current_position FROM switches 
                                  WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ? 
                                  AND map_id = ?''',
                               (track_param_1, track_param_2, switch_type, self.map_id))
        self.current_position = USER_DB_CURSOR.fetchone()[0]
        self.images = {track_param_1: SWITCHES_STRAIGHT.get_region(*self.switch_region),
                       track_param_2: SWITCHES_DIVERGING.get_region(*self.switch_region)}
        USER_DB_CURSOR.execute('''SELECT locked FROM switches 
                                  WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ? 
                                  AND map_id = ?''',
                               (track_param_1, track_param_2, switch_type, self.map_id))
        self.locked = bool(USER_DB_CURSOR.fetchone()[0])
        self.sprite = RailroadSwitchSprite(map_id, track_param_1, track_param_2, switch_type,
                                           parent_viewport=self.viewport)
        self.on_init_content()

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
        if not self.locked:
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

    def on_change_current_position(self, current_position):
        self.current_position = current_position
        self.sprite.on_update_texture(self.images[self.current_position])

    def on_unlock(self):
        self.locked = False
        # this workaround is needed for switch to be displayed immediately on the map
        self.on_change_base_offset(self.base_offset)
