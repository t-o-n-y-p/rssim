from abc import ABC

from ui import *


class SettingsKnob(ABC):
    def __init__(self, column, row, on_update_state_action, parent_viewport, logger):
        self.logger = logger
        self.column, self.row = column, row
        self.parent_viewport = parent_viewport
        self.viewport = Viewport()
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.on_update_state_action = on_update_state_action
        self.screen_resolution = (0, 0)
        self.description_label = None
        self.knob = None
        self.is_activated = False
        self.opacity = 0
        self.on_window_resize_handlers = [self.on_window_resize, ]
        self.on_mouse_motion_handlers = []
        self.on_mouse_press_handlers = []
        self.on_mouse_release_handlers = []
        self.on_mouse_drag_handlers = []

    @final
    def on_activate(self):
        self.is_activated = True
        self.description_label.create()
        self.knob.on_activate()

    @final
    def on_deactivate(self):
        self.is_activated = False
        self.knob.on_deactivate()

    @final
    @window_size_has_changed
    def on_window_resize(self, width, height):
        self.screen_resolution = width, height
        self.viewport.x1 = self.parent_viewport.x1 \
                           + (self.column + 1) * (self.parent_viewport.x2 - self.parent_viewport.x1) // 4 \
                           + 2 * get_bottom_bar_height(self.screen_resolution)
        self.viewport.x2 = self.viewport.x1 + (self.parent_viewport.x2 - self.parent_viewport.x1) // 2 \
                           - 4 * get_bottom_bar_height(self.screen_resolution)
        mid_line = (self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution)
                    + self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution)) // 2
        self.viewport.y1 = mid_line + self.row * (5 * get_top_bar_height(self.screen_resolution) // 8) \
                           - get_top_bar_height(self.screen_resolution)
        self.viewport.y2 = self.viewport.y1 + get_bottom_bar_height(self.screen_resolution)

    @final
    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.description_label.on_update_current_locale(self.current_locale)
        self.knob.on_update_current_locale(self.current_locale)

    @final
    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.description_label.on_update_opacity(self.opacity)
        self.knob.on_update_opacity(self.opacity)
