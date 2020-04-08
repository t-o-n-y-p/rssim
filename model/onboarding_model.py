from logging import getLogger
from typing import final

from database import USER_DB_CURSOR, on_commit
from model import AppBaseModel


@final
class OnboardingModel(AppBaseModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, logger=getLogger('root.app.onboarding.model'))

    def on_save_state(self):
        pass

    @staticmethod
    def on_save_and_commit_onboarding_state():
        USER_DB_CURSOR.execute('UPDATE game_progress SET onboarding_required = 0')
        on_commit()
