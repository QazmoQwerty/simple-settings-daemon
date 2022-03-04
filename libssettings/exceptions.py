
class SSettingsError(Exception):
    pass

class QuitException(Exception):
    def __init__(self) -> None:
        super().__init__('Quitting...')
