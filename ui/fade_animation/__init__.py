from database import USER_DB_CURSOR


def fade_animation_is_active(fn):
    """
    Use this decorator to execute function only if fade animation is active.

    :param fn:                          function to decorate
    :return:                            decorator function
    """
    def _handle_if_fade_animation_is_active(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_fade_animation_is_active


def fade_animation_is_not_active(fn):
    """
    Use this decorator to execute function only if fade animation is not active.

    :param fn:                          function to decorate
    :return:                            decorator function
    """
    def _handle_if_fade_animation_is_not_active(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_fade_animation_is_not_active


def fade_animation_needed(fn):
    """
    Use this decorator to execute function only if object view opacity
    is not already last in animation opacity chart.

    :param fn:                          function to decorate
    :return:                            decorator function
    """
    def _handle_if_object_view_is_visible(*args, **kwargs):
        if args[0].animation_object.view.opacity != args[0].opacity_chart[-1]:
            fn(*args, **kwargs)

    return _handle_if_object_view_is_visible


class FadeAnimation:
    """
    Implements base class for fade animation.
    """
    def __init__(self, animation_object, logger):
        """
        Properties:
            animation_object                    target object controller
            logger                              telemetry instance
            opacity_chart                       opacity chart over time (in frames) within the animation
            current_opacity_chart_index         current position within the opacity chart
            is_activated                        indicates if fade animation is active
            on_deactivate_listener              transition animation which waits for fade animation deactivation event
            fade_animations_enabled             indicates if fade animations are enabled by player

        :param animation_object:                target object controller
        :param logger:                          telemetry instance
        """
        self.animation_object = animation_object
        self.logger = logger
        self.opacity_chart = []
        self.current_opacity_chart_index = 0
        self.is_activated = False
        self.on_deactivate_listener = None
        USER_DB_CURSOR.execute('SELECT fade_animations_enabled FROM graphics')
        self.fade_animations_enabled = bool(USER_DB_CURSOR.fetchone()[0])

    def on_activate(self):
        """
        Activates the animation and initializes opacity chart position.
        """
        pass

    def on_deactivate(self):
        """
        Deactivates the animation and notifies the listener about it.
        """
        pass

    @fade_animation_is_active
    def on_update(self):
        """
        Updates object view with new opacity value based on opacity chart.
        Deactivates animation if it last position of the chart.
        """
        if self.current_opacity_chart_index == len(self.opacity_chart) - 1:
            self.on_deactivate()
        else:
            if self.fade_animations_enabled:
                self.current_opacity_chart_index += 1
            else:
                self.current_opacity_chart_index = len(self.opacity_chart) - 1

            self.animation_object.view.on_update_opacity(self.opacity_chart[self.current_opacity_chart_index])

    def on_update_fade_animation_state(self, new_state):
        """
        Turns fade animation on/off based on player action.

        :param new_state:                       new fade_animations_enabled flag value
        """
        self.fade_animations_enabled = new_state
