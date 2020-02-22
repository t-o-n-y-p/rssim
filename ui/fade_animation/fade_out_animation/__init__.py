from ui.fade_animation import *


class FadeOutAnimation(FadeAnimation, ABC):
    def __init__(self, animation_object, logger):
        super().__init__(animation_object=animation_object, logger=logger)
        self.opacity_chart = [255, 238, 221, 204, 187, 170, 153, 136, 119, 102, 85, 68, 51, 34, 17, 0]

    def on_activate(self):
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.opacity)
        self.animation_object.on_deactivate()

    @final
    @fade_animation_is_active
    def on_deactivate(self):
        self.is_activated = False
        if self.on_deactivate_listener is not None:
            self.on_deactivate_listener.on_fade_out_animation_deactivate()
