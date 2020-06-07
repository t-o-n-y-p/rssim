from typing import final

from pyglet.window import FPSDisplay

from ui import WINDOW, window_size_has_changed, UIObject
from ui.label_v2.fps_label_v2 import FPSLabelV2


@final
class FPSDisplayV2(FPSDisplay, UIObject):
    def __init__(self, logger, parent_viewport):
        super(FPSDisplay, self).__init__(WINDOW)
        super(UIObject, self).__init__(logger, parent_viewport)
        self.label = FPSLabelV2(self.logger.getChild('fps_label_v2'), self.viewport)
        self.on_window_resize_handlers.extend(self.label.on_window_resize_handlers)
        self.fade_in_animation.child_animations.append(self.label.fade_in_animation)
        self.fade_out_animation.child_animations.append(self.label.fade_out_animation)

    def set_fps(self, fps):
        self.label.on_fps_update(int(fps))                                                                      # noqa

    @window_size_has_changed
    def on_window_resize(self, width, height):
        super().on_window_resize(width, height)
        self.viewport.x1, self.viewport.y1 = 0, 0
        self.viewport.x2, self.viewport.y2 = width, height
