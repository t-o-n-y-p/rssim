from logging import getLogger

from pyglet.gl import GL_QUADS
from pyshaders import from_files_names

from view import *
from ui.button.accept_settings_button import AcceptSettingsButton
from ui.button.reject_settings_button import RejectSettingsButton
from ui.settings.enum_value_control.screen_resolution_control import ScreenResolutionControl
from ui.settings.checkbox.display_fps_checkbox import DisplayFPSCheckbox
from ui.settings.checkbox.fade_animations_enabled_checkbox import FadeAnimationsEnabledCheckbox
from ui.settings.checkbox.clock_24h_checkbox import Clock24HCheckbox
from ui.settings.checkbox_group.notifications_checkbox_group import NotificationsCheckboxGroup


class SettingsView(View):
    """
    Implements Settings view.
    Settings object is responsible for user-defined settings.
    """
    def __init__(self):
        """
        Settings are located within the grid.
        Columns indexes are -1 (left part of the screen), 0 (middle) and 1 (right part of the screen).
        Row indexes start from middle line, distance between rows is top_bar_height * 5/8.
        All settings inside the same column must use only odd or only even row numbers.

        Button click handlers:
            on_accept_changes                   on_click handler for accept changes button
            on_reject_changes                   on_click handler for reject changes button

        Action handlers for controls:
            on_update_windowed_resolution_state     is activated when player changes screen resolution inside control
            on_update_display_fps_state             is activated when player turns FPS on/off
            on_update_fade_animations_state         is activated when player turns fade animations on/off
            on_update_clock_24h_state               is activated when player turns 24h clock on/off
            on_update_level_up_notifications_state
                                            is activated when player turns level up notifications on/off
            on_update_feature_unlocked_notifications_state
                                            is activated when player turns feature unlocked notifications on/off
            on_update_construction_completed_notifications_state
                                            is activated when player turns construction completed notifications on/off
            on_update_enough_money_notifications_state
                                            is activated when player turns enough money notifications on/off

        Properties:
            temp_windowed_resolution            windowed resolution selected by player
            temp_display_fps                    display_fps flag value selected by player
            temp_fade_animations_enabled        fade_animations_enabled flag value selected by player
            temp_clock_24h_enabled              clock_24h_enabled flag value selected by player
            display_fps_checkbox                DisplayFPSCheckbox object
            fade_animations_checkbox            FadeAnimationsEnabledCheckbox object
            clock_24h_checkbox                  Clock24HCheckbox object
            temp_level_up_notification_enabled
                                            level_up_notification_enabled flag value selected by player
            temp_feature_unlocked_notification_enabled
                                            feature_unlocked_notification_enabled flag value selected by player
            temp_construction_completed_notification_enabled
                                            construction_completed_notification_enabled flag value selected by player
            temp_enough_money_notification_enabled
                                            enough_money_notification_enabled flag value selected by player
            notifications_checkbox_group        NotificationsCheckboxGroup object
            temp_log_level                      log level selected by player
            settings_opacity                    general opacity for settings screen
            available_windowed_resolutions      list of screen resolutions available for windowed mode
            available_windowed_resolutions_position
                                            index of screen resolution selected by player
            screen_resolution_control           ScreenResolutionControl object
            accept_settings_button              AcceptSettingsButton object
            reject_settings_button              RejectSettingsButton object
            buttons                             list of all buttons

        """
        def on_accept_changes(button):
            """
            Notifies controller that player accepts changes.

            :param button:                      button that was clicked
            """
            self.controller.on_save_and_commit_state()
            if self.controller.navigated_from_main_menu:
                self.controller.navigated_from_main_menu = False

            if self.controller.navigated_from_game:
                self.controller.navigated_from_game = False
                self.controller.parent_controller.game_to_settings_transition_animation.on_deactivate()
                self.controller.parent_controller.settings_to_game_transition_animation.on_activate()

        def on_reject_changes(button):
            """
            Notifies controller that player rejects changes.

            :param button:                      button that was clicked
            """
            if self.controller.navigated_from_main_menu:
                self.controller.navigated_from_main_menu = False

            if self.controller.navigated_from_game:
                self.controller.navigated_from_game = False
                self.controller.parent_controller.game_to_settings_transition_animation.on_deactivate()
                self.controller.parent_controller.settings_to_game_transition_animation.on_activate()

        def on_update_windowed_resolution_state(index):
            """
            Updates temp windowed resolution value when player uses value control.

            :param index:                       index from available resolutions list
            """
            self.on_change_temp_windowed_resolution(self.available_windowed_resolutions[index])

        def on_update_display_fps_state(new_state):
            """
            Updates temp_display_fps flag value when player uses corresponding checkbox.

            :param new_state:                   new flag value
            """
            self.temp_display_fps = new_state

        def on_update_fade_animations_state(new_state):
            """
            Updates temp_fade_animations_enabled flag value when player uses corresponding checkbox.

            :param new_state:                   new flag value
            """
            self.temp_fade_animations_enabled = new_state

        def on_update_clock_24h_state(new_state):
            """
            Updates temp_clock_24h_enabled flag value when player uses corresponding checkbox.

            :param new_state:                   new flag value
            """
            self.temp_clock_24h_enabled = new_state

        def on_update_level_up_notifications_state(new_state):
            """
            Updates temp_level_up_notification_enabled flag value
            when player uses corresponding checkbox.

            :param new_state:                   new flag value
            """
            self.temp_level_up_notification_enabled = new_state

        def on_update_feature_unlocked_notifications_state(new_state):
            """
            Updates temp_feature_unlocked_notification_enabled flag value
            when player uses corresponding checkbox.

            :param new_state:                   new flag value
            """
            self.temp_feature_unlocked_notification_enabled = new_state

        def on_update_construction_completed_notifications_state(new_state):
            """
            Updates temp_construction_completed_notification_enabled flag value
            when player uses corresponding checkbox.

            :param new_state:                   new flag value
            """
            self.temp_construction_completed_notification_enabled = new_state

        def on_update_enough_money_notifications_state(new_state):
            """
            Updates temp_enough_money_notification_enabled flag value
            when player uses corresponding checkbox.

            :param new_state:                   new flag value
            """
            self.temp_enough_money_notification_enabled = new_state

        super().__init__(logger=getLogger('root.app.settings.view'))
        self.temp_windowed_resolution = (0, 0)
        self.temp_display_fps = False
        self.temp_fade_animations_enabled = False
        self.temp_clock_24h_enabled = False
        self.display_fps_checkbox \
            = DisplayFPSCheckbox(-1, -1, on_update_state_action=on_update_display_fps_state)
        self.fade_animations_checkbox \
            = FadeAnimationsEnabledCheckbox(-1, -3, on_update_state_action=on_update_fade_animations_state)
        self.clock_24h_checkbox = Clock24HCheckbox(-1, -5, on_update_state_action=on_update_clock_24h_state)
        self.temp_level_up_notification_enabled = False
        self.temp_feature_unlocked_notification_enabled = False
        self.temp_construction_completed_notification_enabled = False
        self.temp_enough_money_notification_enabled = False
        self.notifications_checkbox_group \
            = NotificationsCheckboxGroup(1, 4,
                                         on_update_state_actions=[on_update_level_up_notifications_state,
                                                                  on_update_feature_unlocked_notifications_state,
                                                                  on_update_construction_completed_notifications_state,
                                                                  on_update_enough_money_notifications_state])
        self.temp_log_level = 0
        self.config_db_cursor.execute('''SELECT app_width, app_height FROM screen_resolution_config 
                                         WHERE manual_setup = 1 AND app_width <= ?''',
                                      (windll.user32.GetSystemMetrics(0),))
        self.available_windowed_resolutions = self.config_db_cursor.fetchall()
        self.available_windowed_resolutions_position = 0
        self.screen_resolution_control \
            = ScreenResolutionControl(-1, 5, possible_values_list=self.available_windowed_resolutions,
                                      on_update_state_action=on_update_windowed_resolution_state)
        self.accept_settings_button = AcceptSettingsButton(on_click_action=on_accept_changes)
        self.reject_settings_button = RejectSettingsButton(on_click_action=on_reject_changes)
        self.buttons = [self.accept_settings_button, self.reject_settings_button,
                        *self.screen_resolution_control.buttons, *self.display_fps_checkbox.buttons,
                        *self.fade_animations_checkbox.buttons, *self.clock_24h_checkbox.buttons,
                        *self.notifications_checkbox_group.buttons]
        self.shader = from_files_names('shaders/shader.vert', 'shaders/settings_view/shader.frag')
        self.shader_sprite = None
        self.on_init_graphics()

    def on_update_opacity(self, new_opacity):
        """
        Updates view opacity with given value.

        :param new_opacity:                     new opacity value
        """
        self.opacity = new_opacity
        self.on_update_sprite_opacity()
        self.screen_resolution_control.on_update_opacity(new_opacity)
        self.display_fps_checkbox.on_update_opacity(new_opacity)
        self.fade_animations_checkbox.on_update_opacity(new_opacity)
        self.clock_24h_checkbox.on_update_opacity(new_opacity)
        self.notifications_checkbox_group.on_update_opacity(new_opacity)
        for b in self.buttons:
            b.on_update_opacity(new_opacity)

    def on_update_sprite_opacity(self):
        """
        Applies new opacity value to all sprites and labels.
        """
        if self.opacity <= 0:
            self.shader_sprite.delete()
            self.shader_sprite = None

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.is_activated = True
        self.screen_resolution_control.on_activate()
        self.screen_resolution_control.on_init_state(self.available_windowed_resolutions_position)
        self.display_fps_checkbox.on_activate()
        self.display_fps_checkbox.on_init_state(self.temp_display_fps)
        self.fade_animations_checkbox.on_activate()
        self.fade_animations_checkbox.on_init_state(self.temp_fade_animations_enabled)
        self.clock_24h_checkbox.on_activate()
        self.clock_24h_checkbox.on_init_state(self.temp_clock_24h_enabled)
        self.notifications_checkbox_group.on_activate()
        self.notifications_checkbox_group.on_init_state([self.temp_level_up_notification_enabled,
                                                         self.temp_feature_unlocked_notification_enabled,
                                                         self.temp_construction_completed_notification_enabled,
                                                         self.temp_enough_money_notification_enabled])
        if self.shader_sprite is None:
            self.shader_sprite\
                = self.batches['main_frame'].add(4, GL_QUADS, self.groups['main_frame'],
                                                 ('v2f/static', (-1.0, -1.0, -1.0, 1.0, 1.0, 1.0, 1.0, -1.0)))

        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
        """
        self.is_activated = False
        self.screen_resolution_control.on_deactivate()
        self.display_fps_checkbox.on_deactivate()
        self.fade_animations_checkbox.on_deactivate()
        self.clock_24h_checkbox.on_deactivate()
        self.notifications_checkbox_group.on_deactivate()
        for b in self.buttons:
            b.on_deactivate()
            b.state = 'normal'

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.on_recalculate_ui_properties(screen_resolution)
        self.screen_resolution_control.on_change_screen_resolution(screen_resolution)
        self.display_fps_checkbox.on_change_screen_resolution(screen_resolution)
        self.fade_animations_checkbox.on_change_screen_resolution(screen_resolution)
        self.clock_24h_checkbox.on_change_screen_resolution(screen_resolution)
        self.notifications_checkbox_group.on_change_screen_resolution(screen_resolution)
        self.accept_settings_button.x_margin = self.screen_resolution[0] - self.bottom_bar_height * 2 + 2
        self.accept_settings_button.y_margin = 0
        self.accept_settings_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height))
        self.reject_settings_button.x_margin = self.screen_resolution[0] - self.bottom_bar_height
        self.reject_settings_button.y_margin = 0
        self.reject_settings_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height))
        for b in self.buttons:
            b.on_position_changed((b.x_margin, b.y_margin))

    def on_change_temp_windowed_resolution(self, windowed_resolution):
        """
        Updates temp windowed resolution and text label for it, windowed resolution position.
        Activates and deactivates windowed resolution buttons if needed.

        :param windowed_resolution:             selected windowed resolution
        """
        self.temp_windowed_resolution = windowed_resolution
        self.available_windowed_resolutions_position \
            = self.available_windowed_resolutions.index(self.temp_windowed_resolution)

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        self.screen_resolution_control.on_update_current_locale(new_locale)
        self.display_fps_checkbox.on_update_current_locale(new_locale)
        self.fade_animations_checkbox.on_update_current_locale(new_locale)
        self.clock_24h_checkbox.on_update_current_locale(new_locale)
        self.notifications_checkbox_group.on_update_current_locale(new_locale)

    @shader_sprite_exists
    def on_apply_shaders_and_draw_vertices(self):
        """
        Activates the shader, initializes all shader uniforms, draws shader sprite and deactivates the shader.
        """
        self.shader.use()
        self.shader.uniforms.settings_opacity = self.opacity
        is_button_activated = []
        button_x = []
        button_y = []
        button_w = []
        button_h = []
        for b in self.buttons:
            is_button_activated.append(int(b.is_activated))
            button_x.append(b.position[0])
            button_y.append(b.position[1])
            button_w.append(b.button_size[0])
            button_h.append(b.button_size[1])

        self.shader.uniforms.is_button_activated = is_button_activated
        self.shader.uniforms.button_x = button_x
        self.shader.uniforms.button_y = button_y
        self.shader.uniforms.button_w = button_w
        self.shader.uniforms.button_h = button_h
        self.shader.uniforms.number_of_buttons = len(self.buttons)
        self.shader_sprite.draw(GL_QUADS)
        self.shader.clear()

    def on_init_graphics(self):
        """
        Initializes the view based on saved screen resolution and base offset.
        """
        self.on_change_screen_resolution(self.screen_resolution)
