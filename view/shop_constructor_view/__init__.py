from logging import getLogger

from view import *
from ui.button.clear_shop_storage_button import ClearShopStorageButton
from ui.rectangle_progress_bar.shop_storage_progress_bar import ShopStorageProgressBar
from ui.shop_constructor import ShopStageCell
from ui.label.current_hourly_profit_description_label import CurrentHourlyProfitDescriptionLabel
from ui.label.current_exp_bonus_description_label import CurrentExpBonusDescriptionLabel
from ui.label.current_hourly_profit_value_label import CurrentHourlyProfitValueLabel
from ui.label.current_exp_bonus_value_label import CurrentExpBonusValueLabel
from ui.shader_sprite.shop_constructor_view_shader_sprite import ShopConstructorViewShaderSprite
from notifications.shop_storage_almost_full_notification import ShopStorageAlmostFullNotification
from notifications.shop_storage_full_notification import ShopStorageFullNotification


class ShopConstructorView(View):
    def __init__(self, map_id, shop_id):
        def on_clear_storage(button):
            self.controller.on_clear_storage()

        def on_buy_stage_action(stage_number):
            self.controller.on_put_stage_under_construction(stage_number)

        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.constructor.view'))
        self.map_id = map_id
        self.shop_id = shop_id
        self.shop_stages_state_matrix = {}
        USER_DB_CURSOR.execute('''SELECT current_stage, shop_storage_money
                                  FROM shops WHERE map_id = ? AND shop_id = ?''', (self.map_id, self.shop_id))
        self.current_stage, self.shop_storage_money = USER_DB_CURSOR.fetchone()
        USER_DB_CURSOR.execute('''SELECT shop_storage_notification_enabled FROM notification_settings''')
        self.shop_storage_notification_enabled = bool(USER_DB_CURSOR.fetchone()[0])
        self.shop_stages_cells_position = (0, 0)
        self.shop_stages_cells_size = (0, 0)
        USER_DB_CURSOR.execute('''SELECT last_known_shop_window_position FROM graphics''')
        self.last_known_shop_window_position = tuple(map(int, USER_DB_CURSOR.fetchone()[0].split(',')))
        self.shader_sprite = ShopConstructorViewShaderSprite(view=self)
        self.current_hourly_profit_label = CurrentHourlyProfitDescriptionLabel(parent_viewport=self.viewport)
        self.current_exp_bonus_label = CurrentExpBonusDescriptionLabel(parent_viewport=self.viewport)
        self.hourly_profit_value_label = CurrentHourlyProfitValueLabel(parent_viewport=self.viewport)
        self.exp_bonus_value_label = CurrentExpBonusValueLabel(parent_viewport=self.viewport)
        self.shop_storage_progress_bar = ShopStorageProgressBar(parent_viewport=self.viewport)
        self.clear_shop_storage_button = ClearShopStorageButton(on_click_action=on_clear_storage,
                                                                parent_viewport=self.viewport)
        self.buttons = [self.clear_shop_storage_button, ]
        self.shop_stage_cells = {}
        for i in range(1, 5):
            self.shop_stage_cells[i] = ShopStageCell(stage_number=i, on_buy_stage_action=on_buy_stage_action,
                                                     parent_viewport=self.viewport)
            self.buttons.append(self.shop_stage_cells[i].build_button)

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        self.shader_sprite.create()
        self.current_hourly_profit_label.create()
        self.current_exp_bonus_label.create()
        if self.current_stage == 0:
            self.hourly_profit_value_label.on_update_args((0, ))
        else:
            self.hourly_profit_value_label\
                .on_update_args((self.shop_stages_state_matrix[self.current_stage][HOURLY_PROFIT], ))

        self.hourly_profit_value_label.create()
        if self.current_stage == 0:
            self.exp_bonus_value_label.on_update_args((0.0, ))
        else:
            self.exp_bonus_value_label.on_update_args((self.shop_stages_state_matrix[self.current_stage][EXP_BONUS],))

        self.exp_bonus_value_label.create()
        self.shop_storage_progress_bar.on_activate()
        for stage_cell in self.shop_stage_cells:
            self.shop_stage_cells[stage_cell].on_activate()

    @final
    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()
        self.shop_storage_progress_bar.on_deactivate()
        for stage_cell in self.shop_stage_cells:
            self.shop_stage_cells[stage_cell].on_deactivate()

    @final
    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.viewport.x1 = get_inner_area_rect(self.screen_resolution)[0]
        self.viewport.y1 = get_inner_area_rect(self.screen_resolution)[1]
        self.viewport.x2 = self.viewport.x1 + get_inner_area_rect(self.screen_resolution)[2]
        self.viewport.y2 = self.viewport.y1 + get_inner_area_rect(self.screen_resolution)[3]
        self.current_hourly_profit_label.on_change_screen_resolution(self.screen_resolution)
        self.current_exp_bonus_label.on_change_screen_resolution(self.screen_resolution)
        self.hourly_profit_value_label.on_change_screen_resolution(self.screen_resolution)
        self.exp_bonus_value_label.on_change_screen_resolution(self.screen_resolution)
        self.shader_sprite.on_change_screen_resolution(self.screen_resolution)
        self.shop_stages_cells_position = (self.viewport.x1 + get_top_bar_height(self.screen_resolution) // 4,
                                           self.viewport.y1 + get_top_bar_height(self.screen_resolution) // 4)
        self.shop_stages_cells_size = ((self.viewport.x2 - self.viewport.x1)
                                       - get_top_bar_height(self.screen_resolution) // 2,
                                       3 * get_bottom_bar_height(self.screen_resolution)
                                       - get_bottom_bar_height(self.screen_resolution) // 8)
        self.shop_storage_progress_bar.on_change_screen_resolution(self.screen_resolution)
        for stage_cell in self.shop_stage_cells:
            self.shop_stage_cells[stage_cell].on_change_screen_resolution(self.screen_resolution)

        for b in self.buttons:
            b.on_change_screen_resolution(self.screen_resolution)

    @final
    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.shop_storage_progress_bar.on_update_opacity(self.opacity)
        for stage_cell in self.shop_stage_cells:
            self.shop_stage_cells[stage_cell].on_update_opacity(self.opacity)

        self.shader_sprite.on_update_opacity(self.opacity)
        self.current_hourly_profit_label.on_update_opacity(self.opacity)
        self.current_exp_bonus_label.on_update_opacity(self.opacity)
        self.hourly_profit_value_label.on_update_opacity(self.opacity)
        self.exp_bonus_value_label.on_update_opacity(self.opacity)
        for b in self.buttons:
            b.on_update_opacity(self.opacity)

    @final
    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.current_hourly_profit_label.on_update_current_locale(self.current_locale)
        self.current_exp_bonus_label.on_update_current_locale(self.current_locale)
        self.exp_bonus_value_label.on_update_current_locale(self.current_locale)
        for stage_cell in self.shop_stage_cells:
            self.shop_stage_cells[stage_cell].on_update_current_locale(self.current_locale)

    @final
    def on_apply_shaders_and_draw_vertices(self):
        self.shader_sprite.draw()

    @final
    def on_update_stage_state(self, stage_number):
        self.shop_stage_cells[stage_number].on_update_state()

    @final
    @view_is_active
    def on_update_storage_money(self, storage_money):
        self.shop_storage_money = storage_money
        if self.shop_storage_money > 0:
            self.clear_shop_storage_button.on_activate()
        else:
            self.clear_shop_storage_button.on_disable()

        self.shop_storage_progress_bar.on_update_text_label_args((storage_money, ))
        if self.current_stage > 0:
            self.shop_storage_progress_bar\
                .on_update_progress_bar_state(storage_money,
                                              self.shop_stages_state_matrix[self.current_stage][STORAGE_CAPACITY])
        else:
            self.shop_storage_progress_bar.on_update_progress_bar_state(storage_money, 0)

    @final
    def on_update_money(self, money):
        for stage_cell in self.shop_stage_cells:
            self.shop_stage_cells[stage_cell].on_update_money(money)

    @final
    def on_unlock_stage(self, stage):
        self.current_stage = stage
        self.hourly_profit_value_label\
            .on_update_args((self.shop_stages_state_matrix[self.current_stage][HOURLY_PROFIT],))
        self.exp_bonus_value_label.on_update_args((self.shop_stages_state_matrix[self.current_stage][EXP_BONUS],))
        self.shop_storage_progress_bar \
            .on_update_progress_bar_state(self.shop_storage_money,
                                          self.shop_stages_state_matrix[self.current_stage][STORAGE_CAPACITY])

    @final
    def on_change_shop_storage_notification_state(self, notification_state):
        self.shop_storage_notification_enabled = notification_state

    @final
    @notifications_available
    @shop_storage_notification_enabled
    def on_send_shop_storage_almost_full_notification(self):
        shop_storage_almost_full_notification = ShopStorageAlmostFullNotification()
        shop_storage_almost_full_notification.send(self.current_locale, message_args=(self.shop_id + 1, ))
        self.controller.parent_controller.parent_controller.parent_controller.parent_controller\
            .on_append_notification(shop_storage_almost_full_notification)

    @final
    @notifications_available
    @shop_storage_notification_enabled
    def on_send_shop_storage_full_notification(self):
        shop_storage_full_notification = ShopStorageFullNotification()
        shop_storage_full_notification.send(self.current_locale, message_args=(self.shop_id + 1, ))
        self.controller.parent_controller.parent_controller.parent_controller.parent_controller\
            .on_append_notification(shop_storage_full_notification)
