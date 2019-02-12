from logging import getLogger

from model import *


class FPSModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor,
                         logger=getLogger('root.app.fps.model'))
        self.fps = 0

    @model_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.view.on_activate()

    @model_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_update_fps(self, fps):
        self.fps = fps
        self.view.on_update_fps(fps)
