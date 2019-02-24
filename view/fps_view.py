from logging import getLogger

from pyglet.text import Label

from view import *


class FPSView(View):
    """
    Implements FPS view.
    FPS object is responsible for real-time FPS calculation.
    """
    def __init__(self, user_db_cursor, config_db_cursor, surface, batches, groups):
        """
        Properties:
            fps_label                           text label for current FPS value

        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        :param surface:                         surface to draw all UI objects on
        :param batches:                         batches to group all labels and sprites
        :param groups:                          defines drawing layers (some labels and sprites behind others)
        """
        super().__init__(user_db_cursor, config_db_cursor, surface, batches, groups,
                         logger=getLogger('root.app.fps.view'))
        self.logger.info('START INIT')
        self.fps_label = None
        self.logger.info('END INIT')

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
        self.fps_label = Label(text='0 FPS', font_name='Courier New', font_size=int(16 / 40 * self.top_bar_height),
                               x=self.screen_resolution[0] - self.top_bar_height * 3 - 10,
                               y=self.screen_resolution[1] - self.top_bar_height // 2,
                               anchor_x='right', anchor_y='center', batch=self.batches['ui_batch'],
                               group=self.groups['button_text'])
        self.logger.debug(f'fps_label text: {self.fps_label.text}')
        self.logger.debug(f'fps_label position: {(self.fps_label.x, self.fps_label.y)}')
        self.logger.debug(f'fps_label font size: {self.fps_label.font_size}')
        self.logger.info('END ON_ACTIVATE')

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all sprites and labels.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
        self.fps_label.delete()
        self.fps_label = None
        self.logger.debug(f'fps_label: {self.fps_label}')
        self.logger.info('END ON_DEACTIVATE')

    @view_is_active
    def on_update_fps(self, fps):
        """
        Updates FPS label text.

        :param fps:                             new FPS value
        """
        self.logger.info('START ON_UPDATE_FPS')
        self.fps_label.text = f'{fps} FPS'
        self.logger.debug(f'fps_label text: {self.fps_label.text}')
        self.logger.info('END ON_UPDATE_FPS')

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.logger.info('START ON_CHANGE_SCREEN_RESOLUTION')
        self.on_recalculate_ui_properties(screen_resolution)
        self.fps_label.x = self.screen_resolution[0] - self.top_bar_height * 3 - 10
        self.fps_label.y = self.screen_resolution[1] - self.top_bar_height // 2
        self.fps_label.font_size = int(16 / 40 * self.top_bar_height)
        self.logger.debug(f'fps_label position: {(self.fps_label.x, self.fps_label.y)}')
        self.logger.debug(f'fps_label font size: {self.fps_label.font_size}')
        self.logger.info('END ON_CHANGE_SCREEN_RESOLUTION')
