from toribash_records.util.get_all_records import get_tfc_history


if __name__ == "__main__":
    players = get_tfc_history()
    player_name = "sorude"
    player_stats = players[player_name].get_stats()
    wins, losses, draws = players[player_name].get_win_loss()
    print(f"\n--- {player_name} stats ---")
    print(f"[W-L-D]: {wins}-{losses}-{draws}")
    for key in sorted(player_stats.keys()):
        print(f"{key}: {player_stats[key]}")

    print(f"\n--- {player_name} match history ---")
    for match in sorted(players[player_name].get_matches(), key=lambda x: x.event_name):
        msg = ""
        if match.winner:
            if match.winner.lower() == player_name.lower():
                msg += f"**W** {match.result[-1]}"
            else:
                msg += f"**L** {match.result[-1]}"
        elif match.result[-1] == "DRAW":
            msg += f"**D** {match.result[-1]}"
        msg += f" in {match.file_path.split("/")[-2]} ({match.file_path.split("/")[-1]})"
        print(msg)