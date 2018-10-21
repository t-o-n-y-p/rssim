class GameObject:
    def __init__(self, game_config):
        self.c = game_config

    def read_state(self):
        pass

    def save_state(self):
        pass

    def update(self, game_paused):
        pass

    def update_sprite(self, base_offset):
        pass
