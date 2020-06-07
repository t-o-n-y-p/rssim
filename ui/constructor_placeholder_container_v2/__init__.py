from abc import ABC
from typing import final

from ui import window_size_has_changed, UIObject, localizable


class ConstructorPlaceholderContainerV2(UIObject, ABC):
    @localizable
    def __init__(self, logger, parent_viewport, bottom_parent_viewport, top_parent_viewport):
        super().__init__(logger, parent_viewport)
        self.bottom_parent_viewport = bottom_parent_viewport
        self.top_parent_viewport = top_parent_viewport

    def on_update_top_parent_viewport(self, top_parent_viewport):
        self.top_parent_viewport = top_parent_viewport
        self.viewport.y2 = self.top_parent_viewport.y2

    @final
    @window_size_has_changed
    def on_window_resize(self, width, height):
        super().on_window_resize(width, height)
        self.viewport.x1, self.viewport.x2 = self.bottom_parent_viewport.x1, self.bottom_parent_viewport.x2
        self.viewport.y1 = self.bottom_parent_viewport.y1
        self.viewport.y2 = self.top_parent_viewport.y2
