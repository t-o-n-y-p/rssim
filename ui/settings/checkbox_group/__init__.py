from pyglet.text import Label

from i18n import I18N_RESOURCES
from ui import *


class CheckboxGroup:
    """
    Implements base class for all checkbox groups in the app.
    """
    def __init__(self, column, row, current_locale, logger):
        """
        Properties:
            logger                              telemetry instance
            column                              number of settings column
            row                                 number of settings row
            surface                             surface to draw all UI objects on
            batches                             batches to group all labels and sprites
            groups                              defines drawing layers (some labels and sprites behind others)
            current_locale                      current locale selected by player
            screen_resolution                   current game window resolution
            anchor_left_center_point            left center point of settings screen cell
            height                              settings cell height
            description_key                     resource key for checkbox description
            description_label                   text label for checkbox description
            is_activated                        indicates if checkbox is activated or not
            checkboxes                          list of all checkboxes in the group
            buttons                             list of all checkbox buttons
            opacity                             current checkbox group opacity

        :param column:                          number of settings column
        :param row:                             number of settings row
        :param current_locale:                  current locale selected by player
        :param logger:                          telemetry instance
        """
        self.logger = logger
        self.column, self.row = column, row
        self.surface, self.batches, self.groups, self.current_locale = SURFACE, BATCHES, GROUPS, current_locale
        self.description_key = None
        self.description_label = None
        self.checkboxes = []
        self.buttons = []
        self.is_activated = False
        self.screen_resolution = (1280, 720)
        self.anchor_left_center_point = (0, 0)
        self.height = 0
        self.opacity = 0

    def on_update_opacity(self, new_opacity):
        """
        Updates group opacity with given value.

        :param new_opacity:                     new opacity value
        """
        self.opacity = new_opacity
        self.on_update_sprite_opacity()
        for checkbox in self.checkboxes:
            checkbox.on_update_opacity(new_opacity)

    def on_update_sprite_opacity(self):
        """
        Applies new opacity value to all sprites and labels.
        """
        if self.opacity <= 0:
            self.description_label.delete()
            self.description_label = None
        else:
            self.description_label.color = (*WHITE_RGB, self.opacity)

    def on_activate(self):
        """
        Activates the checkbox group, creates description label and activates checkboxes.
        """
        self.is_activated = True
        if self.description_label is None:
            self.description_label = Label(I18N_RESOURCES[self.description_key][self.current_locale],
                                           font_name='Arial', font_size=self.height // 5 * 2,
                                           color=(*WHITE_RGB, self.opacity),
                                           x=self.anchor_left_center_point[0] + self.screen_resolution[0] // 4,
                                           y=self.anchor_left_center_point[1], anchor_x='center', anchor_y='center',
                                           batch=self.batches['ui_batch'], group=self.groups['button_text'])

        for checkbox in self.checkboxes:
            checkbox.on_activate()

    def on_init_state(self, checkbox_state_list):
        """
        Activates checkbox buttons depending on initial state of the checkboxes.

        :param checkbox_state_list:                   list of checkbox initial state flags
        """
        for i in range(len(self.checkboxes)):
            self.checkboxes[i].on_init_state(checkbox_state_list[i])

    def on_deactivate(self):
        """
        Deactivates the checkbox group, deletes all labels, deactivates all buttons and checkboxes.
        """
        self.is_activated = False
        for checkbox in self.checkboxes:
            checkbox.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.screen_resolution = screen_resolution
        medium_line = self.screen_resolution[1] // 2 + int(72 / 1280 * self.screen_resolution[0]) // 4
        self.height = int(72 / 1280 * self.screen_resolution[0]) // 2
        row_step = 5 * self.height // 8
        column_step = self.screen_resolution[0] // 4
        self.anchor_left_center_point = (self.screen_resolution[0] // 4 + self.column * column_step,
                                         medium_line + self.row * row_step)
        if self.description_label is not None:
            self.description_label.x = self.anchor_left_center_point[0] + self.screen_resolution[0] // 4
            self.description_label.y = self.anchor_left_center_point[1]
            self.description_label.font_size = self.height // 5 * 2

        for checkbox in self.checkboxes:
            checkbox.on_change_screen_resolution(screen_resolution)

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        if self.description_label is not None:
            self.description_label.text = I18N_RESOURCES[self.description_key][self.current_locale]

        for checkbox in self.checkboxes:
            checkbox.on_update_current_locale(new_locale)
