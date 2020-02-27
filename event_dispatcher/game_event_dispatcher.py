from typing import final

from pyglet.event import EventDispatcher


@final
class GameEventDispatcher(EventDispatcher):
    def __init__(self):
        super().__init__()
        self.on_save_handlers = []
        self.on_time_update_handlers = []
        self.on_time_speed_update_handlers = []
        self.on_time_format_update_handlers = []
        self.on_level_up_handlers = []
        self.on_level_up_notification_state_update_handlers = []
        self.on_money_gain_handlers = []
        self.on_money_spend_handlers = []
        self.on_exp_gain_handlers = []
        self.on_exp_bonus_code_activate_handlers = []
        self.on_money_bonus_code_activate_handlers = []
        self.on_exp_bonus_code_deactivate_handlers = []
        self.on_money_bonus_code_deactivate_handlers = []
