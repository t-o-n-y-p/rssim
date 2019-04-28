from logging import getLogger

from ui.fade_animation.fade_in_animation import *


class MapFadeInAnimation(FadeInAnimation):
    """
    Implements fade-in animation for Map view.
    """
    def __init__(self, map_controller):
        """
        Properties:
            signal_fade_in_animations           list of fade-in animations fo all signals on the map
            railroad_switch_fade_in_animations  list of fade-in animations fo all switches on the map
            crossover_fade_in_animations        list of fade-in animations fo all crossovers on the map
            train_fade_in_animations            list of fade-in animations fo all trains on the map

        :param map_controller:                  Map controller
        """
        super().__init__(animation_object=map_controller, logger=getLogger('root.app.game.map.fade_in_animation'))
        self.signal_fade_in_animations = []
        self.railroad_switch_fade_in_animations = []
        self.crossover_fade_in_animations = []
        self.train_fade_in_animations = []

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        """
        Activates the animation and initializes opacity chart position.
        """
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
