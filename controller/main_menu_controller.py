from logging import getLogger

from controller import *


class MainMenuController(Controller):
    def __init__(self, app):
        super().__init__(parent_controller=app, logger=getLogger('root.app.main_menu.controller'))
        self.licenses = None

    def on_update_view(self):
        """
        Notifies the view and Map view to update fade-in/fade-out animations.
        """
        self.view.on_update()
        # self.licenses.on_update_view()

    @controller_is_not_active
    def on_activate(self):
        """
        Activates MainMenu object: controller and model. Model activates the view if necessary.
        """
        self.is_activated = True
        self.model.on_activate()

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates MainMenu object: controller, view and model. Also deactivates all child objects.
        """
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()
        # self.licenses.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        """
        Notifies the view and all child controllers about screen resolution update.

        :param screen_resolution:       new screen resolution
        """
        self.view.on_change_screen_resolution(screen_resolution)
        # self.licenses.on_change_screen_resolution(screen_resolution)

    def on_activate_view(self):
        """
        Activates the view if user opened main menu screen in the app.
        """
        self.model.on_activate_view()

    def on_deactivate_view(self):
        """
        Deactivates the view and all child views if user either closed main menu screen or opened settings screen.
        """
        self.view.on_deactivate()
        # self.licenses.on_deactivate_view()

    def on_apply_shaders_and_draw_vertices(self):
        """
        Notifies the view and child controllers to draw all sprites with shaders.
        """
        self.view.on_apply_shaders_and_draw_vertices()
        # self.licenses.on_apply_shaders_and_draw_vertices()

    def on_update_current_locale(self, new_locale):
        """
        Notifies the view and child controllers (if any) about current locale value update.

        :param new_locale:                      selected locale
        """
        self.view.on_update_current_locale(new_locale)
        # self.licenses..on_update_current_locale(new_locale)
