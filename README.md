# combined-adblock-lists

A combined filter list of the very best cosmetic rules for use in Adblockers like
 **uBlock Origin** and **AdGuard**'s browser extension or app for Windows 11.

[![Python CI - analyse with Pylint, lint with flake8, format with black](https://github.com/hl2guide/combined-adblock-lists/actions/workflows/python_ci.yml/badge.svg)](https://github.com/hl2guide/combined-adblock-lists/actions/workflows/python_ci.yml)
[![Python Run - run a script and then save to GitHub repo](https://github.com/hl2guide/combined-adblock-lists/actions/workflows/python_run_script.yml/badge.svg)](https://github.com/hl2guide/combined-adblock-lists/actions/workflows/python_run_script.yml)

## Important News

### 2026-07-04

**Users of the Blocklist please be sure to update the links to the new ~50MB sized links.**

## Details

- Python code runs on GitHub directly using GitHub Actions
    - Updates about every 5 hours, each day (depending on GitHub Actions uptime)
- Comments and duplicate lines are ignored and the lists are sorted

### Cosmetic Combined Filterlist

Cosmetic rules to hide elements within page content.

_Recommended for use in the AdGuard app or in AdGuard or uBlock Origin browser extensions._

- Includes specific filter lists from _AdBlockPlus_, _AdGuard_, _Brave_, _EasyList_, _EasyPrivacy_, _Fanboy_ and _uBlock_
    - (can be viewed in the `create_cosmetic_list_v2.py` file.)
    - includes extra international rules
- All domain blocking rules are excluded from the list
    - _Does not work in AdGuard Home or similar domain-based software_
- The list is approximately 13MB in size

#### Direct raw text link

```
https://raw.githubusercontent.com/hl2guide/combined-adblock-lists/refs/heads/main/cosmetic_combined_filterlist.txt
```

### Blocklist Combined Filterlist

Blocks bad domains including known bad sites, scams, malware, ads etc.

_Recommended for use in AdGuard Home or similar domain-based software._

- Includes specific filter lists from _The Block List Project_
    - (can be viewed in the `create_blocklist_list_v1.py` file.)
- Only domain blocking rules are included in the list
    - Consider performance reasons to not use it in browser-based extensions
- The lists are approximately 205 MB in size

#### Direct raw text links

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

## Recent News

[HISTORY.md](HISTORY.md)

## Credits

[CREDITS.md](CREDITS.md)
