import os
import sys

from player import Player
from result import MatchResult

# TODO update paths to pathLib
class Fight:
    file_path:os.PathLike = None
    player1:Player = None
    player2:Player = None
    winner = None
    result:MatchResult = None

    def __init__(self, file_path, player1:Player=None, player2:Player=None):
        self.file_path = file_path
        if player1 and player2:
            self.player1 = player1
            self.player2 = player2
        elif file_path.endswith('.txt'):
            self.player1 = Player(os.path.basename(self.file_path).split("_vs_")[0], txt=self.file_path)
            self.player2 = Player(os.path.basename(file_path).split("_vs_")[1].rstrip(".txt"), txt=self.file_path)
        else:
            self.player1 = Player(os.path.basename(self.file_path).split("_vs_")[0], json=self.file_path)
            self.player2 = Player(os.path.basename(file_path).split("_vs_")[1].rstrip(".txt"), json=self.file_path)

        self.find_result()

    def __str__(self):
        out = (f"--- {os.path.basename(self.file_path)} ---\n"
                f"{self.player1}"
                f"{self.player2}"
                f"--- Result ---\n")
        if self.winner:
            out += f"{self.winner.name} {self.result.value}\n"
            return out
        else:
            out += f"{self.result.value}\n"
            return out

    def find_result(self):
        with open(self.file_path, "rb") as file:
            file.seek(-2, os.SEEK_END)
            while file.read(1) != b"\n":
                file.seek(-2, os.SEEK_CUR)
            last_line = file.readline().decode("utf-8").rstrip("\n")
            self.result = MatchResult.from_line(last_line)
            if self.result is None:
                raise RuntimeWarning(f"Result of {self.file_path} not found in enum.")
            if self.result is not MatchResult.UNDOCUMENTED:
                if last_line.split(" ")[0] is self.player1.name:
                    self.winner = self.player1
                else:
                    self.winner = self.player2


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "..", "..", "Data", "Events_Stats", "TFC", "TFC_4")
    for file in os.listdir(path):
        match_path = os.path.join(path, file)
        print(match_path)
        print(Fight(match_path))
