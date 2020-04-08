from logging import getLogger
from typing import final

from ui.fade_animation.fade_out_animation import FadeOutAnimation


@final
class MapSwitcherFadeOutAnimation(FadeOutAnimation):
    def __init__(self, map_switcher_view):
        super().__init__(
            animation_object=map_switcher_view, logger=getLogger('root.app.game.map_switcher.fade_out_animation')
        )
