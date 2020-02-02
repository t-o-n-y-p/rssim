from logging import getLogger

from ui.fade_animation.fade_in_animation import *
from database import USER_DB_CURSOR


@final
class GameFadeInAnimation(FadeInAnimation):
    def __init__(self, game_view):
        super().__init__(animation_object=game_view, logger=getLogger('root.app.game.fade_in_animation'))
        self.bonus_code_manager_fade_in_animation = None
        self.map_switcher_fade_in_animation = None
        self.map_fade_in_animations = []

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
        self.bonus_code_manager_fade_in_animation.on_activate()
        USER_DB_CURSOR.execute('''SELECT last_known_map_id FROM graphics''')
        self.map_fade_in_animations[USER_DB_CURSOR.fetchone()[0]].on_activate()
