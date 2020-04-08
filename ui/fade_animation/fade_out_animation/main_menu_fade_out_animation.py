from logging import getLogger
from typing import final

from ui.fade_animation.fade_out_animation import FadeOutAnimation


@final
class MainMenuFadeOutAnimation(FadeOutAnimation):
    def __init__(self, main_menu_view):
        super().__init__(animation_object=main_menu_view, logger=getLogger('root.app.main_menu.fade_out_animation'))
