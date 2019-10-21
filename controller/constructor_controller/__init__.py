from logging import getLogger

from controller import *


class ConstructorController(AppBaseController, GameBaseController, MapBaseController):
    def __init__(self, map_id, parent_controller):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.constructor.controller'))
        self.map_id = map_id

    @final
    def on_deactivate_view(self):
        super().on_deactivate_view()
        self.parent_controller.on_close_constructor()

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
    def on_change_feature_unlocked_notification_state(self, notification_state):
        self.view.on_change_feature_unlocked_notification_state(notification_state)

    @final
    def on_change_construction_completed_notification_state(self, notification_state):
        self.view.on_change_construction_completed_notification_state(notification_state)
