from logging import getLogger

from controller import *


class DispatcherController(GameBaseController):
    def __init__(self, map_id, parent_controller):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.dispatcher.controller'))
        self.map_id = map_id

    @final
    def on_add_train(self, train_controller):
        self.model.on_add_train(train_controller)

    @final
    def on_leave_track(self, track):
        self.model.on_leave_track(track)

    @final
    def on_unlock_track(self, track):
        self.model.on_unlock_track(track)
