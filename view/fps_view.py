from logging import getLogger
from ctypes import windll

from database import CONFIG_DB_CURSOR
from view import *
from ui.label.fps_label import FPSLabel


class FPSView(View):
    def __init__(self):
        super().__init__(logger=getLogger('root.app.fps.view'))
        self.fps_label = FPSLabel(parent_viewport=self.viewport)
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
        self.fps_label.create()

    @view_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.viewport.x1 = 0
        self.viewport.y1 = 0
        self.viewport.x2, self.viewport.y2 = self.screen_resolution
        self.fps_label.on_change_screen_resolution(screen_resolution)

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.fps_label.on_update_opacity(self.opacity)

    @view_is_active
    def on_update_fps(self, fps):
        self.fps_label.on_update_args(new_args=(fps, ))
