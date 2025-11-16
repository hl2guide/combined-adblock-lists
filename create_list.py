
"""
Creates a text file every hour using GitHub actions.
This module is being developed.
"""

# Downloads and then combines cosmetic filter lists into one text file.
# It also REMOVES allow rules, comment lines and duplicate lines.

# Version 1.0.2
# Edited: 2025-11-16 21:36:37 +1100

# Generated using AI
# Tested on local PC

# IMPORTS
from datetime import datetime
from zoneinfo import ZoneInfo
import requests

URL_PREFIX_GH = \
    "https://raw.githubusercontent.com"
URL_PREFIX_EASYLIST = \
    "https://cdn.statically.io/gh/uBlockOrigin/uAssetsCDN/main/thirdparties"
URL_PREFIX_EASYLIST2 = \
    "https://cdn.jsdelivr.net/gh/uBlockOrigin/uAssetsCDN@main/thirdparties"
URL_PART_ADG = \
    "AdguardTeam/FiltersRegistry/master/filters"
URL_PART_EL = \
    "easylist/antiadblockfilters/refs/heads/master/antiadblockfilters"
URL_PART_BR = \
    "brave/adblock-lists/refs/heads/master/brave-lists"
URL_PART_UB = \
    "uBlockOrigin/uAssets/refs/heads/master/filters"
URL_PART_YTS = \
    "gijsdev/ublock-hide-yt-shorts/refs/heads/master"
URL_PART_1 = \
    "filter_20_Annoyances_MobileApp"
URL_PART_2 = \
    "filter_21_Annoyances_Other"
URL_PREFIX_1 = \
    "https://cdn.statically.io/gh/uBlockOrigin/uAssetsCDN/main"

