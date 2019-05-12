from logging import getLogger

from model import *


class GameModel(Model):
    """
    Implements Game model.
    Game object is responsible for properties, UI and events related to the game process.
    """
    def __init__(self):
        """
        Properties:
            game_paused                         indicates if game is paused or not
            game_time                           current in-game time
            level                               current player level
            exp                                 current player exp
            money                               current bank account state
            money_target                        reserved for future use
            player_progress                     exp needed to hit next level
            exp_multiplier                      multiplier for exp based on exp bonus from shops

        """
        super().__init__(logger=getLogger('root.app.game.model'))
        self.game_paused = True
        self.user_db_cursor.execute('SELECT game_time FROM epoch_timestamp')
        self.game_time = self.user_db_cursor.fetchone()[0]
        self.user_db_cursor.execute('SELECT level, exp, money, money_target, exp_multiplier FROM game_progress')
        self.level, self.exp, self.money, self.money_target, self.exp_multiplier = self.user_db_cursor.fetchone()
        self.config_db_cursor.execute('''SELECT player_progress FROM player_progress_config 
                                         WHERE level = ?''', (self.level, ))
        self.player_progress = self.config_db_cursor.fetchone()[0]

    @model_is_not_active
    def on_activate(self):
        """
        Activates the model and the view.
        """
        self.is_activated = True

    @model_is_active
    def on_deactivate(self):
        """
        Deactivates the model.
        """
        self.is_activated = False

    def on_activate_view(self):
        """
        Activates view and refreshes all data: time, level, exp, money.
        Activates pause/resume button depending on current game state.
        """
        self.view.on_activate()
        self.view.on_update_time(self.game_time)
        self.view.on_update_level(self.level)
        self.view.on_update_exp(self.exp, self.player_progress)
        self.view.on_update_money(self.money, self.money_target)
        if self.game_paused:
            self.view.resume_game_button.on_activate()
        else:
            self.view.pause_game_button.on_activate()

    def on_pause_game(self):
        """
        Updates game state and notifies the view about it.
        """
        self.game_paused = True
        self.view.on_pause_game()

    def on_resume_game(self):
        """
        Updates game state and notifies the view about it.
        """
        self.game_paused = False
        self.view.on_resume_game()

    @model_is_active
    def on_update_time(self):
        """
        Increases in-game time by 1 each frame. When number of frames in 1 in-game minute divides the counter,
        notifies the view to update time.
        """
        if self.game_time % FRAMES_IN_ONE_MINUTE == 0:
            self.view.on_update_time(self.game_time)

        self.game_time += 1

    def on_save_state(self):
        """
        Saves game state to user progress database.
        """
        self.user_db_cursor.execute('UPDATE epoch_timestamp SET game_time = ?', (self.game_time, ))
        self.user_db_cursor.execute('''UPDATE game_progress SET level = ?, exp = ?, money = ?, 
                                    money_target = ?''', (self.level, self.exp, self.money, self.money_target))

    @maximum_level_not_reached
    def on_add_exp(self, exp):
        """
        Adds right amount of exp and increases the level if amount of exp is enough to hit new level.
        Notifies the view about exp update.

        :param exp:                     amount of exp gained
        """
        self.exp += exp * self.exp_multiplier
        if self.exp >= self.player_progress and self.level < MAXIMUM_LEVEL:
            self.controller.on_level_up()

        self.view.on_update_exp(self.exp, self.player_progress)

    def on_level_up(self):
        """
        Calculates new exp value when user hits new level.
        Reads new accumulated_player_progress and player_progress values for new level from the database.
        Notifies the view about level update.
        """
        self.exp -= self.player_progress
        self.level += 1
        if self.level == MAXIMUM_LEVEL:
            self.exp = 0.0

        self.config_db_cursor.execute('''SELECT player_progress FROM player_progress_config 
                                      WHERE level = ?''', (self.level, ))
        self.player_progress = self.config_db_cursor.fetchone()[0]
        self.view.on_update_level(self.level)
        self.view.on_send_level_up_notification(self.level)

    @maximum_money_not_reached
    def on_add_money(self, money):
        """
        Notifies the view to send notification if money target is reached.
        Updates bank account state change when user gains money.
        Notifies the view about state change.

        :param money:                   amount of money gained
        """
        if self.money_target > 0 and self.money < self.money_target <= self.money + money:
            for map_ in self.controller.maps:
                if map_.constructor.model.money_target_activated:
                    if map_.constructor.model.money_target_cell_position[0] == TRACKS:
                        self.view.on_send_enough_money_track_notification()
                    elif map_.constructor.model.money_target_cell_position[0] == ENVIRONMENT:
                        self.view.on_send_enough_money_environment_notification()

        self.money += money
        if self.money > MONEY_LIMIT:
            self.money = MONEY_LIMIT

        self.view.on_update_money(self.money, self.money_target)

    def on_pay_money(self, money):
        """
        Updates bank account state change when user spends money.
        Notifies the view about state change.

        :param money:                   amount of money spent
        """
        self.money -= money
        self.view.on_update_money(self.money, self.money_target)

    def on_update_money_target(self, money_target):
        """
        Updates money target value and notifies the view about value update.

        :param money_target:            new money target value
        """
        self.money_target = money_target
        self.view.on_update_money(self.money, self.money_target)

    def get_active_map(self):
        """
        Returns ID of the currently opened map from the database.

        :return:                        ID of the currently opened map
        """
        self.user_db_cursor.execute('SELECT map_id FROM graphics')
        return self.user_db_cursor.fetchone()[0]
