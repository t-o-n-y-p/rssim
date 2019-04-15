from logging import getLogger

from model import *


class MainMenuModel(Model):
    def __init__(self):
        super().__init__(logger=getLogger('root.app.main_menu.model'))

    @model_is_not_active
    def on_activate(self):
        """
        Activates the model and the view.
        """
        self.is_activated = True
        self.on_activate_view()

    @model_is_active
    def on_deactivate(self):
        """
        Deactivates the model.
        """
        self.is_activated = False

    def on_activate_view(self):
        """
        Activates view and refreshes all data.
        """
        self.view.on_activate()

