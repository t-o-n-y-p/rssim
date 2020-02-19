from logging import getLogger
from typing import final

from notifications import Notification


@final
class EnoughMoneyTrackNotification(Notification):
    def __init__(self, current_locale):
        super().__init__(logger=getLogger('root.notification.enough_money_track_notification'),
                         caption_key='enough_money_track_notification_caption_string',
                         message_key='enough_money_track_notification_message_string',
                         current_locale=current_locale)
