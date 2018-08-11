from game_object import GameObject


class Track(GameObject):
    def __init__(self):
        super().__init__()
        self.base_routes = []
        self.busy = False
        self.last_entered_by = None
        self.override = False

    def update(self, game_paused):
        # if game is paused, track status should not be updated
        # if track settings are overridden, we do nothing too
        if not game_paused and not self.override:
            busy_1 = False
            # if any of 4 base routes are busy, all track will become busy
            for i in self.base_routes:
                busy_1 = busy_1 or i.route_config['busy']
                if i.route_config['busy']:
                    self.last_entered_by = i.route_config['last_entered_by']

            self.busy = busy_1
