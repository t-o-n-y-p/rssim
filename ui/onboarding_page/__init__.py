from ui import *
from database import USER_DB_CURSOR


class OnboardingPage:
    def __init__(self, logger, parent_viewport):
        self.logger = logger
        self.parent_viewport = parent_viewport
        self.viewport = Viewport()
        self.is_activated = False
        self.screen_resolution = (1280, 720)
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.help_label = None
        self.opacity = 0

    @final
    def on_activate(self):
        self.is_activated = True
        self.help_label.create()

    @final
    def on_deactivate(self, instant=False):
        self.is_activated = False
        if instant:
            self.opacity = 0
            self.help_label.delete()

    @final
    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.viewport.x1, self.viewport.x2 = self.parent_viewport.x1, self.parent_viewport.x2
        self.viewport.y1 = self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution)
        self.viewport.y2 = self.parent_viewport.y2
        self.help_label.on_change_screen_resolution(self.screen_resolution)

    @final
    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.help_label.on_update_current_locale(self.current_locale)

    @final
    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.help_label.on_update_opacity(self.opacity)
