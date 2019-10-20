from logging import getLogger

from controller import *


@final
class LicenseController(AppBaseController):
    def __init__(self, app):
        super().__init__(parent_controller=app, logger=getLogger('root.app.license.controller'))
