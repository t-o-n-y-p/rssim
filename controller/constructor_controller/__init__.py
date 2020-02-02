from logging import getLogger

from controller import *
from model.constructor_model import ConstructorModel
from view.constructor_view import ConstructorView
from ui.fade_animation.fade_in_animation.constructor_fade_in_animation import ConstructorFadeInAnimation
from ui.fade_animation.fade_out_animation.constructor_fade_out_animation import ConstructorFadeOutAnimation


class ConstructorController(MapBaseController):
    def __init__(self, model: ConstructorModel, view: ConstructorView, map_id, parent_controller):
        super().__init__(model, view, map_id, parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.constructor.controller'))
        self.fade_in_animation = ConstructorFadeInAnimation(self.view)
        self.fade_out_animation = ConstructorFadeOutAnimation(self.view)
        view.construction_state_matrix = model.construction_state_matrix
        self.view.on_init_content()

    def create_constructor_elements(self):
        pass

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
