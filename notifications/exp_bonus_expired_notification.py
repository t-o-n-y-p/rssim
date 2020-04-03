from logging import getLogger
from typing import final

from notifications import Notification


@final
class ExpBonusExpiredNotification(Notification):
    def __init__(self, current_locale):
        super().__init__(
            logger=getLogger('root.notification.exp_bonus_expired_notification'),
            caption_key='exp_bonus_expired_notification_caption_string',
            message_key='exp_bonus_expired_notification_message_string', current_locale=current_locale
        )
