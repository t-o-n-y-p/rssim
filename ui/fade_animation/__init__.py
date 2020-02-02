from typing import final

from database import USER_DB_CURSOR


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


def fade_animation_needed(fn):
    def _handle_if_object_view_is_visible(*args, **kwargs):
        if args[0].animation_object.view.opacity != args[0].opacity_chart[-1]:
            fn(*args, **kwargs)

    return _handle_if_object_view_is_visible


class FadeAnimation:
    def __init__(self, animation_object, logger):
        self.animation_object = animation_object
        self.logger = logger
        self.opacity_chart = []
        self.current_opacity_chart_index = 0
        self.is_activated = False
        self.on_deactivate_listener = None
        USER_DB_CURSOR.execute('SELECT fade_animations_enabled FROM graphics')
        self.fade_animations_enabled = bool(USER_DB_CURSOR.fetchone()[0])

    def on_activate(self):
        pass

    def on_deactivate(self):
        pass

    @final
    @fade_animation_is_active
    def on_update(self):
        if self.current_opacity_chart_index == len(self.opacity_chart) - 1:
            self.on_deactivate()
        else:
            if self.fade_animations_enabled:
                self.current_opacity_chart_index += 1
            else:
                self.current_opacity_chart_index = len(self.opacity_chart) - 1

            self.animation_object.on_update_opacity(self.opacity_chart[self.current_opacity_chart_index])

    @final
    def on_update_fade_animation_state(self, new_state):
        self.fade_animations_enabled = new_state
