from logging import getLogger

from notifications import Notification


class ShopStorageFullNotification(Notification):
    def __init__(self):
        super().__init__(logger=getLogger('root.notification.shop_storage_full_notification'))
        self.caption_key = 'shop_storage_full_notification_caption_string'
        self.message_key = 'shop_storage_full_notification_message_string'
