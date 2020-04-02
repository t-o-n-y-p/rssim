from logging import getLogger
from typing import final

from notifications import Notification


@final
class VoiceNotFoundNotification(Notification):
    def __init__(self, current_locale):
        super().__init__(logger=getLogger('root.notification.voice_not_found_notification'),
                         caption_key='voice_not_found_notification_caption_string',
                         message_key='voice_not_found_notification_message_string',
                         current_locale=current_locale)
