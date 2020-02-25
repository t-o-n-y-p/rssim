from pyglet.event import EventDispatcher

from database import USER_DB_CURSOR, on_commit


class AppEventDispatcher(EventDispatcher):
    @staticmethod
    def on_language_update(language):
        USER_DB_CURSOR.execute('UPDATE i18n SET current_locale = ?', (language, ))
        on_commit()


AppEventDispatcher.register_event_type('on_language_update')
