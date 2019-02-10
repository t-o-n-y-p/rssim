from sys import exit
from logging import getLogger

from controller import *


class AppController(Controller):
    """
    Implements App controller.
    App object is responsible for high-level properties, UI and events.
    """
    def __init__(self, loader):
        """
        Properties:
            game                        Game object controller
            settings                    Settings object controller
            fps                         FPS object controller
            loader                      RSSim class instance

        :param loader:                  RSSim class instance
        """
        super().__init__(logger=getLogger('root.app.controller'))
        self.logger.info('START INIT')
        self.game = None
        self.settings = None
        self.fps = None
        self.loader = loader
        self.logger.debug('loader assigned successfully')
        self.logger.info('END INIT')

    def on_update_view(self):
        """
        Notifies the view, Game view and Settings view to update fade-in/fade-out animations.
        """
        self.logger.info('START ON_UPDATE_VIEW')
        self.view.on_update()
        self.game.on_update_view()
        self.settings.on_update_view()
        self.logger.info('END ON_UPDATE_VIEW')

    @controller_is_not_active
    def on_activate(self):
        """
        Activates App object: controller and model. Model activates the view if necessary.
        When App object is activated, we also activate Game object
        (because game process is started right away) and FPS object (to display FPS counter).
        TODO adjust this behavior when main menu will be implemented:
            Game object will not be activated by default anymore, Main menu object will be activated instead
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
        self.model.on_activate()
        self.game.on_activate()
        self.fps.on_activate()
        self.logger.info('END ON_ACTIVATE')

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates App object: controller, view and model. Also deactivates all child objects.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
        self.model.on_deactivate()
        self.view.on_deactivate()
        self.game.on_deactivate()
        self.settings.on_deactivate()
        self.fps.on_deactivate()
        self.logger.info('END ON_DEACTIVATE')

    def on_fullscreen_button_click(self):
        """
        Handles Fullscreen button being clicked on.
        We need to apply new screen resolution and switch app window mode to fullscreen
        (if fullscreen mode is available for user display).
        """
        self.logger.info('START ON_FULLSCREEN_BUTTON_CLICK')
        self.on_change_screen_resolution(self.settings.model.fullscreen_resolution)
        self.logger.debug(f'fullscreen mode available: {self.model.fullscreen_mode_available}')
        if self.model.fullscreen_mode_available:
            self.on_fullscreen_mode_turned_on()

        self.logger.info('END ON_FULLSCREEN_BUTTON_CLICK')

    def on_restore_button_click(self):
        """
        Handles Restore button being clicked on.
        We need to apply new screen resolution and switch app window mode to windowed.
        """
        self.logger.info('START ON_RESTORE_BUTTON_CLICK')
        self.on_fullscreen_mode_turned_off()
        self.on_change_screen_resolution(self.settings.model.windowed_resolution)
        self.logger.info('END ON_RESTORE_BUTTON_CLICK')

    def on_fullscreen_mode_turned_on(self):
        """
        Notifies the model to make the game fullscreen.
        Note that adjusting screen resolution is made by on_change_screen_resolution handler,
        this function only switches the app window mode.
        """
        self.logger.info('START ON_FULLSCREEN_MODE_TURNED_ON')
        self.model.on_fullscreen_mode_turned_on()
        self.logger.info('END ON_FULLSCREEN_MODE_TURNED_ON')

    def on_fullscreen_mode_turned_off(self):
        """
        Notifies the model to make the game windowed.
        Note that adjusting screen resolution is made by on_change_screen_resolution handler,
        this function only switches the app window mode.
        """
        self.logger.info('START ON_FULLSCREEN_MODE_TURNED_OFF')
        self.model.on_fullscreen_mode_turned_off()
        self.logger.info('END ON_FULLSCREEN_MODE_TURNED_OFF')

    def on_change_screen_resolution(self, screen_resolution):
        """
        Notifies the model and all child controllers about screen resolution update.

        :param screen_resolution:       new screen resolution
        """
        self.logger.info('START ON_CHANGE_SCREEN_RESOLUTION')
        self.model.on_change_screen_resolution(screen_resolution)
        self.game.on_change_screen_resolution(screen_resolution)
        self.settings.on_change_screen_resolution(screen_resolution)
        self.fps.on_change_screen_resolution(screen_resolution)
        self.logger.info('END ON_CHANGE_SCREEN_RESOLUTION')

    def on_close_game(self):
        """
        Handles Close button being clicked on.
        Here we deactivate the app, notify game controller to save game progress and close the app window.
        """
        self.logger.info('START ON_CLOSE_GAME')
        self.on_deactivate()
        self.game.on_save_and_commit_state()
        self.logger.info('GOODBYE')
        exit()

    def on_activate_main_menu_view(self):
        """
        Reserved for future use.
        """
        pass

    def on_activate_game_view(self):
        """
        Notifies Game controller to activate the game screen
        in case the settings screen was opened from game screen and then user closes settings screen.
        """
        self.logger.info('START ON_ACTIVATE_GAME_VIEW')
        self.game.on_activate_view()
        self.logger.info('END ON_ACTIVATE_GAME_VIEW')

    def on_deactivate_current_view(self):
        """
        Determines where the user is located when Open settings button was clicked on:
        either game screen or main menu screen (not implemented at the moment).
        Corresponding flag is enabled for Settings controller.
        """
        self.logger.info('START ON_DEACTIVATE_CURRENT_VIEW')
        self.logger.debug(f'game view is activated: {self.game.view.is_activated}')
        if self.game.view.is_activated:
            self.game.on_deactivate_view()
            self.settings.navigated_from_game = True
            self.logger.debug(f'settings.navigated_from_game = {self.settings.navigated_from_game}')

        self.logger.info('END ON_DEACTIVATE_CURRENT_VIEW')

    def on_activate_open_settings_button(self):
        """
        Activates Open settings button back when user closes settings screen.
        """
        self.logger.info('START ON_ACTIVATE_OPEN_SETTINGS_BUTTON')
        self.view.open_settings_button.on_activate()
        self.logger.info('END ON_ACTIVATE_OPEN_SETTINGS_BUTTON')

    def on_update_fps(self, fps):
        """
        Notifies FPS controller about FPS value update.

        :param fps:                     new FPS value
        """
        self.logger.info('START ON_UPDATE_FPS')
        self.fps.on_update_fps(fps)
        self.logger.info('END ON_UPDATE_FPS')

    def on_display_fps(self):
        """
        Reserved for future use.
        """
        self.logger.info('START ON_DISPLAY_FPS')
        self.fps.on_activate()
        self.logger.info('END ON_DISPLAY_FPS')

    def on_hide_fps(self):
        """
        Reserved for future use.
        """
        self.logger.info('START ON_HIDE_FPS')
        self.fps.on_deactivate()
        self.logger.info('END ON_HIDE_FPS')

    def on_set_up_main_frame_shader_uniforms(self, shader):
        """
        Each time main frame shader is activated we need to set up values for all its uniforms.

        :param shader:                  main frame shader
        """
        self.logger.info('START ON_SET_UP_MAIN_FRAME_SHADER_UNIFORMS')
        self.view.on_set_up_main_frame_shader_uniforms(shader)
        self.logger.info('END ON_SET_UP_MAIN_FRAME_SHADER_UNIFORMS')

    def on_save_log_level(self, log_level):
        """
        Reserved for future use.

        :param log_level:               new log level
        """
        self.logger.info('START ON_SAVE_LOG_LEVEL')
        self.loader.on_save_log_level(log_level)
        self.logger.info('END ON_SAVE_LOG_LEVEL')
