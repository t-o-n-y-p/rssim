from logging import getLogger

from model import *


@final
class BonusCodeActivationModel(AppBaseModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, logger=getLogger('root.app.bonus_code_activation.model'))
