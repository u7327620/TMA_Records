from records.util.get_all_records import get_tfc_history


if __name__ == "__main__":
    players = get_tfc_history()
    for match in players["cryink"].matches:
        print(match)
    print(players["cryink"].get_win_loss())