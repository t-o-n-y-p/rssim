from logging import getLogger
from typing import final

from notifications import Notification


@final
class EnvironmentConstructionCompletedNotification(Notification):
    def __init__(self):
        super().__init__(logger=getLogger('root.notification.environment_construction_completed_notification'))
        self.caption_key = 'environment_construction_completed_notification_caption_string'
        self.message_key = 'environment_construction_completed_notification_message_string'
