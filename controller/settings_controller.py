from logging import getLogger

from controller import *


@final
class SettingsController(AppBaseController):
    def __init__(self, app):
        super().__init__(parent_controller=app, logger=getLogger('root.app.settings.controller'))
        self.navigated_from_main_menu = False
        self.navigated_from_game = False

    def on_save_and_commit_state(self):
        self.model.on_save_and_commit_state()

    def on_apply_clock_state(self, clock_24h_enabled):
        self.model.on_apply_clock_state(clock_24h_enabled)
