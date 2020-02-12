from abc import ABC

from pyglet.text.document import FormattedDocument
from pyglet.text.layout import IncrementalTextLayout

from ui import *
from database import USER_DB_CURSOR


def page_is_active(fn):
    def _handle_if_page_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_page_is_activated


def cursor_is_inside_the_text_box(fn):
    def _handle_scroll_if_cursor_is_inside_the_text_box(*args, **kwargs):
        if args[0].viewport.x1 < args[1] < args[0].viewport.x2 and args[0].viewport.y1 < args[2] < args[0].viewport.y2:
            fn(*args, **kwargs)

    return _handle_scroll_if_cursor_is_inside_the_text_box


class LicensePage(ABC):
    def __init__(self, logger, parent_viewport):
        self.is_activated = False
        self.logger = logger
        self.parent_viewport = parent_viewport
        self.viewport = Viewport()
        self.screen_resolution = (0, 0)
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.license_text = ''
        self.document = None
        self.license_layout = None
        self.opacity = 0
        self.on_resize_handlers = [self.on_resize, ]

    @final
    def on_activate(self):
        self.is_activated = True
        if self.document is None:
            self.document = FormattedDocument(text=self.license_text)

        self.document.set_style(0, len(self.document.text), {
            'font_name': 'Arial',
            'font_size': get_bottom_bar_height(self.screen_resolution) // 5,
            'bold': False,
            'italic': False,
            'color': (*WHITE_RGB, self.opacity),
            'align': 'center'
        })
        self.license_layout = IncrementalTextLayout(document=self.document,
                                                    width=self.viewport.x2 - self.viewport.x1,
                                                    height=self.viewport.y2 - self.viewport.y1,
                                                    multiline=True, batch=BATCHES['ui_batch'],
                                                    group=GROUPS['button_text'])
        self.license_layout.x, self.license_layout.y = self.viewport.x1, self.viewport.y1

    @final
    def on_deactivate(self, instant=False):
        self.is_activated = False
        if instant:
            self.opacity = 0
            self.license_layout.delete()
            self.license_layout = None

    @final
    @window_size_has_changed
    def on_resize(self, width, height):
        self.screen_resolution = width, height
        self.viewport.x1, self.viewport.x2 = self.parent_viewport.x1, self.parent_viewport.x2
        self.viewport.y1 = self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution)
        self.viewport.y2 = self.parent_viewport.y2
        if self.is_activated:
            self.license_layout.x, self.license_layout.y = self.viewport.x1, self.viewport.y1
            self.license_layout.width = self.viewport.x2 - self.viewport.x1
            self.license_layout.height = self.viewport.y2 - self.viewport.y1
            self.document.set_style(0, len(self.document.text), {
                'font_size': get_bottom_bar_height(self.screen_resolution) // 5
            })

    def on_update_current_locale(self, new_locale):
        pass

    @final
    @page_is_active
    @cursor_is_inside_the_text_box
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.license_layout.view_y += scroll_y * self.document.get_style('font_size')

    @final
    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        if self.opacity <= 0:
            self.license_layout.delete()
            self.license_layout = None
        else:
            if self.document is not None:
                self.document.set_style(0, len(self.document.text), {
                    'color': (*WHITE_RGB, self.opacity)
                })
