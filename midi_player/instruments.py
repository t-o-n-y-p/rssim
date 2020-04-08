from typing import final

from midi_player import Instrument, assign_to_channel


@final
@assign_to_channel
class Piano(Instrument):
    instrument_id = 0
    channel_id = 0


@final
@assign_to_channel
class Harp(Instrument):
    instrument_id = 46
    channel_id = 1


@final
@assign_to_channel
class Violin(Instrument):
    instrument_id = 40
    channel_id = 2


# drums are not assigned because they are already assigned according to the MIDI standard
@final
class Drums(Instrument):
    instrument_id = 0
    channel_id = 9
