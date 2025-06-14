import json
import os


class ToribashMatch:
    """
    Represents a recorded (as a .json) match as documented by Yahummy.

    Attributes:
        file_path (os.path): the file path to the recorded match
        player1_name (str): first player to appear in the text file
        player2_name (str): second player to appear in the text file
        stats (dict[str, Player]): stats for both players accessible by player name
        meta (): metadata contained in the .json file
        winner (None or str): if winner, their name .lower() else None
        result (List[str]): Result key from the .json file
        records (): Records key from the .json file
        event_name (str): name of the event that was recorded [TFC_22, TFC_21]
    """
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

    def __str__(self):
        if self.winner:
           return (f"{self.winner} beats "
                   f"{self.player1_name if self.winner!=self.player1_name else self.player2_name} in: {self.file_path}")
        elif self.result[-1] == "DRAW":
            return f"{self.player1_name} draws with {self.player2_name} in: {self.file_path}"
        else:
            return f"{self.player1_name} vs {self.player2_name} in: {self.file_path}"

    def extract_file_data(self, file_path: str=None):
        """Extracts from .json into the ToribashMatch format. Prints when encountering unknown keys"""
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
                self.winner = f_data[key].lower()
            else:
                if not self.player1_name:
                    self.player1_name = key.lower()
                    self.stats.update({key.lower(): f_data[key]})
                elif not self.player2_name:
                    self.player2_name = key.lower()
                    self.stats.update({key.lower(): f_data[key]})
                else:
                    print(f"Unknown key in data: {key} from {file_path}")
