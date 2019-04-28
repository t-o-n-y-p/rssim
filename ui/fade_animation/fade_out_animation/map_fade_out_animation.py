from logging import getLogger

from ui.fade_animation.fade_out_animation import *


class MapFadeOutAnimation(FadeOutAnimation):
    """
    Implements fade-out animation for Map view.
    """
    def __init__(self, map_controller):
        """
        Properties:
            constructor_fade_out_animation          fade-out animation for constructor view
            scheduler_fade_out_animation            fade-out animation for scheduler view
            dispatcher_fade_out_animation           fade-out animation for dispatcher view
            signal_fade_out_animations              list of fade-out animations fo all signals on the map
            railroad_switch_fade_out_animations     list of fade-out animations fo all switches on the map
            crossover_fade_out_animations           list of fade-out animations fo all crossovers on the map
            train_fade_out_animations               list of fade-out animations fo all trains on the map
            train_route_fade_out_animations         list of fade-out animations fo all train routes on the map

        :param map_controller:                      Map controller
        """
        super().__init__(animation_object=map_controller, logger=getLogger('root.app.game.map.fade_out_animation'))
        self.constructor_fade_out_animation = None
        self.scheduler_fade_out_animation = None
        self.dispatcher_fade_out_animation = None
        self.signal_fade_out_animations = []
        self.railroad_switch_fade_out_animations = []
        self.crossover_fade_out_animations = []
        self.train_fade_out_animations = []
        self.train_route_fade_out_animations = []

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        """
        Activates the animation and initializes opacity chart position.
        """
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
        self.constructor_fade_out_animation.on_activate()
        self.scheduler_fade_out_animation.on_activate()
        self.dispatcher_fade_out_animation.on_activate()
        for animation in self.signal_fade_out_animations:
            animation.on_activate()

        for animation in self.railroad_switch_fade_out_animations:
            animation.on_activate()

        for animation in self.crossover_fade_out_animations:
            animation.on_activate()

        for animation in self.train_fade_out_animations:
            animation.on_activate()

        for animation in self.train_route_fade_out_animations:
            animation.on_activate()
