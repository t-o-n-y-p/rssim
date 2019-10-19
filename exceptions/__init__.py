from typing import final


@final
class VideoAdapterNotSupportedException(Exception):
    def __init__(self):
        super().__init__()
        self.caption = 'Video Adapter Error'
        self.text = 'Unfortunately, your video adapter is not supported. \nMake sure your operating system uses correct video adapter for this game. \nIf yes, please upgrade your computer.'


@final
class MonitorNotSupportedException(Exception):
    def __init__(self):
        super().__init__()
        self.caption = 'Monitor Resolution Error'
        self.text = 'Unfortunately, your monitor resolution is too low to launch this game. \nOnly 1280x720 and higher resolutions are supported.'


@final
class UpdateIncompatibleException(Exception):
    def __init__(self):
        super().__init__()
        self.caption = 'Update failed'
        self.text = 'Unfortunately, current game version is incompatible with your previous game version. \nYou need to play the game again from scratch.'


@final
class HackingDetectedException(Exception):
    def __init__(self):
        super().__init__()
        self.caption = 'Hacking detected'
        self.text = 'We believe you tried to modify game configuration illegally. \nYou are not welcome to play this game.'
