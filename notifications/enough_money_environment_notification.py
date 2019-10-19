from logging import getLogger
from typing import final

from notifications import Notification


@final
class EnoughMoneyEnvironmentNotification(Notification):
    def __init__(self):
        super().__init__(logger=getLogger('root.notification.enough_money_environment_notification'))
        self.caption_key = 'enough_money_environment_notification_caption_string'
        self.message_key = 'enough_money_environment_notification_message_string'
