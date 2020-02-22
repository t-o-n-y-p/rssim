from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class SettingsFadeOutAnimation(FadeOutAnimation):
    def __init__(self, settings_view):
        super().__init__(animation_object=settings_view,
                         logger=getLogger('root.app.settings.fade_out_animation'))
