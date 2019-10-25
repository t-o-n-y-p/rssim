from logging import getLogger
from typing import final

from notifications import Notification


@final
class ConstructionTimeBonusExpiredNotification(Notification):
    def __init__(self):
        super().__init__(logger=getLogger('root.notification.construction_time_bonus_expired_notification'))
        self.caption_key = 'construction_time_bonus_expired_notification_caption_string'
        self.message_key = 'construction_time_bonus_expired_notification_message_string'
