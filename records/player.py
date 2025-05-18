from records.toribash_match import ToribashMatch


class Player:
    def __init__(self, player_name):
        self.player_name: str = player_name
        self.matches: list[ToribashMatch] = []

    def __eq__(self, other):
        return self.player_name.lower() == other.player_name.lower()

    def add_match(self, match: ToribashMatch):
        self.matches.append(match)

    def get_matches(self, event_name: str=None) -> list[ToribashMatch]:
        if event_name: # Filter by specific event
            return [x for x in self.matches if x.event_name == event_name]
        else:
            return self.matches

    def get_win_loss(self, event_name: str=None) -> {}:
        if event_name:
            matches = [x for x in self.matches if x.event_name == event_name]
        else:
            matches = self.matches

        wins = len([x for x in self.matches if x.result])

    def get_stats(self, event_name: str=None) -> dict:
        if event_name: # Filter by specific event
            matches = [x for x in self.matches if x.event_name == event_name]
        else:
            matches = self.matches

        stats = {}
        for match in matches:
            if match.player1_name == self.player_name:
                p = match.player1_name
            elif match.player2_name == self.player_name:
                p = match.player2_name
            else:
                raise RuntimeError(f"{match.player1_name} nor player object {match.player2_name} match {self.player_name}")
            for key in match.stats[p]:
                if key in stats.keys():
                    stats[key] += match.stats[p][key]
                else:
                    stats.update({key: match.stats[p][key]})
        return stats
