from logging import getLogger
from typing import final

from database import PRICE, UNLOCK_CONDITION_FROM_PREVIOUS_STAGE, LEVEL_REQUIRED, UNLOCK_CONDITION_FROM_LEVEL, \
    EXP_BONUS, STORAGE_CAPACITY, HOURLY_PROFIT, UNLOCK_AVAILABLE, MINUTES_IN_ONE_HOUR, SECONDS_IN_ONE_MINUTE, \
    CONSTRUCTION_TIME, SECONDS_IN_ONE_HOUR, UNDER_CONSTRUCTION, USER_DB_CURSOR, LOCKED
from ui import get_inner_area_rect, get_bottom_bar_height, window_size_has_changed, Viewport

from ui.button.build_shop_stage_button import BuildShopStageButton
from ui.label.shop_stage_locked_label import ShopStageLockedLabel
from ui.label.shop_stage_level_placeholder_label import ShopStageLevelPlaceholderLabel
from ui.label.shop_stage_previous_stage_placeholder_label import ShopStagePreviousStagePlaceholderLabel
from ui.label.shop_stage_under_construction_label import ShopStageUnderConstructionLabel
from ui.label.shop_stage_price_label import ShopStagePriceLabel
from ui.label.shop_stage_hourly_profit_description_label import ShopStageHourlyProfitDescriptionLabel
from ui.label.shop_stage_exp_bonus_description_label import ShopStageExpBonusDescriptionLabel
from ui.label.shop_stage_storage_capacity_description_label import ShopStageStorageCapacityDescriptionLabel
from ui.label.shop_stage_exp_bonus_value_label import ShopStageExpBonusValueLabel
from ui.label.shop_stage_hourly_profit_value_label import ShopStageHourlyProfitValueLabel
from ui.label.shop_stage_storage_capacity_value_label import ShopStageStorageCapacityValueLabel


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


