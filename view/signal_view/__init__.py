from logging import getLogger
from ctypes import windll

from database import CONFIG_DB_CURSOR
from view import *
from ui.sprite.signal_sprite import SignalSprite


class SignalView(View):
    def __init__(self, map_id, track, base_route):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.signal.{track}.{base_route}.view'))
        self.map_id = map_id
        self.signal_sprite = SignalSprite(self.map_id, track, base_route, parent_viewport=self.viewport)
        self.state = 'red_signal'
        self.locked = True

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

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.signal_sprite.on_update_opacity(self.opacity)

    @view_is_not_active
    def on_activate(self):
        self.is_activated = True
        if not self.locked:
            self.signal_sprite.create()

    @view_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_change_base_offset(self, new_base_offset):
        self.base_offset = new_base_offset
        self.signal_sprite.on_change_base_offset(self.base_offset)
        if self.signal_sprite.is_located_outside_viewport():
            self.signal_sprite.delete()
        elif not self.locked:
            self.signal_sprite.create()

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.viewport.x1, self.viewport.y1 = 0, 0
        self.viewport.x2, self.viewport.y2 = self.screen_resolution

    def on_change_zoom_factor(self, zoom_factor, zoom_out_activated):
        self.zoom_factor = zoom_factor
        self.zoom_out_activated = zoom_out_activated
        self.signal_sprite.on_change_scale(self.zoom_factor)

    def on_unlock(self):
        self.locked = False
        # this workaround is needed for signal to be displayed immediately on the map
        self.on_change_base_offset(self.base_offset)

    def on_change_state(self, state):
        self.state = state
        self.signal_sprite.on_change_state(self.state)
