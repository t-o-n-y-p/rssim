from pyglet.text import Label

from i18n import I18N_RESOURCES


class CheckboxGroup:
    def __init__(self, column, row, surface, batches, groups, current_locale, logger):
        self.logger = logger
        self.column, self.row = column, row
        self.surface, self.batches, self.groups, self.current_locale = surface, batches, groups, current_locale
        self.description_key = None
        self.description_label = None
        self.checkboxes = []
        self.buttons = []
        self.is_activated = False
        self.screen_resolution = (1280, 720)
        self.anchor_left_center_point = (0, 0)
        self.height = 0

    def on_activate(self):
        self.is_activated = True
        self.description_label = Label(I18N_RESOURCES[self.description_key][self.current_locale],
                                       font_name='Arial', font_size=self.height // 5 * 2,
                                       x=self.anchor_left_center_point[0] + self.screen_resolution[0] // 4,
                                       y=self.anchor_left_center_point[1], anchor_x='center', anchor_y='center',
                                       batch=self.batches['ui_batch'], group=self.groups['button_text'])
        for checkbox in self.checkboxes:
            checkbox.on_activate()

    def on_init_state(self, checkbox_state_list):
        for i in range(len(self.checkboxes)):
            self.checkboxes[i].on_init_state(checkbox_state_list[i])

    def on_deactivate(self):
        self.is_activated = False
        self.description_label.delete()
        self.description_label = None
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
