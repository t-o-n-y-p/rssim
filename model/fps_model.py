from logging import getLogger

from model import *


class FPSModel(Model):
    """
    Implements FPS model.
    FPS object is responsible for real-time FPS calculation.
    """
    def __init__(self):
        """
        Properties:
            fps                                 current live FPS value
            display_fps                         indicates if FPS should be displayed

        """
        super().__init__(logger=getLogger('root.app.fps.model'))
        self.user_db_cursor.execute('SELECT display_fps FROM graphics')
        self.display_fps = self.user_db_cursor.fetchone()[0]
        self.fps = 0

    @display_fps_enabled
    def on_activate_view(self):
        self.view.on_activate()

    def on_update_fps(self, fps):
        """
        Updates live FPS value.

        :param fps:                     new FPS value
        """
        self.fps = fps
        self.view.on_update_fps(fps)

    def on_update_display_fps(self, display_fps):
        """
        Updates display_fps flag value and (de)activates the view.

        :param display_fps:                     new flag value
        """
        self.display_fps = display_fps
        if not self.display_fps:
            self.view.on_deactivate()
        else:
            self.on_activate_view()
