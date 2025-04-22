# analysis.py
# Command for testing: python analysis.py
#
# This module provides functions to perform basic analysis on fighter records.
# Analysis options include:
#   - Best Win Streak
#   - Best Win-Loss Ratio (with a minimum match requirement)
#   - Fighter with Most Wins
#
# These functions assume that fighter data is stored in a summary sheet (e.g., "Fighter Summary")
# with appropriate column headers (e.g., "Fighter Name", "Win Streak", "Wins", "Losses").

def run_analysis(service, spreadsheet_id):
    """
    Display analysis options to the user and run the selected analysis.
    
    Args:
        service: Authenticated Google Sheets API service.
        spreadsheet_id (str): The ID of the spreadsheet containing fighter data.
    """
    while True:
        print("\n=== Analysis Options ===")
        print("1. Analyze Best Win Streak")
        print("2. Analyze Best Win-Loss Ratio")
        print("3. Analyze Fighter with Most Wins")
        print("0. Back to Main Menu")
        
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            analyze_win_streak(service, spreadsheet_id)
        elif choice == "2":
            analyze_win_loss_ratio(service, spreadsheet_id)
        elif choice == "3":
            analyze_most_wins(service, spreadsheet_id)
        elif choice == "0":
            print("Returning to main menu.")
            break
        else:
            print("Invalid choice. Please try again.")

def analyze_win_streak(service, spreadsheet_id):
    """
    Analyze the summary sheet to determine which fighter has the best win streak.
    
    Assumes that the summary sheet contains a header row with "Win Streak" and fighter names in the first column.
    """
    summary_sheet = input("Enter the name of the summary sheet (default 'Fighter Summary'): ").strip() or "Fighter Summary"
    range_name = f"'{summary_sheet}'!A1:Z100"  # Adjust as needed
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name
    ).execute()
    values = result.get('values', [])
    
    if not values:
        print("No data found in the summary sheet.")
        return

    header = values[0]
    if "Win Streak" not in header:
        print("No 'Win Streak' column found in the summary sheet.")
        return
    
    win_streak_idx = header.index("Win Streak")
    fighter_name_idx = 0  # Assuming fighter name is in the first column.
    max_streak = None
    fighter_with_max = None
    
    for row in values[1:]:
        if len(row) > win_streak_idx:
            try:
                streak = int(row[win_streak_idx])
            except ValueError:
                continue
            if max_streak is None or streak > max_streak:
                max_streak = streak
                fighter_with_max = row[fighter_name_idx]
    
    if fighter_with_max is not None:
        print(f"Fighter with the best win streak: {fighter_with_max} ({max_streak} wins in a row)")
    else:
        print("Unable to determine best win streak.")

def analyze_win_loss_ratio(service, spreadsheet_id):
    """
    Analyze the summary sheet to determine which fighter has the best win-loss ratio,
    considering only fighters with a minimum number of matches.
    
    Assumes that the summary sheet contains "Wins" and "Losses" columns and fighter names in the first column.
    """
    summary_sheet = input("Enter the name of the summary sheet (default 'Fighter Summary'): ").strip() or "Fighter Summary"
    range_name = f"'{summary_sheet}'!A1:Z100"
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name
    ).execute()
    values = result.get('values', [])
    
    if not values:
        print("No data found in the summary sheet.")
        return

    header = values[0]
    if "Wins" not in header or "Losses" not in header:
        print("Required columns 'Wins' and 'Losses' not found in the summary sheet.")
        return
    
    wins_idx = header.index("Wins")
    losses_idx = header.index("Losses")
    fighter_name_idx = 0
    try:
        min_matches = int(input("Enter the minimum number of matches required: ").strip())
    except ValueError:
        print("Invalid input. Using minimum matches = 0.")
        min_matches = 0
    
    best_ratio = None
    fighter_with_best = None
    
    for row in values[1:]:
        try:
            wins = int(row[wins_idx])
            losses = int(row[losses_idx]) if len(row) > losses_idx and row[losses_idx] != "" else 0
        except ValueError:
            continue
        total_matches = wins + losses
        if total_matches < min_matches or total_matches == 0:
            continue
        ratio = wins / total_matches
        if best_ratio is None or ratio > best_ratio:
            best_ratio = ratio
            fighter_with_best = row[fighter_name_idx]
    
    if fighter_with_best is not None:
        print(f"Fighter with the best win-loss ratio: {fighter_with_best} ({best_ratio:.2f} ratio)")
    else:
        print("No fighter met the minimum match requirement for analysis.")

def analyze_most_wins(service, spreadsheet_id):
    """
    Analyze the summary sheet to determine which fighter has the most wins.
    
    Assumes that the summary sheet contains a "Wins" column and fighter names in the first column.
    """
    summary_sheet = input("Enter the name of the summary sheet (default 'Fighter Summary'): ").strip() or "Fighter Summary"
    range_name = f"'{summary_sheet}'!A1:Z100"
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name
    ).execute()
    values = result.get('values', [])
    
    if not values:
        print("No data found in the summary sheet.")
        return

    header = values[0]
    if "Wins" not in header:
        print("No 'Wins' column found in the summary sheet.")
        return
    
    wins_idx = header.index("Wins")
    fighter_name_idx = 0
    max_wins = None
    fighter_with_max = None
    
    for row in values[1:]:
        try:
            wins = int(row[wins_idx])
        except (ValueError, IndexError):
            continue
        if max_wins is None or wins > max_wins:
            max_wins = wins
            fighter_with_max = row[fighter_name_idx]
    
    if fighter_with_max is not None:
        print(f"Fighter with the most wins: {fighter_with_max} ({max_wins} wins)")
    else:
        print("Unable to determine the fighter with the most wins.")

# Allow testing this module independently.
if __name__ == '__main__':
    print("This module is intended to be called from main_menu.py and provided with a Google Sheets service and spreadsheet ID.")
    print("Run main_menu.py to test analysis functionality.")
