class NotSupportedVideoAdapterException(Exception):
    def __init__(self):
        self.surface = None
        self.text = 'Your video adapter is not supported.'
        self.caption = 'Video Adapter Error'
