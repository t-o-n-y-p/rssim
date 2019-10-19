from logging import getLogger
from typing import final

from notifications import Notification


@final
class TrackConstructionCompletedNotification(Notification):
    def __init__(self):
        super().__init__(logger=getLogger('root.notification.track_construction_completed_notification'))
        self.caption_key = 'track_construction_completed_notification_caption_string'
        self.message_key = 'track_construction_completed_notification_message_string'
