from pyglet.text import Label

from .view_base import View


class FPSView(View):
    def __init__(self, surface, batch, groups):
        super().__init__(surface, batch, groups)
        self.fps_label = None
        self.screen_resolution = (1280, 720)

    def on_update(self):
        pass

    def on_activate(self):
        self.is_activated = True
        self.fps_label = Label(text='0 FPS', font_name='Courier New', font_size=16,
                               x=self.screen_resolution[0] - 110, y=self.screen_resolution[1] - 17,
                               anchor_x='right', anchor_y='center', batch=self.batch, group=self.groups['button_text'])

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
