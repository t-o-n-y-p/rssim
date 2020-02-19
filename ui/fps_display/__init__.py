from pyglet.window import FPSDisplay as PygletFPSDisplay

from ui import *
from ui.label.fps_label import FPSLabel


@final
class FPSDisplay(PygletFPSDisplay):
    def __init__(self, parent_viewport):
        super().__init__(WINDOW)
        self.label = FPSLabel(parent_viewport)
        self.screen_resolution = (0, 0)
        self.on_window_resize_handlers = [self.on_window_resize, self.label.on_window_resize]

    def set_fps(self, fps):
        self.label.on_update_args((int(fps), ))

    @window_size_has_changed
    def on_window_resize(self, width, height):
        self.screen_resolution = width, height

    def on_update_opacity(self, new_opacity):
        self.label.on_update_opacity(new_opacity)

    def on_activate(self):
        self.label.create()

    def on_deactivate(self):
        self.label.delete()
