# rename_vs_recursive.py
# Command: python rename_vs.py

import os
import re

def rename_vs_in_filename(filename):
    """
    Given a filename (without its path), return a new filename where any occurrence of
    'vs' that isn't already surrounded by underscores is replaced with '_vs_'.
    """
    base, ext = os.path.splitext(filename)
    new_base = re.sub(r'(?<!_)vs(?!_)', '_vs_', base)
    return new_base + ext

def rename_files_in_subfolders(root_folder):
    """
    Recursively rename all .txt files in root_folder and its subfolders by adding underscores around 'vs'.
    """
    if not os.path.isdir(root_folder):
        print(f"The folder '{root_folder}' does not exist or is not a directory.")
        return

    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith('.txt'):
                new_filename = rename_vs_in_filename(filename)
                # Only rename if there is a change in the file name.
                if new_filename != filename:
                    old_file_path = os.path.join(dirpath, filename)
                    new_file_path = os.path.join(dirpath, new_filename)
                    try:
                        os.rename(old_file_path, new_file_path)
                        print(f"Renamed: '{old_file_path}' -> '{new_file_path}'")
                    except Exception as e:
                        print(f"Error renaming '{old_file_path}': {e}")

def main():
    root_folder = input("Enter the path of the folder containing subfolders with txt files: ").strip()
    rename_files_in_subfolders(root_folder)

if __name__ == '__main__':
    main()
