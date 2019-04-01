from logging import getLogger

from notifications import Notification


class EnoughMoneyTrackNotification(Notification):
    """
    Implements Enough money notification for track.
    It is triggered when user has money target activated and has saved this amount of money.
    """
    def __init__(self):
        """
        Properties:
            caption_key                         i18n resource key for system notification caption
            message_key                         i18n resource key for system notification message
        """
        super().__init__(logger=getLogger('root.notification.enough_money_track_notification'))
        self.caption_key = 'enough_money_track_notification_caption_string'
        self.message_key = 'enough_money_track_notification_message_string'
