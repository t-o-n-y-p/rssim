from logging import getLogger
from typing import final

from model import *
from database import USER_DB_CURSOR, CONFIG_DB_CURSOR


@final
class GameModel(GameBaseModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, logger=getLogger('root.app.game.model'))
        self.game_paused = True
        USER_DB_CURSOR.execute('''SELECT exp, money_target, exp_multiplier FROM game_progress''')
        self.exp, self.money_target, self.exp_multiplier = USER_DB_CURSOR.fetchone()
        CONFIG_DB_CURSOR.execute('''SELECT player_progress FROM player_progress_config 
                                    WHERE level = ?''', (self.level, ))
        self.player_progress = CONFIG_DB_CURSOR.fetchone()[0]

    def on_save_state(self):
        USER_DB_CURSOR.execute('UPDATE epoch_timestamp SET game_time = ?', (self.game_time, ))
        USER_DB_CURSOR.execute('''UPDATE game_progress SET level = ?, exp = ?, money = ?, 
                                  money_target = ?, exp_multiplier = ?, exp_bonus_multiplier = ?, 
                                  money_bonus_multiplier = ?, construction_time_bonus_multiplier = ?''',
                               (self.level, self.exp, self.money, self.money_target, self.exp_multiplier,
                                self.exp_bonus_multiplier, self.money_bonus_multiplier,
                                self.construction_time_bonus_multiplier))

    def on_level_up(self):
        super().on_level_up()
        self.exp -= self.player_progress
        if self.level == MAXIMUM_LEVEL:
            self.exp = 0.0

        CONFIG_DB_CURSOR.execute('''SELECT player_progress FROM player_progress_config 
                                    WHERE level = ?''', (self.level, ))
        self.player_progress = CONFIG_DB_CURSOR.fetchone()[0]
        self.view.on_send_level_up_notification()

    def on_add_money(self, money):
        if self.money_target > 0 and self.money < self.money_target <= self.money + money:
            for m in self.controller.maps:
                if m.constructor.model.money_target_activated:
                    if m.constructor.model.money_target_cell_position[0] == TRACKS:
                        self.view.on_send_enough_money_track_notification()
                    elif m.constructor.model.money_target_cell_position[0] == ENVIRONMENT:
                        self.view.on_send_enough_money_environment_notification()

        super().on_add_money(money)

    def on_pause_game(self):
        self.game_paused = True
        self.view.on_pause_game()

    def on_resume_game(self):
        self.game_paused = False
        self.view.on_resume_game()

    @maximum_level_not_reached
    def on_add_exp(self, exp):
        self.exp += exp * self.exp_multiplier
        while self.exp >= self.player_progress and self.level < MAXIMUM_LEVEL:
            self.controller.on_level_up()

        self.view.on_update_exp(self.exp)

    def on_update_money_target(self, money_target):
        self.money_target = money_target
        self.view.on_update_money_target(self.money_target)

    @staticmethod
    def get_active_map():
        USER_DB_CURSOR.execute('SELECT map_id FROM graphics')
        return USER_DB_CURSOR.fetchone()[0]

    def on_add_exp_bonus(self, value):
        self.exp_multiplier = round(self.exp_multiplier + value, 4)
