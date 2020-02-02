from logging import getLogger

from controller import *
from model.license_model import LicenseModel
from view.license_view import LicenseView
from ui.fade_animation.fade_in_animation.license_fade_in_animation import LicenseFadeInAnimation
from ui.fade_animation.fade_out_animation.license_fade_out_animation import LicenseFadeOutAnimation


@final
class LicenseController(AppBaseController):
    def __init__(self, app):
        super().__init__(parent_controller=app, logger=getLogger('root.app.license.controller'))
        self.view = LicenseView(controller=self)
        self.model = LicenseModel(controller=self, view=self.view)
        self.fade_in_animation = LicenseFadeInAnimation(self.view)
        self.fade_out_animation = LicenseFadeOutAnimation(self.view)
        self.view.on_init_content()
