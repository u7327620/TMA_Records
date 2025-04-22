import os
from result import MatchResult
from Scripts.records.player import Player
from Scripts.records.fight import Fight


class Record:
    def __init__(self, player:Player):
        self.player = player
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.matches = []

    def __str__(self):
        return (f"--- {self.player.name} ---\n"
                f"Wins: {self.wins}\n"
                f"Losses: {self.losses}\n"
                f"Draws: {self.draws}\n"
                f"Matches: {len(self.matches)}\n")

    def to_txt(self):
        return f"{self.player.name}: {self.wins}-{self.draws}-{self.losses} [{len(self.matches)}]"

    def add_fight(self, new_fight:Fight):
        self.matches.append(new_fight)
        if new_fight.result is not MatchResult.UNDOCUMENTED:
            if new_fight.result is MatchResult.DRAW:
                self.draws += 1
            elif new_fight.winner is None: # cancer
                raise RuntimeError(f"{new_fight} has no winner and {new_fight.result} comp to undoc is {new_fight.result is MatchResult.UNDOCUMENTED}")
            elif new_fight.winner.name == self.player.name:
                self.wins += 1
            else:
                self.losses += 1

if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "..", "Data", "Events_Stats", "TFC")
    records:[str, Record] = {}
    for folder in sorted(os.listdir(path)):
        folder_path = os.path.join(path, folder)
        for file in sorted(os.listdir(folder_path)):
            match_path = os.path.join(folder_path, file)
            fight = Fight(match_path)
            if fight.player1.name not in records:
                records[fight.player1.name] = Record(fight.player1)
            if fight.player2.name not in records:
                records[fight.player2.name] = Record(fight.player2)
            records[fight.player2.name].add_fight(fight)
            records[fight.player1.name].add_fight(fight)
    output = "<Name>: <W>-<D>-<L> <played>\n\n"
    for record in sorted(records.values(), key=lambda r: len(r.matches), reverse=True):
        output += record.to_txt() + "\n"
    path = os.path.join(os.getcwd(), "records", "records.txt")
    with open(path, "w") as f:
        f.write(output)