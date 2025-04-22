# report_generator.py
# Command: python report_generator.py
#
# This module provides functions to generate detailed reports and exports.
# Features include:
#   - generate_csv_report: Exports data from a specified sheet to a CSV file.
#   - generate_summary_report: Generates a text summary report from a summary sheet.
#   - Versioning of reports: Older reports in the Reports folder are renamed (incremented)
#     so that the newest report is always named with _1.
#
# Reports are saved in the Reports folder located in the main RecordKeeping folder.

import os
import csv

def version_existing_reports(report_folder, base_report_name):
    """
    Rename existing reports in report_folder so that the new report can be named as {base_report_name}_1.txt.
    Existing reports are incremented by 1 in their version number.
    
    For example, if there's Report_1.txt, it will be renamed to Report_2.txt, etc.
    """
    files = [f for f in os.listdir(report_folder) if f.startswith(base_report_name) and f.endswith('.txt')]
    
    def extract_version(filename):
        # Assumes filename format: base_report_name_N.txt
        try:
            parts = filename.split('_')
            version = int(parts[-1].replace('.txt', ''))
        except:
            version = 0
        return version
    
    # Sort files in descending order by version number
    files.sort(key=extract_version, reverse=True)
    
    for file in files:
        version = extract_version(file)
        new_version = version + 1
        old_path = os.path.join(report_folder, file)
        new_name = f"{base_report_name}_{new_version}.txt"
        new_path = os.path.join(report_folder, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed {old_path} to {new_path}")

def generate_csv_report(service, spreadsheet_id, sheet_name, output_file):
    """
    Export data from the specified sheet to a CSV file.
    
    Args:
        service: Authenticated Google Sheets API service.
        spreadsheet_id (str): The ID of the spreadsheet.
        sheet_name (str): The name of the sheet to export.
        output_file (str): The full path of the output CSV file.
    """
    range_name = f"'{sheet_name}'!A1:Z1000"  # Adjust range as needed
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name
    ).execute()
    values = result.get('values', [])
    
    if not values:
        print("No data found in the sheet.")
        return
    
    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(values)
        print(f"CSV report generated successfully: {output_file}")
    except Exception as e:
        print(f"Error writing CSV report: {e}")

def generate_summary_report(service, spreadsheet_id, summary_sheet="Fighter Summary", report_folder=None):
    """
    Generate a summary report from the summary sheet.
    
    If report_folder is provided, the report is saved as a text file with versioning.
    Otherwise, the report is printed to the console.
    
    Args:
        service: Authenticated Google Sheets API service.
        spreadsheet_id (str): The ID of the spreadsheet.
        summary_sheet (str): The name of the summary sheet.
        report_folder (str): (Optional) The folder where reports are stored.
    """
    range_name = f"'{summary_sheet}'!A1:Z1000"
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name
    ).execute()
    values = result.get('values', [])
    
    if not values:
        print("No data found in the summary sheet.")
        return
    
    header = values[0]
    report_lines = []
    report_lines.append("=== Summary Report ===")
    report_lines.append(" | ".join(header))
    report_lines.append("-" * 50)
    
    for row in values[1:]:
        report_lines.append(" | ".join(row))
    
    report_lines.append("=== End of Report ===")
    report_content = "\n".join(report_lines)
    
    if report_folder:
        os.makedirs(report_folder, exist_ok=True)
        base_report_name = "Report"
        # Version existing reports so the new report becomes Report_1.txt
        version_existing_reports(report_folder, base_report_name)
        output_file = os.path.join(report_folder, f"{base_report_name}_1.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"Summary report saved to {output_file}")
    else:
        print(report_content)

# Allow testing this module independently.
if __name__ == '__main__':
    print("This module is intended to be called from main_menu.py with proper Google Sheets service and spreadsheet_id.")
