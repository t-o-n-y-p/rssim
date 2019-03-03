from logging import getLogger

from notifications import Notification


class LevelUpNotification(Notification):
    def __init__(self):
        super().__init__(logger=getLogger('root.notification.level_up_notification'))
        self.caption_key = 'level_up_notification_caption_string'
        self.message_key = 'level_up_notification_message_string'
