import ctypes
from abc import ABC
from typing import Final, final

from database import USER_DB_CURSOR


_MIDI_DEVICE: Final = ctypes.c_void_p()
ctypes.windll.winmm.midiOutOpen(ctypes.byref(_MIDI_DEVICE), 0, 0, 0, 0)
ctypes.windll.winmm.midiOutSetVolume(_MIDI_DEVICE, 65535)
_PROGRAM_CHANGE_MESSAGE_ID: Final = 0xC0


def assign_to_channel(cls):
    ctypes.windll.winmm.midiOutShortMsg(
        _MIDI_DEVICE, cls.instrument_id << 8 | _PROGRAM_CHANGE_MESSAGE_ID | cls.channel_id
    )
    return cls


class Instrument(ABC):
    instrument_id: int
    channel_id: int


@final
class MIDIPlayer:
    def __init__(self):
        self.music_track = None
        self.narrator_intro = None
        USER_DB_CURSOR.execute('''SELECT master_volume FROM sound''')
        self.master_volume = USER_DB_CURSOR.fetchone()[0]
        self.narrator_intro_opacity = 255
        self.music_track_opacity = 0
        self.is_muted = False

    def add_track(self, music_track):
        music_track.playback_finish_callback = self.on_music_track_playback_finish
        self.music_track = music_track

    def add_narrator_intro(self, narrator_intro):
        narrator_intro.playback_finish_callback = self.on_narrator_intro_playback_finish
        self.narrator_intro = narrator_intro

    def play(self):
        try:
            self.music_track.play(_MIDI_DEVICE, (self.master_volume / 100) * (self.music_track_opacity / 255))
        except AttributeError:
            pass

        try:
            self.narrator_intro.play(_MIDI_DEVICE, (self.master_volume / 100) * (self.narrator_intro_opacity / 255))
        except AttributeError:
            pass

    def on_master_volume_update(self, new_master_volume):
        self.master_volume = new_master_volume

    def on_music_track_opacity_update(self, new_opacity):
        self.music_track_opacity = new_opacity

    def on_narrator_intro_opacity_update(self, new_opacity):
        self.narrator_intro_opacity = new_opacity

    def on_music_track_playback_finish(self):
        self.music_track = None

    def on_narrator_intro_playback_finish(self):
        self.narrator_intro = None

    def on_mute(self):
        self.is_muted = True
        ctypes.windll.winmm.midiOutSetVolume(_MIDI_DEVICE, 0)

    def on_unmute(self):
        self.is_muted = False
        ctypes.windll.winmm.midiOutSetVolume(_MIDI_DEVICE, 65535)
