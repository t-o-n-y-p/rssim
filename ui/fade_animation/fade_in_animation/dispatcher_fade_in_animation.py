from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class DispatcherFadeInAnimation(FadeInAnimation):
    def __init__(self, dispatcher_view):
        super().__init__(animation_object=dispatcher_view,
                         logger=getLogger(
                             f'root.app.game.map.{dispatcher_view.map_id}.dispatcher.fade_in_animation'
                         ))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
