from logging import getLogger

from view import *


class DispatcherView(View):
    """
    Implements Dispatcher view.
    Dispatcher object is responsible for assigning routes to approaching trains.
    """
    def __init__(self):
        """
        Properties:
            none

        """
        self.map_id = None
        self.on_update_map_id()
        super().__init__(logger=getLogger(f'root.app.game.map.{self.map_id}.dispatcher.view'))
        self.on_init_graphics()

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates all sprites and labels (nothing at the moment).
        """
        self.is_activated = True

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
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

    def on_init_graphics(self):
        self.on_change_screen_resolution(self.screen_resolution)
