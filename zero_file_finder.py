import os
import csv
from datetime import datetime

def is_all_zero(file_path):
    """Check if the first 200 bytes of a file are all zero"""
    try:
        with open(file_path, 'rb') as f:
            data = f.read(200)
            # Check if all bytes are zero
            return all(b == 0 for b in data)
    except (OSError, IOError) as e:
        return False, str(e)

def search_zero_files(root_dir, output_file):
    """Search for files with all-zero first 200 bytes and write results to CSV
    Also records files with read errors in error.csv"""
    results = []
    error_results = []
    
    # Walk through the directory recursively
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            result = is_all_zero(file_path)
            if result is not False:
                if result is True:
                    file_size = os.path.getsize(file_path)
                    timestamp = os.path.getmtime(file_path)
                    timestamp_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                    
                    results.append({
                        'path': os.path.dirname(file_path),
                        'filename': filename,
                        'size': file_size,
                        'timestamp': timestamp_str
                    })
                    print(f"Found: {file_path} (Size: {file_size} bytes)")
            else:
                error_results.append({
                    'path': os.path.dirname(file_path),
                    'filename': filename,
                    'error': result[1]
                })
                print(f"Error reading {file_path}: {result[1]}")
    
    # Write results to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['path', 'filename', 'size', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # Write error results to error.csv if there are any errors
    if error_results:
        error_file = os.path.join(os.path.dirname(output_file), 'error.csv')
        with open(error_file, 'w', newline='', encoding='utf-8') as error_csv:
            error_fieldnames = ['path', 'filename', 'error']
            error_writer = csv.DictWriter(error_csv, fieldnames=error_fieldnames)
            error_writer.writeheader()
            error_writer.writerows(error_results)
            print(f"\nError information has been written to {error_file}")

if __name__ == '__main__':
    root_dir = '/Users/hiroyuki/Downloads'
    output_file = '/Users/hiroyuki/Documents/listup.csv'
    
    print(f"Searching for files in {root_dir}...")
    search_zero_files(root_dir, output_file)
    print(f"\nResults have been written to {output_file}")
