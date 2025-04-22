# replace_folder_spaces.py
# Command: python replace_folder_spaces.py

import os

def replace_spaces_in_folder_names(folder_path):
    """
    Replace spaces with underscores in all folder names located within folder_path.
    """
    if not os.path.isdir(folder_path):
        print(f"The folder '{folder_path}' does not exist or is not a directory.")
        return

    # Iterate over each item in the folder_path.
    for item in os.listdir(folder_path):
        full_path = os.path.join(folder_path, item)
        if os.path.isdir(full_path) and " " in item:
            new_item = item.replace(" ", "_")
            new_full_path = os.path.join(folder_path, new_item)
            try:
                os.rename(full_path, new_full_path)
                print(f"Renamed: '{full_path}' --> '{new_full_path}'")
            except Exception as e:
                print(f"Failed to rename '{full_path}' to '{new_full_path}'. Error: {e}")

def main():
    folder_path = input("Enter the path of the folder containing subfolders: ").strip()
    replace_spaces_in_folder_names(folder_path)

if __name__ == '__main__':
    main()
