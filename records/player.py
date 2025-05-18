from records.toribash_match import ToribashMatch


class Player:
    def __init__(self, player_name):
        self.player_name: str = player_name
        self.matches: list[ToribashMatch] = []

    def __eq__(self, other):
        return self.player_name.lower() == other.player_name.lower()

    def add_match(self, match: ToribashMatch):
        pass

    def get_match_history(self, event_name: str=None) -> list[ToribashMatch]:
        if event_name: # Filter by specific event
            return [x for x in self.matches if x.event_name == event_name]
        else:
            return self.matches

    def get_stats(self, event_name: str=None) -> dict:
        if event_name: # Filter by specific event
            matches = [x for x in self.matches if x.event_name == event_name]
        else:
            matches = self.matches

        stats = {}
        for match in matches:
            p = None
            if match.player1_name == self.player_name:
                p = match.player1_name
            elif match.player2_name == self.player_name:
                p = match.player2_name
            else:
                raise RuntimeError(f"{match.player1_name} nor player object {match.player2_name} match {self.player_name}")
            for stat in match.stats[p]:
                stats[stat.name] += stat.value
        return stats
