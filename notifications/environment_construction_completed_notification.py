from logging import getLogger

from notifications import Notification


class EnvironmentConstructionCompletedNotification(Notification):
    """
    Implements Environment construction completed notification.
    It is triggered when environment tier construction is completed and app window is not active.
    """
    def __init__(self):
        """
        Properties:
            caption_key                         i18n resource key for system notification caption
            message_key                         i18n resource key for system notification message
        """
        super().__init__(logger=getLogger('root.notification.environment_construction_completed_notification'))
        self.caption_key = 'environment_construction_completed_notification_caption_string'
        self.message_key = 'environment_construction_completed_notification_message_string'
