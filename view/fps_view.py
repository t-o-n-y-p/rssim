from logging import getLogger

from pyglet.text import Label

from view import *
from ui.label.fps_label import FPSLabel


class FPSView(View):
    """
    Implements FPS view.
    FPS object is responsible for real-time FPS calculation.
    """
    def __init__(self):
        """
        Properties:
            fps_label                           text label for current FPS value

        """
        super().__init__(logger=getLogger('root.app.fps.view'))
        self.fps_label = FPSLabel(args=(0, ))
        self.on_init_graphics()

    def on_update_opacity(self, new_opacity):
        """
        Updates view opacity with given value.

        :param new_opacity:                     new opacity value
        """
        self.opacity = new_opacity
        self.on_update_sprite_opacity()

    def on_update_sprite_opacity(self):
        """
        Applies new opacity value to all sprites and labels.
        """
        if self.opacity <= 0:
            self.fps_label.delete()
        else:
            self.fps_label.on_update_opacity(self.opacity)

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.is_activated = True
        self.fps_label.create()

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
        """
        self.is_activated = False

    @view_is_active
    def on_update_fps(self, fps):
        """
        Updates FPS label text.

        :param fps:                             new FPS value
        """
        self.fps_label.on_update_args(new_args=(fps, ))

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.on_recalculate_ui_properties(screen_resolution)
        self.fps_label.on_change_screen_resolution(screen_resolution)

    def on_init_graphics(self):
        """
        Initializes the view based on saved screen resolution and base offset.
        """
        self.on_change_screen_resolution(self.screen_resolution)
