import datetime

# Get the current date and time
now = datetime.datetime.now()

# Format the date in Australian format (DD/MM/YYYY)
date_string = now.strftime("%d/%m/%Y")

# Create a text file with a specified filename
filename = "current_date.txt"

try:
    with open(filename, 'w') as file:
        # Write only the formatted date string to the file
        file.write(date_string)
    print(f"File '{filename}' created successfully with the date '{date_string}'.")
except IOError as e:
    print(f"An error occurred while creating the file: {e}")
