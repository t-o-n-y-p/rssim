from logging import getLogger

from pyglet.text import Label

from view import *
from ui.button.create_station_button import CreateStationButton
from i18n import I18N_RESOURCES


class MainMenuView(View):
    def __init__(self):
        def on_create_station(button):
            button.on_deactivate()
            self.controller.on_deactivate()
            self.controller.parent_controller.on_resume_game()
            self.controller.parent_controller.on_activate_game_view()

        super().__init__(logger=getLogger('root.app.main_menu.view'))
        self.create_station_button = CreateStationButton(on_click_action=on_create_station)
        self.buttons = [self.create_station_button, ]
        self.create_station_button_label = None
        self.on_init_graphics()

    def on_init_graphics(self):
        self.on_change_screen_resolution(self.screen_resolution)

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.is_activated = True
        self.create_station_button_label = Label(I18N_RESOURCES['create_station_label_string'][self.current_locale],
                                                 font_name='Perfo', bold=True,
                                                 font_size=3 * self.bottom_bar_height // 8,
                                                 x=self.screen_resolution[0] // 2,
                                                 y=self.screen_resolution[1] // 2
                                                   + int(72 / 1280 * self.screen_resolution[0]) // 4,
                                                 anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                                                 group=self.groups['button_text'])
        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
        """
        self.is_activated = False
        self.create_station_button_label.delete()
        self.create_station_button_label = None
        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.on_recalculate_ui_properties(screen_resolution)
        medium_line = self.screen_resolution[1] // 2 + int(72 / 1280 * self.screen_resolution[0]) // 4
        if self.is_activated:
            self.create_station_button_label.x = self.screen_resolution[0] // 2
            self.create_station_button_label.y = medium_line
            self.create_station_button_label.font_size = 3 * self.bottom_bar_height // 8

        self.create_station_button.on_size_changed((self.bottom_bar_height * 7, self.bottom_bar_height))
        self.create_station_button.x_margin = self.screen_resolution[0] // 2 - self.bottom_bar_height * 7 // 2
        self.create_station_button.y_margin = medium_line - self.bottom_bar_height // 2
        for b in self.buttons:
            b.on_position_changed((b.x_margin, b.y_margin))

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        if self.is_activated:
            self.create_station_button_label.text = I18N_RESOURCES['create_station_label_string'][self.current_locale]
