from typing import final

import win32com.client

from database import USER_DB_CURSOR, ANNOUNCEMENT_TYPE, PASS_THROUGH_ANNOUNCEMENT, ANNOUNCEMENT_TRACK_NUMBER, \
    ARRIVAL_ANNOUNCEMENT, ARRIVAL_FINISHED_ANNOUNCEMENT, ANNOUNCEMENT_TRAIN_ID, DEPARTURE_ANNOUNCEMENT, \
    FIVE_MINUTES_LEFT_ANNOUNCEMENT
from i18n import numbers_to_speech_en, numbers_to_speech_ru, ENGLISH, RUSSIAN, I18N_RESOURCES, DATIVE, NOMINATIVE, \
    GENITIVE, PREPOSITIONAL


@final
class Speaker:
    def __init__(self):
        self.speaker = win32com.client.Dispatch('SAPI.SpVoice')
        USER_DB_CURSOR.execute('''SELECT master_volume FROM sound''')
        self.master_volume = USER_DB_CURSOR.fetchone()[0]
        self.speaker.Volume = 100
        self.speaker.Priority = 2
        self.opacity = 0
        # SpVoice hangs during the first speech, so we fake the first one to avoid hanging at the real one
        self.speaker.Speak('<silence msec="10"/>', 9)
        self.track_number_converters = {
            ENGLISH: numbers_to_speech_en.to_cardinal,
            RUSSIAN: numbers_to_speech_ru.to_ordinal
        }
        self.is_muted = False

    def on_announcement_play(self, announcement, locale):
        announcement_resource_location \
            = I18N_RESOURCES[announcement[ANNOUNCEMENT_TYPE] + '_announcement_string'][locale]
        if announcement[ANNOUNCEMENT_TYPE] == PASS_THROUGH_ANNOUNCEMENT:
            self.speaker.Speak(
                announcement_resource_location.format(
                    round(self.master_volume * self.opacity / 255),
                    self.track_number_converters[locale](announcement[ANNOUNCEMENT_TRACK_NUMBER], DATIVE)
                ), 9
            )
        elif announcement[ANNOUNCEMENT_TYPE] in (ARRIVAL_ANNOUNCEMENT, ARRIVAL_FINISHED_ANNOUNCEMENT):
            self.speaker.Speak(
                announcement_resource_location.format(
                    round(self.master_volume * self.opacity / 255),
                    self.track_number_converters[locale](announcement[ANNOUNCEMENT_TRACK_NUMBER], NOMINATIVE),
                    '<silence msec="50"/>'.join(str(announcement[ANNOUNCEMENT_TRAIN_ID]))
                ), 9
            )
        elif announcement[ANNOUNCEMENT_TYPE] == DEPARTURE_ANNOUNCEMENT:
            track_number_category = 'other'
            if locale == RUSSIAN and announcement[ANNOUNCEMENT_TRACK_NUMBER] == 2:
                track_number_category = 'two'

            self.speaker.Speak(
                announcement_resource_location[track_number_category].format(
                    round(self.master_volume * self.opacity / 255),
                    self.track_number_converters[locale](announcement[ANNOUNCEMENT_TRACK_NUMBER], GENITIVE),
                    '<silence msec="50"/>'.join(str(announcement[ANNOUNCEMENT_TRAIN_ID]))
                ), 9
            )
        elif announcement[ANNOUNCEMENT_TYPE] == FIVE_MINUTES_LEFT_ANNOUNCEMENT:
            self.speaker.Speak(
                announcement_resource_location.format(
                    round(self.master_volume * self.opacity / 255),
                    self.track_number_converters[locale](announcement[ANNOUNCEMENT_TRACK_NUMBER], PREPOSITIONAL),
                    '<silence msec="50"/>'.join(str(announcement[ANNOUNCEMENT_TRAIN_ID]))
                ), 9
            )

    def is_not_speaking(self):
        return self.speaker.Status.RunningState == 1

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        if self.opacity <= 0:
            self.speaker.Speak('<silence msec="1"/>', 11)

    def on_master_volume_update(self, new_master_volume):
        self.master_volume = new_master_volume

    def on_mute(self):
        self.is_muted = True
        self.speaker.Volume = 0

    def on_unmute(self):
        self.is_muted = False
        self.speaker.Volume = 100

    def find_voice(self, locale):
        self.speaker.Speak(I18N_RESOURCES['blank_announcement_sample_string'][locale], 9)
