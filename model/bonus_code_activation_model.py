from logging import getLogger

from model import *


class BonusCodeActivationModel(AppBaseModel):
    def __init__(self):
        super().__init__(logger=getLogger('root.app.bonus_code_activation.model'))
