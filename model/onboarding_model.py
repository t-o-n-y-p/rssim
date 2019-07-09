from logging import getLogger

from model import *


class OnboardingModel(Model):
    def __init__(self):
        super().__init__(logger=getLogger('root.app.onboarding.model'))

    def on_activate_view(self):
        self.view.on_activate()

    def on_save_and_commit_onboarding_state(self):
        self.user_db_cursor.execute('UPDATE game_progress SET onboarding_required = 0')
        self.user_db_connection.commit()
