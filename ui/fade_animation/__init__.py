from abc import ABC, abstractmethod
from typing import final, Final

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
        if args[0].animation_object.opacity != args[0].end_opacity:
            fn(*args, **kwargs)

    return _handle_if_object_view_is_visible


class FadeAnimation(ABC):
    FADE_ANIMATION_TIME: Final = 0.25

    def __init__(self, end_opacity, animation_object, logger):
        self.animation_object = animation_object
        self.logger = logger
        self.end_opacity = end_opacity
        self.current_fade_animation_time = 0.0
        self.is_activated = False
        self.on_deactivate_listener = None
        USER_DB_CURSOR.execute('SELECT fade_animations_enabled FROM graphics')
        self.fade_animations_enabled = bool(USER_DB_CURSOR.fetchone()[0])

    @abstractmethod
    def on_activate(self):
        pass

    @abstractmethod
    def on_deactivate(self):
        pass

    @abstractmethod
    def on_calculate_new_opacity(self):
        pass

    @final
    @fade_animation_is_active
    def on_update(self, dt):
        if not self.fade_animations_enabled:
            self.animation_object.on_update_opacity(self.end_opacity)
            self.on_deactivate()
        elif self.current_fade_animation_time < self.FADE_ANIMATION_TIME:
            self.current_fade_animation_time += dt
            self.animation_object.on_update_opacity(self.on_calculate_new_opacity())
        else:
            self.on_deactivate()

    @final
    def on_update_fade_animation_state(self, new_state):
        self.fade_animations_enabled = new_state
