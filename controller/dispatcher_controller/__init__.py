from logging import getLogger

from controller import *
from model.dispatcher_model import DispatcherModel
from view.dispatcher_view import DispatcherView
from ui.fade_animation.fade_in_animation.dispatcher_fade_in_animation import DispatcherFadeInAnimation
from ui.fade_animation.fade_out_animation.dispatcher_fade_out_animation import DispatcherFadeOutAnimation


class DispatcherController(MapBaseController):
    def __init__(self, model: DispatcherModel, view: DispatcherView, map_id, parent_controller):
        super().__init__(model, view, map_id, parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.dispatcher.controller'))
        self.fade_in_animation = DispatcherFadeInAnimation(self.view)
        self.fade_out_animation = DispatcherFadeOutAnimation(self.view)

    def create_dispatcher_elements(self):
        pass

    @final
    def on_add_train(self, train_controller):
        self.model.on_add_train(train_controller)

    @final
    def on_leave_track(self, track):
        self.model.on_leave_track(track)

    @final
    def on_unlock_track(self, track):
        self.model.on_unlock_track(track)
