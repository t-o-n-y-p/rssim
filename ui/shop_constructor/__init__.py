from logging import getLogger

from database import USER_DB_CURSOR
from ui import *
from ui.button.build_shop_stage_button import BuildShopStageButton
from ui.label.shop_stage_locked_label import ShopStageLockedLabel
from ui.label.shop_stage_level_placeholder_label import ShopStageLevelPlaceholderLabel
from ui.label.shop_stage_previous_stage_placeholder_label import ShopStagePreviousStagePlaceholderLabel
from ui.label.shop_stage_under_construction_label import ShopStageUnderConstructionLabel
from ui.label.shop_stage_price_label import ShopStagePriceLabel


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


class ShopStageCell:
    def __init__(self, stage_number, on_buy_stage_action, parent_viewport):
        def on_buy_shop_stage(button):
            button.on_deactivate(instant=True)
            self.on_buy_stage_action(self.stage_number)

        self.logger = getLogger(f'root.app.game.map.shop.view.cell.{stage_number}')
        self.is_activated = False
        self.stage_number = stage_number
        self.surface, self.batches, self.groups = SURFACE, BATCHES, GROUPS
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
        self.hourly_profit_description_label = None
        self.hourly_profit_value_label = None
        self.storage_capacity_description_label = None
        self.storage_capacity_value_label = None
        self.exp_bonus_description_label = None
        self.exp_bonus_value_label = None
        self.price_label = ShopStagePriceLabel(parent_viewport=self.viewport)
        self.under_construction_label = ShopStageUnderConstructionLabel(parent_viewport=self.viewport)
        self.build_button = BuildShopStageButton(on_click_action=on_buy_shop_stage)
        self.buttons = [self.build_button, ]
        self.money = 0
        self.opacity = 0

    @cell_is_active
    def on_update_state(self):
        if self.data[UNDER_CONSTRUCTION]:
            self.locked_label.delete()
            self.level_placeholder_label.delete()
            self.previous_stage_placeholder_label.delete()
            self.under_construction_label.on_update_args((self.data[CONSTRUCTION_TIME] // FRAMES_IN_ONE_HOUR,
                                                          (self.data[CONSTRUCTION_TIME] // FRAMES_IN_ONE_MINUTE)
                                                          % MINUTES_IN_ONE_HOUR))
            self.under_construction_label.create()
            # self.hourly_profit_description_label.delete()
            # self.hourly_profit_value_label.delete()
            # self.storage_capacity_description_label.delete()
            # self.storage_capacity_value_label.delete()
            # self.exp_bonus_description_label.delete()
            # self.exp_bonus_value_label.delete()
            self.price_label.delete()
        elif self.data[UNLOCK_AVAILABLE]:
            self.locked_label.delete()
            self.level_placeholder_label.delete()
            self.previous_stage_placeholder_label.delete()
            self.under_construction_label.delete()
            # self.hourly_profit_description_label.create()
            # self.hourly_profit_value_label.on_update_args((self.data[HOURLY_PROFIT], ))
            # self.hourly_profit_value_label.create()
            # self.storage_capacity_description_label.create()
            # self.storage_capacity_value_label.on_update_args((self.data[STORAGE_CAPACITY], ))
            # self.storage_capacity_value_label.create()
            # self.exp_bonus_description_label.create()
            # self.exp_bonus_value_label.on_update_args((self.data[EXP_BONUS], ))
            # self.exp_bonus_value_label.create()
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
            # self.hourly_profit_description_label.delete()
            # self.hourly_profit_value_label.delete()
            # self.storage_capacity_description_label.delete()
            # self.storage_capacity_value_label.delete()
            # self.exp_bonus_description_label.delete()
            # self.exp_bonus_value_label.delete()
            self.price_label.delete()
        else:
            self.locked_label.delete()
            self.level_placeholder_label.delete()
            self.previous_stage_placeholder_label.delete()
            self.under_construction_label.delete()
            # self.hourly_profit_description_label.delete()
            # self.hourly_profit_value_label.delete()
            # self.storage_capacity_description_label.delete()
            # self.storage_capacity_value_label.delete()
            # self.exp_bonus_description_label.delete()
            # self.exp_bonus_value_label.delete()
            self.price_label.delete()

    def on_update_money(self, money):
        """
        Updates cell state based on available money.

        :param money:                   amount of money the player can operate
        """
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
        """
        Activates the cell.
        """
        self.is_activated = True

    @cell_is_active
    def on_deactivate(self):
        """
        Deactivates the cell and all buttons, clears the data.
        """
        self.is_activated = False
        self.data = []
        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        bottom_bar_height = get_bottom_bar_height(self.screen_resolution)
        general_cells_width = get_inner_area_rect(screen_resolution)[2] - bottom_bar_height // 4
        self.viewport.x1 = self.parent_viewport.x1 + bottom_bar_height // 8 + general_cells_width // 160 \
                           + int((self.stage_number - 1) / 4 * (general_cells_width - general_cells_width // 80))
        self.viewport.y1 = self.parent_viewport.y1 + bottom_bar_height // 8
        self.viewport.x2 = self.viewport.x1 + (general_cells_width - general_cells_width // 80) // 4
        self.viewport.y2 = self.parent_viewport.y1 + 3 * bottom_bar_height - bottom_bar_height // 8
        self.locked_label.on_change_screen_resolution(self.screen_resolution)
        self.level_placeholder_label.on_change_screen_resolution(self.screen_resolution)
        self.previous_stage_placeholder_label.on_change_screen_resolution(self.screen_resolution)
        self.under_construction_label.on_change_screen_resolution(self.screen_resolution)
        # self.hourly_profit_description_label.on_change_screen_resolution(self.screen_resolution)
        # self.hourly_profit_value_label.on_change_screen_resolution(self.screen_resolution)
        # self.storage_capacity_description_label.on_change_screen_resolution(self.screen_resolution)
        # self.storage_capacity_value_label.on_change_screen_resolution(self.screen_resolution)
        # self.exp_bonus_description_label.on_change_screen_resolution(self.screen_resolution)
        # self.exp_bonus_value_label.on_change_screen_resolution(self.screen_resolution)
        self.price_label.on_change_screen_resolution(self.screen_resolution)
        self.build_button.on_size_changed((get_top_bar_height(self.screen_resolution),
                                           get_top_bar_height(self.screen_resolution)))
        self.build_button.x_margin = self.viewport.x1 + 5 * get_top_bar_height(self.screen_resolution)
        self.build_button.y_margin = self.viewport.y1 + 5 * get_top_bar_height(self.screen_resolution) // 4

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        self.level_placeholder_label.on_update_current_locale(self.current_locale)
        self.previous_stage_placeholder_label.on_update_current_locale(self.current_locale)
        self.under_construction_label.on_update_current_locale(self.current_locale)
        # self.hourly_profit_description_label.on_update_current_locale(self.current_locale)
        # self.storage_capacity_description_label.on_update_current_locale(self.current_locale)
        # self.exp_bonus_description_label.on_update_current_locale(self.current_locale)
        # self.exp_bonus_value_label.on_update_current_locale(self.current_locale)

    def on_update_opacity(self, new_opacity):
        """
        Updates cell opacity with given value.

        :param new_opacity:                     new opacity value
        """
        self.opacity = new_opacity
        self.on_update_sprite_opacity()

    def on_update_sprite_opacity(self):
        """
        Applies new opacity value to all sprites and labels.
        """
        if self.opacity <= 0:
            self.locked_label.delete()
            self.level_placeholder_label.delete()
            self.previous_stage_placeholder_label.delete()
            self.under_construction_label.delete()
            # self.hourly_profit_description_label.delete()
            # self.hourly_profit_value_label.delete()
            # self.storage_capacity_description_label.delete()
            # self.storage_capacity_value_label.delete()
            # self.exp_bonus_description_label.delete()
            # self.exp_bonus_value_label.delete()
            self.price_label.delete()
        else:
            self.locked_label.on_update_opacity(self.opacity)
            self.level_placeholder_label.on_update_opacity(self.opacity)
            self.previous_stage_placeholder_label.on_update_opacity(self.opacity)
            self.under_construction_label.on_update_opacity(self.opacity)
            # self.hourly_profit_description_label.on_update_opacity(self.opacity)
            # self.hourly_profit_value_label.on_update_opacity(self.opacity)
            # self.storage_capacity_description_label.on_update_opacity(self.opacity)
            # self.storage_capacity_value_label.on_update_opacity(self.opacity)
            # self.exp_bonus_description_label.on_update_opacity(self.opacity)
            # self.exp_bonus_value_label.on_update_opacity(self.opacity)
            self.price_label.on_update_opacity(self.opacity)
