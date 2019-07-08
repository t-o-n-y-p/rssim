from logging import getLogger

from notifications import Notification


class EnoughMoneyTrackNotification(Notification):
    def __init__(self):
        super().__init__(logger=getLogger('root.notification.enough_money_track_notification'))
        self.caption_key = 'enough_money_track_notification_caption_string'
        self.message_key = 'enough_money_track_notification_message_string'
