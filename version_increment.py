
"""
Creates a VERSION.txt file and then increments it over each
Python script related commit.
"""

# Version 1.0.1
# Edited: 2026-02-09 15:18:54 +1100

# Generated using AI (duck.ai)
# Tested on local PC and on GitHub

# IMPORTS
import os

def read_version():
    """
    Reads the VERSION.txt file as a string.

    Returns:
        string: A version string in the VERSION.txt file.
    """
    with open('VERSION.txt', 'r', encoding="utf-8") as file:
        return file.read().strip()

def write_version(version):
    """
    Writes a new updated version string to the VERSION.txt file as a string.
    """
    with open('VERSION.txt', 'w', encoding="utf-8") as file:
        file.write(version)

def increment_version(version):
    """
    Increments the VERSION.txt file.

    Returns:
        string: An incremented version string.
    """
    major, minor, patch = map(int, version.split('.'))
    # Increment the patch version
    patch += 1
    return f"{major}.{minor}.{patch}"

if __name__ == "__main__":
    current_version = ''
    new_version = ''
    if os.path.exists('VERSION.txt'):
        current_version = read_version()
        new_version = increment_version(current_version)
    else:
        new_version = "1.0.1"  # Starting version
    write_version(new_version)
    print(f"Existing Version: {current_version}")
    print(f"New Version: {new_version}")
    print("Updated Version File: VERSION.txt")
