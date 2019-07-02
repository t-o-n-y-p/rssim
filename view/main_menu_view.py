from logging import getLogger

from view import *
from ui.button.create_station_button import CreateStationButton
from ui.button.back_to_the_station_button import BackToTheStationButton
from ui.button.open_license_button import OpenLicenseButton
from ui.shader_sprite.main_menu_view_shader_sprite import MainMenuViewShaderSprite


class MainMenuView(View):
    """
    Implements MainMenu view.
    MainMenu object is responsible for properties, UI and events related to the main menu screen.
    """
    def __init__(self):
        """
        Button click handlers:
            on_create_station                   on_click handler for create station button
            on_back_to_the_station              on_click handler for back to the station button
            on_open_license                     on_click handler for open license button

        Properties:
            create_station_button               CreateStationButton object
            back_to_the_station_button          BackToTheStationButton
            open_license_button                 OpenLicenseButton object
            buttons                             list of all buttons
            create_station_button_label         label from "Create new station" title
            back_to_the_station_label           label from "Back to the station" title

        """
        def on_create_station(button):
            """
            Performs transition from main menu screen to onboarding screen.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            self.controller.parent_controller.license_to_main_menu_transition_animation.on_deactivate()
            self.controller.parent_controller.game_to_main_menu_transition_animation.on_deactivate()
            self.controller.parent_controller.main_menu_to_onboarding_transition_animation.on_activate()

        def on_back_to_the_station(button):
            """
            Performs transition from main menu screen to game screen.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            self.controller.parent_controller.license_to_main_menu_transition_animation.on_deactivate()
            self.controller.parent_controller.game_to_main_menu_transition_animation.on_deactivate()
            self.controller.parent_controller.main_menu_to_game_transition_animation.on_activate()
            self.controller.parent_controller.on_resume_game()

        def on_open_license(button):
            """
            Performs transition from main menu screen to license screen.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            self.controller.parent_controller.on_open_license()

        super().__init__(logger=getLogger('root.app.main_menu.view'))
        self.create_station_button = CreateStationButton(on_click_action=on_create_station)
        self.back_to_the_station_button = BackToTheStationButton(on_click_action=on_back_to_the_station)
        self.open_license_button = OpenLicenseButton(on_click_action=on_open_license)
        self.buttons = [self.create_station_button, self.back_to_the_station_button, self.open_license_button]
        self.shader_sprite = MainMenuViewShaderSprite(view=self)
        self.on_init_graphics()

    def on_init_graphics(self):
        """
        Initializes the view based on saved screen resolution and base offset.
        """
        self.on_change_screen_resolution(self.screen_resolution)

    def on_update_opacity(self, new_opacity):
        """
        Updates view opacity with given value.

        :param new_opacity:                     new opacity value
        """
        self.opacity = new_opacity
        self.on_update_sprite_opacity()
        for b in self.buttons:
            b.on_update_opacity(new_opacity)

    def on_update_sprite_opacity(self):
        """
        Applies new opacity value to all sprites and labels.
        """
        if self.opacity <= 0:
            self.shader_sprite.delete()

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.is_activated = True
        self.shader_sprite.create()
        self.user_db_cursor.execute('SELECT onboarding_required FROM game_progress')
        onboarding_required = bool(self.user_db_cursor.fetchone()[0])
        if onboarding_required:
            self.create_station_button.on_activate()
        else:
            self.back_to_the_station_button.on_activate()

        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
        """
        self.is_activated = False
        for b in self.buttons:
            b.on_deactivate()
            b.state = 'normal'

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.on_recalculate_ui_properties(screen_resolution)
        self.shader_sprite.on_change_screen_resolution(self.screen_resolution)
        medium_line = self.screen_resolution[1] // 2 + int(72 / 1280 * self.screen_resolution[0]) // 4
        self.open_license_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height))
        self.create_station_button.on_size_changed((self.bottom_bar_height * 7, self.bottom_bar_height))
        self.create_station_button.x_margin = self.screen_resolution[0] // 2 - self.bottom_bar_height * 7 // 2
        self.create_station_button.y_margin = medium_line - self.bottom_bar_height // 2
        self.back_to_the_station_button.on_size_changed((self.bottom_bar_height * 7, self.bottom_bar_height))
        self.back_to_the_station_button.x_margin = self.screen_resolution[0] // 2 - self.bottom_bar_height * 7 // 2
        self.back_to_the_station_button.y_margin = medium_line - self.bottom_bar_height // 2
        for b in self.buttons:
            b.on_position_changed((b.x_margin, b.y_margin))

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        self.create_station_button.on_update_current_locale(new_locale)
        self.back_to_the_station_button.on_update_current_locale(new_locale)

    @shader_sprite_exists
    def on_apply_shaders_and_draw_vertices(self):
        """
        Activates the shader, initializes all shader uniforms, draws shader sprite and deactivates the shader.
        """
        self.shader_sprite.draw()
