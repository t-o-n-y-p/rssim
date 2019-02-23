from logging import getLogger

from view import *


class TrainRouteView(View):
    """
    Implements Train route view.
    Train route object is responsible for properties, UI and events related to the train route.
    """
    def __init__(self, user_db_cursor, config_db_cursor, surface, batches, groups, track, train_route):
        """
        Properties:
            none

        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        :param surface:                         surface to draw all UI objects on
        :param batches:                         batches to group all labels and sprites
        :param groups:                          defines drawing layers (some labels and sprites behind others)
        :param track:                           route track number
        :param train_route:                     route type (e.g. left/right entry/exit)
        """
        super().__init__(user_db_cursor, config_db_cursor, surface, batches, groups,
                         logger=getLogger(f'root.app.game.map.train_route.{track}.{train_route}.view'))
        self.logger.info('START INIT')
        self.logger.info('END INIT')

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates all sprites and labels (nothing at the moment).
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
        self.logger.info('END ON_ACTIVATE')

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all sprites and labels.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
        self.logger.info('END ON_DEACTIVATE')

    def on_change_base_offset(self, new_base_offset):
        """
        Updates base offset and moves all labels and sprites to its new positions (nothing at the moment).

        :param new_base_offset:         new base offset
        """
        self.logger.info('START ON_CHANGE_BASE_OFFSET')
        self.base_offset = new_base_offset
        self.logger.debug(f'base_offset: {self.base_offset}')
        self.logger.info('END ON_CHANGE_BASE_OFFSET')

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions (nothing at the moment).

        :param screen_resolution:       new screen resolution
        """
        self.logger.info('START ON_CHANGE_SCREEN_RESOLUTION')
        self.on_recalculate_ui_properties(screen_resolution)
        self.logger.info('END ON_CHANGE_SCREEN_RESOLUTION')

    def on_change_zoom_factor(self, zoom_factor, zoom_out_activated):
        """
        Zooms in/out all sprites (nothing at the moment).
        Note that adjusting base offset is made by on_change_base_offset handler,
        this function only changes scale.

        :param zoom_factor                      sprite scale coefficient
        :param zoom_out_activated               indicates if zoom out mode is activated
        """
        self.logger.info('START ON_CHANGE_ZOOM_FACTOR')
        self.zoom_factor = zoom_factor
        self.logger.debug(f'zoom_factor: {self.zoom_factor}')
        self.zoom_out_activated = zoom_out_activated
        self.logger.debug(f'zoom_out_activated: {self.zoom_out_activated}')
        self.logger.info('END ON_CHANGE_ZOOM_FACTOR')
