from logging import getLogger

from model import *


class MainMenuModel(AppBaseModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, logger=getLogger('root.app.main_menu.model'))
