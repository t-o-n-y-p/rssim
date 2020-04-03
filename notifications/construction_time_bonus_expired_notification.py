from logging import getLogger
from typing import final

from notifications import Notification


@final
class ConstructionTimeBonusExpiredNotification(Notification):
    def __init__(self, current_locale):
        super().__init__(
            logger=getLogger('root.notification.construction_time_bonus_expired_notification'),
            caption_key='construction_time_bonus_expired_notification_caption_string',
            message_key='construction_time_bonus_expired_notification_message_string', current_locale=current_locale
        )
