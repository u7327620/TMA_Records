import os
from importlib.resources import files


class ToribashMatch:
    def __init__(self, file_path: str):
        self.file_path: os.path = files(file_path)
        self.player1 = None
        self.player2 = None
        self.event_name = None

    