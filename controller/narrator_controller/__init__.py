from abc import ABC
from logging import getLogger
from typing import final

from controller import MapBaseController
from ui.fade_animation.fade_in_animation.narrator_fade_in_animation import NarratorFadeInAnimation
from ui.fade_animation.fade_out_animation.narrator_fade_out_animation import NarratorFadeOutAnimation


class NarratorController(MapBaseController, ABC):
    def __init__(self, map_id, parent_controller):
        super().__init__(map_id, parent_controller, logger=getLogger(f'root.app.game.map.{map_id}.narrator.controller'))
        self.view, self.model = self.create_view_and_model()
        self.fade_in_animation = NarratorFadeInAnimation(self.view)
        self.fade_out_animation = NarratorFadeOutAnimation(self.view)

    @final
    def on_announcement_add(self, announcement_time, announcement_type, train_id, track_number):
        self.model.on_announcement_add(announcement_time, announcement_type, train_id, track_number)

    @final
    def on_update_announcements_state(self, new_state):
        self.view.on_update_announcements_state(new_state)
