from .model_base import Model


def _model_is_active(fn):
    def _handle_if_model_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_model_is_activated


def _model_is_not_active(fn):
    def _handle_if_model_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_model_is_not_activated


class SignalModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.state = None
        self.locked = None

    @_model_is_not_active
    def on_activate(self):
        self.is_activated = True
        if self.state is None and self.locked is None:
            self.user_db_cursor.execute('SELECT state, locked FROM signals WHERE track = ? AND base_route = ?',
                                        (self.controller.track, self.controller.base_route))
            self.state, self.locked = self.user_db_cursor.fetchone()
            self.locked = bool(self.locked)

        self.config_db_cursor.execute('SELECT x, y, flip_needed FROM signal_config WHERE track = ? AND base_route = ?',
                                      (self.controller.track, self.controller.base_route))
        x, y, self.view.flip_needed = self.config_db_cursor.fetchone()
        self.view.position = (x, y)
        self.on_activate_view()

    def on_activate_view(self):
        self.view.state = self.state
        self.view.locked = self.locked
        self.view.on_activate()

    @_model_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_save_state(self):
        self.user_db_cursor.execute('UPDATE signals SET state = ?, locked = ? WHERE track = ? AND base_route = ?',
                                    (self.state, int(self.locked), self.controller.track, self.controller.base_route))

    def on_unlock(self):
        self.locked = False
        self.view.on_unlock()

    def on_switch_to_green(self, train_route):
        self.state = 'green_state'
        self.view.on_change_state('green_state')

    def on_switch_to_red(self, train_route):
        self.state = 'green_state'
        self.view.on_change_state('red_state')
