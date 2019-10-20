from logging import getLogger

from controller import *


@final
class BonusCodeActivationController(AppBaseController):
    def __init__(self, app):
        super().__init__(parent_controller=app, logger=getLogger('root.app.bonus_code_activation.controller'))
