from logging import getLogger

from model import *


class GameModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor,
                         logger=getLogger('root.app.game.model'))
        self.game_paused = False
        self.user_db_cursor.execute('SELECT game_time FROM epoch_timestamp')
        self.game_time = self.user_db_cursor.fetchone()[0]
        self.user_db_cursor.execute('SELECT level, exp, accumulated_exp, money, money_target FROM game_progress')
        self.level, self.exp, self.accumulated_exp, self.money, self.money_target = self.user_db_cursor.fetchone()
        self.config_db_cursor.execute('''SELECT accumulated_player_progress, player_progress FROM player_progress_config 
                                      WHERE level = ?''', (self.level, ))
        self.accumulated_player_progress, self.player_progress = self.config_db_cursor.fetchone()

    @model_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.on_activate_view()

    @model_is_active
    def on_deactivate(self):
        self.view.exp_percent = int(self.exp / self.player_progress)
        if self.money_target > 0:
            self.view.money_percent = int(self.money / self.money_target)
        else:
            self.view.money_percent = 0

        self.is_activated = False

    def on_activate_view(self):
        self.view.on_activate()
        self.view.on_update_game_time(self.game_time)
        self.view.on_update_level(self.level)
        self.view.on_update_exp(self.exp, self.player_progress)
        self.view.on_update_money(self.money, self.money_target)
        if self.game_paused:
            self.view.resume_game_button.on_activate()
        else:
            self.view.pause_game_button.on_activate()

    def on_pause_game(self):
        self.game_paused = True
        self.view.on_pause_game()

    def on_resume_game(self):
        self.game_paused = False
        self.view.on_resume_game()

    @model_is_active
    def on_update_time(self):
        if self.game_time % 240 == 0:
            self.view.on_update_game_time(self.game_time)

        self.game_time += 1

    def on_save_state(self):
        self.user_db_cursor.execute('UPDATE epoch_timestamp SET game_time = ?', (self.game_time, ))
        self.user_db_cursor.execute('''UPDATE game_progress SET level = ?, exp = ?, accumulated_exp = ?, money = ?, 
                                    money_target = ?''', (self.level, self.exp, self.accumulated_exp, self.money,
                                                          self.money_target))

    @maximum_level_not_reached
    def on_add_exp(self, exp):
        self.exp += exp
        self.accumulated_exp += exp
        if self.accumulated_exp >= self.accumulated_player_progress and self.level < MAXIMUM_LEVEL:
            self.controller.on_level_up()

        self.view.on_update_exp(self.exp, self.player_progress)

    def on_level_up(self):
        self.exp = self.accumulated_exp - self.accumulated_player_progress
        self.level += 1
        if self.level == MAXIMUM_LEVEL:
            self.exp = 0.0

        self.config_db_cursor.execute('''SELECT accumulated_player_progress, player_progress FROM player_progress_config 
                                      WHERE level = ?''', (self.level, ))
        self.accumulated_player_progress, self.player_progress = self.config_db_cursor.fetchone()
        self.view.on_update_level(self.level)

    @maximum_money_not_reached
    def on_add_money(self, money):
        self.money += money
        if self.money > MONEY_LIMIT:
            self.money = MONEY_LIMIT
        self.view.on_update_money(self.money, self.money_target)

    def on_pay_money(self, money):
        self.money -= money
        self.view.on_update_money(self.money, self.money_target)

    def on_update_money_target(self, money_target):
        self.money_target = money_target
        self.view.on_update_money(self.money, self.money_target)
