from pyglet.text import Label

from .view_base import View


def _view_is_active(fn):
    def _handle_if_view_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_activated


def _view_is_not_active(fn):
    def _handle_if_view_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_not_activated


class FPSView(View):
    def __init__(self, user_db_cursor, config_db_cursor, surface, batch, groups):
        super().__init__(user_db_cursor, config_db_cursor, surface, batch, groups)
        self.fps_label = None
        self.screen_resolution = (1280, 720)

    def on_update(self):
        pass

    @_view_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.fps_label = Label(text='0 FPS', font_name='Courier New', font_size=16,
                               x=self.screen_resolution[0] - 110, y=self.screen_resolution[1] - 17,
                               anchor_x='right', anchor_y='center', batch=self.batch, group=self.groups['button_text'])

    @_view_is_active
    def on_deactivate(self):
        self.is_activated = False
        self.fps_label.delete()
        self.fps_label = None

    def on_update_fps(self, fps):
        self.fps_label.text = f'{fps} FPS'

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.fps_label.delete()
        self.fps_label = None
        self.fps_label = Label(text='0 FPS', font_name='Courier New', font_size=16,
                               x=self.screen_resolution[0] - 110, y=self.screen_resolution[1] - 17,
                               anchor_x='right', anchor_y='center', batch=self.batch, group=self.groups['button_text'])
