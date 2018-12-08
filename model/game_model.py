from .model_base import Model


def _model_is_active(fn):
    def _handle_if_model_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_model_is_activated


def _maximum_level_not_reached(fn):
    def _add_exp_if_max_level_not_reached(*args, **kwargs):
        if args[0].level < args[0].maximum_level:
            fn(*args, **kwargs)

    return _add_exp_if_max_level_not_reached


def _money_target_exists(fn):
    def _update_money_progress_if_money_target_exists(*args, **kwargs):
        if args[0].money_target > 0:
            fn(*args, **kwargs)

    return _update_money_progress_if_money_target_exists


def _maximum_money_not_reached(fn):
    def _add_money_if_maximum_money_is_not_reached(*args, **kwargs):
        if args[0].money < 99999999.0:
            fn(*args, **kwargs)

    return _add_money_if_maximum_money_is_not_reached


class GameModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.game_paused = False
        self.user_db_cursor.execute('SELECT game_time FROM epoch_timestamp')
        self.game_time = self.user_db_cursor.fetchone()[0]
        self.maximum_level = 100
        self.unlock_tracks_matrix = ([], [], [], [], [], [], [], [], [], [5, 6],
                                     [], [], [], [], [], [], [], [], [], [7, 8],
                                     [], [], [], [], [], [], [], [], [], [9, 10],
                                     [], [], [], [], [], [], [], [], [], [11, 12],
                                     [], [], [], [], [], [], [], [], [], [13, 14],
                                     [], [], [], [], [15, 16], [], [], [], [], [17, 18],
                                     [], [], [], [], [19, 20], [], [], [], [], [21, ],
                                     [], [], [], [], [22, ], [], [], [], [], [23, 24],
                                     [], [], [], [], [25, 26], [], [], [], [], [27, 28],
                                     [], [], [], [], [29, 30], [], [], [], [], [31, 32])
        self.user_db_cursor.execute('SELECT level, exp, accumulated_exp, money, money_target FROM game_progress')
        self.level, self.exp, self.accumulated_exp, self.money, self.money_target = self.user_db_cursor.fetchone()
        self.config_db_cursor.execute('''SELECT accumulated_player_progress, player_progress FROM player_progress_config 
                                      WHERE level = ?''', (self.level, ))
        self.accumulated_player_progress, self.player_progress = self.config_db_cursor.fetchone()

    def on_activate(self):
        self.is_activated = True
        self.on_activate_view()

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

    @_model_is_active
    def on_update_time(self):
        if self.game_time % 240 == 0:
            self.view.on_update_game_time(self.game_time)

        self.game_time += 1

    def on_save_state(self):
        self.user_db_cursor.execute('UPDATE epoch_timestamp SET game_time = ?', (self.game_time, ))
        self.user_db_cursor.execute('''UPDATE game_progress SET level = ?, exp = ?, accumulated_exp = ?, money = ?, 
                                    money_target = ?''', (self.level, self.exp, self.accumulated_exp, self.money,
                                                          self.money_target))

    @_maximum_level_not_reached
    def on_add_exp(self, exp):
        self.exp += exp
        self.accumulated_exp += exp
        if self.accumulated_exp >= self.accumulated_player_progress:
            self.controller.on_level_up()

        self.view.on_update_exp(self.exp, self.player_progress)

    @_maximum_level_not_reached
    def on_level_up(self):
        self.exp = self.accumulated_exp - self.accumulated_player_progress
        self.level += 1
        if self.level == self.maximum_level:
            self.exp = 0.0

        self.config_db_cursor.execute('''SELECT accumulated_player_progress, player_progress FROM player_progress_config 
                                      WHERE level = ?''', (self.level, ))
        self.accumulated_player_progress, self.player_progress = self.config_db_cursor.fetchone()
        self.view.on_update_level(self.level)

    @_maximum_money_not_reached
    def on_add_money(self, money):
        self.money += money
        if self.money > 99999999.01:
            self.money = 99999999.01
        self.view.on_update_money(self.money, self.money_target)

    def on_pay_money(self, money):
        self.money -= money
        self.view.on_update_money(self.money, self.money_target)
