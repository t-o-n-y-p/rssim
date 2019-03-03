from logging import getLogger

from notifications import Notification


class LevelUpNotification(Notification):
    """
    Implements Level up notification.
    It is triggered when user reaches new level and app window is not active.
    """
    def __init__(self):
        """
        Properties:
            caption_key                         i18n resource key for system notification caption
            message_key                         i18n resource key for system notification message
        """
        super().__init__(logger=getLogger('root.notification.level_up_notification'))
        self.caption_key = 'level_up_notification_caption_string'
        self.message_key = 'level_up_notification_message_string'
