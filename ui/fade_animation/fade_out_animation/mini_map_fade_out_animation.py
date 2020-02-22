from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class MiniMapFadeOutAnimation(FadeOutAnimation):
    def __init__(self, mini_map_view):
        super().__init__(animation_object=mini_map_view,
                         logger=getLogger(f'root.app.game.map.{mini_map_view.map_id}.mini_map.fade_out_animation'))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
