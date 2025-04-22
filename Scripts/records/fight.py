import os
import sys

from player import Player
from result import MatchResult

class Fight:
    file_path:os.PathLike = None
    player1:Player = None
    player2:Player = None
    result:MatchResult = None

    def __init__(self, file_path, player1:Player=None, player2:Player=None):
        self.file_path = file_path
        if player1 is None:
            self.player1 = Player(os.path.basename(self.file_path).split("_vs_")[0])
        else:
            self.player1 = player1
        if player2 is None:
            self.player2 = Player(os.path.basename(file_path).split("_vs_")[1].rstrip(".txt"))
        else:
            self.player2 = player2
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