
"""
Creates a combined text file of blocklist filters every 5 hours using GitHub actions.
"""

# Downloads in parallel and then combines cosmetic filter lists into one text file.
# It also REMOVES allow rules, comment lines and duplicate lines.

# Version 1.0.1
# Edited: 2026-03-05 15:30:55 +1100

# Generated using AI (duck.ai)
# Tested on local PC and on GitHub

# IMPORTS
from datetime import datetime
from zoneinfo import ZoneInfo
import queue
import threading
import time
import urllib.request
import sys

start = time.perf_counter()

def datetime_sydney() -> str:
    """
    Returns the current datetime in Sydney, Australia as a string.

    Returns:
        string: The current datetime in Sydney, Australia.
    """
    now = datetime.now(ZoneInfo("Australia/Sydney"))
    return now.strftime("%Y.%m.%d.%H%M%z AEST")  # e.g., 2025.11.22.1435+1100

def download_worker(url_q: queue.Queue, result_q: queue.Queue):
    """
    Pull a URL from `url_q`, fetch its text, and push the result onto `result_q`.
    Any exception is caught and reported, then the thread moves on to the next URL.
    """
    while True:
        try:
            url = url_q.get_nowait()
        except queue.Empty:
            break  # nothing left for this thread

        try:
            # Fetch the raw bytes; we’ll decode as UTF‑8 (fallback to latin‑1)
            with urllib.request.urlopen(url, timeout=20) as resp:
                raw = resp.read()
                try:
                    txt = raw.decode("utf-8")
                except UnicodeDecodeError:
                    txt = raw.decode("latin-1")   # best‑effort fallback

            # Push the successful result (url, text) onto the result queue
            result_q.put((url, txt))
            print(f"\n[{threading.current_thread().name}] ✓ {url}")

        except (TimeoutError, ConnectionRefusedError, ConnectionResetError, BrokenPipeError, OSError) as exc:
            # Record the failure so the main thread can see it
            result_q.put((url, f"<error: {exc}>"))
            print(f"[{threading.current_thread().name}] ✗ {url} - {exc}")

        finally:
            url_q.task_done()

def main():
    """
    The main function.
    """

    # Queues: one for work, one for results
    work_q = queue.Queue()
    result_q = queue.Queue()

    for u in TESTING_URLS:
        work_q.put(u)

    # Start the worker threads
    threads = []
    for i in range(NUM_WORKERS):
        t = threading.Thread(
            target=download_worker,
            args=(work_q, result_q),
            name=f"Worker-{i+1}"
        )
        t.start()
        threads.append(t)

    # Wait until all URLs have been processed
    work_q.join()

    # All workers are now idle; optionally join them cleanly
    for t in threads:
        t.join()

    # -----------------------------------------------------------------
    # Assemble the final string that holds every successful download.
    # You could also keep a dict if you need per‑URL access.
    # -----------------------------------------------------------------
    all_text1 = ""
    errors = []

    while not result_q.empty():
        url, payload = result_q.get()
        if payload.startswith("<error"):
            errors.append((url, payload))
        else:
            # Separate each file with a clear delimiter (optional)
            all_text1 += f"\n--- Begin {url} ---\n{payload}\n--- End {url} ---\n"

    # -----------------------------------------------------------------
    # Output / further processing
    # -----------------------------------------------------------------
    #print("\n=== Combined Text ===")
    #print(ALL_TEXT[:500])          # preview first 500 chars
    #print("…")                     # indicate there may be more

    if errors:
        print("\nThe following URLs failed:")
        for u, msg in errors:
            print(f" • {u}: {msg}")
            # Report the error to console (CLI)
            sys.exit(1)

    # `ALL_TEXT` now contains the concatenated contents of every successful download
    # You can return it, write it to a file, feed it to another function, etc.
    return all_text1

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
    # https://github.com/blocklistproject/Lists
    "https://blocklistproject.github.io/Lists/adguard/abuse-ags.txt",
    "https://blocklistproject.github.io/Lists/adguard/ads-ags.txt",
    "https://blocklistproject.github.io/Lists/adguard/crypto-ags.txt",
    "https://blocklistproject.github.io/Lists/adguard/drugs-ags.txt",
    "https://blocklistproject.github.io/Lists/adguard/facebook-ags.txt",
    "https://blocklistproject.github.io/Lists/adguard/fraud-ags.txt",
    "https://blocklistproject.github.io/Lists/adguard/gambling-ags.txt",
    "https://blocklistproject.github.io/Lists/adguard/malware-ags.txt",
    "https://blocklistproject.github.io/Lists/adguard/phishing-ags.txt",
    "https://blocklistproject.github.io/Lists/adguard/ransomware-ags.txt",
    "https://blocklistproject.github.io/Lists/adguard/scam-ags.txt",
    "https://blocklistproject.github.io/Lists/adguard/tiktok-ags.txt",
    "https://blocklistproject.github.io/Lists/adguard/tracking-ags.txt",
    "https://blocklistproject.github.io/Lists/adguard/twitter-ags.txt",
    "https://blocklistproject.github.io/Lists/adguard/vaping-ags.txt"
]

print()
print('Starting Filter List downloads..')

# How many threads should run in parallel?
# NUM_WORKERS = 24
# TESTING MORE WORKERS
NUM_WORKERS = 32

# Combines the URL lists to one list of URLs
URLS = TESTING_URLS

# Sorts the combined list of URLs : 2026-03-05 15:46:19 +1100
URLS = sorted(URLS)

FILTER_LISTS = []

all_text = ''

if __name__ == "__main__":
    all_text = main()

# print(len(ALL_TEXT.splitlines()))

COMBINED = all_text

# Combines and cleans up text data
print()
print("Combining and cleaning lists..")
# COMBINED = "\n".join(FILTER_LISTS)
LINES = set(LINE.strip() for LINE in COMBINED.splitlines()
            if (
                LINE.strip() and
                # Skips lines that are allow rules or comments
                not LINE.startswith("!") and
                not LINE.startswith("! Search Results") and
                not LINE.startswith("#") and
                not LINE.startswith("%") and
                not LINE.startswith("&") and
                not LINE.startswith("-") and
                not LINE.startswith("@@") and
                not LINE.startswith("[Adblock Plus") and
                not LINE.startswith("[uBlock") and
                not LINE.startswith("мв")
            )
)

OUTPUT_FILE = "blocklist_combined_filterlist.txt"

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

LAST_MODIFIED = datetime_sydney()

with open('VERSION.txt', 'r', encoding="utf-8") as f:
    VERSION = f.read().strip()

COMMENT_BLOCK = f"""[Adblock Plus 2.0]
! Title: Blocklist Combined Filterlist
! Version: {VERSION}
! Last Modified: {LAST_MODIFIED}
! Expires: 4 hours (update frequency)
! Homepage: https://github.com/hl2guide/combined-adblock-lists
! License: https://github.com/hl2guide/combined-adblock-lists?tab=MIT-1-ov-file#readme
!

!--------------------------Cosmetic filtering rules-----------------------------!
"""

# Adds the comment block to start of the text file
UNIQUE_LINES.insert(0, COMMENT_BLOCK)

# Writes out the text file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.writelines(UNIQUE_LINES)

elapsed = time.perf_counter() - start
print()
print(f"Elapsed: {elapsed:.6f} seconds")
print()
print(f"Version String: {VERSION}")
print()
print(f'Saved to: {OUTPUT_FILE}')
print()
print('Python script completed.')
print()