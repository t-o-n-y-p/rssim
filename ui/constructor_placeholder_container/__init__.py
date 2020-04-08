from abc import ABC
from typing import final

from database import USER_DB_CURSOR
from ui import Viewport, window_size_has_changed
from ui.label import LocalizedLabel


def container_is_active(fn):
    def _handle_if_container_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_container_is_activated


def container_is_not_active(fn):
    def _handle_if_container_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_container_is_not_activated


class ConstructorPlaceholderContainer(ABC):
    placeholder_label: LocalizedLabel

    def __init__(self, bottom_parent_viewport, top_parent_viewport, logger):
        self.logger = logger
        self.bottom_parent_viewport = bottom_parent_viewport
        self.top_parent_viewport = top_parent_viewport
        self.viewport = Viewport()
        self.screen_resolution = (0, 0)
        self.opacity = 0
        self.is_activated = False
        self.on_window_resize_handlers = [self.on_window_resize, ]
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]

    @final
    @container_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.placeholder_label.create()

    @final
    @container_is_active
    def on_deactivate(self):
        self.is_activated = False

    @final
    @window_size_has_changed
    def on_window_resize(self, width, height):
        self.screen_resolution = width, height
        self.viewport.x1, self.viewport.x2 = self.bottom_parent_viewport.x1, self.bottom_parent_viewport.x2
        self.viewport.y1 = self.bottom_parent_viewport.y1
        self.viewport.y2 = self.top_parent_viewport.y2

    @final
    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.placeholder_label.on_update_current_locale(self.current_locale)

    @final
    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.placeholder_label.on_update_opacity(self.opacity)

    @final
    def on_update_top_parent_viewport(self, top_parent_viewport):
        self.top_parent_viewport = top_parent_viewport
        self.viewport.y2 = self.top_parent_viewport.y2
        self.placeholder_label.on_position_changed()
