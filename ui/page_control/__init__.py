from pyglet.text import Label

from i18n import I18N_RESOURCES
from ui import SURFACE, BATCHES, GROUPS
from ui.button.previous_page_button import PreviousPageButton
from ui.button.next_page_button import NextPageButton


class PageControl:
    def __init__(self, current_locale, logger):
        def on_navigate_to_previous_page(button):
            self.pages[self.current_page].on_deactivate()
            self.current_page -= 1
            self.pages[self.current_page].on_activate()
            self.current_page_label.text = I18N_RESOURCES[self.current_page_label_key][self.current_locale] \
                .format(self.current_page + 1, len(self.pages))
            self.on_update_page_control_buttons()

        def on_navigate_to_next_page(button):
            self.pages[self.current_page].on_deactivate()
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
        self.surface, self.batches, self.groups, self.current_locale = SURFACE, BATCHES, GROUPS, current_locale
        self.pages = []
        self.current_page = 0
        self.current_page_label_key = 'page_control_label_string'
        self.current_page_label = None
        self.previous_page_button = PreviousPageButton(on_click_action=on_navigate_to_previous_page)
        self.next_page_button = NextPageButton(on_click_action=on_navigate_to_next_page)
        self.buttons = [self.previous_page_button, self.next_page_button]

    def on_activate(self):
        self.is_activated = True
        self.current_page = 0
        text = I18N_RESOURCES[self.current_page_label_key][self.current_locale]\
            .format(self.current_page + 1, len(self.pages))
        self.current_page_label \
            = Label(text, font_name='Arial',
                    font_size=int(self.previous_page_button.base_font_size_property
                                  * int(72 / 1280 * self.screen_resolution[0]) // 2),
                    x=self.screen_resolution[0] // 2,
                    y=self.position[0] + int(72 / 1280 * self.screen_resolution[0]) // 4,
                    anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                    group=self.groups['button_text'])
        self.pages[self.current_page].on_activate()
        self.next_page_button.on_activate()

    def on_deactivate(self):
        self.is_activated = False
        self.current_page_label.delete()
        self.current_page_label = None
        self.pages[self.current_page].on_deactivate()
        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
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
            self.current_page_label.y = self.position[0] + bottom_bar_height // 4
            self.current_page_label.font_size \
                = int(self.previous_page_button.base_font_size_property * bottom_bar_height // 2)

        self.previous_page_button.on_size_changed((bottom_bar_height // 2, bottom_bar_height // 2))
        self.next_page_button.on_size_changed((bottom_bar_height // 2, bottom_bar_height // 2))
        self.previous_page_button.x_margin = self.screen_resolution[0] // 2 - 5 * bottom_bar_height // 2
        self.previous_page_button.y_margin = self.position[1]
        self.next_page_button.x_margin = self.screen_resolution[0] // 2 + bottom_bar_height * 2
        self.next_page_button.y_margin = self.position[1]

    def on_update_page_control_buttons(self):
        if self.current_page == 0:
            self.previous_page_button.on_deactivate()
        else:
            self.previous_page_button.on_activate()

        if self.current_page == len(self.pages) - 1:
            self.next_page_button.on_deactivate()
        else:
            self.next_page_button.on_activate()
