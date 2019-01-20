from model import *


class SignalModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.state = None
        self.locked = None
        self.flip_needed = None
        self.position = None

    def on_signal_setup(self, track, base_route):
        self.user_db_cursor.execute('SELECT state, locked FROM signals WHERE track = ? AND base_route = ?',
                                    (track, base_route))
        self.state, self.locked = self.user_db_cursor.fetchone()
        self.locked = bool(self.locked)
        self.config_db_cursor.execute('SELECT x, y, flip_needed FROM signal_config WHERE track = ? AND base_route = ?',
                                      (track, base_route))
        x, y, self.flip_needed = self.config_db_cursor.fetchone()
        self.position = (x, y)

    @model_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.on_activate_view()

    def on_activate_view(self):
        self.view.state = self.state
        self.view.locked = self.locked
        self.view.flip_needed = self.flip_needed
        self.view.position = self.position
        self.view.on_activate()

    @model_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_save_state(self):
        self.user_db_cursor.execute('UPDATE signals SET state = ?, locked = ? WHERE track = ? AND base_route = ?',
                                    (self.state, int(self.locked), self.controller.track, self.controller.base_route))

    def on_unlock(self):
        self.locked = False
        self.view.on_unlock()

    def on_switch_to_green(self):
        self.state = 'green_signal'
        self.view.on_change_state('green_signal')

    def on_switch_to_red(self):
        self.state = 'red_signal'
        self.view.on_change_state('red_signal')
