from logging import getLogger

from model import *


class MainMenuModel(Model):
    def __init__(self):
        super().__init__(logger=getLogger('root.app.main_menu.model'))

    def on_activate_view(self):
        self.view.on_activate()

