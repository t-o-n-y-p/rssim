from logging import getLogger
from typing import final

from ui.fade_animation.fade_out_animation import FadeOutAnimation


@final
class LicenseFadeOutAnimation(FadeOutAnimation):
    def __init__(self, license_view):
        super().__init__(animation_object=license_view, logger=getLogger('root.app.license.fade_out_animation'))
