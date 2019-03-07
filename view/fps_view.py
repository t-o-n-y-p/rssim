from logging import getLogger

from pyglet.text import Label

from view import *


class FPSView(View):
    """
    Implements FPS view.
    FPS object is responsible for real-time FPS calculation.
    """
    def __init__(self, user_db_cursor, config_db_cursor, surface, batches, groups):
        """
        Properties:
            fps_label                           text label for current FPS value

        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        :param surface:                         surface to draw all UI objects on
        :param batches:                         batches to group all labels and sprites
        :param groups:                          defines drawing layers (some labels and sprites behind others)
        """
        super().__init__(user_db_cursor, config_db_cursor, surface, batches, groups,
                         logger=getLogger('root.app.fps.view'))
        self.fps_label = None

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.is_activated = True
        self.fps_label = Label(text='0 FPS', font_name='Courier New', font_size=int(16 / 40 * self.top_bar_height),
                               x=self.screen_resolution[0] - self.top_bar_height * 3 - 10,
                               y=self.screen_resolution[1] - self.top_bar_height // 2,
                               anchor_x='right', anchor_y='center', batch=self.batches['ui_batch'],
                               group=self.groups['button_text'])

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
        """
        self.is_activated = False
        self.fps_label.delete()
        self.fps_label = None

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
            self.fps_label.x = self.screen_resolution[0] - self.top_bar_height * 3 - 10
            self.fps_label.y = self.screen_resolution[1] - self.top_bar_height // 2
            self.fps_label.font_size = int(16 / 40 * self.top_bar_height)
