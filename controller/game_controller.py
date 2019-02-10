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
            map                         Map object controller

        :param app:                     App controller (parent controller)
        """
        super().__init__(parent_controller=app, logger=getLogger('root.app.game.controller'))
        self.logger.info('START INIT')
        self.map = None
        self.logger.info('END INIT')

    def on_update_view(self):
        """
        Notifies the view and Map view to update fade-in/fade-out animations.
        """
        self.logger.info('START ON_UPDATE_VIEW')
        self.view.on_update()
        self.map.on_update_view()
        self.logger.info('END ON_UPDATE_VIEW')

    @controller_is_not_active
    def on_activate(self):
        """
        Activates Game object: controller and model. Model activates the view if necessary.
        When App object is activated, we also activate Map object.
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
        self.model.on_activate()
        self.map.on_activate()
        self.logger.info('END ON_ACTIVATE')

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates App object: controller, view and model. Also deactivates all child objects.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
        self.model.on_deactivate()
        self.view.on_deactivate()
        self.map.on_deactivate()
        self.logger.info('END ON_DEACTIVATE')

    def on_change_screen_resolution(self, screen_resolution):
        """
        Notifies the view and all child controllers about screen resolution update.

        :param screen_resolution:       new screen resolution
        """
        self.logger.info('START ON_CHANGE_SCREEN_RESOLUTION')
        self.view.on_change_screen_resolution(screen_resolution)
        self.map.on_change_screen_resolution(screen_resolution)
        self.logger.info('END ON_CHANGE_SCREEN_RESOLUTION')

    def on_pause_game(self):
        """
        Notifies the model the game was paused.
        """
        self.logger.info('START ON_PAUSE_GAME')
        self.model.on_pause_game()
        self.logger.info('END ON_PAUSE_GAME')

    def on_resume_game(self):
        """
        Notifies the model the game was resumed.
        """
        self.logger.info('START ON_RESUME_GAME')
        self.model.on_resume_game()
        self.logger.info('END ON_RESUME_GAME')

    def on_unlock_track(self, track):
        """
        Notifies the map the track is unlocked.

        :param track:                   track number
        """
        self.logger.info('START ON_UNLOCK_TRACK')
        self.map.on_unlock_track(track)
        self.logger.info('END ON_UNLOCK_TRACK')

    def on_activate_view(self):
        """
        Activates the view and Map controller if user opened game screen in the app.
        """
        self.logger.info('START ON_ACTIVATE_VIEW')
        self.model.on_activate_view()
        self.map.on_activate_view()
        self.logger.info('END ON_ACTIVATE_VIEW')

    def on_deactivate_view(self):
        """
        Deactivates the view and all child views if user either closed game screen or opened settings screen.
        """
        self.logger.info('START ON_DEACTIVATE_VIEW')
        self.view.on_deactivate()
        self.map.on_deactivate_view()
        self.logger.info('END ON_DEACTIVATE_VIEW')

    @controller_is_active
    @game_is_not_paused
    def on_update_time(self):
        """
        Notifies Map controller about time change.
        Notifies the model to update in-game time.
        Calls on_save_and_commit_state handler every 2 in-game hours.
        """
        self.logger.info('START ON_UPDATE_TIME')
        self.map.on_update_time(self.model.game_time)
        self.model.on_update_time()
        if self.model.game_time % FRAMES_IN_2_HOURS == 0:
            self.logger.debug('calling on_save_and_commit_state handler')
            self.on_save_and_commit_state()

        self.logger.info('END ON_UPDATE_TIME')

    def on_save_and_commit_state(self):
        """
        Notifies the model and Map controller to save state to user progress database and commit.
        """
        self.logger.info('START ON_SAVE_AND_COMMIT_STATE')
        self.model.on_save_state()
        self.map.on_save_state()
        self.model.user_db_connection.commit()
        self.logger.info('END ON_SAVE_AND_COMMIT_STATE')

    def on_level_up(self):
        """
        Notifies the model and Map controller about level change.
        """
        self.logger.info('START ON_LEVEL_UP')
        self.model.on_level_up()
        self.map.on_level_up(self.model.level)
        self.logger.info('END ON_LEVEL_UP')

    def on_update_money_target(self, money_target):
        """
        Reserved for future use.

        :param money_target:            new money target
        """
        self.logger.info('START ON_UPDATE_MONEY_TARGET')
        self.model.on_update_money_target(money_target)
        self.logger.info('END ON_UPDATE_MONEY_TARGET')

    def on_add_exp(self, exp):
        """
        Notifies the model about exp change when user gains exp.

        :param exp:                     amount of exp gained
        """
        self.logger.info('START ON_ADD_EXP')
        self.model.on_add_exp(exp)
        self.logger.info('END ON_ADD_EXP')

    def on_add_money(self, money):
        """
        Notifies the model and Map controller about bank account state change when user gains money.

        :param money:                   amount of money gained
        """
        self.logger.info('START ON_ADD_MONEY')
        self.model.on_add_money(money)
        self.map.on_add_money(money)
        self.logger.info('END ON_ADD_MONEY')

    def on_pay_money(self, money):
        """
        Notifies the model and Map controller about bank account state change when user pays money.

        :param money:                   amount of money spent
        """
        self.logger.info('START ON_PAY_MONEY')
        self.model.on_pay_money(money)
        self.map.on_pay_money(money)
        self.logger.info('END ON_PAY_MONEY')
