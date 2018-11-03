class VideoAdapterNotSupportedException(Exception):
    def __init__(self):
        super().__init__()
        self.text = 'Your video adapter is not supported.'
        self.caption = 'Video Adapter Error'
