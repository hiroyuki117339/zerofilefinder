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
    except (OSError, IOError):
        return False

def search_zero_files(root_dir, output_file):
    """Search for files with all-zero first 200 bytes and write results to CSV"""
    results = []
    
    # Walk through the directory recursively
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if is_all_zero(file_path):
                try:
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
                except OSError:
                    continue
    
    # Write results to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['path', 'filename', 'size', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

if __name__ == '__main__':
    root_dir = '/Users/hiroyuki/Downloads'
    output_file = '/Users/hiroyuki/Documents/listup.csv'
    
    print(f"Searching for files in {root_dir}...")
    search_zero_files(root_dir, output_file)
    print(f"\nResults have been written to {output_file}")
