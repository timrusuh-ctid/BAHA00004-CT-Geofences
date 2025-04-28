import os
import csv
import argparse

def extract_filenames_to_csv(folder_path, output_csv):
    """
    Extract filenames from a folder and save them to a CSV file.
    Remove file extensions and add numbering.
    """
    # Check if folder exists
    if not os.path.isdir(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return False
    
    # Get all files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # Sort files alphabetically
    files.sort()
    
    # Write to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['No', 'Filename'])
        
        # Write data rows
        for i, filename in enumerate(files, 1):
            # Remove file extension
            name_without_extension = os.path.splitext(filename)[0]
            writer.writerow([i, name_without_extension])
    
    print(f"Successfully created CSV file: {output_csv}")
    print(f"Processed {len(files)} files from {folder_path}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract filenames from a folder to CSV format.')
    parser.add_argument('folder', help='Path to the folder containing files')
    parser.add_argument('--output', '-o', default='filenames.csv', help='Output CSV file path (default: filenames.csv)')
    
    args = parser.parse_args()
    extract_filenames_to_csv(args.folder, args.output)