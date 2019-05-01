from pyglet.text.document import FormattedDocument
from pyglet.text.layout import IncrementalTextLayout

from ui import *
from database import USER_DB_CURSOR


def page_is_active(fn):
    """
    Use this decorator to execute function only if page is active.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_page_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_page_is_activated


def cursor_is_inside_the_text_box(fn):
    """
    Use this decorator to execute function only if mouse cursor is inside license text box.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_scroll_if_cursor_is_inside_the_text_box(*args, **kwargs):
        if args[0].position[0] < args[1] < args[0].position[0] + args[0].size[0] \
                and args[0].position[1] < args[2] < args[0].position[1] + args[0].size[1]:
            fn(*args, **kwargs)

    return _handle_scroll_if_cursor_is_inside_the_text_box


class LicensePage:
    """
    Base class for a single license page on license screen.
    """
    def __init__(self, logger):
        """
        Properties:
            logger                              telemetry instance
            surface                             surface to draw all UI objects on
            batches                             batches to group all labels and sprites
            groups                              defines drawing layers (some labels and sprites behind others)
            is_activated                        indicates if page is active
            screen_resolution                   current screen resolution
            current_locale                      current locale selected by player
            position                            absolute position of the text box
            size                                text box size
            license_text                        actual text of the license
            document                            document from the license text
            license_layout                      layout from the license text
            opacity                             current page opacity

        :param logger:                          telemetry instance
        """
        self.is_activated = False
        self.logger = logger
        self.screen_resolution = (1280, 720)
        self.position = (0, 0)
        self.size = (0, 0)
        self.surface, self.batches, self.groups = SURFACE, BATCHES, GROUPS
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.license_text = ''
        self.document = None
        self.license_layout = None
        self.opacity = 0

    def on_activate(self):
        """
        Activates the page, creates document and layout if not exist.
        """
        self.is_activated = True
        if self.document is None:
            self.document = FormattedDocument(text=self.license_text)

        self.document.set_style(0, len(self.document.text), {
            'font_name': 'Arial',
            'font_size': int(72 / 1280 * self.screen_resolution[0]) // 5,
            'bold': False,
            'italic': False,
            'color': (*WHITE_RGB, self.opacity),
            'align': 'center'
        })
        self.license_layout = IncrementalTextLayout(document=self.document, width=self.size[0], height=self.size[1],
                                                    multiline=True, batch=self.batches['ui_batch'],
                                                    group=self.groups['button_text'])
        self.license_layout.x, self.license_layout.y = self.position

    def on_deactivate(self, instant=False):
        """
        Deactivates the page. Removes layout from the graphics memory.

        :param instant:                 indicates if page should be deactivated with zero opacity straight away
        """
        self.is_activated = False
        if instant:
            self.opacity = 0
            self.license_layout.delete()
            self.license_layout = None

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
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
                'font_size': int(72 / 1280 * self.screen_resolution[0]) // 5
            })

    def on_update_current_locale(self, new_locale):
        """
        Not used at the moment, licenses are not localized.
        """
        pass

    @page_is_active
    @cursor_is_inside_the_text_box
    def handle_mouse_scroll(self, x, y, scroll_x, scroll_y):
        """
        Scrolls license text when user moves mouse wheel.

        :param x:               mouse cursor X position
        :param y:               mouse cursor Y position
        :param scroll_x:        number of “clicks” the horizontal wheel moved
        :param scroll_y:        number of “clicks” the vertical wheel moved
        """
        self.license_layout.view_y += scroll_y * self.document.get_style('font_size')

    def on_update_opacity(self, new_opacity):
        """
        Updates page opacity with given value.

        :param new_opacity:                     new opacity value
        """
        self.opacity = new_opacity
        self.on_update_sprite_opacity()

    def on_update_sprite_opacity(self):
        """
        Applies new opacity value to all sprites and labels.
        """
        if self.opacity <= 0:
            self.license_layout.delete()
            self.license_layout = None
        else:
            self.document.set_style(0, len(self.document.text), {
                'color': (*WHITE_RGB, self.opacity)
            })
