# fighter_processing.py
# Command for testing: python fighter_processing.py
#
# This module processes fighter profile text files by:
#   - Parsing fighter files (supporting both old and new formats, filling missing fields with defaults).
#   - Duplicating a template Google Sheet (named "Template") and renaming/updating it with the fighter's name.
#   - Updating the fighter sheet with parsed and computed stats.
#   - Updating the Records (or Rankings) sheet with each fighter's record.
#
# Computed fields:
#   - "Average Striking Differential" and "Longest Win-Streak" are set to "TBD".
#   - "Win-Loss Ratio" is computed from wins and losses.
#   - "Average Knockdowns" is computed from knockdowns divided by fights.
#
# Also, a delay and retry/backoff mechanism is applied to API calls.

import os
import time
from utility import retry_on_rate_limit

# Delay constant (if needed in addition to retry decorator)
DELAY_SECONDS = 1

def parse_fighter_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    if not lines:
        raise ValueError("Fighter file is empty")
    
    fighter_name = lines[0]
    stats = {}
    bonuses = []
    bonus_section = False
    for line in lines[1:]:
        if line.startswith('---'):
            bonus_section = True
            continue
        if bonus_section:
            bonuses.append(line.lstrip("- ").strip())
        else:
            parts = line.rsplit(' ', 1)
            if len(parts) == 2:
                category, value = parts
                stats[category.strip()] = value.strip()
            else:
                stats[line] = ""
    return fighter_name, stats, bonuses

@retry_on_rate_limit()
def get_template_sheet_id(service, spreadsheet_id, template_sheet_name):
    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    time.sleep(DELAY_SECONDS)
    sheets = sheet_metadata.get('sheets', [])
    for sheet in sheets:
        properties = sheet.get('properties', {})
        if properties.get('title').strip().lower() == template_sheet_name.strip().lower():
            return properties.get('sheetId')
    return None

@retry_on_rate_limit()
def get_sheet_id_by_name(service, spreadsheet_id, sheet_name):
    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    time.sleep(DELAY_SECONDS)
    sheets = sheet_metadata.get('sheets', [])
    for sheet in sheets:
        properties = sheet.get('properties', {})
        if properties.get('title').strip().lower() == sheet_name.strip().lower():
            return properties.get('sheetId')
    return None

@retry_on_rate_limit()
def duplicate_template_sheet(service, spreadsheet_id, template_sheet_id, new_sheet_name):
    existing_sheet_id = get_sheet_id_by_name(service, spreadsheet_id, new_sheet_name)
    if existing_sheet_id is not None:
        print(f"Sheet with name '{new_sheet_name}' already exists. Updating existing sheet.")
        return existing_sheet_id
    body = {
        "requests": [
            {
                "duplicateSheet": {
                    "sourceSheetId": template_sheet_id,
                    "insertSheetIndex": 1,
                    "newSheetName": new_sheet_name
                }
            }
        ]
    }
    response = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()
    time.sleep(DELAY_SECONDS)
    replies = response.get('replies', [])
    if replies:
        return replies[0]['duplicateSheet']['properties']['sheetId']
    return None

@retry_on_rate_limit()
def update_fighter_sheet(service, spreadsheet_id, sheet_name, stats):
    range_name = f"'{sheet_name}'!A1:A100"
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name
    ).execute()
    time.sleep(DELAY_SECONDS)
    values = result.get('values', [])
    
    category_to_row = {}
    for i, row in enumerate(values, start=1):
        if row:
            category_to_row[row[0].strip().lower()] = i
    
    normalized_stats = { key.strip().lower(): value for key, value in stats.items() }
    
    expected_defaults = {
        "strikes defended": "0",
        "strike defense rate": "0",
        "knocked down": "0",
        "point deductions": "0",
        "forfeit wins": "0",
        "forfeit losses": "0"
    }
    for key, default in expected_defaults.items():
        if key not in normalized_stats:
            normalized_stats[key] = default
    
    if "average striking" in normalized_stats:
        normalized_stats["average striking differential"] = normalized_stats.pop("average striking")
    
    computed_fields = {
        "average striking differential": "TBD",
        "longest win-streak": "TBD"
    }
    
    data = []
    not_updated = []
    for key, value in normalized_stats.items():
        if key in computed_fields:
            continue
        if key in category_to_row:
            row_number = category_to_row[key]
            cell_range = f"'{sheet_name}'!B{row_number}"
            data.append({"range": cell_range, "values": [[value]]})
        else:
            not_updated.append(key)
    
    if "win-loss ratio" in category_to_row:
        try:
            wins = int(normalized_stats.get("wins", "0"))
            losses = int(normalized_stats.get("losses", "0"))
            total = wins + losses
            computed_ratio = f"{wins / total:.2f}" if total > 0 else "N/A"
        except ValueError:
            computed_ratio = "N/A"
        computed_fields["win-loss ratio"] = computed_ratio
    
    if "average knockdowns" in category_to_row:
        try:
            knockdowns = int(normalized_stats.get("knockdowns", "0"))
            fights = int(normalized_stats.get("fights", "0"))
            computed_avg = f"{knockdowns / fights:.2f}" if fights > 0 else "N/A"
        except ValueError:
            computed_avg = "N/A"
        computed_fields["average knockdowns"] = computed_avg
    
    for key, computed_value in computed_fields.items():
        if key in category_to_row:
            row_number = category_to_row[key]
            cell_range = f"'{sheet_name}'!B{row_number}"
            data.append({"range": cell_range, "values": [[computed_value]]})
    
    if data:
        body = {"valueInputOption": "USER_ENTERED", "data": data}
        service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body
        ).execute()
        time.sleep(DELAY_SECONDS)
        non_computed = [k for k in not_updated if k not in computed_fields]
        if non_computed:
            print("Note: The following non-computed categories were not updated (they may not be in the template):")
            print(", ".join(non_computed))
        else:
            print("All non-computed categories updated successfully.")
    else:
        print("No matching data to update in the sheet.")

