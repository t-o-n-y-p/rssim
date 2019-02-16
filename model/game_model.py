from logging import getLogger

from model import *


class GameModel(Model):
    """
    Implements Game model.
    Game object is responsible for properties, UI and events related to the game process.
    """
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        """
        Properties:
            game_paused                         indicates if game is paused or not
            game_time                           current in-game time
            level                               current player level
            exp                                 current player exp
            accumulated_exp                     all accumulated exp from level 1 to current state
            money                               current bank account state
            money_target                        reserved for future use
            accumulated_player_progress         accumulated exp needed to hit next level
            player_progress                     exp needed to hit next level

        :param user_db_connection:              connection to the user DB (stores game state and user-defined settings)
        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        """
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor,
                         logger=getLogger('root.app.game.model'))
        self.logger.info('START INIT')
        self.game_paused = False
        self.logger.debug(f'game_paused: {self.game_paused}')
        self.user_db_cursor.execute('SELECT game_time FROM epoch_timestamp')
        self.game_time = self.user_db_cursor.fetchone()[0]
        self.logger.debug(f'game_time: {self.game_time}')
        self.user_db_cursor.execute('SELECT level, exp, accumulated_exp, money, money_target FROM game_progress')
        self.level, self.exp, self.accumulated_exp, self.money, self.money_target = self.user_db_cursor.fetchone()
        self.logger.debug(f'level: {self.level}')
        self.logger.debug(f'exp: {self.exp}')
        self.logger.debug(f'accumulated_exp: {self.accumulated_exp}')
        self.logger.debug(f'money: {self.money}')
        self.logger.debug(f'money_target: {self.money_target}')
        self.config_db_cursor.execute('''SELECT accumulated_player_progress, player_progress FROM player_progress_config 
                                      WHERE level = ?''', (self.level, ))
        self.accumulated_player_progress, self.player_progress = self.config_db_cursor.fetchone()
        self.logger.debug(f'accumulated_player_progress: {self.accumulated_player_progress}')
        self.logger.debug(f'player_progress: {self.player_progress}')
        self.logger.info('END INIT')

    @model_is_not_active
    def on_activate(self):
        """
        Activates the model and the view.
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
        self.on_activate_view()
        self.logger.info('END ON_ACTIVATE')

    @model_is_active
    def on_deactivate(self):
        """
        Deactivates the model.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
        self.logger.info('END ON_DEACTIVATE')

    def on_activate_view(self):
        """
        Activates view and refreshes all data: time, level, exp, money.
        Activates pause/resume button depending on current game state.
        """
        self.logger.info('START ON_ACTIVATE_VIEW')
        self.view.on_activate()
        self.view.on_update_game_time(self.game_time)
        self.view.on_update_level(self.level)
        self.view.on_update_exp(self.exp, self.player_progress)
        self.view.on_update_money(self.money, self.money_target)
        self.logger.debug(f'game_paused: {self.game_paused}')
        if self.game_paused:
            self.logger.debug('game is paused, activate resume button')
            self.view.resume_game_button.on_activate()
        else:
            self.logger.debug('game is not paused, activate pause button')
            self.view.pause_game_button.on_activate()

        self.logger.info('END ON_ACTIVATE_VIEW')

    def on_pause_game(self):
        """
        Updates game state and notifies the view about it.
        """
        self.logger.info('START ON_PAUSE_GAME')
        self.game_paused = True
        self.logger.debug(f'game_paused: {self.game_paused}')
        self.view.on_pause_game()
        self.logger.info('END ON_PAUSE_GAME')

    def on_resume_game(self):
        """
        Updates game state and notifies the view about it.
        """
        self.logger.info('START ON_RESUME_GAME')
        self.game_paused = False
        self.logger.debug(f'game_paused: {self.game_paused}')
        self.view.on_resume_game()
        self.logger.info('END ON_RESUME_GAME')

    @model_is_active
    def on_update_time(self):
        """
        Increases in-game time by 1 each frame. When number of frames in 1 in-game minute divides the counter,
        notifies the view to update time.
        """
        self.logger.info('START ON_UPDATE_TIME')
        self.logger.debug(f'game_time: {self.game_time}')
        if self.game_time % FRAMES_IN_ONE_MINUTE == 0:
            self.logger.debug('need to update time on the screen')
            self.view.on_update_game_time(self.game_time)

        self.game_time += 1
        self.logger.debug(f'game_time: {self.game_time}')
        self.logger.info('END ON_UPDATE_TIME')

    def on_save_state(self):
        """
        Saves game state to user progress database.
        """
        self.logger.info('START ON_SAVE_STATE')
        self.logger.debug(f'game_time: {self.game_time}')
        self.user_db_cursor.execute('UPDATE epoch_timestamp SET game_time = ?', (self.game_time, ))
        self.logger.debug('game time saved successfully')
        self.logger.debug(f'level: {self.level}')
        self.logger.debug(f'exp: {self.exp}')
        self.logger.debug(f'accumulated_exp: {self.accumulated_exp}')
        self.logger.debug(f'money: {self.money}')
        self.logger.debug(f'money_target: {self.money_target}')
        self.user_db_cursor.execute('''UPDATE game_progress SET level = ?, exp = ?, accumulated_exp = ?, money = ?, 
                                    money_target = ?''', (self.level, self.exp, self.accumulated_exp, self.money,
                                                          self.money_target))
        self.logger.debug('game progress saved successfully')
        self.logger.info('END ON_SAVE_STATE')

    @maximum_level_not_reached
    def on_add_exp(self, exp):
        """
        Adds right amount of exp and increases the level if amount of exp is enough to hit new level.
        Notifies the view about exp update.

        :param exp:                     amount of exp gained
        """
        self.logger.info('START ON_ADD_EXP')
        self.exp += exp
        self.logger.debug(f'exp: {self.exp}')
        self.accumulated_exp += exp
        self.logger.debug(f'accumulated_exp: {self.accumulated_exp}')
        self.logger.debug(f'accumulated_player_progress: {self.accumulated_player_progress}')
        self.logger.debug(f'level: {self.level}')
        if self.accumulated_exp >= self.accumulated_player_progress and self.level < MAXIMUM_LEVEL:
            self.logger.debug('both conditions are met, user hits new level')
            self.controller.on_level_up()

        self.view.on_update_exp(self.exp, self.player_progress)
        self.logger.info('END ON_ADD_EXP')

    def on_level_up(self):
        """
        Calculates new exp value when user hits new level.
        Reads new accumulated_player_progress and player_progress values for new level from the database.
        Notifies the view about level update.
        """
        self.logger.info('START ON_LEVEL_UP')
        self.exp = self.accumulated_exp - self.accumulated_player_progress
        self.level += 1
        self.logger.debug(f'level: {self.level}')
        if self.level == MAXIMUM_LEVEL:
            self.logger.debug('user has hit maximum level, exp is always 0 here')
            self.exp = 0.0

        self.logger.debug(f'exp: {self.exp}')
        self.config_db_cursor.execute('''SELECT accumulated_player_progress, player_progress FROM player_progress_config 
                                      WHERE level = ?''', (self.level, ))
        self.accumulated_player_progress, self.player_progress = self.config_db_cursor.fetchone()
        self.logger.debug(f'accumulated_player_progress: {self.accumulated_player_progress}')
        self.logger.debug(f'player_progress: {self.player_progress}')
        self.view.on_update_level(self.level)
        self.logger.info('END ON_LEVEL_UP')

    @maximum_money_not_reached
    def on_add_money(self, money):
        """
        Updates bank account state change when user gains money.
        Notifies the view about state change.

        :param money:                   amount of money gained
        """
        self.logger.info('START ON_ADD_MONEY')
        self.money += money
        self.logger.debug(f'money: {self.money}')
        if self.money > MONEY_LIMIT:
            self.logger.debug('reduced to money limit')
            self.money = MONEY_LIMIT

        self.view.on_update_money(self.money, self.money_target)
        self.logger.info('END ON_ADD_MONEY')

    def on_pay_money(self, money):
        """
        Updates bank account state change when user spends money.
        Notifies the view about state change.

        :param money:                   amount of money spent
        """
        self.logger.info('START ON_PAY_MONEY')
        self.money -= money
        self.logger.debug(f'money: {self.money}')
        self.view.on_update_money(self.money, self.money_target)
        self.logger.info('END ON_PAY_MONEY')

    def on_update_money_target(self, money_target):
        """
        Reserved for future use.

        :param money_target:            new money target value
        """
        self.logger.info('START ON_UPDATE_MONEY_TARGET')
        self.money_target = money_target
        self.logger.debug(f'money_target: {self.money_target}')
        self.view.on_update_money(self.money, self.money_target)
        self.logger.info('END ON_UPDATE_MONEY_TARGET')
