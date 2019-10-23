from logging import getLogger

from model import *


class LicenseModel(AppBaseModel):
    def __init__(self):
        super().__init__(logger=getLogger('root.app.license.model'))
