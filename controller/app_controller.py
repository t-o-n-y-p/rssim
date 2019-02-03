from sys import exit

from controller import *


class AppController(Controller):
    """
    Implements App object controller. It is responsible for high-level properties, UI and events.
    """
    def __init__(self, loader):
        """
        Properties:
            game                        Game object controller
            settings                    Settings object controller
            fps                         FPS object controller
            loader                      RSSim class instance

        :param loader:              RSSim class instance
        """
        super().__init__()
        self.game = None
        self.settings = None
        self.fps = None
        self.loader = loader

    def on_update_view(self):
        """
        Updates fade-in/fade-out animations for App object view, Game object view and Settings object view.
        """
        self.view.on_update()
        self.game.on_update_view()
        self.settings.on_update_view()

    @controller_is_not_active
    def on_activate(self):
        """
        Activates App object: controller and model. Model activates the view if necessary.
        When App object is activated, we also activate Game object
        (because game process is started right away) and FPS object (to display FPS counter).
        TODO adjust this behavior when main menu will be implemented
        """
        self.is_activated = True
        self.model.on_activate()
        self.game.on_activate()
        self.fps.on_activate()

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates App object: controller, view and model. Also deactivates all child objects.
        TODO adjust this behavior when main menu will be implemented
        """
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()
        self.game.on_deactivate()
        self.settings.on_deactivate()
        self.fps.on_deactivate()

    def on_fullscreen_mode_turned_on(self):
        self.model.on_fullscreen_mode_turned_on()

    def on_change_screen_resolution(self, screen_resolution):
        self.model.on_change_screen_resolution(screen_resolution)
        self.game.on_change_screen_resolution(screen_resolution)
        self.settings.on_change_screen_resolution(screen_resolution)
        self.fps.on_change_screen_resolution(screen_resolution)

    def on_fullscreen_mode_turned_off(self):
        self.model.on_fullscreen_mode_turned_off()

    def on_close_game(self):
        self.on_deactivate()
        self.game.on_save_and_commit_state()
        exit()

    def on_activate_main_menu_view(self):
        pass

    def on_activate_game_view(self):
        self.game.on_activate_view()

    def on_deactivate_current_view(self):
        if self.game.view.is_activated:
            self.game.on_deactivate_view()
            self.settings.navigated_from_game = True

    def on_activate_open_settings_button(self):
        self.view.open_settings_button.on_activate()

    def on_update_fps(self, fps):
        self.fps.on_update_fps(fps)

    def on_display_fps(self):
        self.fps.on_activate()

    def on_hide_fps(self):
        self.fps.on_deactivate()

    def on_set_up_main_frame_shader_uniforms(self, shader):
        self.view.on_set_up_main_frame_shader_uniforms(shader)

    def on_save_log_level(self, log_level):
        self.loader.on_save_log_level(log_level)

    def on_fullscreen_button_click(self):
        self.on_change_screen_resolution(self.settings.model.fullscreen_resolution)
        if self.model.fullscreen_mode_available:
            self.on_fullscreen_mode_turned_on()

    def on_restore_button_click(self):
        self.on_fullscreen_mode_turned_off()
        self.on_change_screen_resolution(self.settings.model.windowed_resolution)
