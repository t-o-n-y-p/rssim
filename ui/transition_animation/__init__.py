from logging import getLogger


def transition_animation_is_active(fn):
    def _handle_if_transition_animation_is_active(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_transition_animation_is_active


def transition_animation_is_not_active(fn):
    def _handle_if_transition_animation_is_not_active(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_transition_animation_is_not_active


class TransitionAnimation:
    def __init__(self, fade_out_animation, fade_in_animation):
        self.logger = getLogger('{}-{}_transition_animation'.format(fade_out_animation.view.__class__.__name__,
                                                                    fade_in_animation.view.__class__.__name__))
        self.fade_out_animation, self.fade_in_animation = fade_out_animation, fade_in_animation
        self.fade_out_animation.on_deactivate_listener = self
        self.fade_in_animation.on_deactivate_listener = self
        self.is_activated = False

    @transition_animation_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.fade_out_animation.on_activate()

    @transition_animation_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_fade_out_animation_deactivate(self):
        self.fade_in_animation.on_activate()

    def on_fade_in_animation_deactivate(self):
        self.on_deactivate()
