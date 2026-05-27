
"""
Splits a combined text file of blocklist filters.
"""

# Version 1.0.0
# Edited: 2026-05-28 06:09:15 +10:00

# Generated using AI (duck.ai)
# Tested on local PC and on GitHub

# IMPORTS
import os

def split_file_by_size(filename, chunk_size_mb=80):
    """
    Splits a file into chunks of specified size (in MB).
    Output files are named: *_000.txt, *_001.txt, etc.
    """
    chunk_size = chunk_size_mb * 1024 * 1024  # Convert MB to bytes
    file_number = 0

    with open(filename, 'rb') as f_in:
        while True:
            chunk = f_in.read(chunk_size)
            if not chunk:
                break

            # Create output filename with 3-digit numbering (e.g., .000, .001)
            out_filename = f"{filename}_{file_number:03d}.txt"

            with open(out_filename, 'wb') as f_out:
                f_out.write(chunk)

            print(f"Created {out_filename} ({len(chunk)} bytes)")
            file_number += 1

# Usage
BLOCKLIST_COMBINED = 'blocklist_combined_filterlist.txt'
split_file_by_size(blocklist_combined, 80)

try:
    os.remove(blocklist_combined)
    print(f"{blocklist_combined} deleted successfully.")
except FileNotFoundError:
    print(f"{blocklist_combined} does not exist.")
except PermissionError:
    print(f"Permission denied to delete {blocklist_combined}.")
