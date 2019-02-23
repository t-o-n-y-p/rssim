from logging import getLogger

from pyglet.text import Label

from view import *


class FPSView(View):
    def __init__(self, user_db_cursor, config_db_cursor, surface, batches, groups):
        super().__init__(user_db_cursor, config_db_cursor, surface, batches, groups,
                         logger=getLogger('root.app.fps.view'))
        self.fps_label = None

    @view_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.fps_label = Label(text='0 FPS', font_name='Courier New', font_size=int(16 / 40 * self.top_bar_height),
                               x=self.screen_resolution[0] - self.top_bar_height * 3 - 10,
                               y=self.screen_resolution[1] - self.top_bar_height // 2,
                               anchor_x='right', anchor_y='center', batch=self.batches['ui_batch'],
                               group=self.groups['button_text'])

    @view_is_active
    def on_deactivate(self):
        self.is_activated = False
        self.fps_label.delete()
        self.fps_label = None

    @view_is_active
    def on_update_fps(self, fps):
        self.fps_label.text = f'{fps} FPS'

    def on_change_screen_resolution(self, screen_resolution):
        self.on_recalculate_ui_properties(screen_resolution)
        self.fps_label.x = self.screen_resolution[0] - self.top_bar_height * 3 - 10
        self.fps_label.y = self.screen_resolution[1] - self.top_bar_height // 2
        self.fps_label.font_size = int(16 / 40 * self.top_bar_height)
