from ui import *
from database import USER_DB_CURSOR


class CheckboxGroup:
    def __init__(self, column, row, parent_viewport, logger):
        self.logger = logger
        self.column, self.row = column, row
        self.parent_viewport = parent_viewport
        self.viewport = Viewport()
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.description_label = None
        self.checkboxes = []
        self.buttons = []
        self.is_activated = False
        self.screen_resolution = (1280, 720)
        self.opacity = 0

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.description_label.on_update_opacity(self.opacity)
        for checkbox in self.checkboxes:
            checkbox.on_update_opacity(self.opacity)

    def on_activate(self):
        self.is_activated = True
        self.description_label.create()
        for checkbox in self.checkboxes:
            checkbox.on_activate()

    def on_init_state(self, checkbox_state_list):
        for i in range(len(self.checkboxes)):
            self.checkboxes[i].on_init_state(checkbox_state_list[i])

    def on_deactivate(self):
        self.is_activated = False
        for checkbox in self.checkboxes:
            checkbox.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.viewport.x1 = self.parent_viewport.x1 \
                           + (self.column + 1) * (self.parent_viewport.x2 - self.parent_viewport.x1) // 4
        self.viewport.x2 = self.viewport.x1 + (self.parent_viewport.x2 - self.parent_viewport.x1) // 2
        mid_line = (self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution)
                    + self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution)) // 2
        self.viewport.y1 = mid_line + self.row * (5 * get_top_bar_height(self.screen_resolution) // 8) \
                           - get_top_bar_height(self.screen_resolution) // 2
        self.viewport.y2 = mid_line + self.row * (5 * get_top_bar_height(self.screen_resolution) // 8) \
                           + get_top_bar_height(self.screen_resolution) // 2
        self.description_label.on_change_screen_resolution(self.screen_resolution)
        for checkbox in self.checkboxes:
            checkbox.on_change_screen_resolution(self.screen_resolution)

    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.description_label.on_update_current_locale(self.current_locale)
        for checkbox in self.checkboxes:
            checkbox.on_update_current_locale(self.current_locale)
