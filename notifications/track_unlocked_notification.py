from logging import getLogger

from notifications import Notification


class TrackUnlockedNotification(Notification):
    def __init__(self):
        super().__init__(logger=getLogger('root.notification.track_unlocked_notification'))
        self.caption_key = 'track_unlocked_notification_caption_string'
        self.message_key = 'track_unlocked_notification_message_string'
