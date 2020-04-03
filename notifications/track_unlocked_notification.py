from logging import getLogger
from typing import final

from i18n import I18N_RESOURCES
from notifications import Notification


@final
class TrackUnlockedNotification(Notification):
    def __init__(self, current_locale, map_id, track):
        super().__init__(
            logger=getLogger('root.notification.track_unlocked_notification'),
            caption_key='track_unlocked_notification_caption_string',
            message_key='track_unlocked_notification_message_string', current_locale=current_locale,
            message_args=(I18N_RESOURCES['map_title_string'][current_locale][map_id], track)
        )
