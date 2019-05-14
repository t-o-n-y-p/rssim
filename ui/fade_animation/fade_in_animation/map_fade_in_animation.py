from logging import getLogger

from ui.fade_animation.fade_in_animation import *


class MapFadeInAnimation(FadeInAnimation):
    """
    Implements fade-in animation for Map view.
    """
    def __init__(self, map_controller):
        """
        Properties:
            constructor_fade_in_animation           fade-in animation for constructor view
            scheduler_fade_in_animation             fade-in animation for scheduler view
            dispatcher_fade_in_animation            fade-in animation for dispatcher view
            signal_fade_in_animations               list of fade-in animations for all signals on the map
            railroad_switch_fade_in_animations      list of fade-in animations for all switches on the map
            crossover_fade_in_animations            list of fade-in animations for all crossovers on the map
            train_fade_in_animations                list of fade-in animations for all trains on the map
            train_route_fade_in_animations          list of fade-in animations for all train routes on the map

        :param map_controller:                  Map controller
        """
        super().__init__(animation_object=map_controller,
                         logger=getLogger(f'root.app.game.map.{map_controller.map_id}.fade_in_animation'))
        self.constructor_fade_in_animation = None
        self.scheduler_fade_in_animation = None
        self.dispatcher_fade_in_animation = None
        self.signal_fade_in_animations = []
        self.railroad_switch_fade_in_animations = []
        self.crossover_fade_in_animations = []
        self.train_fade_in_animations = []
        self.train_route_fade_in_animations = []

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        """
        Activates the animation and initializes opacity chart position.
        """
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
        self.animation_object.on_activate_view()
        for animation in self.signal_fade_in_animations:
            animation.on_activate()

        for animation in self.railroad_switch_fade_in_animations:
            animation.on_activate()

        for animation in self.crossover_fade_in_animations:
            animation.on_activate()

        for animation in self.train_fade_in_animations:
            animation.on_activate()
