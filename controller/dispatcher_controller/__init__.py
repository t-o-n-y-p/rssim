from logging import getLogger

from controller import *
from ui.fade_animation.fade_in_animation.dispatcher_fade_in_animation import DispatcherFadeInAnimation
from ui.fade_animation.fade_out_animation.dispatcher_fade_out_animation import DispatcherFadeOutAnimation


class DispatcherController(MapBaseController, ABC):
    def __init__(self, map_id, parent_controller):
        super().__init__(map_id, parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.dispatcher.controller'))
        self.view, self.model = self.create_view_and_model()
        self.fade_in_animation = DispatcherFadeInAnimation(self.view)
        self.fade_out_animation = DispatcherFadeOutAnimation(self.view)

    @final
    def on_add_train(self, train_controller):
        self.model.on_add_train(train_controller)

    @final
    def on_leave_track(self, track):
        self.model.on_leave_track(track)

    @final
    def on_unlock_track(self, track):
        self.model.on_unlock_track(track)
