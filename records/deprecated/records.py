from result import MatchResult
from records.player import Player
from records import Fight

class Record:
    def __init__(self, player:Player):
        self.player = player
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.matches: list[Fight] = []

    def __str__(self):
        return (f"--- {self.player.name} ---\n"
                f"Wins: {self.wins}\n"
                f"Losses: {self.losses}\n"
                f"Draws: {self.draws}\n"
                f"Matches: {len(self.matches)}\n")

    def to_txt(self):
        return f"{self.player.name}: {self.wins}-{self.losses}-{self.draws} [{len(self.matches)}]"

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
