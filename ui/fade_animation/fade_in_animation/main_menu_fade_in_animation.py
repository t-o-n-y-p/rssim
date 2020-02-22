from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class MainMenuFadeInAnimation(FadeInAnimation):
    def __init__(self, main_menu_view):
        super().__init__(animation_object=main_menu_view, logger=getLogger('root.app.main_menu.fade_in_animation'))
