
"""
Creates a text file every hour using GitHub actions.
This module is being developed.
"""

# Downloads and then combines cosmetic filter lists into one text file.
# It also REMOVES allow rules, comment lines and duplicate lines.

# Version 1.0.1
# Edited: 2025-11-14 13:29:04 +1100

# Generated using AI
# Tested on local PC

# IMPORTS
import locale
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
import requests

# Testing list URLs
TESTING_URLS = [
    # Brave - YouTube Shorts (https://github.com/brave/adblock-lists/tree/master/brave-lists)
    "https://raw.githubusercontent.com/brave/adblock-lists/refs/heads/master/brave-lists/yt-shorts.txt",
    # Brave - YouTube Recommendations (https://github.com/brave/adblock-lists/tree/master/brave-lists)
    "https://raw.githubusercontent.com/brave/adblock-lists/refs/heads/master/brave-lists/yt-recommended.txt",
    # Brave - YouTube Distractions (https://github.com/brave/adblock-lists/tree/master/brave-lists)
    "https://raw.githubusercontent.com/brave/adblock-lists/refs/heads/master/brave-lists/yt-distracting.txt",
    # Brave - Social Elements Blocker (https://github.com/brave/adblock-lists/tree/master/brave-lists)
    "https://raw.githubusercontent.com/brave/adblock-lists/refs/heads/master/brave-lists/brave-social.txt",
    # Brave-specific additions to Easylist Cookie (https://github.com/brave/adblock-lists/tree/master/brave-lists)
    "https://raw.githubusercontent.com/brave/adblock-lists/refs/heads/master/brave-lists/brave-cookie-specific.txt",
    # uBlock - Cookie Notices
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/refs/heads/master/filters/annoyances-cookies.txt",
    # uBlock - Other Annoyances
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/refs/heads/master/filters/annoyances-others.txt",
    # uBlock - Badware Risks
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/refs/heads/master/filters/badware.txt",
    # uBlock filters (years)
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/refs/heads/master/filters/filters-2020.txt",
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/refs/heads/master/filters/filters-2021.txt",
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/refs/heads/master/filters/filters-2022.txt",
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/refs/heads/master/filters/filters-2023.txt",
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/refs/heads/master/filters/filters-2024.txt",
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/refs/heads/master/filters/filters-2025.txt",
    # uBlock - Privacy
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/refs/heads/master/filters/privacy.txt",
    # uBlock - Filters
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/refs/heads/master/filters/filters.txt",
    # uBlock - Unbreak
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/refs/heads/master/filters/unbreak.txt",
    # EasyList
    "https://cdn.statically.io/gh/uBlockOrigin/uAssetsCDN/main/thirdparties/easylist.txt",
    # AdGuard - Base filter
    "https://filters.adtidy.org/extension/ublock/filters/2_without_easylist.txt",
    # AdGuard - Mobile Ads filter
    "https://filters.adtidy.org/extension/ublock/filters/11.txt",
    # EasyPrivacy
    "https://ublockorigin.pages.dev/thirdparties/easyprivacy.txt",
    # EasyList - Cookie Notices
    "https://cdn.statically.io/gh/uBlockOrigin/uAssetsCDN/main/thirdparties/easylist-cookies.txt",
    # EasyList - Social Widgets
    "https://cdn.jsdelivr.net/gh/uBlockOrigin/uAssetsCDN@main/thirdparties/easylist-social.txt",
    # AdGuard Social Media filter
    "https://filters.adtidy.org/extension/ublock/filters/4.txt",
    # Anti-Facebook List
    "https://secure.fanboy.co.nz/fanboy-antifacebook.txt",
    # EasyList - Chat Widgets
    "https://cdn.jsdelivr.net/gh/uBlockOrigin/uAssetsCDN@main/thirdparties/easylist-chat.txt",
    # EasyList - Newsletter Notices
    "https://ublockorigin.pages.dev/thirdparties/easylist-newsletters.txt",
    # EasyList - Notifications
    "https://cdn.jsdelivr.net/gh/uBlockOrigin/uAssetsCDN@main/thirdparties/easylist-notifications.txt",
    # EasyList - Annoyances
    "https://cdn.statically.io/gh/uBlockOrigin/uAssetsCDN/main/thirdparties/easylist-annoyances.txt",
    # uBlock filters - Annoyances
    "https://cdn.statically.io/gh/uBlockOrigin/uAssetsCDN/main/filters/annoyances.min.txt",
    # YouTube Neuter - sponsorblock
    "https://raw.githubusercontent.com/mchangrh/yt-neuter/main/filters/sponsorblock.txt",
    # YouTube Neuter
    "https://raw.githubusercontent.com/mchangrh/yt-neuter/main/yt-neuter.txt",
    # HaGeZi's The World's Most Abused TLDs
    "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/spam-tlds-ublock.txt",
    # YouTube Clear View
    "https://raw.githubusercontent.com/yokoffing/filterlists/main/youtube_clear_view.txt",
    # Web Annoyances Ultralist by yourduskquibbles
    "https://raw.githubusercontent.com/yourduskquibbles/webannoyances/master/ultralist.txt",
    # Hide YouTube Shorts
    "https://raw.githubusercontent.com/gijsdev/ublock-hide-yt-shorts/refs/heads/master/list.txt",
    # AdGuard Popups filter
    "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_19_Annoyances_Popups/filter.txt",
    # AdGuard Cookie Notices filter
    "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_18_Annoyances_Cookies/filter.txt",
    # AdGuard Mobile App Banners filter
    "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_20_Annoyances_MobileApp/filter.txt",
    # AdGuard Other Annoyances filter
    "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_21_Annoyances_Other/filter.txt",
    # AdGuard Widgets filter
    "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_22_Annoyances_Widgets/filter.txt",
    # Adblock Warning Removal List
    "https://raw.githubusercontent.com/easylist/antiadblockfilters/refs/heads/master/antiadblockfilters/antiadblock_english.txt",
    # Fanboy's Anti-Facebook List
    "https://www.fanboy.co.nz/fanboy-antifacebook.txt"
]

