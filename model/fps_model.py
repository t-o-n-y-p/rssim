from logging import getLogger

from model import *
from database import USER_DB_CURSOR


class FPSModel(AppBaseModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, logger=getLogger('root.app.fps.model'))
        USER_DB_CURSOR.execute('SELECT display_fps FROM graphics')
        self.display_fps = USER_DB_CURSOR.fetchone()[0]
        self.fps = 0

    def on_update_fps(self, fps):
        self.fps = fps
        self.view.on_update_fps(fps)

    def on_update_display_fps(self, display_fps):
        self.display_fps = display_fps
        if not self.display_fps:
            self.view.on_deactivate()
        else:
            self.view.on_activate()
