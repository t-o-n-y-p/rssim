from abc import ABC, abstractmethod
from typing import final, Final

from database import USER_DB_CURSOR
from ui import is_active


def fade_animation_needed(f):
    def _handle_if_object_view_is_visible(*args, **kwargs):
        if args[0].animation_object.opacity != args[0].end_opacity:
            f(*args, **kwargs)

    return _handle_if_object_view_is_visible


class FadeAnimationV2(ABC):
    FADE_ANIMATION_DURATION: Final = 0.25

    def __init__(self, end_opacity, animation_object, logger):
        self.animation_object = animation_object
        self.logger = logger
        self.end_opacity = end_opacity
        self.current_fade_animation_time = 0.0
        self.is_activated = False
        self.on_deactivate_listener = None
        USER_DB_CURSOR.execute('SELECT fade_animations_enabled FROM graphics')
        self.fade_animations_enabled = USER_DB_CURSOR.fetchone()[0]
        self.child_animations = []

    def on_activate(self):
        self.is_activated = True
        for a in self.child_animations:
            a.on_activate()

    def on_deactivate(self):
        self.is_activated = False
        self.current_fade_animation_time = 0.0

    @abstractmethod
    def on_calculate_new_opacity(self):
        pass

    @final
    @is_active
    def on_update(self, dt):
        if not self.fade_animations_enabled:
            self.animation_object.on_update_opacity(self.end_opacity)
            self.on_deactivate()
        elif self.current_fade_animation_time < self.FADE_ANIMATION_DURATION:
            self.current_fade_animation_time += dt
            self.animation_object.on_update_opacity(self.on_calculate_new_opacity())
        else:
            self.on_deactivate()

    @final
    def on_update_fade_animation_state(self, new_state):
        self.fade_animations_enabled = new_state
