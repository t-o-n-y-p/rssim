from logging import getLogger

from pyglet.text import Label
from pyglet.gl import GL_QUADS
from win32api import GetCursorPos
from win32gui import GetActiveWindow, GetWindowRect, SetWindowPos
from win32con import HWND_TOP, SWP_NOREDRAW

from view import *
from button.close_game_button import CloseGameButton
from button.iconify_game_button import IconifyGameButton
from button.fullscreen_button import FullscreenButton
from button.restore_button import RestoreButton
from button.open_settings_button import OpenSettingsButton


class AppView(View):
    """
    Implements App view.
    App object is responsible for high-level properties, UI and events.
    """
    def __init__(self, user_db_cursor, config_db_cursor, surface, batches, groups):
        """
        Button click handlers:
            on_close_game                       on_click handler for close game button
            on_iconify_game                     on_click handler for iconify game button
            on_app_window_fullscreen            on_click handler for fullscreen button
            on_app_window_restore               on_click handler for restore button
            on_open_settings                    on_click handler for settings button

        Properties:
            title_label                         text label for game title
            main_frame_sprite                   sprite for main frame
            close_game_button                   CloseGameButton object
            iconify_game_button                 IconifyGameButton object
            fullscreen_button                   FullscreenButton object
            restore_button                      RestoreButton object
            open_settings_button                OpenSettingsButton object
            buttons                             list of all buttons
            app_window_move_mode                indicates if player is about to move the app window
            app_window_move_offset              mouse cursor position at the beginning of the app window move
            game_window_handler                 Win32 app window handler
            game_window_position                Win32 app window position
            absolute_mouse_pos                  Win32 mouse cursor position
            on_mouse_press_handlers             list of on_mouse_press event handlers
            on_mouse_release_handlers           list of on_mouse_release event handlers
            on_mouse_drag_handlers              list of on_mouse_drag event handlers

        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        :param surface:                         surface to draw all UI objects on
        :param batches:                         batches to group all labels and sprites
        :param groups:                          defines drawing layers (some labels and sprites behind others)
        """
        def on_close_game(button):
            """
            Notifies controller that player has closed game.

            :param button:                      button that was clicked
            """
            self.controller.on_close_game()

        def on_iconify_game(button):
            """
            Notifies controller that player has minimized game.

            :param button:                      button that was clicked
            """
            self.surface.minimize()

        def on_app_window_fullscreen(button):
            """
            Deactivates fullscreen button. Activates restore button.
            Notifies controller that player has turned on fullscreen mode.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            button.paired_button.on_activate()
            self.controller.on_fullscreen_button_click()

        def on_app_window_restore(button):
            """
            Deactivates restore button. Activates fullscreen button.
            Notifies controller that player has turned off fullscreen mode.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            button.paired_button.on_activate()
            self.controller.on_restore_button_click()

        def on_open_settings(button):
            """
            Deactivates settings button.
            Notifies controller that player has opened settings screen.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            self.controller.settings.on_activate()

        super().__init__(user_db_cursor, config_db_cursor, surface, batches, groups,
                         logger=getLogger('root.app.view'))
        self.title_label = None
        self.main_frame_sprite = None
        self.close_game_button = CloseGameButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                 groups=self.groups, on_click_action=on_close_game)
        self.iconify_game_button = IconifyGameButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                     groups=self.groups, on_click_action=on_iconify_game)
        self.fullscreen_button = FullscreenButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                  groups=self.groups, on_click_action=on_app_window_fullscreen)
        self.restore_button = RestoreButton(surface=self.surface, batch=self.batches['ui_batch'],
                                            groups=self.groups, on_click_action=on_app_window_restore)
        self.open_settings_button = OpenSettingsButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                       groups=self.groups, on_click_action=on_open_settings)
        self.fullscreen_button.paired_button = self.restore_button
        self.restore_button.paired_button = self.fullscreen_button
        self.buttons.append(self.close_game_button)
        self.buttons.append(self.iconify_game_button)
        self.buttons.append(self.fullscreen_button)
        self.buttons.append(self.restore_button)
        self.buttons.append(self.open_settings_button)
        self.app_window_move_mode = False
        self.app_window_move_offset = (0, 0)
        self.game_window_handler = GetActiveWindow()
        self.game_window_position = GetWindowRect(self.game_window_handler)
        self.absolute_mouse_pos = GetCursorPos()
        self.on_mouse_press_handlers.append(self.handle_mouse_press)
        self.on_mouse_release_handlers.append(self.handle_mouse_release)
        self.on_mouse_drag_handlers.append(self.handle_mouse_drag)

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates all sprites and labels.
        """
        self.is_activated = True
        self.title_label = Label('Railway Station Simulator', font_name='Arial',
                                 font_size=int(16 / 40 * self.top_bar_height),
                                 x=self.top_bar_height // 4, y=self.screen_resolution[1] - self.top_bar_height // 2,
                                 anchor_x='left', anchor_y='center', batch=self.batches['ui_batch'],
                                 group=self.groups['button_text'])
        if self.main_frame_sprite is None:
            self.main_frame_sprite\
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
        self.main_frame_sprite.delete()
        self.main_frame_sprite = None
        self.title_label.delete()
        self.title_label = None
        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.on_recalculate_ui_properties(screen_resolution)
        self.surface.set_size(screen_resolution[0], screen_resolution[1])
        if self.is_activated:
            self.title_label.x = self.top_bar_height // 4
            self.title_label.y = self.screen_resolution[1] - self.top_bar_height // 2
            self.title_label.font_size = int(16 / 40 * self.top_bar_height)
            self.close_game_button.x_margin = self.screen_resolution[0] - self.top_bar_height
            self.close_game_button.y_margin = self.screen_resolution[1] - self.top_bar_height
            self.close_game_button.on_size_changed((self.top_bar_height, self.top_bar_height),
                                                   int(19 / 40 * self.top_bar_height))
            self.fullscreen_button.x_margin = self.screen_resolution[0] - self.top_bar_height * 2 + 2
            self.fullscreen_button.y_margin = self.screen_resolution[1] - self.top_bar_height
            self.fullscreen_button.on_size_changed((self.top_bar_height, self.top_bar_height),
                                                   int(19 / 40 * self.top_bar_height))
            self.restore_button.x_margin = self.screen_resolution[0] - self.top_bar_height * 2 + 2
            self.restore_button.y_margin = self.screen_resolution[1] - self.top_bar_height
            self.restore_button.on_size_changed((self.top_bar_height, self.top_bar_height),
                                                int(19 / 40 * self.top_bar_height))
            self.iconify_game_button.x_margin = self.screen_resolution[0] - self.top_bar_height * 3 + 4
            self.iconify_game_button.y_margin = self.screen_resolution[1] - self.top_bar_height
            self.iconify_game_button.on_size_changed((self.top_bar_height, self.top_bar_height),
                                                     int(19 / 40 * self.top_bar_height))
            self.open_settings_button.x_margin = self.screen_resolution[0] - self.bottom_bar_height
            self.open_settings_button.y_margin = 0
            self.open_settings_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height),
                                                      int(30 / 80 * self.bottom_bar_height))
            for b in self.buttons:
                b.on_position_changed((b.x_margin, b.y_margin))

    def on_fullscreen_mode_turned_on(self):
        """
        Makes the game fullscreen.
        Note that adjusting screen resolution is made by on_change_screen_resolution handler,
        this function only switches the app window mode.
        """
        self.surface.set_fullscreen(fullscreen=True)

    def on_fullscreen_mode_turned_off(self):
        """
        Makes the game windowed.
        Note that adjusting screen resolution is made by on_change_screen_resolution handler,
        this function only switches the app window mode.
        """
        self.surface.set_fullscreen(fullscreen=False)

    @game_window_is_active
    @game_is_not_fullscreen
    @left_mouse_button
    @view_is_active
    def handle_mouse_press(self, x, y, button, modifiers):
        """
        When left button is pressed and mouse cursor is over the top bar, activates app window move mode.

        :param x:               mouse cursor X position inside the app window
        :param y:               mouse cursor Y position inside the app window
        :param button:          determines which mouse button was pressed
        :param modifiers:       determines if some modifier key is held down (at the moment we don't use it)
        """
        y = self.screen_resolution[1] - y
        if x in range(self.screen_resolution[0] - self.top_bar_height * 3) and y in range(self.top_bar_height):
            self.app_window_move_mode = True
            self.app_window_move_offset = (x, y)

    @game_window_is_active
    @left_mouse_button
    def handle_mouse_release(self, x, y, button, modifiers):
        """
        When left button is released, deactivates app window move mode.

        :param x:               mouse cursor X position inside the app window
        :param y:               mouse cursor Y position inside the app window
        :param button:          determines which mouse button was pressed
        :param modifiers:       determines if some modifier key is held down (at the moment we don't use it)
        """
        self.app_window_move_mode = False

    @game_window_is_active
    @app_window_move_mode_enabled
    def handle_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """
        Moves app window if app window move mode is active and player moves his mouse.

        :param x:               mouse cursor X position inside the app window
        :param y:               mouse cursor Y position inside the app window
        :param dx:              relative X position from the previous mouse position
        :param dy:              relative Y position from the previous mouse position
        :param buttons:         determines which mouse button was pressed
        :param modifiers:       determines if some modifier key is held down (at the moment we don't use it)
        """
        self.absolute_mouse_pos = GetCursorPos()
        self.game_window_position = GetWindowRect(self.game_window_handler)
        SetWindowPos(self.game_window_handler, HWND_TOP,
                     self.absolute_mouse_pos[0] - self.app_window_move_offset[0],
                     self.absolute_mouse_pos[1] - self.app_window_move_offset[1],
                     self.game_window_position[2] - self.game_window_position[0],
                     self.game_window_position[3] - self.game_window_position[1], SWP_NOREDRAW)

    def on_set_up_main_frame_shader_uniforms(self, shader):
        """
        Each time main frame shader is activated we need to set up values for all its uniforms.

        :param shader:                  main frame shader
        """
        shader.uniforms.screen_resolution = self.screen_resolution
        shader.uniforms.base_offset = ((-1) * self.controller.game.map.view.base_offset[0],
                                       (-1) * self.controller.game.map.view.base_offset[1])
        shader.uniforms.bottom_bar_height = self.bottom_bar_height
        shader.uniforms.top_bar_height = self.top_bar_height
        shader.uniforms.top_left_cell \
            = (self.controller.game.map.constructor.view.track_cells_positions[0][0],
               self.controller.game.map.constructor.view.track_cells_positions[0][1] + self.bottom_bar_height - 1)
        shader.uniforms.top_right_cell \
            = (self.controller.game.map.constructor.view.environment_cell_positions[0][0],
               self.controller.game.map.constructor.view.environment_cell_positions[0][1] + self.bottom_bar_height - 1)
        shader.uniforms.game_frame_opacity = self.controller.game.view.game_frame_opacity
        shader.uniforms.schedule_opacity = self.controller.game.map.scheduler.view.schedule_opacity
        shader.uniforms.constructor_opacity = self.controller.game.map.constructor.view.constructor_opacity
        shader.uniforms.settings_is_activated = int(self.controller.settings.view.is_activated)
        shader.uniforms.zoom_buttons_activated \
            = int(self.controller.game.map.view.zoom_in_button.is_activated
                  or self.controller.game.map.view.zoom_out_button.is_activated)
        shader.uniforms.track_build_button_is_activated \
            = int(self.controller.game.map.constructor.view.build_track_button.is_activated)
        shader.uniforms.mini_map_opacity = self.controller.game.map.view.mini_map_opacity
        shader.uniforms.zoom_out_activated = int(self.controller.game.map.view.zoom_out_activated)
        shader.uniforms.mini_map_position = self.controller.game.map.view.mini_map_position
        shader.uniforms.mini_map_width = self.controller.game.map.view.mini_map_width
        shader.uniforms.mini_map_height = self.controller.game.map.view.mini_map_height
        shader.uniforms.is_decrement_resolution_button_activated \
            = int(self.controller.settings.view.decrement_windowed_resolution_button.is_activated)
        shader.uniforms.is_increment_resolution_button_activated \
            = int(self.controller.settings.view.increment_windowed_resolution_button.is_activated)
