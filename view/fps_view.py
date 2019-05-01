from logging import getLogger

from pyglet.text import Label

from view import *


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
        self.fps_label = None
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
            self.fps_label = None
        else:
            self.fps_label.color = (*WHITE_RGB, self.opacity)

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.is_activated = True
        if self.fps_label is None:
            self.fps_label = Label(text='0 FPS', font_name='Courier New', font_size=int(16 / 40 * self.top_bar_height),
                                   color=(*WHITE_RGB, self.opacity),
                                   x=self.screen_resolution[0] - self.top_bar_height * 3 - self.top_bar_height // 4,
                                   y=self.screen_resolution[1] - self.top_bar_height // 2,
                                   anchor_x='right', anchor_y='center', batch=self.batches['ui_batch'],
                                   group=self.groups['button_text'])

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
        self.fps_label.text = f'{fps} FPS'

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.on_recalculate_ui_properties(screen_resolution)
        if self.is_activated:
            self.fps_label.x = self.screen_resolution[0] - self.top_bar_height * 3 - self.top_bar_height // 4
            self.fps_label.y = self.screen_resolution[1] - self.top_bar_height // 2
            self.fps_label.font_size = int(16 / 40 * self.top_bar_height)

    def on_init_graphics(self):
        """
        Initializes the view based on saved screen resolution and base offset.
        """
        self.on_change_screen_resolution(self.screen_resolution)
