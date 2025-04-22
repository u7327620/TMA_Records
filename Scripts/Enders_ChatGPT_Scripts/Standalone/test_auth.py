import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the scope for full access to Google Sheets.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def main():
    # Prompt the user for the credentials JSON file path.
    credentials_file = input("Enter the path to your credentials JSON file: ").strip()
    if not os.path.exists(credentials_file):
        print("The file does not exist. Please check the path and try again.")
        return

    # Set up the OAuth flow using the provided credentials file.
    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
    creds = flow.run_local_server(port=0)  # Opens your browser for authentication.

    # Build the Sheets API service.
    service = build('sheets', 'v4', credentials=creds)

    # Use your provided spreadsheet ID.
    spreadsheet_id = '1SVzVUSdprXhI9_gtq-u4dsAZnp-ptt5B4yodxIAnmes'
    
    # Prompt the user for the range name or use a default.
    default_range = 'Sheet1!A1:D5'
    range_name = input(f"Enter the range name to read from (default: {default_range}): ").strip() or default_range

    # Retrieve data from the spreadsheet.
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    # Display the retrieved data.
    if not values:
        print('No data found.')
    else:
        print("Data from spreadsheet:")
        for row in values:
            print(row)

if __name__ == '__main__':
    main()
