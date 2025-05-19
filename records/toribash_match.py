import json
import os


class ToribashMatch:
    def __init__(self, file_path: str | os.PathLike):
        self.file_path: os.path = file_path
        self.player1_name = None
        self.player2_name = None
        self.stats = {}
        self.meta = None
        self.winner = None
        self.result = None
        self.records = None
        self.event_name = None
        self.extract_file_data()

    def extract_file_data(self, file_path: str=None):
        if file_path is None:
            file_path = self.file_path

        with open(file_path, mode='r', encoding='utf-8') as f:
            f_data = json.load(f)

        for key in f_data:
            if key == "Meta":
                self.meta = f_data[key]
                self.event_name = self.meta["Event"]
            elif key == "Result":
                self.result = f_data[key]
            elif key == 'Records':
                self.records = f_data[key]
            elif key == 'Winner':
                self.winner = f_data[key]
            else:
                if not self.player1_name:
                    self.player1_name = key.lower()
                    self.stats.update({key.lower(): f_data[key]})
                elif not self.player2_name:
                    self.player2_name = key.lower()
                    self.stats.update({key.lower(): f_data[key]})
                else:
                    print(f"Unknown key in data: {key} from {file_path}")
