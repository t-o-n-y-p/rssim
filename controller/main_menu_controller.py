from logging import getLogger

from controller import *


@final
class MainMenuController(AppBaseController):
    def __init__(self, app):
        super().__init__(parent_controller=app, logger=getLogger('root.app.main_menu.controller'))
