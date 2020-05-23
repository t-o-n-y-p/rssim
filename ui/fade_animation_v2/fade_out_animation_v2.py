from typing import final

from ui.fade_animation_v2 import FadeAnimationV2, fade_animation_needed, fade_animation_is_not_active, \
    fade_animation_is_active


class FadeOutAnimationV2(FadeAnimationV2):
    def __init__(self, animation_object, logger):
        super().__init__(end_opacity=0, animation_object=animation_object, logger=logger)

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
        self.animation_object.on_deactivate()
        self.current_fade_animation_time = (1 - self.animation_object.opacity / 255) * self.FADE_ANIMATION_DURATION

    @final
    @fade_animation_is_active
    def on_deactivate(self):
        super().on_deactivate()
        if self.on_deactivate_listener:
            self.on_deactivate_listener.on_fade_out_animation_deactivate()

    @final
    def on_calculate_new_opacity(self):
        return max(round((1 - self.current_fade_animation_time / self.FADE_ANIMATION_DURATION) * 255), self.end_opacity)
