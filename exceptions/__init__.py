class VideoAdapterNotSupportedException(Exception):
    def __init__(self):
        super().__init__()
        self.text = 'Unfortunately, your video adapter is not supported. \nMake sure your operating system uses correct video adapter for this game. \nIf yes, please upgrade your computer.'
        self.caption = 'Video Adapter Error'


class MonitorNotSupportedException(Exception):
    def __init__(self):
        super().__init__()
        self.text = 'Unfortunately, your monitor resolution is too low to launch this game. \nOnly 1280x720 and higher resolutions are supported.'
        self.caption = 'Monitor Resolution Error'


class UpdateIncompatibleException(Exception):
    def __init__(self):
        super().__init__()
        self.text = 'Unfortunately, current game version is incompatible with your previous game version. \nYou need to play the game again from scratch.'
        self.caption = 'Update failed'
