# utility.py
# Command: python utility.py
#
# This module provides utility functions used across the project.
# Features include:
#   - get_credentials_path: Automatically returns the path to credentials.json.
#   - dynamic_module_discovery: Discover Python modules in a specified folder.
#   - run_git_pull: Stub function for performing a Git pull to update local scripts.
#   - retry_on_rate_limit: Decorator to retry API calls when a rate limit error (HTTP 429) occurs.
#   - reorder_sheets: Reorder sheets in the spreadsheet to a specified order.

import os
import subprocess
import time
import functools
from googleapiclient.errors import HttpError

def get_credentials_path():
    """
    Returns the default path to credentials.json.
    Assumes the file is located in a folder named 'Credentials' one level up from the current script's directory.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    credentials_path = os.path.join(base_dir, "Credentials", "credentials.json")
    return credentials_path

def dynamic_module_discovery(scripts_folder):
    """
    Discover Python modules in the specified scripts folder.
    
    Args:
        scripts_folder (str): The path to the folder containing Python scripts.
    
    Returns:
        list: A list of module names (without the .py extension) available in the folder.
    """
    modules = []
    if not os.path.isdir(scripts_folder):
        print(f"Scripts folder '{scripts_folder}' does not exist.")
        return modules
    
    for filename in os.listdir(scripts_folder):
        if filename.endswith(".py") and filename != os.path.basename(__file__):
            module_name = os.path.splitext(filename)[0]
            modules.append(module_name)
    return modules

def run_git_pull(repo_path):
    """
    Run 'git pull' in the specified repository path.
    
    Args:
        repo_path (str): The path to the Git repository.
    """
    if not os.path.isdir(repo_path):
        print(f"Repository path '{repo_path}' does not exist.")
        return
    
    try:
        result = subprocess.run(["git", "-C", repo_path, "pull"], capture_output=True, text=True)
        print("Git pull output:")
        print(result.stdout)
    except Exception as e:
        print(f"Error running git pull: {e}")

def retry_on_rate_limit(max_retries=5, initial_delay=2):
    """
    Decorator that retries the decorated function when an HTTP 429 (rate limit exceeded) error occurs.
    Uses exponential backoff.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except HttpError as e:
                    if e.resp.status == 429:
                        print(f"Rate limit exceeded in {func.__name__}. Retrying in {delay} seconds... (attempt {attempt+1}/{max_retries})")
                        time.sleep(delay)
                        delay *= 2
                    else:
                        raise
            raise Exception("Max retries exceeded due to rate limit.")
        return wrapper
    return decorator

def reorder_sheets(service, spreadsheet_id):
    """
    Reorder sheets in the spreadsheet to have the following order:
      1. "TFC Mod History"
      2. "Records" (or "Rankings")
      3. "Template"
      4. All other sheets (assumed to be fighter sheets) in alphabetical order by title.
    """
    # Retrieve spreadsheet metadata.
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = spreadsheet.get('sheets', [])
    
    # Fixed sheet names (case-insensitive).
    fixed_order_names = ["TFC Mod History", "Records", "Template"]
    fixed_sheets = {}
    other_sheets = []
    
    for sheet in sheets:
        props = sheet.get("properties", {})
        title = props.get("title", "")
        sheet_id = props.get("sheetId")
        if title.lower() in [name.lower() for name in fixed_order_names]:
            fixed_sheets[title.lower()] = (sheet_id, title)
        else:
            other_sheets.append((sheet_id, title))
    
    # Build new order list.
    new_order = []
    for fixed_name in fixed_order_names:
        key = fixed_name.lower()
        if key in fixed_sheets:
            new_order.append(fixed_sheets[key])
    other_sheets.sort(key=lambda x: x[1].lower())
    new_order.extend(other_sheets)
    
    # Prepare batchUpdate requests.
    requests = []
    for index, (sheet_id, title) in enumerate(new_order):
        requests.append({
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sheet_id,
                    "index": index
                },
                "fields": "index"
            }
        })
    
    if requests:
        body = {"requests": requests}
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute()
        print("Sheets reordered successfully.")
    else:
        print("No sheets to reorder.")

def utilities_menu(service, spreadsheet_id):
    """
    Display a utilities menu.
    Currently available:
      1. Reorder Sheets
      0. Return to Main Menu
    """
    while True:
        print("\n=== Utilities Menu ===")
        print("1. Reorder Sheets")
        print("0. Return to Main Menu")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            reorder_sheets(service, spreadsheet_id)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

# Allow testing this module independently.
if __name__ == '__main__':
    print("Testing utility functions:")
    print("Default credentials path:", get_credentials_path())
    
    scripts_folder = os.path.dirname(os.path.abspath(__file__))
    print("Discovered modules in the scripts folder:", dynamic_module_discovery(scripts_folder))
    
    # Uncomment and set repo_path to test git pull functionality:
    # repo_path = "<your_repo_path_here>"
    # run_git_pull(repo_path)