# Testing list URLs
TESTING_URLS = [
    # Brave Filterlists: (https://github.com/brave/adblock-lists/tree/master/brave-lists)
    # Brave - YouTube Shorts
    f"{URL_PREFIX_GH}/{URL_PART_BR}/yt-shorts.txt",
    # Brave - YouTube Recommendations
    f"{URL_PREFIX_GH}/{URL_PART_BR}/yt-recommended.txt",
    # Brave - YouTube Distractions
    f"{URL_PREFIX_GH}/{URL_PART_BR}/yt-distracting.txt",
    # Brave - Social Elements Blocker
    f"{URL_PREFIX_GH}/{URL_PART_BR}/brave-social.txt",
    # Brave-specific additions to Easylist Cookie
    f"{URL_PREFIX_GH}/{URL_PART_BR}/brave-cookie-specific.txt",
    # uBlock Filterlists
    # uBlock - Cookie Notices
    f"{URL_PREFIX_GH}/{URL_PART_UB}/annoyances-cookies.txt",
    # uBlock - Other Annoyances
    f"{URL_PREFIX_GH}/{URL_PART_UB}/annoyances-others.txt",
    # uBlock - Badware Risks
    f"{URL_PREFIX_GH}/{URL_PART_UB}/badware.txt",
    # uBlock filters (years)
    f"{URL_PREFIX_GH}/{URL_PART_UB}/filters-2020.txt",
    f"{URL_PREFIX_GH}/{URL_PART_UB}/filters-2021.txt",
    f"{URL_PREFIX_GH}/{URL_PART_UB}/filters-2022.txt",
    f"{URL_PREFIX_GH}/{URL_PART_UB}/filters-2023.txt",
    f"{URL_PREFIX_GH}/{URL_PART_UB}/filters-2024.txt",
    f"{URL_PREFIX_GH}/{URL_PART_UB}/filters-2025.txt",
    # uBlock - Privacy
    f"{URL_PREFIX_GH}/{URL_PART_UB}/privacy.txt",
    # uBlock - Filters
    f"{URL_PREFIX_GH}/{URL_PART_UB}/filters.txt",
    # uBlock - Unbreak
    f"{URL_PREFIX_GH}/{URL_PART_UB}/unbreak.txt",
    # uBlock filters - Annoyances
    f"{URL_PREFIX_1}/filters/annoyances.min.txt",
    # YouTube Neuter - sponsorblock
    f"{URL_PREFIX_GH}/mchangrh/yt-neuter/main/filters/sponsorblock.txt",
    # YouTube Neuter
    f"{URL_PREFIX_GH}/mchangrh/yt-neuter/main/yt-neuter.txt",
    # YouTube Clear View
    f"{URL_PREFIX_GH}/yokoffing/filterlists/main/youtube_clear_view.txt",
    # Hide YouTube Shorts
    f"{URL_PREFIX_GH}/{URL_PART_YTS}/list.txt",
    # HaGeZi's The World's Most Abused TLDs
    f"{URL_PREFIX_GH}/hagezi/dns-blocklists/main/adblock/spam-tlds-ublock.txt",
    # Web Annoyances Ultralist by yourduskquibbles
    f"{URL_PREFIX_GH}/yourduskquibbles/webannoyances/master/ultralist.txt",
    # AdGuard Popups filter
    f"{URL_PREFIX_GH}/{URL_PART_ADG}/filter_19_Annoyances_Popups/filter.txt",
    # AdGuard Cookie Notices filter
    f"{URL_PREFIX_GH}/{URL_PART_ADG}/filter_18_Annoyances_Cookies/filter.txt",
    # AdGuard Mobile App Banners filter
    f"{URL_PREFIX_GH}/{URL_PART_ADG}/{URL_PART_1}/filter.txt",
    # AdGuard Other Annoyances filter
    f"{URL_PREFIX_GH}/{URL_PART_ADG}/{URL_PART_2}/filter.txt",
    # AdGuard Widgets filter
    f"{URL_PREFIX_GH}/{URL_PART_ADG}/filter_22_Annoyances_Widgets/filter.txt",
    # Adblock Warning Removal List
    f"{URL_PREFIX_GH}/{URL_PART_EL}/antiadblock_english.txt",
    # EasyList
    f"{URL_PREFIX_1}/thirdparties/easylist.txt",
    # AdGuard - Base filter
    "https://filters.adtidy.org/extension/ublock/filters/" +
    "2_without_easylist.txt",
    # AdGuard - Mobile Ads filter
    "https://filters.adtidy.org/extension/ublock/filters/11.txt",
    # AdGuard Social Media filter
    "https://filters.adtidy.org/extension/ublock/filters/4.txt",
    # Anti-Facebook List
    "https://secure.fanboy.co.nz/fanboy-antifacebook.txt",
    # EasyPrivacy
    "https://ublockorigin.pages.dev/thirdparties/easyprivacy.txt",
    # EasyList - Cookie Notices
    f"{URL_PREFIX_EASYLIST}/easylist-cookies.txt",
    # EasyList - Social Widgets
    "https://cdn.jsdelivr.net/gh/uBlockOrigin/uAssetsCDN@main/" +
    "thirdparties/easylist-social.txt",
    # EasyList - Chat Widgets
    "https://cdn.jsdelivr.net/gh/uBlockOrigin/uAssetsCDN@main/" +
    "thirdparties/easylist-chat.txt",
    # EasyList - Newsletter Notices
    "https://ublockorigin.pages.dev/thirdparties/" +
    "easylist-newsletters.txt",
    # EasyList - Notifications
    f"{URL_PREFIX_EASYLIST2}/easylist-notifications.txt",
    # EasyList - Annoyances
    f"{URL_PREFIX_EASYLIST}/easylist-annoyances.txt",
    # Fanboy's Anti-Facebook List
    "https://www.fanboy.co.nz/fanboy-antifacebook.txt"
]

# Combines the URL lists to one list of URLs
URLS = TESTING_URLS

# Sorts the combined list of URLs : 2025-11-16 21:34:58 +1100
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
LINES = set(LINE.strip() for LINE in COMBINED.splitlines()
            if (
                LINE.strip() and
                # Skips lines that are allow rules or comments
                not LINE.startswith("!") and
                not LINE.startswith("#") and
                not LINE.startswith("%") and
                not LINE.startswith("&") and
                not LINE.startswith("-") and
                not LINE.startswith("[Adblock Plus") and
                not LINE.startswith("||") and
                not LINE.startswith("мв")
            )
)

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
        # Formats 0.0.0.0 rules to adblock rules
        LINE = LINE.replace("0.0.0.0 ", "||")
        # line = line + "||"
        # line = line.replace("||||","||")
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
