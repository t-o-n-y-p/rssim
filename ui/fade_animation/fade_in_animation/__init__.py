from ui.fade_animation import *


class FadeInAnimation(FadeAnimation, ABC):
    def __init__(self, animation_object, logger):
        super().__init__(end_opacity=255, animation_object=animation_object, logger=logger)

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.current_fade_animation_time = self.animation_object.opacity / 255 * self.FADE_ANIMATION_TIME
        self.animation_object.on_activate()

    def on_calculate_new_opacity(self):
        return round(self.current_fade_animation_time / self.FADE_ANIMATION_TIME * 255)

    @final
    @fade_animation_is_active
    def on_deactivate(self):
        self.is_activated = False
        self.current_fade_animation_time = 0.0
        if self.on_deactivate_listener is not None:
            self.on_deactivate_listener.on_fade_in_animation_deactivate()
