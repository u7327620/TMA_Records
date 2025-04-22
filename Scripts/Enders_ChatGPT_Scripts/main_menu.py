# main_menu.py
# Command: python main_menu.py

import os
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import subprocess

from fighter_processing import process_all_fighters, process_single_fighter
from event_processing import update_specific_event
from analysis import run_analysis
from utility import get_credentials_path, utilities_menu

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def authenticate(credentials_file):
    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('sheets', 'v4', credentials=creds)
    return service

def get_fighter_file_by_name(fighter_name):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fighters_dir = os.path.join(base_dir, "Data", "Fighters")
    for file in os.listdir(fighters_dir):
        if file.lower().endswith('.txt'):
            base_name = os.path.splitext(file)[0]
            if base_name.lower() == fighter_name.lower():
                return os.path.join(fighters_dir, file)
    return None

def run_standalone_scripts():
    """
    Look in the 'Standalone' folder for .py scripts,
    list them with numbers, and allow the user to run a script by selecting its number.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    standalone_dir = os.path.join(base_dir, "Standalone")
    
    if not os.path.isdir(standalone_dir):
        print("Standalone folder not found at:", standalone_dir)
        return
    
    scripts = [f for f in os.listdir(standalone_dir) if f.lower().endswith('.py')]
    if not scripts:
        print("No standalone scripts found in the Standalone folder.")
        return
    
    print("\nStandalone Scripts:")
    # Sort scripts alphabetically.
    scripts = sorted(scripts)
    for i, script in enumerate(scripts, start=1):
        print(f"{i}. {script}")
    
    choice = input("Enter the number of the script to run (or 0 to cancel): ").strip()
    try:
        choice_num = int(choice)
    except ValueError:
        print("Invalid input. Returning to main menu.")
        return
    
    if choice_num == 0:
        return
    if 1 <= choice_num <= len(scripts):
        script_to_run = os.path.join(standalone_dir, scripts[choice_num - 1])
        print(f"Running {script_to_run} ...")
        subprocess.call(["python", script_to_run])
    else:
        print("Invalid choice number.")

def main():
    print("=== TFC Record Keeping Main Menu ===")
    credentials_file = get_credentials_path()
    if not os.path.exists(credentials_file):
        print("Credentials file not found at:", credentials_file)
        sys.exit(1)
    
    service = authenticate(credentials_file)
    
    spreadsheet_id = "1SVzVUSdprXhI9_gtq-u4dsAZnp-ptt5B4yodxIAnmes"
    template_sheet_name = "Template"
    
    while True:
        print("\nMain Menu Options:")
        print("1. Process ALL fighters")
        print("2. Update with a specific event")
        print("3. Process a specific fighter")
        print("4. Run Analysis / Generate Reports")
        print("5. Utilities")
        print("6. Standalone Scripts")
        print("0. Exit")
        
        choice = input("Enter your choice (number): ").strip()
        
        if choice == "1":
            process_all_fighters(service, spreadsheet_id, template_sheet_name)
        elif choice == "2":
            update_specific_event(service, spreadsheet_id, template_sheet_name)
        elif choice == "3":
            fighter_name = input("Enter the fighter's name: ").strip()
            fighter_file = get_fighter_file_by_name(fighter_name)
            if fighter_file is None:
                print(f"No fighter profile found for '{fighter_name}' in the Data/Fighters folder.")
            else:
                process_single_fighter(service, spreadsheet_id, template_sheet_name, fighter_file)
        elif choice == "4":
            run_analysis(service, spreadsheet_id)
        elif choice == "5":
            utilities_menu(service, spreadsheet_id)
        elif choice == "6":
            run_standalone_scripts()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
