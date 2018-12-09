class Model:
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        self.view = None
        self.controller = None
        self.is_activated = False
        self.user_db_connection = user_db_connection
        self.user_db_cursor = user_db_cursor
        self.config_db_cursor = config_db_cursor

    def on_activate(self):
        pass

    def on_deactivate(self):
        pass

    def on_save_state(self):
        pass
