from logging import getLogger
from typing import final

from ui.label.money_bonus_value_percent_label import MoneyBonusValuePercentLabel
from ui.label.exp_bonus_value_percent_label import ExpBonusValuePercentLabel
from ui.label.exp_bonus_placeholder_label import ExpBonusPlaceholderLabel
from ui.label.money_bonus_placeholder_label import MoneyBonusPlaceholderLabel
from notifications.exp_bonus_expired_notification import ExpBonusExpiredNotification
from notifications.money_bonus_expired_notification import MoneyBonusExpiredNotification
from notifications.construction_time_bonus_expired_notification import ConstructionTimeBonusExpiredNotification
from view import bonus_expired_notification_enabled, game_progress_notifications_available, GameBaseView, \
    view_is_not_active, view_is_active


@final
class BonusCodeManagerView(GameBaseView):
    def __init__(self, controller):
        super().__init__(controller, logger=getLogger('root.app.game.bonus_code_manager.view'))
        self.exp_bonus_percent_label = ExpBonusValuePercentLabel(parent_viewport=self.viewport)
        self.money_bonus_percent_label = MoneyBonusValuePercentLabel(parent_viewport=self.viewport)
        self.exp_bonus_placeholder_label = ExpBonusPlaceholderLabel(parent_viewport=self.viewport)
        self.money_bonus_placeholder_label = MoneyBonusPlaceholderLabel(parent_viewport=self.viewport)
        self.on_window_resize_handlers.extend(
            [
                self.exp_bonus_percent_label.on_window_resize, self.money_bonus_percent_label.on_window_resize,
                self.exp_bonus_placeholder_label.on_window_resize, self.money_bonus_placeholder_label.on_window_resize
            ]
        )
        self.on_append_window_handlers()

    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        if self.exp_bonus_multiplier > 1.0:
            self.exp_bonus_placeholder_label.delete()
            self.exp_bonus_percent_label.on_update_args((round(self.exp_bonus_multiplier * 100 - 100), ))
            self.exp_bonus_percent_label.create()
        else:
            self.exp_bonus_percent_label.delete()
            self.exp_bonus_placeholder_label.create()

        if self.money_bonus_multiplier > 1.0:
            self.money_bonus_placeholder_label.delete()
            self.money_bonus_percent_label.on_update_args((round(self.money_bonus_multiplier * 100 - 100), ))
            self.money_bonus_percent_label.create()
        else:
            self.money_bonus_percent_label.delete()
            self.money_bonus_placeholder_label.create()

    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()

    @view_is_active
    def on_update(self):
        pass

    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.exp_bonus_percent_label.on_update_opacity(self.opacity)
        self.money_bonus_percent_label.on_update_opacity(self.opacity)
        self.exp_bonus_placeholder_label.on_update_opacity(self.opacity)
        self.money_bonus_placeholder_label.on_update_opacity(self.opacity)

    def on_activate_exp_bonus_code(self, value):
        super().on_activate_exp_bonus_code(value)
        if self.is_activated:
            self.exp_bonus_placeholder_label.delete()
            self.exp_bonus_percent_label.on_update_args((round(self.exp_bonus_multiplier * 100 - 100), ))
            self.exp_bonus_percent_label.create()

    def on_deactivate_exp_bonus_code(self):
        super().on_deactivate_exp_bonus_code()
        if self.is_activated:
            self.exp_bonus_percent_label.delete()
            self.exp_bonus_placeholder_label.create()

    def on_activate_money_bonus_code(self, value):
        super().on_activate_money_bonus_code(value)
        if self.is_activated:
            self.money_bonus_placeholder_label.delete()
            self.money_bonus_percent_label.on_update_args((round(self.money_bonus_multiplier * 100 - 100), ))
            self.money_bonus_percent_label.create()

    def on_deactivate_money_bonus_code(self):
        super().on_deactivate_money_bonus_code()
        if self.is_activated:
            self.money_bonus_percent_label.delete()
            self.money_bonus_placeholder_label.create()

    @game_progress_notifications_available
    @bonus_expired_notification_enabled
    def on_send_exp_bonus_expired_notification(self):
        self.game_progress_notifications.append(ExpBonusExpiredNotification(self.current_locale))

    @game_progress_notifications_available
    @bonus_expired_notification_enabled
    def on_send_money_bonus_expired_notification(self):
        self.game_progress_notifications.append(MoneyBonusExpiredNotification(self.current_locale))

    @game_progress_notifications_available
    @bonus_expired_notification_enabled
    def on_send_construction_time_bonus_expired_notification(self):
        self.game_progress_notifications.append(ConstructionTimeBonusExpiredNotification(self.current_locale))
