from logging import getLogger

from controller import *


class SettingsController(Controller):
    """
    Implements Settings controller.
    Settings object is responsible for user-defined settings.
    """
    def __init__(self, app):
        """
        Properties:
            navigated_from_main_menu            indicates if settings screen was opened from main menu
            navigated_from_game                 indicates if settings screen was opened from game screen

        :param app:          App controller (parent controller)
        """
        super().__init__(parent_controller=app, logger=getLogger('root.app.settings.controller'))
        self.logger.info('START INIT')
        self.navigated_from_main_menu = False
        self.logger.debug(f'navigated_from_main_menu: {self.navigated_from_main_menu}')
        self.navigated_from_game = False
        self.logger.debug(f'navigated_from_game: {self.navigated_from_game}')
        self.logger.info('END INIT')

    def on_update_view(self):
        """
        Notifies the view to update fade-in/fade-out animations.
        """
        self.logger.info('START ON_UPDATE_VIEW')
        self.view.on_update()
        self.logger.info('END ON_UPDATE_VIEW')

    @controller_is_not_active
    def on_activate(self):
        """
        Activates Settings object: controller and model. Model activates the view if necessary.
        Determines which screen was activated before.
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
        self.model.on_activate()
        self.parent_controller.on_deactivate_current_view()
        self.logger.info('END ON_ACTIVATE')

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates Settings object: controller, view and model.
        Activates view which was activated before settings screen.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
        self.model.on_deactivate()
        self.view.on_deactivate()
        self.logger.debug(f'navigated_from_main_menu: {self.navigated_from_main_menu}')
        if self.navigated_from_main_menu:
            self.navigated_from_main_menu = False
            self.logger.debug(f'navigated_from_main_menu: {self.navigated_from_main_menu}')
            self.parent_controller.on_activate_main_menu_view()

        self.logger.debug(f'navigated_from_game: {self.navigated_from_game}')
        if self.navigated_from_game:
            self.navigated_from_game = False
            self.logger.debug(f'navigated_from_game: {self.navigated_from_game}')
            self.parent_controller.on_activate_game_view()

        self.parent_controller.on_activate_open_settings_button()
        self.logger.info('END ON_DEACTIVATE')

    def on_change_screen_resolution(self, screen_resolution):
        """
        Notifies the view about screen resolution update.

        :param screen_resolution:       new screen resolution
        """
        self.logger.info('START ON_CHANGE_SCREEN_RESOLUTION')
        self.model.on_change_screen_resolution(screen_resolution)
        self.logger.info('END ON_CHANGE_SCREEN_RESOLUTION')

    def on_save_and_commit_state(self):
        """
        Notifies the model to save user-defined settings to user progress database and commit.
        """
        self.logger.info('START ON_SAVE_AND_COMMIT_STATE')
        self.model.on_save_and_commit_state()
        self.logger.info('END ON_SAVE_AND_COMMIT_STATE')
