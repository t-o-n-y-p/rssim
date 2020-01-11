from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class MiniMapFadeOutAnimation(FadeOutAnimation):
    def __init__(self, map_switcher_controller):
        super().__init__(animation_object=map_switcher_controller,
                         logger=getLogger('root.app.game.map.mini_map.fade_out_animation'))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
