from toribash_records.objects.toribash_match import ToribashMatch


class Player:
    """
    Represents a player in a ToribashMatch

    Attributes:
        player_name (str): name of this player [Used for EQ]
        matches (list[ToribashMatch]): list of ToribashMatch objects the player participated in
    """

    def __init__(self, player_name):
        self.player_name: str = player_name
        self.matches: list[ToribashMatch] = []

    def __eq__(self, other):
        return self.player_name.lower() == other.player_name.lower()

    def add_match(self, match: ToribashMatch):
        """Adds a match to this player's list of matches without any safety checks"""
        self.matches.append(match)

    def get_matches(self, event_name: str=None) -> list[ToribashMatch]:
        """Returns list[ToribashMatch] optionally filtered by ToribashMatch.event_name"""
        if event_name: # Filter by specific event
            return [x for x in self.matches if x.event_name == event_name]
        else:
            return self.matches

    def get_win_loss(self, event_name: str=None) -> tuple[int, int, int]:
        """Returns W/L/D optionally filtered by ToribashMatch.event_name"""
        if event_name:
            matches = [x for x in self.matches if x.event_name == event_name]
        else:
            matches = self.matches

        wins, losses, draws = 0, 0, 0
        for match in matches:
            if match.winner:
                if match.winner.lower() == self.player_name.lower():
                    wins += 1
                else:
                    losses += 1
            else:
                if match.result[-1] == "DRAW":
                    draws += 1
        return wins, losses, draws

    def get_stats(self, event_name: str=None) -> dict:
        """Returns dict of stats found in ToribashMatches optionally filtered by ToribashMatch.event_name"""
        if event_name: # Filter by specific event
            matches = [x for x in self.matches if x.event_name == event_name]
        else:
            matches = self.matches

        stats = {"Successful Submissions": 0, "Strikes Defended": 0}
        for match in matches:
            if match.player1_name == self.player_name:
                p = match.player1_name
            elif match.player2_name == self.player_name:
                p = match.player2_name
            else:
                raise RuntimeError(f"{match.player1_name} nor player object {match.player2_name} match {self.player_name}")

            silly_keys = ["Accuracy", "Strike Defense Rate", "Takedown Accuracy", "Takedown Defense Rate"]
            for key in match.stats[p]:
                if key in silly_keys:
                    continue
                elif key in stats.keys():
                    stats[key] += match.stats[p][key]
                else:
                    stats.update({key: match.stats[p][key]})
            if match.result[-1] == "SUBMISSION":
                stats["Successful Submissions"] += 1

        try:
            if stats["Strikes Thrown"] != 0:
                stats.update({"Accuracy": stats["Strikes Landed"] / stats["Strikes Thrown"] * 100})
            else:
                stats.update({"Accuracy": "N/A"})
            if stats["Takedowns Attempted"] != 0:
                stats.update({"Takedown Accuracy": stats["Takedowns Finished"] / stats["Takedowns Attempted"] * 100})
            else:
                stats.update({"Takedown Accuracy": "N/A"})
            if stats["Takedowns Defended"] + stats["Times Taken Down"] != 0:
                stats.update({"Takedown Defense Rate": stats["Takedowns Defended"] / (stats["Takedowns Defended"] + stats["Times Taken Down"]) * 100})
            else:
                stats.update({"Takedown Defense Rate": "N/A"})
            if "Strikes Defended" in stats.keys():
                if stats["Strikes Absorbed"] != 0:
                    stats.update({"Strike Defense Rate": stats["Strikes Defended"] / stats["Strikes Absorbed"] * 100})
        except KeyError as e:
            print(f"KeyError {e} during {self.player_name} stat retrieval")
        return stats
