from logging import getLogger

from notifications import Notification


class MoneyBonusExpiredNotification(Notification):
    def __init__(self):
        super().__init__(logger=getLogger('root.notification.money_bonus_expired_notification'))
        self.caption_key = 'money_bonus_expired_notification_caption_string'
        self.message_key = 'money_bonus_expired_notification_message_string'
