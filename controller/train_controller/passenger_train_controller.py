from logging import getLogger

from controller.train_controller import TrainController


class PassengerTrainController(TrainController):
    def __init__(self, map_controller, train_id):
        super().__init__(parent_controller=map_controller, train_id=train_id,
                         logger=getLogger(f'root.app.game.map.0.train.{train_id}.controller'))
