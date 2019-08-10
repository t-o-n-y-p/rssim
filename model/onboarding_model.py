from logging import getLogger

from model import *
from database import USER_DB_CURSOR, on_commit


class OnboardingModel(Model):
    def __init__(self):
        super().__init__(logger=getLogger('root.app.onboarding.model'))

    def on_activate_view(self):
        self.view.on_activate()

    @staticmethod
    def on_save_and_commit_onboarding_state():
        USER_DB_CURSOR.execute('UPDATE game_progress SET onboarding_required = 0')
        on_commit()
