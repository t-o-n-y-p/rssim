from logging import getLogger

from notifications import Notification


class EnvironmentUnlockedNotification(Notification):
    def __init__(self):
        super().__init__(logger=getLogger('root.notification.environment_unlocked_notification'))
        self.caption_key = 'environment_unlocked_notification_caption_string'
        self.message_key = 'environment_unlocked_notification_message_string'
