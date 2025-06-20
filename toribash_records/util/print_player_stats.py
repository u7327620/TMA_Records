from toribash_records.player import Player
from toribash_records.util.path_finding import from_relative
from toribash_records.util.get_all_records import get_tfc_history

def update_fighters_txt(players: dict[str, Player]):
    fighter_directory = from_relative("../Data/Fighters")
    for player in players.values():
        data = pretty_player_stats(player.player_name, players)
        with open(f"{fighter_directory}/{player.player_name}_Database.txt", "w") as txt_file:
            txt_file.writelines(data)


def pretty_player_stats(player_name: str, players: dict[str, Player]) -> str:
    output = ""
    player_stats = players[player_name].get_stats()
    wins, losses, draws = players[player_name].get_win_loss()

    output += f"--- {player_name} stats ---\n"
    output += f"[W-L-D]: {wins}-{losses}-{draws}\n"
    for key in sorted(player_stats.keys()):
        if type(player_stats[key]) == float:
            output += f"{key}: {player_stats[key]:.1f}%\n"
        else:
            output += f"{key}: {player_stats[key]:}\n"

    output += f"\n--- {player_name} match history ---\n"
    for match in sorted(players[player_name].get_matches(), key=lambda x: int(x.event_name.split("_")[1])):
        if match.winner:
            if match.winner.lower() == player_name.lower():
                output += f"**W** "
            else:
                output += f"**L** "
        elif match.result[-1] == "DRAW":
            output += f"**D** "

        if match.result[-1] not in ["UNDOCUMENTED", "TKO", "DECISION", "DRAW", "SUBMISSION", "FORFEIT"]:
            raise RuntimeError(f"Bullshit {match.result[-1]} in {match.file_path.split("\\")[-2]} ({match.file_path.split("\\")[-1]})\n")
        output += f"{match.result[-1]} in {match.file_path.split("\\")[-2]} ({match.file_path.split("\\")[-1]})\n"
    return output


if __name__ == "__main__":
    players = get_tfc_history()
    update_fighters_txt(players)