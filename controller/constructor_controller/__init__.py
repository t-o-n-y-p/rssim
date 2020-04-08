from abc import ABC
from logging import getLogger
from typing import final

from controller import MapBaseController
from ui.fade_animation.fade_in_animation.constructor_fade_in_animation import ConstructorFadeInAnimation
from ui.fade_animation.fade_out_animation.constructor_fade_out_animation import ConstructorFadeOutAnimation


class ConstructorController(MapBaseController, ABC):
    def __init__(self, map_id, parent_controller):
        super().__init__(
            map_id, parent_controller, logger=getLogger(f'root.app.game.map.{map_id}.constructor.controller')
        )
        self.view, self.model = self.create_view_and_model()
        self.fade_in_animation = ConstructorFadeInAnimation(self.view)
        self.fade_out_animation = ConstructorFadeOutAnimation(self.view)

    @final
    def on_put_under_construction(self, construction_type, entity_number):
        self.model.on_put_under_construction(construction_type, entity_number)

    @final
    def on_activate_money_target(self, construction_type, row):
        self.model.on_activate_money_target(construction_type, row)
        self.parent_controller.parent_controller.on_deactivate_money_target_for_inactive_maps(self.map_id)

    @final
    def on_deactivate_money_target(self):
        self.model.on_deactivate_money_target()

    @final
    def on_unlock_track(self, track):
        self.model.on_unlock_track(track)

    @final
    def on_remove_track_from_matrix(self, track):
        self.model.on_remove_track_from_matrix(track)
