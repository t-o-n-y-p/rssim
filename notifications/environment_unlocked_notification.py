from logging import getLogger

from notifications import Notification


class EnvironmentUnlockedNotification(Notification):
    """
    Implements Environment unlocked notification.
    It is triggered when new environment tier is unlocked and app window is not active.
    """
    def __init__(self):
        """
        Properties:
            caption_key                         i18n resource key for system notification caption
            message_key                         i18n resource key for system notification message
        """
        super().__init__(logger=getLogger('root.notification.environment_unlocked_notification'))
        self.caption_key = 'environment_unlocked_notification_caption_string'
        self.message_key = 'environment_unlocked_notification_message_string'
