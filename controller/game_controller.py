from logging import getLogger

from controller import *


class GameController(Controller):
    """
    Implements Game controller.
    Game object is responsible for properties, UI and events related to the game process.
    """
    def __init__(self, app):
        """
        Properties:
            maps                        Map object controllers list
            map_transition_animations   navigation animations from maps (not used at the moment)

        :param app:                     App controller (parent controller)
        """
        super().__init__(parent_controller=app, logger=getLogger('root.app.game.controller'))
        self.maps = []
        self.map_transition_animations = []

    def on_update_view(self):
        """
        Notifies the view, Map views, and fade-in/fade-out animations.
        """
        self.view.on_update()
        self.fade_in_animation.on_update()
        self.fade_out_animation.on_update()
        for map_ in self.maps:
            map_.on_update_view()

    @controller_is_not_active
    def on_activate(self):
        """
        Activates Game object: controller and model. Model activates the view if necessary. Activates maps.
        When App object is activated, we also activate Map object.
        """
        self.is_activated = True
        self.model.on_activate()
        for map_ in self.maps:
            map_.on_activate()

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates Game object: controller, view and model. Also deactivates all child objects.
        """
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()
        for map_ in self.maps:
            map_.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        """
        Notifies the view and all child controllers about screen resolution update.

        :param screen_resolution:       new screen resolution
        """
        self.view.on_change_screen_resolution(screen_resolution)
        for map_ in self.maps:
            map_.on_change_screen_resolution(screen_resolution)

    def on_pause_game(self):
        """
        Notifies the model the game was paused.
        """
        self.model.on_pause_game()

    def on_resume_game(self):
        """
        Notifies the model the game was resumed.
        """
        self.model.on_resume_game()

    def on_activate_view(self):
        """
        Activates the view and Map controller if user opened game screen in the app.
        """
        self.model.on_activate_view()
        self.maps[self.model.get_active_map()].on_activate_view()

    def on_deactivate_view(self):
        """
        Deactivates the view and all child views if user either closed game screen or opened settings screen.
        """
        self.view.on_deactivate()
        for map_ in self.maps:
            map_.on_deactivate_view()

    @controller_is_active
    @game_is_not_paused
    def on_update_time(self):
        """
        Notifies Map controllers about time change.
        Notifies the model to update in-game time.
        Calls on_save_and_commit_state handler every 2 in-game hours.
        """
        for map_ in self.maps:
            map_.on_update_time(self.model.game_time)

        self.model.on_update_time()
        if self.model.game_time % (FRAMES_IN_ONE_HOUR * 2) == 0:
            self.on_save_and_commit_state()

    def on_save_and_commit_state(self):
        """
        Notifies the model and Map controllers to save state to user progress database and commit.
        """
        self.model.on_save_state()
        for map_ in self.maps:
            map_.on_save_state()

        self.model.user_db_connection.commit()

    def on_level_up(self):
        """
        Notifies the model and Map controllers about level update.
        """
        self.model.on_level_up()
        for map_ in self.maps:
            map_.on_level_up(self.model.level)

    def on_update_money_target(self, money_target):
        """
        Notifies the model to update money target.

        :param money_target:            new money target value
        """
        self.model.on_update_money_target(money_target)

    def on_add_exp(self, exp):
        """
        Notifies the model about exp update when user gains exp.

        :param exp:                     amount of exp gained
        """
        self.model.on_add_exp(exp)

    def on_add_money(self, money):
        """
        Notifies the model and Map controllers about bank account state update when user gains money.

        :param money:                   amount of money gained
        """
        self.model.on_add_money(money)
        for map_ in self.maps:
            map_.on_add_money(money)

    def on_pay_money(self, money):
        """
        Notifies the model and Map controllers about bank account state update when user pays money.

        :param money:                   amount of money spent
        """
        self.model.on_pay_money(money)
        for map_ in self.maps:
            map_.on_pay_money(money)

    def on_update_current_locale(self, new_locale):
        """
        Notifies the view and child controllers (if any) about current locale value update.

        :param new_locale:                      selected locale
        """
        self.view.on_update_current_locale(new_locale)
        for map_ in self.maps:
            map_.on_update_current_locale(new_locale)

    def on_disable_notifications(self):
        """
        Disables system notifications for the view and all child controllers.
        """
        self.view.on_disable_notifications()
        for map_ in self.maps:
            map_.on_disable_notifications()

    def on_enable_notifications(self):
        """
        Enables system notifications for the view and all child controllers.
        """
        self.view.on_enable_notifications()
        for map_ in self.maps:
            map_.on_enable_notifications()

    def on_change_level_up_notification_state(self, notification_state):
        """
        Notifies the view about level up notification state update.

        :param notification_state:              new notification state defined by player
        """
        self.view.on_change_level_up_notification_state(notification_state)

    def on_change_feature_unlocked_notification_state(self, notification_state):
        """
        Notifies the Map controllers about feature unlocked notification state update.

        :param notification_state:              new notification state defined by player
        """
        for map_ in self.maps:
            map_.on_change_feature_unlocked_notification_state(notification_state)

    def on_change_construction_completed_notification_state(self, notification_state):
        """
        Notifies the Map controllers about construction completed notification state update.

        :param notification_state:              new notification state defined by player
        """
        for map_ in self.maps:
            map_.on_change_construction_completed_notification_state(notification_state)

    def on_change_enough_money_notification_state(self, notification_state):
        """
        Notifies the view about enough money notification state update.

        :param notification_state:              new notification state defined by player
        """
        self.view.on_change_enough_money_notification_state(notification_state)

    def on_apply_shaders_and_draw_vertices(self):
        """
        Notifies the view and child controllers to draw all sprites with shaders.
        """
        self.view.on_apply_shaders_and_draw_vertices()
        for map_ in self.maps:
            map_.on_apply_shaders_and_draw_vertices()

    def on_update_fade_animation_state(self, new_state):
        """
        Notifies fade-in/fade-out animations about state update.

        :param new_state:                       indicates if fade animations were enabled or disabled
        """
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)
        for map_ in self.maps:
            map_.on_update_fade_animation_state(new_state)

    def on_deactivate_money_target_for_inactive_maps(self, active_map_id):
        """
        Deactivates money target for all maps except the given one.

        :param active_map_id:                   ID of the given map
        """
        for i in range(len(self.maps)):
            if i != active_map_id:
                self.maps[i].constructor.on_deactivate_money_target()

    def on_update_clock_state(self, clock_24h_enabled):
        """
        Notifies the view and child controllers (if any) about clock state update.

        :param clock_24h_enabled:               indicates if 24h clock is enabled
        """
        self.view.on_update_clock_state(clock_24h_enabled)
        for map_ in self.maps:
            map_.on_update_clock_state(clock_24h_enabled)
