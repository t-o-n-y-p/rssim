from logging import getLogger

from notifications import Notification


class ExpBonusExpiredNotification(Notification):
    def __init__(self):
        super().__init__(logger=getLogger('root.notification.exp_bonus_expired_notification'))
        self.caption_key = 'exp_bonus_expired_notification_caption_string'
        self.message_key = 'exp_bonus_expired_notification_message_string'
