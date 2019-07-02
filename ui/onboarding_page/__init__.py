from pyglet.text import Label

from ui import *
from database import USER_DB_CURSOR
from i18n import I18N_RESOURCES


class OnboardingPage:
    def __init__(self, logger):
        self.logger = logger
        self.is_activated = False
        self.screen_resolution = (1280, 720)
        self.position = (0, 0)
        self.size = (0, 0)
        self.surface, self.batches, self.groups = SURFACE, BATCHES, GROUPS
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.help_text_key = None
        self.help_label = None
        self.opacity = 0

    def on_activate(self):
        """
        Activates the page, creates app window frame and label if not exist.
        """
        self.is_activated = True
        if self.help_label is None:
            self.help_label = Label(I18N_RESOURCES[self.help_text_key][self.current_locale], font_name='Arial',
                                    font_size=int(72 / 1280 * self.screen_resolution[0]) // 5,
                                    color=(*WHITE_RGB, self.opacity),
                                    x=self.screen_resolution[0] // 2 + self.size[0] // 4,
                                    y=self.position[1] + self.size[1] // 2, width=7 * self.size[0] // 16,
                                    anchor_x='center', anchor_y='center',
                                    align='center', multiline=True,
                                    batch=self.batches['ui_batch'], group=self.groups['button_text'])

    def on_deactivate(self, instant=False):
        """
        Deactivates the page. Removes label and frame from the graphics memory.

        :param instant:                 indicates if page should be deactivated with zero opacity straight away
        """
        self.is_activated = False
        if instant:
            self.opacity = 0
            self.help_label.delete()
            self.help_label = None

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
            self.help_label.x, self.help_label.y \
                = self.screen_resolution[0] // 2 + self.size[0] // 4, self.position[1] + self.size[1] // 2
            self.help_label.font_size = int(72 / 1280 * self.screen_resolution[0]) // 5
            self.help_label.width = 7 * self.size[0] // 16

    def on_update_current_locale(self, new_locale):
        """
        Updates onboarding text according to new locale.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        if self.help_label is not None:
            self.help_label.text = I18N_RESOURCES[self.help_text_key][self.current_locale]

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
            self.help_label.delete()
            self.help_label = None
        else:
            self.help_label.color = (*WHITE_RGB, self.opacity)
