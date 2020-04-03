from abc import ABC

from ui import *
from ui.button import create_two_state_button
from ui.button.checked_checkbox_button import CheckedCheckboxButton
from ui.button.unchecked_checkbox_button import UncheckedCheckboxButton
from database import USER_DB_CURSOR


class Checkbox(ABC):
    def __init__(self, column, row, on_update_state_action, parent_viewport, logger):
        def on_check(button):
            self.on_change_state(TRUE)
            self.on_update_state_action(TRUE)

        def on_uncheck(button):
            self.on_change_state(FALSE)
            self.on_update_state_action(FALSE)

        self.logger = logger
        self.column, self.row = column, row
        self.parent_viewport = parent_viewport
        self.viewport = Viewport()
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.on_update_state_action = on_update_state_action
        self.checked_checkbox_button, self.unchecked_checkbox_button = create_two_state_button(
            CheckedCheckboxButton(on_click_action=on_uncheck, parent_viewport=self.viewport),
            UncheckedCheckboxButton(on_click_action=on_check, parent_viewport=self.viewport)
        )
        self.buttons = [self.checked_checkbox_button, self.unchecked_checkbox_button]
        self.screen_resolution = (0, 0)
        self.description_label = None
        self.is_activated = False
        self.opacity = 0
        self.on_window_resize_handlers = [self.on_window_resize, ]

    @final
    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.description_label.on_update_opacity(self.opacity)

    @final
    def on_activate(self):
        self.is_activated = True
        self.description_label.create()

    @final
    def on_change_state(self, state):
        if state:
            self.checked_checkbox_button.opacity = self.opacity
            self.checked_checkbox_button.on_activate()
            self.unchecked_checkbox_button.on_deactivate(instant=True)
        else:
            self.checked_checkbox_button.on_deactivate(instant=True)
            self.unchecked_checkbox_button.opacity = self.opacity
            self.unchecked_checkbox_button.on_activate()

    @final
    def on_deactivate(self):
        self.is_activated = False
        for b in self.buttons:
            b.on_deactivate()

    @final
    @window_size_has_changed
    def on_window_resize(self, width, height):
        self.screen_resolution = width, height
        self.viewport.x1 \
            = self.parent_viewport.x1 + (self.column + 1) * (self.parent_viewport.x2 - self.parent_viewport.x1) // 4
        self.viewport.x2 = self.viewport.x1 + (self.parent_viewport.x2 - self.parent_viewport.x1) // 2
        mid_line = (
            self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution)
            + self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution)
        ) // 2
        self.viewport.y1 \
            = mid_line + self.row * (5 * get_top_bar_height(self.screen_resolution) // 8) \
            - get_top_bar_height(self.screen_resolution) // 2
        self.viewport.y2 \
            = mid_line + self.row * (5 * get_top_bar_height(self.screen_resolution) // 8) \
            + get_top_bar_height(self.screen_resolution) // 2

    @final
    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.description_label.on_update_current_locale(self.current_locale)
