from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class GameFadeOutAnimation(FadeOutAnimation):
    def __init__(self, game_controller):
        super().__init__(animation_object=game_controller, logger=getLogger('root.app.game.fade_out_animation'))
        self.bonus_code_manager_fade_out_animation = None
        self.map_fade_out_animations = []

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
        self.bonus_code_manager_fade_out_animation.on_activate()
        for animation in self.map_fade_out_animations:
            animation.on_activate()
