def fade_animation_is_active(fn):
    def _handle_if_fade_animation_is_active(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_fade_animation_is_active


def fade_animation_is_not_active(fn):
    def _handle_if_fade_animation_is_not_active(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_fade_animation_is_not_active


class FadeAnimation:
    def __init__(self, animation_object, logger):
        self.animation_object = animation_object
        self.logger = logger
        self.opacity_chart = []
        self.current_opacity_chart_index = 0
        self.is_activated = False
        self.on_deactivate_listener = None
        self.fade_animations_enabled = True

    @fade_animation_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.opacity)

    @fade_animation_is_active
    def on_update(self):
        if self.fade_animations_enabled:
            self.current_opacity_chart_index += 1
        else:
            self.current_opacity_chart_index = len(self.opacity_chart) - 1

        self.animation_object.on_update_opacity(self.opacity_chart[self.current_opacity_chart_index])
        if self.current_opacity_chart_index == len(self.opacity_chart) - 1:
            self.on_deactivate()

    def on_deactivate(self):
        pass

    def on_update_fade_animation_state(self, new_state):
        self.fade_animations_enabled = new_state
