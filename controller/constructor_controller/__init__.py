from controller import *


class ConstructorController(Controller):
    """
    Implements Constructor controller.
    Constructor object is responsible for building new tracks and station environment.
    """
    def __init__(self, parent_controller, logger):
        super().__init__(parent_controller=parent_controller, logger=logger)

    def on_update_view(self):
        """
        Notifies the view to update fade-in/fade-out animations and create sprites if some are missing.
        Not all sprites are created at once, they are created one by one to avoid massive FPS drop.
        """
        self.view.on_update()

    @controller_is_not_active
    def on_activate(self):
        """
        Activates Constructor object: controller and model. Model activates the view if necessary.
        """
        self.is_activated = True
        self.model.on_activate()

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates Constructor object: controller, view and model.
        Notifies Map controller about it.
        """
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()
        self.parent_controller.on_close_constructor()

    def on_save_state(self):
        """
        Notifies the model to save constructor state to user progress database.
        """
        self.model.on_save_state()

    def on_update_time(self, game_time):
        """
        Notifies the model about in-game time update.

        :param game_time:               current in-game time
        """
        self.model.on_update_time(game_time)

    def on_change_screen_resolution(self, screen_resolution):
        """
        Notifies the view about screen resolution update.

        :param screen_resolution:       new screen resolution
        """
        self.view.on_change_screen_resolution(screen_resolution)

    def on_activate_view(self):
        """
        Activates the view if user opened constructor screen in the app.
        """
        self.model.on_activate_view()

    def on_deactivate_view(self):
        """
        Deactivates the view if user either closed constructor screen or opened schedule screen.
        Notifies Map controller about it.
        """
        self.view.on_deactivate()
        self.parent_controller.on_close_constructor()

    def on_level_up(self, level):
        """
        Notifies the model about level update when user hits new level.

        :param level:                   new level value
        """
        self.model.on_level_up(level)

    def on_put_under_construction(self, construction_type, entity_number):
        """
        Notifies model to put construction with given type and number under construction.

        :param construction_type:       type of construction: track or environment
        :param entity_number:           number of track or environment tier
        """
        self.model.on_put_under_construction(construction_type, entity_number)

    def on_add_money(self, money):
        """
        Notifies the model about bank account state change when user gains money.

        :param money:                   amount of money gained
        """
        self.model.on_add_money(money)

    def on_pay_money(self, money):
        """
        Notifies the model about bank account state change when user pays money.

        :param money:                   amount of money spent
        """
        self.model.on_pay_money(money)

    def on_update_current_locale(self, new_locale):
        """
        Notifies the view and child controllers (if any) about current locale value update.

        :param new_locale:                      selected locale
        """
        self.view.on_update_current_locale(new_locale)

    def on_disable_notifications(self):
        """
        Disables system notifications for the view and all child controllers.
        """
        self.view.on_disable_notifications()

    def on_enable_notifications(self):
        """
        Enables system notifications for the view and all child controllers.
        """
        self.view.on_enable_notifications()

    def on_activate_money_target(self, construction_type, row):
        """
        Notifies model that money target was activated at given cell.

        :param construction_type:               column to activate money target: tracks or environment
        :param row:                             number of cell in a given column
        """
        self.model.on_activate_money_target(construction_type, row)

    def on_deactivate_money_target(self):
        """
        Notifies model that money target was deactivated.
        """
        self.model.on_deactivate_money_target()

    def on_change_feature_unlocked_notification_state(self, notification_state):
        """
        Notifies the view about feature unlocked notification state update.

        :param notification_state:              new notification state defined by player
        """
        self.view.on_change_feature_unlocked_notification_state(notification_state)

    def on_change_construction_completed_notification_state(self, notification_state):
        """
        Notifies the view about construction completed notification state update.

        :param notification_state:              new notification state defined by player
        """
        self.view.on_change_construction_completed_notification_state(notification_state)

    def on_apply_shaders_and_draw_vertices(self):
        """
        Notifies the view and child controllers to draw all sprites with shaders.
        """
        self.view.on_apply_shaders_and_draw_vertices()
