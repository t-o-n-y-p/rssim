from logging import getLogger
from typing import final

from notifications import Notification


@final
class MapUnlockedNotification(Notification):
    def __init__(self):
        super().__init__(logger=getLogger('root.notification.map_unlocked_notification'))
        self.caption_key = 'map_unlocked_notification_caption_string'
        self.message_key = 'map_unlocked_notification_message_string'
