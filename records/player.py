from records.toribash_match import ToribashMatch


class Player:
    def __init__(self, player_name):
        self.player_name = player_name
        self.matches: list[ToribashMatch] = []

    def add_match(self, match: ToribashMatch):
        pass

    def get_match_history(self, event_name: str=None) -> list[ToribashMatch]:
        if event_name: # Filter by specific event
            pass
        else:
            pass

    def get_stats(self, event_name: str=None) -> dict:
        if event_name: # Filter by specific event
            pass
        else:
            pass