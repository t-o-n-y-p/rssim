from pyglet.text.document import FormattedDocument
from pyglet.text.layout import ScrollableTextLayout

from ui import SURFACE, BATCHES, GROUPS


class LicensePage:
    def __init__(self, current_locale, logger):
        self.is_activated = False
        self.logger = logger
        self.screen_resolution = (1280, 720)
        self.position = (0, 0)
        self.size = (0, 0)
        self.surface, self.batches, self.groups, self.current_locale = SURFACE, BATCHES, GROUPS, current_locale
        self.license_text = ''
        self.document = None
        self.license_layout = None

    def on_activate(self):
        self.is_activated = True
        self.document = FormattedDocument(text=self.license_text)
        self.document.set_style(0, len(self.document.text), {
            'font_name': 'Arial',
            'font_size': int(72 / 1280 * self.screen_resolution[0]) // 5,
            'bold': False,
            'italic': False,
            'color': (255, 255, 255, 255),
            'align': 'center'
        })
        self.license_layout = ScrollableTextLayout(document=self.document, width=self.size[0], height=self.size[1],
                                                   multiline=True, batch=self.batches['ui_batch'],
                                                   group=self.groups['button_text'])
        self.license_layout.x, self.license_layout.y = self.position

    def on_deactivate(self):
        self.is_activated = False
        self.license_layout.delete()
        self.license_layout = None

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        bottom_bar_height = int(72 / 1280 * self.screen_resolution[0])
        self.size = (int(6.875 * bottom_bar_height) * 2 + bottom_bar_height // 4, 15 * bottom_bar_height // 4)
        self.position = ((self.screen_resolution[0] - self.size[0]) // 2,
                         (self.screen_resolution[1] - self.size[1]
                          - bottom_bar_height - 3 * bottom_bar_height // 2) // 2
                         + bottom_bar_height + bottom_bar_height)
        if self.is_activated:
            self.license_layout.x, self.license_layout.y = self.position
            self.license_layout.width, self.license_layout.height = self.size
            self.document.set_style(0, len(self.document.text), {
                'font_name': 'Arial',
                'font_size': int(72 / 1280 * self.screen_resolution[0]) // 5,
                'bold': False,
                'italic': False,
                'color': (255, 255, 255, 255),
                'align': 'center'
            })

    def on_update_current_locale(self, new_locale):
        pass
