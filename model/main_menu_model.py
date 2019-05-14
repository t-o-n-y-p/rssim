from logging import getLogger

from model import *


class MainMenuModel(Model):
    """
    Implements MainMenu model.
    MainMenu object is responsible for properties, UI and events related to the main menu screen.
    """
    def __init__(self):
        super().__init__(logger=getLogger('root.app.main_menu.model'))

    def on_activate_view(self):
        """
        Activates view and refreshes all data.
        """
        self.view.on_activate()

