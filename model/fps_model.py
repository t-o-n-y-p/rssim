from logging import getLogger

from model import *


class FPSModel(Model):
    """
    Implements FPS model.
    FPS object is responsible for real-time FPS calculation.
    """
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        """
        Properties:
            fps                                 current live FPS value

        :param user_db_connection:              connection to the user DB (stores game state and user-defined settings)
        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        """
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor,
                         logger=getLogger('root.app.fps.model'))
        self.fps = 0

    @model_is_not_active
    def on_activate(self):
        """
        Activates the model and the view.
        """
        self.is_activated = True
        self.view.on_activate()

    @model_is_active
    def on_deactivate(self):
        """
        Deactivates the model.
        """
        self.is_activated = False

    def on_update_fps(self, fps):
        """
        Updates live FPS value.

        :param fps:                     new FPS value
        """
        self.fps = fps
        self.view.on_update_fps(fps)
