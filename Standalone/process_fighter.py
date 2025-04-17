import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the scope for full access to Google Sheets.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def authenticate(credentials_file):
    """Authenticate using OAuth for a desktop app and return a Sheets service object."""
    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('sheets', 'v4', credentials=creds)
    return service

def parse_fighter_file(file_path):
    """
    Parse a fighter profile text file.
    Assumes the first non-empty line is the fighter's name.
    Lines after that (until a bonus section) are stat lines in the format:
       CategoryName [whitespace] Value
    After a line starting with '---' the remaining lines are treated as bonus entries.
    Returns: (fighter_name, stats_dict, bonuses_list)
    """
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
            # Remove leading '-' if present.
            bonuses.append(line.lstrip("- ").strip())
        else:
            # Split the line from the right so the last token is considered the value.
            parts = line.rsplit(' ', 1)
            if len(parts) == 2:
                category, value = parts
                stats[category.strip()] = value.strip()
            else:
                # If there's no value (like "Average Striking Differential")
                stats[line] = ""
    return fighter_name, stats, bonuses

def get_template_sheet_id(service, spreadsheet_id, template_sheet_name):
    """
    Retrieve the sheet ID for a sheet with title template_sheet_name.
    """
    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = sheet_metadata.get('sheets', [])
    for sheet in sheets:
        properties = sheet.get('properties', {})
        if properties.get('title') == template_sheet_name:
            return properties.get('sheetId')
    return None

def duplicate_template_sheet(service, spreadsheet_id, template_sheet_id, new_sheet_name):
    """
    Duplicate the template sheet and rename it to new_sheet_name.
    Returns the new sheet's ID.
    """
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
    replies = response.get('replies', [])
    if replies:
        return replies[0]['duplicateSheet']['properties']['sheetId']
    return None

def update_fighter_sheet(service, spreadsheet_id, sheet_name, stats):
    """
    Update the sheet named sheet_name (which is the newly duplicated sheet)
    by matching stat categories in column A with the keys from stats.
    The corresponding value is written in column B.
    """
    # Assume the template has category names in A1:A100.
    range_name = f"'{sheet_name}'!A1:A100"
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    
    # Map categories to their row number (starting at 1)
    category_to_row = {}
    for i, row in enumerate(values, start=1):
        if row:
            category_to_row[row[0].strip()] = i

    data = []
    for category, value in stats.items():
        if category in category_to_row:
            row_number = category_to_row[category]
            cell_range = f"'{sheet_name}'!B{row_number}"
            data.append({
                "range": cell_range,
                "values": [[value]]
            })
        else:
            print(f"Warning: Category '{category}' not found in sheet '{sheet_name}'")
    
    if data:
        body = {
            "valueInputOption": "USER_ENTERED",
            "data": data
        }
        service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()
    else:
        print("No matching data to update in the sheet.")

def main():
    # Prompt for the credentials JSON file path.
    credentials_file = input("Enter the path to your credentials JSON file: ").strip()
    if not os.path.exists(credentials_file):
        print("The file does not exist. Please check the path and try again.")
        return
    service = authenticate(credentials_file)
    
    # Spreadsheet setup: use your fighter profiles spreadsheet.
    spreadsheet_id = '1SVzVUSdprXhI9_gtq-u4dsAZnp-ptt5B4yodxIAnmes'
    template_sheet_name = "Sheet1"  # The template with category names in column A.
    
    # Prompt for the fighter file path.
    fighter_file = input("Enter the path to the fighter profile text file: ").strip()
    if not os.path.exists(fighter_file):
        print("The fighter file does not exist. Please check the path and try again.")
        return
    
    # Parse the fighter file.
    fighter_name, stats, bonuses = parse_fighter_file(fighter_file)
    print("Parsed fighter:", fighter_name)
    print("Stats:", stats)
    print("Bonuses:", bonuses)
    
    # Duplicate the template sheet and rename it with the fighter's name.
    template_sheet_id = get_template_sheet_id(service, spreadsheet_id, template_sheet_name)
    if template_sheet_id is None:
        print(f"Template sheet '{template_sheet_name}' not found.")
        return
    new_sheet_id = duplicate_template_sheet(service, spreadsheet_id, template_sheet_id, fighter_name)
    if new_sheet_id is None:
        print("Failed to duplicate the template sheet.")
        return
    print(f"Duplicated template sheet as '{fighter_name}' (Sheet ID: {new_sheet_id}).")
    
    # Update the new fighter sheet with the fighter's stats.
    update_fighter_sheet(service, spreadsheet_id, fighter_name, stats)
    print(f"Updated fighter sheet '{fighter_name}' with stats.")

if __name__ == '__main__':
    main()
