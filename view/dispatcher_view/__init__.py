from logging import getLogger
from ctypes import windll

from database import CONFIG_DB_CURSOR
from view import *


class DispatcherView(View):
    def __init__(self, map_id):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.dispatcher.view'))
        self.map_id = map_id

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
        super().on_activate()

    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()

    def on_change_base_offset(self, new_base_offset):
        self.base_offset = new_base_offset

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity

    def on_change_zoom_factor(self, zoom_factor, zoom_out_activated):
        self.zoom_factor = zoom_factor
        self.zoom_out_activated = zoom_out_activated

