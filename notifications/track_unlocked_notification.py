from logging import getLogger

from notifications import Notification


class TrackUnlockedNotification(Notification):
    """
    Implements Track unlocked notification.
    It is triggered when new track is unlocked and app window is not active.
    """
    def __init__(self):
        """
        Properties:
            caption_key                         i18n resource key for system notification caption
            message_key                         i18n resource key for system notification message
        """
        super().__init__(logger=getLogger('root.notification.track_unlocked_notification'))
        self.caption_key = 'track_unlocked_notification_caption_string'
        self.message_key = 'track_unlocked_notification_message_string'
