from pyglet.window import FPSDisplay as PygletFPSDisplay

from ui import *
from ui.label.fps_label import FPSLabel


@final
class FPSDisplay(PygletFPSDisplay):
    def __init__(self, parent_viewport):
        super().__init__(WINDOW)
        self.label = FPSLabel(parent_viewport)
        self.screen_resolution = (1280, 720)

    def set_fps(self, fps):
        self.label.on_update_args((int(fps), ))

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.label.on_change_screen_resolution(screen_resolution)

    def on_update_opacity(self, new_opacity):
        self.label.on_update_opacity(new_opacity)

    def on_activate(self):
        self.label.create()

    def on_deactivate(self):
        self.label.delete()
