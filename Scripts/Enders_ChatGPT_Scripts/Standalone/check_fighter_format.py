#!/usr/bin/env python
# check_fighter_format.py
# Command: python check_fighter_format.py
#
# This script scans text files and extracts the keys used, comparing them against two known formats.
# It supports both fighter files and fight files.
# For each file, it prints:
#   - The detected format (OLD, NEW, or AMBIGUOUS)
#   - Differences (missing keys and extra keys) and their count.
#
# Folder structure is assumed to be:
#   <RecordKeeping>/
#       Data/
#           Fighters/      (fighter text files)
#           Event_Stats/   (fight text files, organized by event subfolder)
#
# Expected Keys (normalized to lowercase):
#
# OLD FIGHTER FORMAT:
OLD_FIGHTER_KEYS = {
    "player",
    "strikes landed",
    "strikes thrown",
    "strikes absorbed",
    "accuracy",
    "knockdowns",
    "highest striking differential",
    "average striking differential",
    "takedowns finished",
    "takedowns attempted",
    "takedown accuracy",
    "takedowns defended",
    "times taken down",
    "takedown defense rate",
    "submissions attempted",
    "submissions",
    "submission accuracy",
    "tko wins",
    "decision wins",
    "fights",
    "wins",
    "losses",
    "draws",
    "tko losses",
    "submission losses",
    "decision losses"
}

# NEW FIGHTER FORMAT:
NEW_FIGHTER_KEYS = {
    "player",
    "strikes landed",
    "strikes thrown",
    "accuracy",
    "strikes absorbed",
    "strikes defended",
    "strike defense rate",
    "knockdowns",
    "knocked down",
    "highest striking differential",
    "average striking differential",
    "takedowns finished",
    "takedowns attempted",
    "takedown accuracy",
    "takedowns defended",
    "times taken down",
    "takedown defense rate",
    "submissions attempted",
    "submissions",
    "submission accuracy",
    "point deductions",
    "tko wins",
    "decision wins",
    "forfeit wins",
    "fights",
    "wins",
    "losses",
    "draws",
    "tko losses",
    "submission losses",
    "decision losses",
    "forfeit losses"
}

# OLD FIGHT FORMAT:
OLD_FIGHT_KEYS = {
    "player",
    "strikes landed",
    "strikes thrown",
    "strikes absorbed",
    "accuracy",
    "knockdowns",
    "striking differential",
    "takedowns finished",
    "takedowns attempted",
    "takedown accuracy",
    "takedowns defended",
    "times taken down",
    "takedown defense rate",
    "submissions attempted"
}

# NEW FIGHT FORMAT:
NEW_FIGHT_KEYS = {
    "player",
    "strikes landed",
    "strikes thrown",
    "accuracy",
    "strikes absorbed",
    "strikes defended",
    "strike defense rate",
    "knockdowns",
    "knocked down",
    "striking differential",
    "takedowns finished",
    "takedowns attempted",
    "takedown accuracy",
    "takedowns defended",
    "times taken down",
    "takedown defense rate",
    "submissions attempted"
}

import os

def extract_format_keys(file_path):
    """
    Extract keys from a text file.
    Assumes the first non-empty line is the fighter's name (or event name).
    Then, all subsequent lines up to a line starting with '---' are taken as keys.
    Returns a set of keys normalized to lowercase.
    """
    keys = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    if not lines:
        return set()
    # Skip the first line.
    for line in lines[1:]:
        if line.startswith('---'):
            break
        keys.append(line.lower())
    return set(keys)

def compare_formats(file_keys, format_keys):
    """
    Compare file keys with expected keys.
    Returns a tuple (missing_keys, extra_keys) as sets.
    """
    missing = format_keys - file_keys
    extra = file_keys - format_keys
    return missing, extra

