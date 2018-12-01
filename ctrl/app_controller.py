from .controller_base import Controller


class AppController(Controller):
    def __init__(self):
        super().__init__()
        self.to_be_activated_during_startup = True
