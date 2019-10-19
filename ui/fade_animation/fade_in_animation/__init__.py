from ui.fade_animation import *


class FadeInAnimation(FadeAnimation):
    def __init__(self, animation_object, logger):
        super().__init__(animation_object=animation_object, logger=logger)
        self.opacity_chart = [0, 17, 34, 51, 68, 85, 102, 119, 136, 153, 170, 187, 204, 221, 238, 255]

    def on_activate(self):
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
        self.animation_object.on_activate_view()

    @final
    @fade_animation_is_active
    def on_deactivate(self):
        self.is_activated = False
        if self.on_deactivate_listener is not None:
            self.on_deactivate_listener.on_fade_in_animation_deactivate()
