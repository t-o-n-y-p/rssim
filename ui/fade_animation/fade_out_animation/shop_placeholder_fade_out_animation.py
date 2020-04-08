from logging import getLogger
from typing import final

from ui.fade_animation.fade_out_animation import FadeOutAnimation


@final
class ShopPlaceholderFadeOutAnimation(FadeOutAnimation):
    def __init__(self, shop_placeholder_view):
        super().__init__(
            animation_object=shop_placeholder_view, logger=getLogger(
                f'root.app.game.map.{shop_placeholder_view.map_id}.shop.{shop_placeholder_view.shop_id}.placeholder.fade_out_animation'
            )
        )
