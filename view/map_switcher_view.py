from logging import getLogger

from view import *
from ui.button.close_map_switcher_button import CloseMapSwitcherButton
from ui.label.map_switcher_title_label import MapSwitcherTitleLabel
from ui.shader_sprite.map_switcher_view_shader_sprite import MapSwitcherViewShaderSprite
from ui.map_switcher_cell.passenger_map_switcher_cell import PassengerMapSwitcherCell
from ui.map_switcher_cell.freight_map_switcher_cell import FreightMapSwitcherCell
from database import MAP_SWITCHER_STATE_MATRIX, MAP_PRICE, MAP_LOCKED, MAP_LEVEL_REQUIRED
from notifications.map_unlocked_notification import MapUnlockedNotification
from i18n import I18N_RESOURCES


@final
class MapSwitcherView(GameBaseView):
    def __init__(self, controller):
        def on_close_map_switcher(button):
            self.controller.parent_controller.on_close_map_switcher()

        def on_buy_map(map_id):
            self.controller.parent_controller.on_pay_money(MAP_SWITCHER_STATE_MATRIX[map_id][MAP_PRICE])
            self.controller.parent_controller.on_unlock_map(map_id)
            self.controller.parent_controller.on_switch_map(map_id)

        def on_switch_map(map_id):
            self.controller.parent_controller.on_switch_map(map_id)

        super().__init__(controller, logger=getLogger(f'root.app.game.map_switcher.view'), child_window=True)
        self.shader_sprite = MapSwitcherViewShaderSprite(view=self)
        self.title_label = MapSwitcherTitleLabel(parent_viewport=self.viewport)
        self.close_map_switcher_button = CloseMapSwitcherButton(on_click_action=on_close_map_switcher,
                                                                parent_viewport=self.viewport)
        self.map_switcher_cells = [PassengerMapSwitcherCell(on_buy_map, on_switch_map, None, None,
                                                            parent_viewport=self.viewport),
                                   FreightMapSwitcherCell(on_buy_map, on_switch_map, None, None,
                                                          parent_viewport=self.viewport)]
        self.buttons = [self.close_map_switcher_button, ]
        for c in self.map_switcher_cells:
            self.buttons.extend(c.buttons)
            self.on_window_resize_handlers.extend(c.on_window_resize_handlers)

        self.on_window_resize_handlers.extend([
            self.shader_sprite.on_window_resize, self.title_label.on_window_resize
        ])
        self.on_append_window_handlers()

    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        self.shader_sprite.create()
        self.title_label.create()
        for c in self.map_switcher_cells:
            c.on_activate()

    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()
        for c in self.map_switcher_cells:
            c.on_deactivate()

    @view_is_active
    def on_update(self):
        pass

    def on_update_current_locale(self, new_locale):
        super().on_update_current_locale(new_locale)
        self.title_label.on_update_current_locale(self.current_locale)
        for c in self.map_switcher_cells:
            c.on_update_current_locale(self.current_locale)

    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.shader_sprite.on_update_opacity(self.opacity)
        self.title_label.on_update_opacity(self.opacity)
        for c in self.map_switcher_cells:
            c.on_update_opacity(self.opacity)

    def on_level_up(self):
        super().on_level_up()
        for m in range(len(MAP_SWITCHER_STATE_MATRIX)):
            if self.level == MAP_SWITCHER_STATE_MATRIX[m][MAP_LEVEL_REQUIRED]:
                self.on_send_map_unlocked_notification(m)

        for c in self.map_switcher_cells:
            c.on_level_up()

    def on_update_money(self, money):
        super().on_update_money(money)
        for c in self.map_switcher_cells:
            c.on_update_money(self.money)

    @staticmethod
    def on_unlock_map(map_id):
        MAP_SWITCHER_STATE_MATRIX[map_id][MAP_LOCKED] = False

    @notifications_available
    @feature_unlocked_notification_enabled
    def on_send_map_unlocked_notification(self, map_id):
        map_unlocked_notification = MapUnlockedNotification()
        map_unlocked_notification.send(self.current_locale,
                                       message_args=(I18N_RESOURCES['map_title_string'][self.current_locale][map_id], ))
        self.controller.parent_controller.parent_controller\
            .on_append_notification(map_unlocked_notification)
