from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class MainMenuFadeInAnimation(FadeInAnimation):
    def __init__(self, main_menu_controller):
        super().__init__(animation_object=main_menu_controller,
                         logger=getLogger('root.app.main_menu.fade_in_animation'))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
