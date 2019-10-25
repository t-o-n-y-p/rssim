from logging import getLogger

from model import *


class LicenseModel(AppBaseModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, logger=getLogger('root.app.license.model'))
