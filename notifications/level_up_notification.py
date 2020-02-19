from logging import getLogger
from typing import final

from notifications import Notification


@final
class LevelUpNotification(Notification):
    def __init__(self, current_locale, level):
        super().__init__(logger=getLogger('root.notification.level_up_notification'),
                         caption_key='level_up_notification_caption_string',
                         message_key='level_up_notification_message_string',
                         current_locale=current_locale, message_args=(level, ))
