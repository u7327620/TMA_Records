import os

from records.player import Player
from records.toribash_match import ToribashMatch
from records.util.path_finding import from_relative


def get_tfc_history() -> dict[str, Player]:
    all_matches: list[ToribashMatch] = get_all_matches()
    all_players: dict[str, Player] = {}

    for match in all_matches:
        if match.player1_name not in all_players.keys():
            all_players[match.player1_name] = Player(match.player1_name)
        if match.player2_name not in all_players.keys():
            all_players[match.player2_name] = Player(match.player2_name)

        all_players[match.player1_name].add_match(match)
        all_players[match.player2_name].add_match(match)

    return all_players

def get_tfc_player_records():
    r = sorted(get_tfc_history().values(), key=lambda x: x.player_name)
    a = []
    i = []
    recent_tfc = ["TFC_22", "TFC_21", "TFC_20"]
    for player in r:
        wins, losses, draws = player.get_win_loss()
        streak = []
        active = False
        for tfc in recent_tfc:
            match = player.get_matches(tfc)
            if len(match) > 0:
                active = True
                match = match[0] # No handling for multiple fights in one event
                if match.winner:
                    if match.winner.lower() == player.player_name.lower():
                        streak.append("w")
                        continue
                    else:
                        streak.append("l")
                        continue
            streak.append("?")

        if active:
            a.append(f"{player.player_name}: {wins}-{losses}-{draws} [{"-".join(streak)}]")
        else:
            i.append(f"{player.player_name}: {wins}-{losses}-{draws}")

    print("# Active rankings (last 2 TFC)")
    print(f"<Name>: <W>-<L>-<D> <{", ".join(recent_tfc)}>\n")
    print("\n".join(a))
    print("\n# Inactive rankings")
    print(f"<Name>: <W>-<L>-<D>\n")
    print("\n".join(i))

def get_all_matches() -> list[ToribashMatch]:
    all_matches: list[ToribashMatch] = []
    tfc_dir = from_relative("../Data/Events_Stats/TFC")
    for folder in os.listdir(tfc_dir):
        current_tfc_dir = os.path.join(tfc_dir, folder)
        for filename in os.listdir(current_tfc_dir):
            if filename.endswith(".json"):
                all_matches.append(ToribashMatch(os.path.join(current_tfc_dir, filename)))
    return all_matches
