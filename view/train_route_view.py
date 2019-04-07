from logging import getLogger

from view import *


class TrainRouteView(View):
    """
    Implements Train route view.
    Train route object is responsible for properties, UI and events related to the train route.
    """
    def __init__(self, user_db_cursor, config_db_cursor, track, train_route):
        """
        Properties:
            none

        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        :param track:                           route track number
        :param train_route:                     route type (e.g. left/right entry/exit)
        """
        self.map_id = None
        self.on_update_map_id()
        super().__init__(user_db_cursor, config_db_cursor,
                         logger=getLogger(f'root.app.game.map.train_route.{track}.{train_route}.view'))

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates all sprites and labels (nothing at the moment).
        """
        self.is_activated = True

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all sprites and labels.
        """
        self.is_activated = False

    def on_change_base_offset(self, new_base_offset):
        """
        Updates base offset and moves all labels and sprites to its new positions (nothing at the moment).

        :param new_base_offset:         new base offset
        """
        self.base_offset = new_base_offset

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions (nothing at the moment).

        :param screen_resolution:       new screen resolution
        """
        self.on_recalculate_ui_properties(screen_resolution)

    def on_change_zoom_factor(self, zoom_factor, zoom_out_activated):
        """
        Zooms in/out all sprites (nothing at the moment).
        Note that adjusting base offset is made by on_change_base_offset handler,
        this function only changes scale.

        :param zoom_factor                      sprite scale coefficient
        :param zoom_out_activated               indicates if zoom out mode is activated
        """
        self.zoom_factor = zoom_factor
        self.zoom_out_activated = zoom_out_activated

    def on_update_map_id(self):
        self.map_id = 0
