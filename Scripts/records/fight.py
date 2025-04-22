import os
import sys

from player import Player
from result import MatchResult

# TODO update paths to pathLib
class Fight:
    file_path:os.PathLike = None
    player1:Player = None
    player2:Player = None
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

        self.result = self.find_result()

    def __str__(self):
        return (f"--- {os.path.basename(self.file_path)} ---\n"
                f"{self.player1}"
                f"{self.player2}"
                f"--- Result ---\n"
                f"{self.result.value}\n")

    def find_result(self): # TODO Add a result finding logic
        return MatchResult.CLOSE_DECISION

if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "..", "..", "Data", "Events_Stats", "TFC", sys.argv[1]) # i.e. TFC_1/Bladerunnr_vs_Danewninja.txt
    print(Fight(path))