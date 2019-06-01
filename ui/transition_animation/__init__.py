from logging import getLogger


def transition_animation_is_active(fn):
    """
    Use this decorator to execute function only if transition animation is active.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_transition_animation_is_active(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_transition_animation_is_active


def transition_animation_is_not_active(fn):
    """
    Use this decorator to execute function only if transition animation is not active.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_transition_animation_is_not_active(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_transition_animation_is_not_active


class TransitionAnimation:
    """
    Implements base class for transition animations.
    """
    def __init__(self, fade_out_animation, fade_in_animation):
        """
        Properties:
            logger                              telemetry instance
            fade_out_animation                  fade-out animation from first screen
            fade_in_animation                   fade-in animation from second screen
            is_activated                        indicates if transition animation is activated

        :param fade_out_animation:
        :param fade_in_animation:
        """
        self.logger = getLogger('root.{}->{}_transition_animation'
                                .format(fade_out_animation.animation_object.__class__.__name__,
                                        fade_in_animation.animation_object.__class__.__name__))
        self.fade_out_animation, self.fade_in_animation = fade_out_animation, fade_in_animation
        self.is_activated = False

    @transition_animation_is_not_active
    def on_activate(self):
        """
        Activates fade-out animation and subscribes for deactivation events.
        """
        self.is_activated = True
        self.fade_out_animation.on_activate()
        self.fade_out_animation.on_deactivate_listener = self
        self.fade_in_animation.on_deactivate_listener = self

    @transition_animation_is_active
    def on_deactivate(self):
        """
        Deactivates fade-out and fade-in animations and unsubscribes for deactivation events.
        """
        self.is_activated = False
        self.fade_out_animation.on_deactivate()
        self.fade_in_animation.on_deactivate()
        self.fade_out_animation.on_deactivate_listener = None
        self.fade_in_animation.on_deactivate_listener = None

    def on_fade_out_animation_deactivate(self):
        """
        Fade-out animation deactivation event handler.
        """
        self.fade_in_animation.on_activate()

    def on_fade_in_animation_deactivate(self):
        """
        Fade-in animation deactivation event handler.
        """
        self.on_deactivate()
