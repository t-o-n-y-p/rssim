class VideoAdapterNotSupportedException(Exception):
    """
    This exception is raised when video adapter maximum texture size is less than maximum texture size in the app
    (currently 8192).
    """
    def __init__(self):
        super().__init__()
        self.text = 'Unfortunately, your video adapter is not supported. \nMake sure your operating system uses correct video adapter for this game. \nIf yes, please upgrade your computer.'
        self.caption = 'Video Adapter Error'


class MonitorNotSupportedException(Exception):
    """
    This exception is raised when monitor resolution (width or height) is less than minimum required
    (currently 1280x720).
    """
    def __init__(self):
        super().__init__()
        self.text = 'Unfortunately, your monitor resolution is too low to launch this game. \nOnly 1280x720 and higher resolutions are supported.'
        self.caption = 'Monitor Resolution Error'
