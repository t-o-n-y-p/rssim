from logging import getLogger

from ui.fade_animation.fade_in_animation import *


class MapFadeInAnimation(FadeInAnimation):
    def __init__(self, game_controller):
        super().__init__(animation_object=game_controller, logger=getLogger('root.app.game.map.fade_in_animation'))
        self.signal_fade_in_animations = []
        self.railroad_switch_fade_in_animations = []
        self.crossover_fade_in_animations = []
        self.train_fade_in_animations = []

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
        for animation in self.signal_fade_in_animations:
            animation.on_activate()

        for animation in self.railroad_switch_fade_in_animations:
            animation.on_activate()

        for animation in self.crossover_fade_in_animations:
            animation.on_activate()

        for animation in self.train_fade_in_animations:
            animation.on_activate()
