import os
import csv
from datetime import datetime

def is_all_zero(file_path):
    """Check if the first 200 bytes of a file are all zero"""
    try:
        with open(file_path, 'rb') as f:
            data = f.read(200)
            # Check if all bytes are zero
            if all(b == 0 for b in data):
                return True, True
            return True, False
    except (OSError, IOError) as e:
        return False, str(e)

def search_zero_files(root_dir, regular_output_file, broken_output_file):
    """Search for files with all-zero first 200 bytes and write results to CSV
    Also records files with read errors in error.csv"""
    regular_results = []
    corrupted_results = []
    error_results = []
    
    # Walk through the directory recursively
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            # Skip system files
            if (filename == '.DS_Store' or
                filename.lower() == 'thumbs.db' or
                (filename.lower().startswith('thumbcache_') and filename.lower().endswith('.db'))):
                continue
            
            file_path = os.path.join(dirpath, filename)
            result = is_all_zero(file_path)
            if result[0]:
                file_size = os.path.getsize(file_path)
                timestamp = os.path.getmtime(file_path)
                timestamp_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                
                if result[1]:  # Check if all bytes are zero
                    corrupted_results.append({
                        'full_path': file_path,
                        'path': os.path.dirname(file_path),
                        'filename': filename,
                        'size': file_size,
                        'timestamp': timestamp_str
                    })
                    print(f"Found corrupted file: {file_path} (Size: {file_size} bytes)")
                else:  # Regular file (not all-zero bytes)
                    regular_results.append({
                        'full_path': file_path,
                        'path': os.path.dirname(file_path),
                        'filename': filename,
                        'size': file_size,
                        'timestamp': timestamp_str
                    })
                    print(f"Found valid file: {file_path} (Size: {file_size} bytes)")
            elif not result[0]:
                error_results.append({
                    'path': os.path.dirname(file_path),
                    'filename': filename,
                    'error': result[1]
                })
                print(f"Error reading {file_path}: {result[1]}")
    
    # Write valid results to CSV
    with open(regular_output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['full_path', 'path', 'filename', 'size', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Write count as first line
        csvfile.write(f"Number of regular files: {len(regular_results)}\n")
        writer.writeheader()
        writer.writerows(regular_results)
        print(f"\nRegular files have been written to {regular_output_file}")

    # Write broken results to CSV
    with open(broken_output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['full_path', 'path', 'filename', 'size', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Write count as first line
        csvfile.write(f"Number of broken files: {len(corrupted_results)}\n")
        writer.writeheader()
        writer.writerows(corrupted_results)
        print(f"\nBroken files have been written to {broken_output_file}")

    # Write error results to error.csv if there are any errors
    if error_results:
        error_file = os.path.join(os.path.dirname(regular_output_file), 'error.csv')
        with open(error_file, 'w', newline='', encoding='utf-8') as error_csv:
            error_fieldnames = ['path', 'filename', 'error']
            error_writer = csv.DictWriter(error_csv, fieldnames=error_fieldnames)
            error_writer.writeheader()
            error_writer.writerows(error_results)
            print(f"\nError information has been written to {error_file}")

if __name__ == '__main__':
    root_dir = '/Volumes/MacData/01.最新'
    regular_output_file = '/Users/hiroyuki/Documents/regular_file_list.csv'
    broken_output_file = '/Users/hiroyuki/Documents/broken_file_list.csv'
    
    print(f"Searching for files in {root_dir}...")
    search_zero_files(root_dir, regular_output_file, broken_output_file)
    print("\nSearch completed.")
