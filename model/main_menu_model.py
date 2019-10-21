from logging import getLogger

from model import *


class MainMenuModel(AppBaseModel):
    def __init__(self):
        super().__init__(logger=getLogger('root.app.main_menu.model'))
