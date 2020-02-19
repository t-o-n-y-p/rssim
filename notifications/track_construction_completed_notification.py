from logging import getLogger
from typing import final

from notifications import Notification


@final
class TrackConstructionCompletedNotification(Notification):
    def __init__(self, current_locale, track):
        super().__init__(logger=getLogger('root.notification.track_construction_completed_notification'),
                         caption_key='track_construction_completed_notification_caption_string',
                         message_key='track_construction_completed_notification_message_string',
                         current_locale=current_locale, message_args=(track, ))
