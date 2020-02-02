from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class MainMenuFadeOutAnimation(FadeOutAnimation):
    def __init__(self, main_menu_view):
        super().__init__(animation_object=main_menu_view, logger=getLogger('root.app.main_menu.fade_out_animation'))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
