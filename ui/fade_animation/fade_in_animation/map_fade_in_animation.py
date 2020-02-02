from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class MapFadeInAnimation(FadeInAnimation):
    def __init__(self, map_view):
        super().__init__(animation_object=map_view,
                         logger=getLogger(f'root.app.game.map.{map_view.map_id}.fade_in_animation'))
        self.constructor_fade_in_animation = None
        self.scheduler_fade_in_animation = None
        self.dispatcher_fade_in_animation = None
        self.mini_map_fade_in_animation = None
        self.narrator_fade_in_animation = None
        self.signal_fade_in_animations = []
        self.railroad_switch_fade_in_animations = []
        self.crossover_fade_in_animations = []
        self.train_fade_in_animations = []
        self.train_route_fade_in_animations = []
        self.shop_fade_in_animations = []

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
        self.narrator_fade_in_animation.on_activate()
        for animation in self.signal_fade_in_animations:
            animation.on_activate()

        for animation in self.railroad_switch_fade_in_animations:
            animation.on_activate()

        for animation in self.crossover_fade_in_animations:
            animation.on_activate()

        for animation in self.train_fade_in_animations:
            animation.on_activate()
