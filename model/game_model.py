from logging import getLogger

from model import *


class GameModel(Model):
    def __init__(self):
        super().__init__(logger=getLogger('root.app.game.model'))
        self.game_paused = True
        self.user_db_cursor.execute('SELECT game_time FROM epoch_timestamp')
        self.game_time = self.user_db_cursor.fetchone()[0]
        self.user_db_cursor.execute('SELECT level, exp, money, money_target, exp_multiplier FROM game_progress')
        self.level, self.exp, self.money, self.money_target, self.exp_multiplier = self.user_db_cursor.fetchone()
        self.config_db_cursor.execute('''SELECT player_progress FROM player_progress_config 
                                         WHERE level = ?''', (self.level, ))
        self.player_progress = self.config_db_cursor.fetchone()[0]

    def on_activate_view(self):
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
        self.game_paused = True
        self.view.on_pause_game()

    def on_resume_game(self):
        self.game_paused = False
        self.view.on_resume_game()

    def on_update_time(self):
        if self.game_time % FRAMES_IN_ONE_MINUTE == 0:
            self.view.on_update_time(self.game_time)

        self.game_time += 1

    def on_save_state(self):
        self.user_db_cursor.execute('UPDATE epoch_timestamp SET game_time = ?', (self.game_time, ))
        self.user_db_cursor.execute('''UPDATE game_progress SET level = ?, exp = ?, money = ?, 
                                       money_target = ?, exp_multiplier = ?''',
                                    (self.level, self.exp, self.money, self.money_target, self.exp_multiplier))

    @maximum_level_not_reached
    def on_add_exp(self, exp):
        self.exp += exp * self.exp_multiplier
        while self.exp >= self.player_progress and self.level < MAXIMUM_LEVEL:
            self.controller.on_level_up()

        self.view.on_update_exp(self.exp, self.player_progress)

    def on_level_up(self):
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
        self.money -= money
        self.view.on_update_money(self.money, self.money_target)

    def on_update_money_target(self, money_target):
        self.money_target = money_target
        self.view.on_update_money(self.money, self.money_target)

    def get_active_map(self):
        self.user_db_cursor.execute('SELECT map_id FROM graphics')
        return self.user_db_cursor.fetchone()[0]

    def on_add_exp_bonus(self, exp_bonus):
        self.exp_multiplier += exp_bonus
