from logging import getLogger

from ui import *
from database import USER_DB_CURSOR
from ui.label.bonus_title_label import BonusTitleLabel
from ui.label.activations_title_label import ActivationsTitleLabel
from ui.label.bonus_info_cell_exp_bonus_value_label import BonusInfoCellExpBonusValueLabel
from ui.label.bonus_info_cell_money_bonus_value_label import BonusInfoCellMoneyBonusValueLabel
from ui.label.bonus_info_cell_construction_time_bonus_value_label import BonusInfoCellConstructionTimeBonusValueLabel
from ui.label.activations_value_label import ActivationsValueLabel


def info_cell_is_active(fn):
    def _handle_if_info_cell_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_info_cell_is_activated


def info_cell_is_not_active(fn):
    def _handle_if_info_cell_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_info_cell_is_not_activated


@final
class BonusCodeInfoCell:
    def __init__(self, parent_viewport):
        self.logger = getLogger(f'root.app.bonus_code.view.bonus_code_info_cell')
        self.parent_viewport = parent_viewport
        self.viewport = Viewport()
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.bonus_type = None
        self.bonus_value = None
        self.activations_left = None
        self.bonus_title_label = BonusTitleLabel(parent_viewport=self.viewport)
        self.exp_bonus_value_label = BonusInfoCellExpBonusValueLabel(parent_viewport=self.viewport)
        self.money_bonus_value_label = BonusInfoCellMoneyBonusValueLabel(parent_viewport=self.viewport)
        self.construction_time_bonus_value_label = BonusInfoCellConstructionTimeBonusValueLabel(
            parent_viewport=self.viewport
        )
        self.activations_title_label = ActivationsTitleLabel(parent_viewport=self.viewport)
        self.activations_value_label = ActivationsValueLabel(parent_viewport=self.viewport)
        self.on_window_resize_handlers = [
            self.on_window_resize, self.bonus_title_label.on_window_resize, self.exp_bonus_value_label.on_window_resize,
            self.money_bonus_value_label.on_window_resize, self.construction_time_bonus_value_label.on_window_resize,
            self.activations_title_label.on_window_resize, self.activations_value_label.on_window_resize
        ]
        self.screen_resolution = (0, 0)
        self.is_activated = False
        self.opacity = 0

    def on_activate(self):
        self.is_activated = True

    @info_cell_is_active
    def on_deactivate(self, instant=False):
        self.is_activated = False
        self.bonus_type = None
        self.bonus_value = None
        self.activations_left = None
        if instant:
            self.opacity = 0
            self.bonus_title_label.delete()
            self.exp_bonus_value_label.delete()
            self.money_bonus_value_label.delete()
            self.construction_time_bonus_value_label.delete()
            self.activations_title_label.delete()
            self.activations_value_label.delete()

    @info_cell_is_active
    def on_assign_data(self, bonus_type, bonus_value, activations_left):
        self.bonus_type = bonus_type
        self.bonus_value = bonus_value
        self.activations_left = activations_left
        self.bonus_title_label.create()
        if self.bonus_type == 'exp_bonus':
            self.exp_bonus_value_label.on_update_args((round(self.bonus_value * 100), ))
            self.exp_bonus_value_label.create()
        elif self.bonus_type == 'money_bonus':
            self.money_bonus_value_label.on_update_args((round(self.bonus_value * 100), ))
            self.money_bonus_value_label.create()
        elif self.bonus_type == 'construction_time_bonus':
            self.construction_time_bonus_value_label.on_update_args((round(self.bonus_value * 100), ))
            self.construction_time_bonus_value_label.create()

        self.activations_title_label.create()
        self.activations_value_label.on_update_args((self.activations_left, ))
        self.activations_value_label.create()

    @window_size_has_changed
    def on_window_resize(self, width, height):
        self.screen_resolution = width, height
        self.viewport.x1 \
            = (self.parent_viewport.x1 + self.parent_viewport.x2) // 2 - 5 * get_top_bar_height(self.screen_resolution)
        self.viewport.x2 \
            = (self.parent_viewport.x1 + self.parent_viewport.x2) // 2 + 5 * get_top_bar_height(self.screen_resolution)
        self.viewport.y1 \
            = (
                      self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution)
                      + self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution)
            ) // 2 - 5 * get_bottom_bar_height(self.screen_resolution) // 8 \
            - get_bottom_bar_height(self.screen_resolution) // 2
        self.viewport.y2 \
            = (
                      self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution)
                      + self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution)
            ) // 2 - 5 * get_bottom_bar_height(self.screen_resolution) // 8 \
            + get_bottom_bar_height(self.screen_resolution) // 2

    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.bonus_title_label.on_update_current_locale(self.current_locale)
        self.exp_bonus_value_label.on_update_current_locale(self.current_locale)
        self.money_bonus_value_label.on_update_current_locale(self.current_locale)
        self.construction_time_bonus_value_label.on_update_current_locale(self.current_locale)
        self.activations_title_label.on_update_current_locale(self.current_locale)

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.bonus_title_label.on_update_opacity(self.opacity)
        self.exp_bonus_value_label.on_update_opacity(self.opacity)
        self.money_bonus_value_label.on_update_opacity(self.opacity)
        self.construction_time_bonus_value_label.on_update_opacity(self.opacity)
        self.activations_title_label.on_update_opacity(self.opacity)
        self.activations_value_label.on_update_opacity(self.opacity)
