from typing import final, Final

from pyglet.event import EventDispatcher

from database import on_commit


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
        self.on_construction_time_bonus_code_activate_handlers = []
        self.on_exp_bonus_code_deactivate_handlers = []
        self.on_money_bonus_code_deactivate_handlers = []
        self.on_construction_time_bonus_code_deactivate_handlers = []

    @staticmethod
    def on_save():
        on_commit()


GameEventDispatcher.register_event_type('on_save')
GameEventDispatcher.register_event_type('on_time_update')
GameEventDispatcher.register_event_type('on_time_speed_update')
GameEventDispatcher.register_event_type('on_time_format_update')
GameEventDispatcher.register_event_type('on_level_up')
GameEventDispatcher.register_event_type('on_level_up_notification_state_update')
GameEventDispatcher.register_event_type('on_money_gain')
GameEventDispatcher.register_event_type('on_money_spend')
GameEventDispatcher.register_event_type('on_exp_gain')
GameEventDispatcher.register_event_type('on_exp_bonus_code_activate')
GameEventDispatcher.register_event_type('on_money_bonus_code_activate')
GameEventDispatcher.register_event_type('on_construction_time_bonus_code_activate')
GameEventDispatcher.register_event_type('on_exp_bonus_code_deactivate')
GameEventDispatcher.register_event_type('on_money_bonus_code_deactivate')
GameEventDispatcher.register_event_type('on_construction_time_bonus_code_deactivate')


GAME: Final = GameEventDispatcher()


@GAME.event
def on_save():
    for h in GAME.on_save_handlers:
        h()


@GAME.event
def on_time_update(dt):
    for h in GAME.on_time_update_handlers:
        h(dt)


@GAME.event
def on_time_speed_update(time_speed):
    for h in GAME.on_time_speed_update_handlers:
        h(time_speed)


@GAME.event
def on_time_format_update(time_format):
    for h in GAME.on_time_format_update_handlers:
        h(time_format)


@GAME.event
def on_level_up():
    for h in GAME.on_level_up_handlers:
        h()


@GAME.event
def on_level_up_notification_state_update(state):
    for h in GAME.on_level_up_notification_state_update_handlers:
        h(state)


@GAME.event
def on_money_gain(money_gained):
    for h in GAME.on_money_gain_handlers:
        h(money_gained)


@GAME.event
def on_money_spend(money_spent):
    for h in GAME.on_money_spend_handlers:
        h(money_spent)


@GAME.event
def on_exp_gain(exp_gained):
    for h in GAME.on_exp_gain_handlers:
        h(exp_gained)


@GAME.event
def on_exp_bonus_code_activate(value):
    for h in GAME.on_exp_bonus_code_activate_handlers:
        h(value)


@GAME.event
def on_money_bonus_code_activate(value):
    for h in GAME.on_money_bonus_code_activate_handlers:
        h(value)


@GAME.event
def on_construction_time_bonus_code_activate(value):
    for h in GAME.on_construction_time_bonus_code_activate_handlers:
        h(value)


@GAME.event
def on_exp_bonus_code_deactivate():
    for h in GAME.on_exp_bonus_code_deactivate_handlers:
        h()


@GAME.event
def on_money_bonus_code_deactivate():
    for h in GAME.on_money_bonus_code_deactivate_handlers:
        h()


@GAME.event
def on_construction_time_bonus_code_deactivate(value):
    for h in GAME.on_construction_time_bonus_code_deactivate_handlers:
        h(value)