@retry_on_rate_limit()
def update_records_sheet(service, spreadsheet_id, records_sheet_name, fighter_name, stats, champion_flag):
    normalized_stats = {k.strip().lower(): v for k, v in stats.items()}
    wins = normalized_stats.get("wins", "0")
    losses = normalized_stats.get("losses", "0")
    draws = normalized_stats.get("draws", "0")
    record_str = f"{wins}-{losses}-{draws}"
    
    range_name = f"'{records_sheet_name}'!A2:C"
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name
    ).execute()
    time.sleep(DELAY_SECONDS)
    values = result.get("values", [])
    
    row_to_update = None
    for i, row in enumerate(values, start=2):
        if len(row) >= 2 and row[1].strip().lower() == fighter_name.strip().lower():
            row_to_update = i
            break

    ranking = "Champion" if champion_flag else ""
    new_row = [ranking, fighter_name, record_str]
    
    if row_to_update:
        update_range = f"'{records_sheet_name}'!A{row_to_update}:C{row_to_update}"
        body = {"values": [new_row]}
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=update_range,
            valueInputOption="USER_ENTERED", body=body
        ).execute()
        time.sleep(DELAY_SECONDS)
        print(f"Updated records for fighter '{fighter_name}' in sheet '{records_sheet_name}'.")
    else:
        append_range = f"'{records_sheet_name}'!A2:C"
        body = {"values": [new_row]}
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=append_range,
            valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body=body
        ).execute()
        time.sleep(DELAY_SECONDS)
        print(f"Added fighter '{fighter_name}' to records sheet '{records_sheet_name}'.")

# Global variable for champion flag.
champion_flag_global = False

def process_single_fighter(service, spreadsheet_id, template_sheet_name, fighter_file):
    if not os.path.exists(fighter_file):
        print(f"Fighter file '{fighter_file}' does not exist.")
        return
    try:
        fighter_name, stats, bonuses = parse_fighter_file(fighter_file)
    except Exception as e:
        print(f"Error parsing fighter file '{fighter_file}': {e}")
        return
    print("\nParsed fighter:", fighter_name)
    print("Stats:", stats)
    print("Bonuses:", bonuses)
    
    global champion_flag_global
    champion_flag_global = any("tfc champion" in bonus.lower() for bonus in bonuses)
    
    template_sheet_id = get_template_sheet_id(service, spreadsheet_id, template_sheet_name)
    if template_sheet_id is None:
        print(f"Template sheet '{template_sheet_name}' not found.")
        return
    new_sheet_id = duplicate_template_sheet(service, spreadsheet_id, template_sheet_id, fighter_name)
    if new_sheet_id is None:
        print("Failed to duplicate or retrieve the fighter sheet.")
        return
    print(f"Using fighter sheet '{fighter_name}' (Sheet ID: {new_sheet_id}).")
    
    update_fighter_sheet(service, spreadsheet_id, fighter_name, stats)
    print(f"Updated fighter sheet '{fighter_name}' with stats and computed fields.")
    
    records_sheet_name = "Records"  # or "Rankings" depending on configuration.
    update_records_sheet(service, spreadsheet_id, records_sheet_name, fighter_name, stats, champion_flag_global)

def process_all_fighters(service, spreadsheet_id, template_sheet_name):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fighters_folder = os.path.join(base_dir, "Data", "Fighters")
    if not os.path.isdir(fighters_folder):
        print(f"Fighters folder not found at: {fighters_folder}")
        return
    files = os.listdir(fighters_folder)
    if not files:
        print("No fighter profile files found in folder.")
        return
    for file in files:
        if file.lower().endswith('.txt'):
            fighter_file = os.path.join(fighters_folder, file)
            print("\nProcessing file:", fighter_file)
            process_single_fighter(service, spreadsheet_id, template_sheet_name, fighter_file)

# Allow testing this module independently.
if __name__ == '__main__':
    print("Testing fighter_processing module:")
    test_file = input("Enter the path to a fighter profile text file for testing: ").strip()
    try:
        fighter_name, stats, bonuses = parse_fighter_file(test_file)
        print("Parsed fighter:", fighter_name)
        print("Stats:", stats)
        print("Bonuses:", bonuses)
    except Exception as e:
        print("Error:", e)
