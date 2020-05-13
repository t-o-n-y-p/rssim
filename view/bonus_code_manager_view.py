from logging import getLogger
from typing import final

from notifications.exp_bonus_expired_notification import ExpBonusExpiredNotification
from notifications.money_bonus_expired_notification import MoneyBonusExpiredNotification
from notifications.construction_time_bonus_expired_notification import ConstructionTimeBonusExpiredNotification
from view import bonus_expired_notification_enabled, game_progress_notifications_available, GameBaseView, \
    view_is_active


@final
class BonusCodeManagerView(GameBaseView):
    def __init__(self, controller):
        super().__init__(controller, logger=getLogger('root.app.game.bonus_code_manager.view'))
        self.on_append_window_handlers()

    @view_is_active
    def on_update(self):
        pass

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
