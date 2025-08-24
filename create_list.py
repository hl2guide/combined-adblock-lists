
"""
Creates a text file every hour using GitHub actions.
This module is being developed.
"""

# import datetime
from datetime import datetime
from zoneinfo import ZoneInfo

# Get the current date and time
SYDNEY_TIMEZONE = ZoneInfo('Australia/Sydney')
NOW_IN_SYDNEY = datetime.now(SYDNEY_TIMEZONE)

NOW = NOW_IN_SYDNEY.strftime("%A, %B %d, %Y, %H:%M:%S %p")
DATE_STRING = NOW

# Create a text file with a specified filename
FILENAME = "current_date.txt"

try:
    with open(FILENAME, "w", encoding="utf-8") as file:
        # Write only the formatted date string to the file
        file.write(DATE_STRING)
    print(f"File '{FILENAME}' created with date '{DATE_STRING}'.")
except IOError as e:
    print(f"An error occurred while creating the file: {e}")
