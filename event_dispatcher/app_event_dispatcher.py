from typing import final, Final

from pyglet.event import EventDispatcher

from database import USER_DB_CURSOR, on_commit


@final
class AppEventDispatcher(EventDispatcher):
    def __init__(self):
        super().__init__()
        self.on_language_update_handlers = []
        self.on_view_update_handlers = []
        self.on_fade_animations_update_handlers = []
        self.on_fade_animations_state_update_handlers = []
        self.on_notifications_mute_handlers = []
        self.on_notifications_unmute_handlers = []

    @staticmethod
    def on_language_update(language):
        USER_DB_CURSOR.execute('UPDATE i18n SET current_locale = ?', (language, ))
        on_commit()


AppEventDispatcher.register_event_type('on_language_update')
AppEventDispatcher.register_event_type('on_view_update')
AppEventDispatcher.register_event_type('on_fade_animations_update')
AppEventDispatcher.register_event_type('on_fade_animations_state_update')
AppEventDispatcher.register_event_type('on_notifications_mute')
AppEventDispatcher.register_event_type('on_notifications_unmute')


APP: Final = AppEventDispatcher()


@APP.event
def on_language_update(language):
    for h in APP.on_language_update_handlers:
        h(language)


@APP.event
def on_view_update():
    for h in APP.on_view_update_handlers:
        h()


@APP.event
def on_fade_animations_update():
    for h in APP.on_fade_animations_update_handlers:
        h()


@APP.event
def on_fade_animations_state_update(state):
    for h in APP.on_fade_animations_state_update_handlers:
        h(state)


@APP.event
def on_notifications_mute():
    for h in APP.on_notifications_mute_handlers:
        h()


@APP.event
def on_notifications_unmute():
    for h in APP.on_notifications_unmute_handlers:
        h()
