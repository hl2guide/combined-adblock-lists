
"""
Creates a text file every hour using GitHub actions.
This module is being developed.
"""

import datetime

# Get the current date and time
NOW = datetime.datetime.now()

# Format the date in Australian format (DD/MM/YYYY)
DATE_STRING = NOW.strftime("%d/%m/%Y")

# Create a text file with a specified filename
FILENAME = "current_date.txt"

try:
    with open(FILENAME, "w", encoding="utf-8") as file:
        # Write only the formatted date string to the file
        file.write(DATE_STRING)
    print(f"File '{FILENAME}' created with date '{DATE_STRING}'.")
except IOError as e:
    print(f"An error occurred while creating the file: {e}")
