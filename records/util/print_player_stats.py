from records.util.get_all_records import get_tfc_history


if __name__ == "__main__":
    players = get_tfc_history()
    player_name = "danewninja"
    player_stats = players[player_name].get_stats()
    print(f"\n--- {player_name} stats ---")
    for key in sorted(player_stats.keys()):
        print(f"{key}: {player_stats[key]}")
