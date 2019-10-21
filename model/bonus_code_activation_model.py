from logging import getLogger

from model import *


class BonusCodeActivationModel(Model):
    def __init__(self):
        super().__init__(logger=getLogger('root.app.bonus_code_activation.model'))

    def on_activate_view(self):
        self.view.on_activate()
