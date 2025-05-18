import os

from player import Player
from result import MatchResult

# TODO update paths to pathLib
class Fight:
    def __init__(self, file_path):
        self.file_path: os.path = file_path
        self.winner:Player = None
        self.result = MatchResult.UNDOCUMENTED
        if file_path.endswith('.txt'):
            names = os.path.basename(self.file_path).lower().split("_vs_")
            names[1] = names[1][0:-4]
            self.player1 = Player(names[0], txt=self.file_path)

            # TODO fix this shitty ass naming system
            # Repeat matches are titled "<name>_vs_<name> <n>" where n is the count of repeats
            if len(names[1].split(" "))>1:
                self.player2 = Player(names[1].split(" ")[0], txt=self.file_path)
            else:
                self.player2 = Player(names[1], txt=self.file_path)

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
            if last_line.lower() == "undocumented.":
                self.result = MatchResult(last_line.lower())
            else:
                try:
                    self.result = MatchResult(" ".join(last_line.lower().split(" ")[1:]))
                except ValueError as e:
                    e.add_note(f"{last_line} in {self.file_path}")
                    raise e
                if last_line.split(" ")[0].lower() == self.player1.name:
                    self.winner = self.player1
                else:
                    self.winner = self.player2


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "..", "..", "Data", "Events_Stats", "TFC")
    for folder in os.listdir(path):
        folder_path = os.path.join(path, folder)
        for file in os.listdir(folder_path):
            match_path = os.path.join(folder_path, file)
            print(match_path)
            print(Fight(match_path))
