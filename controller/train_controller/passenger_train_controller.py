from controller.train_controller import TrainController


class PassengerTrainController(TrainController):
    def __init__(self, map_controller, train_id):
        super().__init__(map_id=0, parent_controller=map_controller, train_id=train_id)
