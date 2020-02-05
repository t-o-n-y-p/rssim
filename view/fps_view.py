from logging import getLogger

from view import *
from ui.label.fps_label import FPSLabel


@final
class FPSView(AppBaseView):
    def __init__(self, controller):
        super().__init__(controller, logger=getLogger('root.app.fps.view'))
        self.fps_label = FPSLabel(parent_viewport=self.viewport)

    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        self.fps_label.create()

    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()

    @view_is_active
    def on_update(self):
        pass

    @window_size_has_changed
    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.fps_label.on_change_screen_resolution(self.screen_resolution)

    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.fps_label.on_update_opacity(self.opacity)

    @view_is_active
    def on_update_fps(self, fps):
        self.fps_label.on_update_args(new_args=(fps, ))
