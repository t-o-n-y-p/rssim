from abc import ABC, abstractmethod
from logging import getLogger

from ui import *
from ui.button import create_two_state_button
from ui.button.build_construction_button import BuildConstructionButton
from ui.button.set_money_target_button import SetMoneyTargetButton
from ui.button.reset_money_target_button import ResetMoneyTargetButton
from ui.label.constructor_locked_label import ConstructorLockedLabel
from ui.label.constructor_level_placeholder_label import ConstructorLevelPlaceholderLabel
from ui.label.under_construction_days_label import UnderConstructionDaysLabel
from ui.label.under_construction_hours_minutes_label import UnderConstructionHoursMinutesLabel


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


def unlock_available(fn):
    def _handle_if_unlock_available(*args, **kwargs):
        if len(args[0].data) > 0 and args[0].data[UNLOCK_AVAILABLE]:
            fn(*args, **kwargs)

    return _handle_if_unlock_available


class ConstructorCell(ABC):
    def __init__(
            self, construction_type, row, on_buy_construction_action, on_set_money_target_action,
            on_reset_money_target_action, parent_viewport
    ):
        def on_set_money_target(button):
            button.paired_button.opacity = button.opacity
            button.on_deactivate(instant=True)
            button.paired_button.on_activate()
            self.on_set_money_target_action(self.construction_type, self.row, self.entity_number)

        def on_reset_money_target(button):
            button.paired_button.opacity = button.opacity
            button.on_deactivate(instant=True)
            button.paired_button.on_activate()
            self.on_reset_money_target_action()

        def on_buy_construction(button):
            button.on_deactivate(instant=True)
            self.enable_money_target_button.on_deactivate(instant=True)
            self.disable_money_target_button.on_deactivate(instant=True)
            self.on_buy_construction_action(self.construction_type, self.row, self.entity_number)

        self.logger = getLogger(f'root.app.game.map.constructor.view.cell.{construction_type}.{row}')
        self.is_activated = False
        self.parent_viewport = parent_viewport
        self.viewport = Viewport()
        self.construction_type, self.row = construction_type, row
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.on_buy_construction_action = on_buy_construction_action
        self.on_set_money_target_action = on_set_money_target_action
        self.on_reset_money_target_action = on_reset_money_target_action
        self.entity_number = None
        self.data = []
        self.screen_resolution = (0, 0)
        self.locked_label = ConstructorLockedLabel(parent_viewport=self.viewport)
        self.title_label = None
        self.level_required_label = ConstructorLevelPlaceholderLabel(parent_viewport=self.viewport)
        self.previous_entity_required_label = None
        self.environment_required_label = None
        self.unlock_available_label = None
        self.under_construction_days_label = UnderConstructionDaysLabel(parent_viewport=self.viewport)
        self.under_construction_hours_minutes_label = UnderConstructionHoursMinutesLabel(parent_viewport=self.viewport)
        self.enable_money_target_button, self.disable_money_target_button = create_two_state_button(
            SetMoneyTargetButton(on_click_action=on_set_money_target, parent_viewport=self.viewport),
            ResetMoneyTargetButton(on_click_action=on_reset_money_target, parent_viewport=self.viewport)
        )
        self.build_button = BuildConstructionButton(on_click_action=on_buy_construction, parent_viewport=self.viewport)
        self.buttons = [self.enable_money_target_button, self.disable_money_target_button, self.build_button]
        USER_DB_CURSOR.execute('''SELECT money FROM game_progress''')
        self.money = USER_DB_CURSOR.fetchone()[0]
        self.money_target_activated = False
        self.opacity = 0
        self.on_window_resize_handlers = [
            self.on_window_resize, self.locked_label.on_window_resize, self.level_required_label.on_window_resize,
            self.under_construction_days_label.on_window_resize,
            self.under_construction_hours_minutes_label.on_window_resize
        ]

    @final
    @cell_is_active
    def on_assign_new_data(self, entity_number, data):
        self.entity_number = entity_number
        self.data = data
        # when data is empty, it means no more tracks/tiers are available, only placeholder is active
        if len(self.data) == 0 or self.entity_number == 0:
            self.locked_label.delete()
            self.title_label.delete()
            self.level_required_label.delete()
            self.previous_entity_required_label.delete()
            if self.environment_required_label is not None:
                self.environment_required_label.delete()

            self.unlock_available_label.delete()
            self.under_construction_days_label.delete()
            self.under_construction_hours_minutes_label.delete()
            for b in self.buttons:
                b.on_deactivate()

        else:
            if not self.data[UNLOCK_AVAILABLE] and not self.data[UNDER_CONSTRUCTION]:
                self.locked_label.create()
            else:
                self.locked_label.delete()

            self.title_label.on_update_args((self.entity_number, ))
            self.title_label.create()
            self.unlock_available_label.on_update_args((self.data[PRICE], ))
            self.level_required_label.on_update_args((self.data[LEVEL_REQUIRED], ))
            self.previous_entity_required_label.on_update_args((self.entity_number - 1, ))
            if self.environment_required_label is not None:
                self.environment_required_label.on_update_args((self.data[ENVIRONMENT_REQUIRED], ))

            self.on_update_description_label()
            self.on_update_build_button_state()

    @abstractmethod
    def on_update_description_label(self):
        pass

    @final
    @cell_is_active
    def on_update_state(self):
        self.on_update_description_label()
        # when UNLOCK_AVAILABLE flag becomes enabled, we need to activate build button
        # (or locked label if there is no enough money) and set money target button
        if self.data[UNLOCK_AVAILABLE]:
            self.locked_label.delete()
            self.on_update_build_button_state()
            if not self.money_target_activated and not self.enable_money_target_button.is_activated \
                    and not self.disable_money_target_button.is_activated:
                self.on_deactivate_money_target()

    @final
    def on_update_money(self, money):
        self.money = money
        self.on_update_build_button_state()

    @final
    @cell_is_active
    @unlock_available
    def on_update_build_button_state(self):
        self.build_button.opacity = self.opacity
        if self.money >= self.data[PRICE]:
            self.build_button.on_activate()
        else:
            self.build_button.on_disable()

    @final
    @cell_is_not_active
    def on_activate(self):
        self.is_activated = True

    @final
    @cell_is_active
    def on_deactivate(self):
        self.is_activated = False
        self.data = []
        for b in self.buttons:
            b.on_deactivate()

    @final
    @window_size_has_changed
    def on_window_resize(self, width, height):
        self.screen_resolution = width, height
        bottom_bar_height = get_bottom_bar_height(self.screen_resolution)
        inner_area_rect = get_inner_area_rect(self.screen_resolution)
        self.viewport.x1 \
            = inner_area_rect[0] + self.construction_type * (int(6.875 * bottom_bar_height) + bottom_bar_height // 4)
        self.viewport.x2 = self.viewport.x1 + int(6.875 * bottom_bar_height)
        if self.construction_type == TRACKS:
            self.viewport.y1 = inner_area_rect[1] \
                               + (CONSTRUCTOR_VIEW_TRACK_CELLS - 1 - self.row) \
                               * (bottom_bar_height + bottom_bar_height // 4)
        elif self.construction_type == ENVIRONMENT:
            self.viewport.y1 = inner_area_rect[1] \
                               + (CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS - 1 - self.row) \
                               * (bottom_bar_height + bottom_bar_height // 4)

        self.viewport.y2 = self.viewport.y1 + bottom_bar_height

    @final
    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.title_label.on_update_current_locale(self.current_locale)
        self.level_required_label.on_update_current_locale(self.current_locale)
        self.previous_entity_required_label.on_update_current_locale(self.current_locale)
        if self.environment_required_label is not None:
            self.environment_required_label.on_update_current_locale(self.current_locale)

        self.unlock_available_label.on_update_current_locale(self.current_locale)
        self.under_construction_days_label.on_update_current_locale(self.current_locale)
        self.under_construction_hours_minutes_label.on_update_current_locale(self.current_locale)

    @final
    def on_activate_money_target(self):
        self.money_target_activated = True
        if self.is_activated and len(self.data) > 0:
            self.enable_money_target_button.on_deactivate(instant=True)
            if self.data[UNLOCK_AVAILABLE]:
                self.disable_money_target_button.opacity = self.opacity
                self.disable_money_target_button.on_activate()
            else:
                self.disable_money_target_button.on_deactivate(instant=True)

    @final
    def on_deactivate_money_target(self):
        self.money_target_activated = False
        if self.is_activated and len(self.data) > 0:
            self.disable_money_target_button.on_deactivate(instant=True)
            if self.data[UNLOCK_AVAILABLE]:
                self.enable_money_target_button.opacity = self.opacity
                self.enable_money_target_button.on_activate()
            else:
                self.enable_money_target_button.on_deactivate(instant=True)

    @final
    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.locked_label.on_update_opacity(self.opacity)
        self.title_label.on_update_opacity(self.opacity)
        self.level_required_label.on_update_opacity(self.opacity)
        self.previous_entity_required_label.on_update_opacity(self.opacity)
        if self.environment_required_label is not None:
            self.environment_required_label.on_update_opacity(self.opacity)

        self.unlock_available_label.on_update_opacity(self.opacity)
        self.under_construction_days_label.on_update_opacity(self.opacity)
        self.under_construction_hours_minutes_label.on_update_opacity(self.opacity)
