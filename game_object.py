class GameObject:
    # simply pass this to be overridden by each object
    def __init__(self):
        pass

    # simply pass this to be overridden by each object: "surface" is generic game screen, "base_offset" stands for
    # top left corner of entire map (it can be moved)
    def draw(self, surface, base_offset):
        pass

    # simply pass this to be overridden by each object: "game_stopped" restricts objects that can be updated
    # after user paused the game
    def update(self, game_paused):
        pass
