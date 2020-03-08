from typing import final

from midi_player import Instrument


@final
class Piano(Instrument):
    instrument_id = 0
    channel_id = 0


@final
class Harp(Instrument):
    instrument_id = 46
    channel_id = 1


@final
class Violin(Instrument):
    instrument_id = 40
    channel_id = 2


@final
class Drums(Instrument):
    instrument_id = 0
    channel_id = 9


# drums are not assigned because they are already assigned according to the MIDI standard
Piano.assign_to_channel()
Harp.assign_to_channel()
Violin.assign_to_channel()