@final
class ShopStageCell:
    def __init__(self, stage_number, on_buy_stage_action, parent_viewport):
        def on_buy_shop_stage(button):
            button.on_deactivate(instant=True)
            self.on_buy_stage_action(self.stage_number)

        self.logger = getLogger(f'root.app.game.map.shop.view.cell.{stage_number}')
        self.is_activated = False
        self.stage_number = stage_number
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.on_buy_stage_action = on_buy_stage_action
        self.data = []
        self.screen_resolution = (0, 0)
        self.parent_viewport = parent_viewport
        self.viewport = Viewport()
        self.locked_label = ShopStageLockedLabel(parent_viewport=self.viewport)
        self.level_placeholder_label = ShopStageLevelPlaceholderLabel(parent_viewport=self.viewport)
        self.previous_stage_placeholder_label = ShopStagePreviousStagePlaceholderLabel(parent_viewport=self.viewport)
        self.hourly_profit_description_label = ShopStageHourlyProfitDescriptionLabel(parent_viewport=self.viewport)
        self.hourly_profit_value_label = ShopStageHourlyProfitValueLabel(parent_viewport=self.viewport)
        self.storage_capacity_description_label = ShopStageStorageCapacityDescriptionLabel(
            parent_viewport=self.viewport
        )
        self.storage_capacity_value_label = ShopStageStorageCapacityValueLabel(parent_viewport=self.viewport)
        self.exp_bonus_description_label = ShopStageExpBonusDescriptionLabel(parent_viewport=self.viewport)
        self.exp_bonus_value_label = ShopStageExpBonusValueLabel(parent_viewport=self.viewport)
        self.price_label = ShopStagePriceLabel(parent_viewport=self.viewport)
        self.under_construction_label = ShopStageUnderConstructionLabel(parent_viewport=self.viewport)
        self.build_button = BuildShopStageButton(on_click_action=on_buy_shop_stage, parent_viewport=self.viewport)
        self.buttons = [self.build_button, ]
        USER_DB_CURSOR.execute('''SELECT money FROM game_progress''')
        self.money = USER_DB_CURSOR.fetchone()[0]
        self.opacity = 0
        self.on_window_resize_handlers = [
            self.on_window_resize, self.locked_label.on_window_resize, self.level_placeholder_label.on_window_resize,
            self.previous_stage_placeholder_label.on_window_resize,
            self.hourly_profit_description_label.on_window_resize,
            self.hourly_profit_value_label.on_window_resize, self.storage_capacity_description_label.on_window_resize,
            self.storage_capacity_value_label.on_window_resize, self.exp_bonus_description_label.on_window_resize,
            self.exp_bonus_value_label.on_window_resize, self.price_label.on_window_resize,
            self.under_construction_label.on_window_resize
        ]

    @cell_is_active
    def on_update_state(self):
        if self.data[UNDER_CONSTRUCTION]:
            self.locked_label.delete()
            self.level_placeholder_label.delete()
            self.previous_stage_placeholder_label.delete()
            self.under_construction_label.on_update_args(
                (
                    self.data[CONSTRUCTION_TIME] // SECONDS_IN_ONE_HOUR,
                    (self.data[CONSTRUCTION_TIME] // SECONDS_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR
                )
            )
            self.under_construction_label.create()
            self.hourly_profit_description_label.delete()
            self.hourly_profit_value_label.delete()
            self.storage_capacity_description_label.delete()
            self.storage_capacity_value_label.delete()
            self.exp_bonus_description_label.delete()
            self.exp_bonus_value_label.delete()
            self.price_label.delete()
        elif self.data[UNLOCK_AVAILABLE]:
            self.locked_label.delete()
            self.level_placeholder_label.delete()
            self.previous_stage_placeholder_label.delete()
            self.under_construction_label.delete()
            self.hourly_profit_description_label.create()
            self.hourly_profit_value_label.on_update_args((self.data[HOURLY_PROFIT], ))
            self.hourly_profit_value_label.create()
            self.storage_capacity_description_label.create()
            self.storage_capacity_value_label.on_update_args((self.data[STORAGE_CAPACITY], ))
            self.storage_capacity_value_label.create()
            self.exp_bonus_description_label.create()
            self.exp_bonus_value_label.on_update_args((self.data[EXP_BONUS], ))
            self.exp_bonus_value_label.create()
            self.price_label.on_update_args((self.data[PRICE], ))
            self.price_label.create()
            self.on_update_build_button_state()
        elif self.data[LOCKED]:
            self.locked_label.create()
            if not self.data[UNLOCK_CONDITION_FROM_LEVEL]:
                self.previous_stage_placeholder_label.delete()
                self.level_placeholder_label.on_update_args((self.data[LEVEL_REQUIRED], ))
                self.level_placeholder_label.create()
            elif not self.data[UNLOCK_CONDITION_FROM_PREVIOUS_STAGE]:
                self.level_placeholder_label.delete()
                self.previous_stage_placeholder_label.on_update_args((self.stage_number - 1, ))
                self.previous_stage_placeholder_label.create()

            self.under_construction_label.delete()
            self.hourly_profit_description_label.delete()
            self.hourly_profit_value_label.delete()
            self.storage_capacity_description_label.delete()
            self.storage_capacity_value_label.delete()
            self.exp_bonus_description_label.delete()
            self.exp_bonus_value_label.delete()
            self.price_label.delete()
        else:
            self.locked_label.delete()
            self.level_placeholder_label.delete()
            self.previous_stage_placeholder_label.delete()
            self.under_construction_label.delete()
            self.hourly_profit_description_label.delete()
            self.hourly_profit_value_label.delete()
            self.storage_capacity_description_label.delete()
            self.storage_capacity_value_label.delete()
            self.exp_bonus_description_label.delete()
            self.exp_bonus_value_label.delete()
            self.price_label.delete()

    def on_update_money(self, money):
        self.money = money
        self.on_update_build_button_state()

    @cell_is_active
    @unlock_available
    def on_update_build_button_state(self):
        self.build_button.opacity = self.opacity
        if self.money >= self.data[PRICE]:
            self.build_button.on_activate()
        else:
            self.build_button.on_disable()

    @cell_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.on_update_build_button_state()

    @cell_is_active
    def on_deactivate(self):
        self.is_activated = False
        for b in self.buttons:
            b.on_deactivate()

    @window_size_has_changed
    def on_window_resize(self, width, height):
        self.screen_resolution = width, height
        bottom_bar_height = get_bottom_bar_height(self.screen_resolution)
        general_cells_width = get_inner_area_rect(self.screen_resolution)[2] - bottom_bar_height // 4
        self.viewport.x1 \
            = self.parent_viewport.x1 + bottom_bar_height // 8 + general_cells_width // 160 \
            + int((self.stage_number - 1) / 4 * (general_cells_width - general_cells_width // 80))
        self.viewport.y1 = self.parent_viewport.y1 + bottom_bar_height // 8
        self.viewport.x2 = self.viewport.x1 + (general_cells_width - general_cells_width // 80) // 4
        self.viewport.y2 = self.viewport.y1 + 3 * bottom_bar_height - bottom_bar_height // 8

    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.level_placeholder_label.on_update_current_locale(self.current_locale)
        self.previous_stage_placeholder_label.on_update_current_locale(self.current_locale)
        self.under_construction_label.on_update_current_locale(self.current_locale)
        self.hourly_profit_description_label.on_update_current_locale(self.current_locale)
        self.storage_capacity_description_label.on_update_current_locale(self.current_locale)
        self.exp_bonus_description_label.on_update_current_locale(self.current_locale)
        self.exp_bonus_value_label.on_update_current_locale(self.current_locale)

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.locked_label.on_update_opacity(self.opacity)
        self.level_placeholder_label.on_update_opacity(self.opacity)
        self.previous_stage_placeholder_label.on_update_opacity(self.opacity)
        self.under_construction_label.on_update_opacity(self.opacity)
        self.hourly_profit_description_label.on_update_opacity(self.opacity)
        self.hourly_profit_value_label.on_update_opacity(self.opacity)
        self.storage_capacity_description_label.on_update_opacity(self.opacity)
        self.storage_capacity_value_label.on_update_opacity(self.opacity)
        self.exp_bonus_description_label.on_update_opacity(self.opacity)
        self.exp_bonus_value_label.on_update_opacity(self.opacity)
        self.price_label.on_update_opacity(self.opacity)
