from logging import getLogger

from controller import *
from model.main_menu_model import MainMenuModel
from view.main_menu_view import MainMenuView
from ui.fade_animation.fade_in_animation.main_menu_fade_in_animation import MainMenuFadeInAnimation
from ui.fade_animation.fade_out_animation.main_menu_fade_out_animation import MainMenuFadeOutAnimation


@final
class MainMenuController(AppBaseController):
    def __init__(self, app):
        super().__init__(parent_controller=app, logger=getLogger('root.app.main_menu.controller'))
        self.fade_in_animation = MainMenuFadeInAnimation(self)
        self.fade_out_animation = MainMenuFadeOutAnimation(self)
        self.view = MainMenuView(controller=self)
        self.model = MainMenuModel(controller=self, view=self.view)
        self.view.on_init_content()
