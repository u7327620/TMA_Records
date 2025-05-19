import os

from records.player import Player
from records.toribash_match import ToribashMatch
from records.util.path_finding import from_relative


def get_tfc_history() -> dict[str, Player]:
    all_matches: list[ToribashMatch] = []
    all_players: dict[str, Player] = {}

    tfc_dir = from_relative("../Data/Events_Stats/TFC")
    for folder in os.listdir(tfc_dir):
        current_tfc_dir = os.path.join(tfc_dir, folder)
        for filename in os.listdir(current_tfc_dir):
            if filename.endswith(".json"):
                all_matches.append(ToribashMatch(os.path.join(current_tfc_dir, filename)))

    for match in all_matches:
        if match.player1_name not in all_players.keys():
            all_players[match.player1_name] = Player(match.player1_name)
        if match.player2_name not in all_players.keys():
            all_players[match.player2_name] = Player(match.player2_name)

        all_players[match.player1_name].add_match(match)
        all_players[match.player2_name].add_match(match)

    return all_players

if __name__ == "__main__":
    r = sorted(get_tfc_history().values(), key=lambda x: x.player_name)
    out = []
    for player in r:
        wins, losses, draws = player.get_win_loss()
        out.append(f"{player.player_name}: {wins}-{losses}-{draws}")

    print(f"<Name>: <W>-<L>-<D>\n")
    print("\n".join(out))
