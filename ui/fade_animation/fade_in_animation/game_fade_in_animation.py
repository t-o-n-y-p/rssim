from logging import getLogger

from ui.fade_animation.fade_in_animation import *
from database import USER_DB_CURSOR


@final
class GameFadeInAnimation(FadeInAnimation):
    def __init__(self, game_controller):
        super().__init__(animation_object=game_controller, logger=getLogger('root.app.game.fade_in_animation'))
        self.map_fade_in_animations = []

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
        USER_DB_CURSOR.execute('SELECT map_id FROM graphics')
        self.map_fade_in_animations[USER_DB_CURSOR.fetchone()[0]].on_activate()
