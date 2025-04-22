# spreadsheetformat
# Command: python spreadsheetformat.py

import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# We only need read-only access for this script.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def authenticate(credentials_file):
    """
    Authenticate using OAuth and return a Sheets API service object.
    """
    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('sheets', 'v4', credentials=creds)
    return service

def get_sheet_data(service, spreadsheet_id, sheet_name):
    """
    Retrieve all data from the specified sheet.
    """
    # Using just the sheet name as the range retrieves all data in that sheet.
    range_name = sheet_name
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name
    ).execute()
    values = result.get('values', [])
    return values

def main():
    # Prompt for the credentials file path.
    credentials_file = input("Enter the path to your credentials JSON file: ").strip()
    if not os.path.exists(credentials_file):
        print("The credentials file does not exist. Please check the path and try again.")
        return

    service = authenticate(credentials_file)
    
    # Prompt for the spreadsheet ID.
    spreadsheet_id = input("Enter the spreadsheet ID: ").strip()
    if not spreadsheet_id:
        print("No spreadsheet ID provided.")
        return

    # Prompt for the sheet name; default to "Template"
    sheet_name = input("Enter the sheet name (default: Template): ").strip() or "Template"
    
    values = get_sheet_data(service, spreadsheet_id, sheet_name)
    
    if not values:
        print("No data found in the sheet.")
    else:
        print("Data from the sheet:")
        for row in values:
            print(row)

if __name__ == '__main__':
    main()
