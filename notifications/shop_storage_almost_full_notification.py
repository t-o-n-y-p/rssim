from logging import getLogger
from typing import final

from notifications import Notification


@final
class ShopStorageAlmostFullNotification(Notification):
    def __init__(self, current_locale, shop_id):
        super().__init__(
            logger=getLogger('root.notification.shop_storage_almost_full_notification'),
            caption_key='shop_storage_almost_full_notification_caption_string',
            message_key='shop_storage_almost_full_notification_message_string',
            current_locale=current_locale, message_args=(shop_id, )
        )
