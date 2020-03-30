from logging import getLogger

from win32com.universal import com_error

from music_track.narrator_intro import NarratorIntro
from view import *


class NarratorView(MapBaseView, ABC):
    def __init__(self, controller, map_id):
        super().__init__(controller, map_id, logger=getLogger(f'root.app.game.map.{map_id}.narrator.view'))
        self.is_speaking = False
        self.is_playing_announcement = False
        self.playback_start_time = 0
        self.on_append_window_handlers()

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        for announcement in [a for a in NARRATOR_QUEUE[self.map_id]
                             if a[ANNOUNCEMENT_TYPE] in get_announcement_types_enabled(self.dt_multiplier)]:
            announcement[ANNOUNCEMENT_LOCKED] = FALSE

    @final
    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()
        for announcement in NARRATOR_QUEUE[self.map_id]:
            announcement[ANNOUNCEMENT_LOCKED] = TRUE

    @final
    def on_update(self):
        if SPEAKER.is_not_speaking() and self.is_speaking:
            self.is_speaking = False
            self.is_playing_announcement = False

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        MIDI_PLAYER.on_narrator_intro_opacity_update(self.opacity)
        SPEAKER.on_update_opacity(self.opacity)
        if self.opacity <= 0:
            self.is_speaking = False
            self.is_playing_announcement = False

    @final
    def on_update_time(self, dt):
        super().on_update_time(dt)
        if len(NARRATOR_QUEUE[self.map_id]) > 0:
            # self.logger.debug(f'{self.game_time=}')
            # self.logger.debug(f'{NARRATOR_QUEUE[self.map_id]=}')
            if self.game_time >= NARRATOR_QUEUE[self.map_id][0][ANNOUNCEMENT_TIME] and not self.is_playing_announcement:
                try:
                    SPEAKER.find_voice(self.current_locale)
                    self.is_playing_announcement = True
                    self.playback_start_time = self.game_time
                    if self.is_activated:
                        MIDI_PLAYER.add_narrator_intro(NarratorIntro())

                except com_error:
                    NARRATOR_QUEUE[self.map_id].pop(0)

            if self.game_time >= self.playback_start_time + self.dt_multiplier * 1.2 and self.is_playing_announcement \
                    and not self.is_speaking:
                self.on_announcement_play(NARRATOR_QUEUE[self.map_id][0])
                NARRATOR_QUEUE[self.map_id].pop(0)

    @final
    @view_is_active
    def on_announcement_play(self, announcement):
        SPEAKER.on_announcement_play(announcement, self.current_locale)
        self.is_speaking = True
