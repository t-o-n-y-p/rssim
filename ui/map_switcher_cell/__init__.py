from abc import ABC

from database import USER_DB_CURSOR, MAP_SWITCHER_STATE_MATRIX, MAP_LOCKED, MAP_LEVEL_REQUIRED, MAP_PRICE
from ui import *
from ui.label.map_switcher_cell_locked_label import MapSwitcherCellLockedLabel
from ui.label.map_switcher_level_placeholder_label import MapSwitcherLevelPlaceholderLabel
from ui.label.map_switcher_unlock_available_label import MapSwitcherUnlockAvailableLabel
from ui.button.build_map_button import BuildMapButton
from ui.button.switch_map_button import SwitchMapButton


def cell_is_active(fn):
    def _handle_if_cell_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_cell_is_activated


def cell_is_not_active(fn):
    def _handle_if_cell_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_cell_is_not_activated


class MapSwitcherCell(ABC):
    def __init__(self, map_id, on_buy_map_action, on_switch_map_action, on_set_money_target_action,
                 on_reset_money_target_action, parent_viewport, logger):
        def on_set_money_target(button):
            pass

        def on_reset_money_target(button):
            pass

        def on_buy_map(button):
            button.on_deactivate()
            self.on_buy_map_action(self.map_id)

        def on_switch_map(button):
            self.on_switch_map_action(self.map_id)

        self.logger = logger
        self.is_activated = False
        self.map_id = map_id
        self.parent_viewport = parent_viewport
        self.viewport = Viewport()
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.on_buy_map_action = on_buy_map_action
        self.on_switch_map_action = on_switch_map_action
        self.on_set_money_target_action = on_set_money_target_action
        self.on_reset_money_target_action = on_reset_money_target_action
        self.screen_resolution = (0, 0)
        USER_DB_CURSOR.execute('''SELECT level, money FROM game_progress''')
        self.level, self.money = USER_DB_CURSOR.fetchone()
        self.money_target_activated = False
        self.opacity = 0
        self.build_map_button = BuildMapButton(on_click_action=on_buy_map, parent_viewport=self.viewport)
        self.switch_map_button = SwitchMapButton(on_click_action=on_switch_map, parent_viewport=self.viewport)
        self.buttons = [self.build_map_button, self.switch_map_button]
        self.data = MAP_SWITCHER_STATE_MATRIX[self.map_id]
        self.locked_label = MapSwitcherCellLockedLabel(parent_viewport=self.viewport)
        self.level_placeholder_label = MapSwitcherLevelPlaceholderLabel(parent_viewport=self.viewport)
        self.level_placeholder_label.on_update_args((self.data[MAP_LEVEL_REQUIRED], ))
        self.unlock_available_label = MapSwitcherUnlockAvailableLabel(parent_viewport=self.viewport)
        self.unlock_available_label.on_update_args((self.data[MAP_PRICE], ))
        self.title_label = None
        self.icon_labels = []

    @final
    @cell_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.on_update_cell_state()
        if not self.data[MAP_LOCKED]:
            self.switch_map_button.on_activate()
        elif self.level >= self.data[MAP_LEVEL_REQUIRED]:
            self.switch_map_button.on_deactivate()
            if self.money < self.data[MAP_PRICE]:
                self.build_map_button.on_disable()
            else:
                self.build_map_button.on_activate()

    @final
    @cell_is_active
    def on_deactivate(self):
        self.is_activated = False
        for b in self.buttons:
            b.on_deactivate()

    @final
    def on_update_money(self, money):
        self.money = money
        if self.is_activated and self.data[MAP_LOCKED] and self.level >= self.data[MAP_LEVEL_REQUIRED]:
            if self.money < self.data[MAP_PRICE]:
                self.build_map_button.on_disable(instant=True)
            else:
                self.build_map_button.on_activate(instant=True)

    @final
    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        top_bar_height = get_top_bar_height(self.screen_resolution)
        self.viewport.x1 = self.parent_viewport.x1 \
                           + self.map_id * ((self.parent_viewport.x2 - self.parent_viewport.x1) // 2 - 1)
        self.viewport.x2 = self.viewport.x1 + (self.parent_viewport.x2 - self.parent_viewport.x1) // 2 + 1
        self.viewport.y1 = self.parent_viewport.y1
        self.viewport.y2 = self.parent_viewport.y2 - top_bar_height + 2
        self.locked_label.on_change_screen_resolution(self.screen_resolution)
        self.level_placeholder_label.on_change_screen_resolution(self.screen_resolution)
        self.unlock_available_label.on_change_screen_resolution(self.screen_resolution)
        self.title_label.on_change_screen_resolution(self.screen_resolution)
        for i in self.icon_labels:
            i.on_change_screen_resolution(self.screen_resolution)

    @final
    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.level_placeholder_label.on_update_current_locale(self.current_locale)
        self.unlock_available_label.on_update_current_locale(self.current_locale)
        self.title_label.on_update_current_locale(self.current_locale)

    @final
    def on_activate_money_target(self):
        self.money_target_activated = True

    @final
    def on_deactivate_money_target(self):
        self.money_target_activated = False

    @final
    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.locked_label.on_update_opacity(self.opacity)
        self.level_placeholder_label.on_update_opacity(self.opacity)
        self.unlock_available_label.on_update_opacity(self.opacity)
        self.title_label.on_update_opacity(self.opacity)
        for i in self.icon_labels:
            i.on_update_opacity(self.opacity)

    @final
    def on_level_up(self):
        self.level += 1
        self.on_update_cell_state()
        if self.is_activated and self.data[MAP_LOCKED] and self.level >= self.data[MAP_LEVEL_REQUIRED]:
            if self.money < self.data[MAP_PRICE]:
                self.build_map_button.on_disable(instant=True)
            else:
                self.build_map_button.on_activate(instant=True)

    @final
    def on_update_cell_state(self):
        if self.level < self.data[MAP_LEVEL_REQUIRED]:
            self.title_label.delete()
            self.unlock_available_label.delete()
            self.locked_label.create()
            self.level_placeholder_label.create()
            for i in self.icon_labels:
                i.delete()

        elif self.data[MAP_LOCKED]:
            self.title_label.delete()
            self.locked_label.delete()
            self.level_placeholder_label.delete()
            self.unlock_available_label.create()
            for i in self.icon_labels:
                i.delete()

        else:
            self.unlock_available_label.delete()
            self.locked_label.delete()
            self.level_placeholder_label.delete()
            self.title_label.create()
            for i in self.icon_labels:
                i.create()
