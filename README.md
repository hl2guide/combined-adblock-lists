# combined-adblock-lists

A combined filter list of the very best cosmetic rules for use in Adblockers like
 **uBlock Origin** and **AdGuard**'s browser extension or paid-app for Linux, Windows 11, Android, MacOS or iOS.

_Major Version:_ 1.14

_GUID:_ {850b6f81-011f-4b00-8d75-28739807d89c}

[![Python CI - analyse with Pylint, lint with flake8, format with black](https://github.com/hl2guide/combined-adblock-lists/actions/workflows/python_ci.yml/badge.svg)](https://github.com/hl2guide/combined-adblock-lists/actions/workflows/python_ci.yml)
[![Python Run - run a script and then save to GitHub repo](https://github.com/hl2guide/combined-adblock-lists/actions/workflows/python_run_script.yml/badge.svg)](https://github.com/hl2guide/combined-adblock-lists/actions/workflows/python_run_script.yml)

## Important News

### 2026-10-04

⭐ After careful consideration I've decided to sunset the cosmetic list after plenty of testing.

- The list was way too large and caused side effects
- The blocklist and allowlist will remain

### 2026-07-04

**Users of the Blocklist please be sure to update the links to the new ~50MB sized links.**

## Details

- Python code runs on GitHub directly using GitHub Actions
    - Updates about every 3 hours, each day (depending on GitHub Actions uptime)
- Comments and duplicate lines are ignored and the lists are sorted

## Blocklist Combined Filterlist ⛔

Blocks bad domains including known bad sites, scams, malware, ads etc.

_Recommended for use in AdGuard Home or similar domain-based software._

- Includes specific filter lists from _The Block List Project_
    - (can be viewed in the `create_blocklist_list_v1.py` file.)
- Only domain blocking rules are included in the list
    - Consider performance reasons to not use it in browser-based extensions
- The lists are approximately 235 MB in size

### Direct raw text links

```
https://github.com/hl2guide/combined-adblock-lists/raw/refs/heads/main/blocklist_combined_filterlist.txt_000.txt
```

```
https://github.com/hl2guide/combined-adblock-lists/raw/refs/heads/main/blocklist_combined_filterlist.txt_001.txt
```

```
https://github.com/hl2guide/combined-adblock-lists/raw/refs/heads/main/blocklist_combined_filterlist.txt_002.txt
```

```
https://github.com/hl2guide/combined-adblock-lists/raw/refs/heads/main/blocklist_combined_filterlist.txt_003.txt
```

```
https://github.com/hl2guide/combined-adblock-lists/raw/refs/heads/main/blocklist_combined_filterlist.txt_004.txt
```

## Allowlist ✅

Allows worthwhile websites.

Sourced from my other repo [curated-adblock-lists](https://github.com/hl2guide/curated-adblock-lists).

### Direct raw text link

```
https://raw.githubusercontent.com/hl2guide/curated-adblock-lists/refs/heads/main/lists/allowed.txt
```

## Recent News 📰

[HISTORY.md](HISTORY.md)

## Credits 📖

[CREDITS.md](CREDITS.md)
