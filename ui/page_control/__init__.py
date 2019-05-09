from pyglet.text import Label
from pyglet.gl import GL_QUADS

from i18n import I18N_RESOURCES
from ui import *
from ui.button.previous_page_button import PreviousPageButton
from ui.button.next_page_button import NextPageButton
from database import USER_DB_CURSOR


def shader_sprite_exists(fn):
    """
    Use this decorator to execute function only if shader sprite property is not None.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_shader_sprite_exists(*args, **kwargs):
        if args[0].shader_sprite is not None:
            fn(*args, **kwargs)

    return _handle_if_shader_sprite_exists


class PageControl:
    """
    Implements base class for page controls.
    """
    def __init__(self, logger):
        """
        Button click handlers:
            on_navigate_to_previous_page        on_click handler for previous page button
            on_navigate_to_next_page            on_click handler for next page button

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
            pages                               list of all pages inside the control
            current_page                        number of currently selected page
            current_page_label_key              resource key for current page label
            current_page_label                  indicates number of the current page and number of pages for player
            previous_page_button                PreviousPageButton object
            next_page_button                    NextPageButton object
            buttons                             list of all buttons
            opacity                             current page opacity

        :param logger:                          telemetry instance
        """
        def on_navigate_to_previous_page(button):
            """
            Closes the current page and opens the previous page.

            :param button:                      button that was clicked
            """
            self.pages[self.current_page - 1].opacity = self.pages[self.current_page].opacity
            self.pages[self.current_page].on_deactivate(instant=True)
            self.current_page -= 1
            self.pages[self.current_page].on_activate()
            self.current_page_label.text = I18N_RESOURCES[self.current_page_label_key][self.current_locale] \
                .format(self.current_page + 1, len(self.pages))
            self.on_update_page_control_buttons()

        def on_navigate_to_next_page(button):
            """
            Closes the current page and opens the next page.

            :param button:                      button that was clicked
            """
            self.pages[self.current_page + 1].opacity = self.pages[self.current_page].opacity
            self.pages[self.current_page].on_deactivate(instant=True)
            self.current_page += 1
            self.pages[self.current_page].on_activate()
            self.current_page_label.text = I18N_RESOURCES[self.current_page_label_key][self.current_locale] \
                .format(self.current_page + 1, len(self.pages))
            self.on_update_page_control_buttons()

        self.is_activated = False
        self.logger = logger
        self.screen_resolution = (1280, 720)
        self.position = (0, 0)
        self.size = (0, 0)
        self.surface, self.batches, self.groups = SURFACE, BATCHES, GROUPS
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.pages = []
        self.current_page = 0
        self.current_page_label_key = 'page_control_label_string'
        self.current_page_label = None
        self.previous_page_button = PreviousPageButton(on_click_action=on_navigate_to_previous_page)
        self.next_page_button = NextPageButton(on_click_action=on_navigate_to_next_page)
        self.buttons = [self.previous_page_button, self.next_page_button]
        self.shader = None
        self.shader_sprite = None
        self.opacity = 0

    def on_activate(self):
        """
        Activates the control, creates pade indicator, activates start page.
        """
        self.is_activated = True
        self.current_page = 0
        if self.shader_sprite is None:
            self.shader_sprite\
                = self.batches['main_frame'].add(4, GL_QUADS, self.groups['main_frame'],
                                                 ('v2f/static', (-1.0, -1.0, -1.0, 1.0, 1.0, 1.0, 1.0, -1.0)))

        if self.current_page_label is None:
            text = I18N_RESOURCES[self.current_page_label_key][self.current_locale]\
                .format(self.current_page + 1, len(self.pages))
            self.current_page_label \
                = Label(text, font_name='Arial',
                        font_size=int(self.previous_page_button.base_font_size_property
                                      * int(72 / 1280 * self.screen_resolution[0]) // 2),
                        color=(*WHITE_RGB, self.opacity),
                        x=self.screen_resolution[0] // 2,
                        y=self.position[1] + int(72 / 1280 * self.screen_resolution[0]) // 4,
                        anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                        group=self.groups['button_text'])

        self.pages[self.current_page].on_activate()
        self.next_page_button.on_activate()

    def on_deactivate(self):
        """
        Deactivates the control and currently selected page..
        """
        self.is_activated = False
        self.pages[self.current_page].on_deactivate()
        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.screen_resolution = screen_resolution
        bottom_bar_height = int(72 / 1280 * self.screen_resolution[0])
        self.size = (int(6.875 * bottom_bar_height) * 2 + bottom_bar_height // 4, 19 * bottom_bar_height // 4)
        self.position = ((self.screen_resolution[0] - self.size[0]) // 2,
                         (self.screen_resolution[1] - self.size[1] - 3 * bottom_bar_height // 2) // 2
                         + bottom_bar_height)
        for p in self.pages:
            p.on_change_screen_resolution(screen_resolution)

        if self.is_activated:
            self.current_page_label.x = self.screen_resolution[0] // 2
            self.current_page_label.y = self.position[1] + bottom_bar_height // 4
            self.current_page_label.font_size \
                = int(self.previous_page_button.base_font_size_property * bottom_bar_height // 2)

        self.previous_page_button.on_size_changed((bottom_bar_height // 2, bottom_bar_height // 2))
        self.next_page_button.on_size_changed((bottom_bar_height // 2, bottom_bar_height // 2))
        self.previous_page_button.x_margin = self.screen_resolution[0] // 2 - 5 * bottom_bar_height // 2
        self.previous_page_button.y_margin = self.position[1]
        self.next_page_button.x_margin = self.screen_resolution[0] // 2 + bottom_bar_height * 2
        self.next_page_button.y_margin = self.position[1]

    def on_update_page_control_buttons(self):
        """
        Activates and deactivates buttons for next and last pages based on current page number.
        """
        if self.current_page == 0:
            self.previous_page_button.on_deactivate(instant=True)
            self.previous_page_button.state = 'normal'
        else:
            self.previous_page_button.on_activate(instant=True)

        if self.current_page == len(self.pages) - 1:
            self.next_page_button.on_deactivate(instant=True)
            self.next_page_button.state = 'normal'
        else:
            self.next_page_button.on_activate(instant=True)

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        for p in self.pages:
            p.on_update_current_locale(new_locale)

        if self.current_page_label is not None:
            self.current_page_label.text = I18N_RESOURCES[self.current_page_label_key][self.current_locale]\
                .format(self.current_page + 1, len(self.pages))

    def on_update_opacity(self, new_opacity):
        """
        Updates control opacity with given value.

        :param new_opacity:                     new opacity value
        """
        self.opacity = new_opacity
        self.on_update_sprite_opacity()
        self.pages[self.current_page].on_update_opacity(new_opacity)

    def on_update_sprite_opacity(self):
        """
        Applies new opacity value to all sprites and labels.
        """
        if self.opacity <= 0:
            self.shader_sprite.delete()
            self.shader_sprite = None
            self.current_page_label.delete()
            self.current_page_label = None
        else:
            self.current_page_label.color = (*WHITE_RGB, self.opacity)

    def on_apply_shaders_and_draw_vertices(self):
        """
        Activates the shader, initializes all shader uniforms, draws shader sprite and deactivates the shader.
        """
        pass
