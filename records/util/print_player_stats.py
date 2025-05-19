from records.util.get_all_records import get_tfc_history


if __name__ == "__main__":
    players = get_tfc_history()
    blade = players["bladerunnr"]
    for key, value in blade.get_stats().items():
        print(key, value)