def analyze_file_format(file_path, expected_old, expected_new):
    """
    Analyze a file's format against both expected sets.
    Returns a dict with detected format, differences, and file keys.
    """
    file_keys = extract_format_keys(file_path)
    old_missing, old_extra = compare_formats(file_keys, expected_old)
    new_missing, new_extra = compare_formats(file_keys, expected_new)
    old_diff = len(old_missing) + len(old_extra)
    new_diff = len(new_missing) + len(new_extra)
    
    if old_diff < new_diff:
        detected_format = "OLD"
        diff_count = old_diff
    elif new_diff < old_diff:
        detected_format = "NEW"
        diff_count = new_diff
    else:
        detected_format = "AMBIGUOUS"
        diff_count = old_diff  # they are equal in this case.
    
    return {
        "file": file_path,
        "detected_format": detected_format,
        "diff_count": diff_count,
        "missing": (old_missing if detected_format == "OLD" else new_missing) if detected_format != "AMBIGUOUS" else (old_missing.union(new_missing)),
        "extra": (old_extra if detected_format == "OLD" else new_extra) if detected_format != "AMBIGUOUS" else (old_extra.union(new_extra)),
        "file_keys": file_keys
    }

def process_folder(folder_path, expected_old, expected_new):
    """
    Process all .txt files in folder_path, analyze their formats, and print detailed info.
    Returns a list of result dicts.
    """
    if not os.path.isdir(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return []
    files = [f for f in os.listdir(folder_path) if f.lower().endswith('.txt')]
    if not files:
        print("No .txt files found in the folder.")
        return []
    results = []
    for file in files:
        file_path = os.path.join(folder_path, file)
        result = analyze_file_format(file_path, expected_old, expected_new)
        results.append(result)
        
        print(f"\nFile: {result['file']}")
        print("Detected keys:")
        for key in sorted(result["file_keys"]):
            print(f"  - {key}")
        print(f"Format detected: {result['detected_format']}")
        if result['diff_count'] > 0:
            print(f"Differences count: {result['diff_count']}")
            if result['missing']:
                print("Missing keys:")
                for key in sorted(result['missing']):
                    print(f"  - {key}")
            if result['extra']:
                print("Extra keys:")
                for key in sorted(result['extra']):
                    print(f"  - {key}")
        else:
            print("The file matches the expected format exactly.")
    return results

def main_menu():
    """
    Presents a menu:
      1. Check Fighter Format (from Data/Fighters)
      2. Check Fight Format (from Data/Event_Stats)
      0. Exit
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fighters_folder = os.path.join(base_dir, "Data", "Fighters")
    event_stats_folder = os.path.join(base_dir, "Data", "Event_Stats")
    
    while True:
        print("\n=== Check File Format Menu ===")
        print("1. Check Fighter Format (Data/Fighters)")
        print("2. Check Fight Format (Data/Event_Stats)")
        print("0. Exit")
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            print(f"Processing fighter files in {fighters_folder} ...")
            process_folder(fighters_folder, OLD_FIGHTER_KEYS, NEW_FIGHTER_KEYS)
        elif choice == "2":
            if not os.path.isdir(event_stats_folder):
                print(f"Event_Stats folder not found at: {event_stats_folder}")
                continue
            events = [d for d in os.listdir(event_stats_folder) if os.path.isdir(os.path.join(event_stats_folder, d))]
            if not events:
                print("No event folders found in Event_Stats.")
                continue
            print("\nAvailable Event Folders:")
            for i, event in enumerate(sorted(events), start=1):
                print(f"{i}. {event}")
            print("0. Process all events")
            event_choice = input("Enter the number of the event to process (or 0 for all): ").strip()
            try:
                event_choice_num = int(event_choice)
            except ValueError:
                print("Invalid input.")
                continue
            if event_choice_num == 0:
                selected_events = events
            elif 1 <= event_choice_num <= len(events):
                selected_events = [sorted(events)[event_choice_num - 1]]
            else:
                print("Invalid selection.")
                continue
            for event in selected_events:
                event_folder = os.path.join(event_stats_folder, event)
                print(f"\nProcessing fight files in event folder: {event_folder}")
                process_folder(event_folder, OLD_FIGHT_KEYS, NEW_FIGHT_KEYS)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    main_menu()

if __name__ == '__main__':
    main()
