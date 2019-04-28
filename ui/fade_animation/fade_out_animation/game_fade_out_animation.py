from logging import getLogger

from ui.fade_animation.fade_out_animation import *


class GameFadeOutAnimation(FadeOutAnimation):
    """
    Implements fade-out animation for Game view.
    """
    def __init__(self, game_controller):
        """
        Properties:
            map_fade_out_animations             list of fade-out animations for the maps

        :param game_controller:                 Game controller
        """
        super().__init__(animation_object=game_controller, logger=getLogger('root.app.game.fade_out_animation'))
        self.map_fade_out_animations = []

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        """
        Activates the animation and initializes opacity chart position.
        """
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
        for animation in self.map_fade_out_animations:
            animation.on_activate()