# Combines the URL lists to one list of URLs
#urls = adguardURLs + generalURLs
#urls = urls + testingURLs
URLS = TESTING_URLS

# Sorts the combined list of URLs : 2025-08-31 09:17:43 +1000
URLS = sorted(URLS)

FILTER_LISTS = []

print()
print("Downloading lists..")

# Downloads the text data from the URLs
for URL in URLS:
    print(f"Trying download: {URL}")
    response = requests.get(URL, timeout=10)
    if response.ok:
        FILTER_LISTS.append(response.text)
    else:
        print(f"Failed download: {URL}")

# Combines and cleans up text data
print("Combining and cleaning lists..")
COMBINED = "\n".join(FILTER_LISTS)
LINES = set(LINE.strip() for LINE in COMBINED.splitlines() \
    if LINE.strip() and \
    # Skips lines that are allow rules or comments
    not LINE.startswith("[Adblock Plus") and \
    #not line.startswith("@@") and \
    not LINE.startswith("!") and \
    not LINE.startswith("#") and \
    not LINE.startswith("||") and \
    #not line.startswith("*") and \
    # Remove junk lines (17.10.2025 changes)
    #not line.startswith("$") and \
    #not line.startswith(".") and \
    #not line.startswith("/") and \
    #not line.startswith("~") and \
    not LINE.startswith("%") and \
    not LINE.startswith("-") and \
    not LINE.startswith("&") and \
    not LINE.startswith("мв"))

OUTPUT_FILE = "cosmetic_combined_filterlist.txt"

# Initial write out to the file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(LINES)))

# Force sorts and removes duplicate lines in the text file
# Read, sort, and write back to the same file
with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
    LINES = f.readlines()
# Sorts in ascending (A to Z) order
LINES.sort()
# Keeps only seen lines (removes duplicates)
# Use a set to track seen lines and preserve order
SEEN = set()
UNIQUE_LINES = []
for LINE in LINES:
    if LINE not in SEEN:
        LINE = LINE.replace("0.0.0.0 ","||") # Formats 0.0.0.0 rules to adblock rules
        #line = line + "||"
        #line = line.replace("||||","||")
        SEEN.add(LINE)
        # 3 lines were here.. (|| related)
        UNIQUE_LINES.append(LINE)
# Writes out the text file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.writelines(UNIQUE_LINES)

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
