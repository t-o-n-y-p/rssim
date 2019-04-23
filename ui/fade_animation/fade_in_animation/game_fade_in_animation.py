from logging import getLogger

from ui.fade_animation.fade_in_animation import *
from database import USER_DB_CURSOR


class GameFadeInAnimation(FadeInAnimation):
    def __init__(self, game_controller):
        super().__init__(animation_object=game_controller, logger=getLogger('root.app.game.fade_in_animation'))
        self.map_fade_in_animations = []

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
        USER_DB_CURSOR.execute('SELECT map_id FROM graphics')
        self.map_fade_in_animations[USER_DB_CURSOR.fetchone()[0]].on_activate()