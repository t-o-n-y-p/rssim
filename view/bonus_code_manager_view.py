from logging import getLogger

from view import *
from ui.label.money_bonus_value_percent_label import MoneyBonusValuePercentLabel
from ui.label.exp_bonus_value_percent_label import ExpBonusValuePercentLabel
from ui.label.exp_bonus_placeholder_label import ExpBonusPlaceholderLabel
from ui.label.money_bonus_placeholder_label import MoneyBonusPlaceholderLabel
from notifications.exp_bonus_expired_notification import ExpBonusExpiredNotification
from notifications.money_bonus_expired_notification import MoneyBonusExpiredNotification
from notifications.construction_time_bonus_expired_notification import ConstructionTimeBonusExpiredNotification


@final
class BonusCodeManagerView(GameBaseView):
    def __init__(self, controller):
        super().__init__(controller, logger=getLogger('root.app.game.bonus_code_manager.view'))
        self.exp_bonus_percent_label = ExpBonusValuePercentLabel(parent_viewport=self.viewport)
        self.money_bonus_percent_label = MoneyBonusValuePercentLabel(parent_viewport=self.viewport)
        self.exp_bonus_placeholder_label = ExpBonusPlaceholderLabel(parent_viewport=self.viewport)
        self.money_bonus_placeholder_label = MoneyBonusPlaceholderLabel(parent_viewport=self.viewport)

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

    def on_change_screen_resolution(self, screen_resolution):
        super().on_change_screen_resolution(screen_resolution)
        self.exp_bonus_percent_label.on_change_screen_resolution(self.screen_resolution)
        self.money_bonus_percent_label.on_change_screen_resolution(self.screen_resolution)
        self.exp_bonus_placeholder_label.on_change_screen_resolution(self.screen_resolution)
        self.money_bonus_placeholder_label.on_change_screen_resolution(self.screen_resolution)

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

    @notifications_available
    @bonus_expired_notification_enabled
    def on_send_exp_bonus_expired_notification(self):
        exp_bonus_expired_notification = ExpBonusExpiredNotification()
        exp_bonus_expired_notification.send(self.current_locale)
        self.controller.parent_controller.parent_controller.on_append_notification(exp_bonus_expired_notification)

    @notifications_available
    @bonus_expired_notification_enabled
    def on_send_money_bonus_expired_notification(self):
        money_bonus_expired_notification = MoneyBonusExpiredNotification()
        money_bonus_expired_notification.send(self.current_locale)
        self.controller.parent_controller.parent_controller.on_append_notification(money_bonus_expired_notification)

    @notifications_available
    @bonus_expired_notification_enabled
    def on_send_construction_time_bonus_expired_notification(self):
        construction_time_bonus_expired_notification = ConstructionTimeBonusExpiredNotification()
        construction_time_bonus_expired_notification.send(self.current_locale)
        self.controller.parent_controller.parent_controller\
            .on_append_notification(construction_time_bonus_expired_notification)
