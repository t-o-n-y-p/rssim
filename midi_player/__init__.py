import ctypes
from abc import ABC

from score import *


MIDI_DEVICE: Final = ctypes.c_void_p()
ctypes.windll.winmm.midiOutOpen(ctypes.byref(MIDI_DEVICE), 0, 0, 0, 0)
PROGRAM_CHANGE_MESSAGE_ID: Final = 0xC0


class Instrument(ABC):
    instrument_id: int
    channel_id: int

    @classmethod
    def assign_to_channel(cls):
        ctypes.windll.winmm.midiOutShortMsg(
            MIDI_DEVICE, cls.instrument_id << 8 | PROGRAM_CHANGE_MESSAGE_ID | cls.channel_id
        )


@final
class MIDIPlayer:
    def __init__(self):
        self.music_tracks = []
        self.narrator_intros = []
        self.master_volume = 255
        self.opacity = 255
        self.music_tracks_opacity = 255

    def add_track(self, music_track):
        music_track.playback_finish_callback = self.on_music_track_playback_finish
        self.music_tracks.append(music_track)

    def add_narrator_intro(self, narrator_intro):
        narrator_intro.playback_finish_callback = self.on_narrator_intro_playback_finish
        self.narrator_intros.append(narrator_intro)

    def play(self):
        for t in self.music_tracks:
            t.play((self.master_volume / 255) * (self.opacity / 255) * (self.music_tracks_opacity / 255))

        for i in self.narrator_intros:
            i.play((self.master_volume / 255) * (self.opacity / 255))

    def on_master_volume_update(self, new_volume):
        self.master_volume = new_volume
        ctypes.windll.winmm.midiOutSetVolume(MIDI_DEVICE, self.master_volume << 8 | self.master_volume)

    def on_music_track_playback_finish(self, music_track):
        self.music_tracks.remove(music_track)

    def on_narrator_intro_playback_finish(self, narrator_intro):
        self.narrator_intros.remove(narrator_intro)
