# combined-adblock-lists

A combined filter list of the very best cosmetic rules for use in Adblockers like **uBlock Origin** and **AdGuard**'s browser extension or app for Windows 11.

## Direct raw text link

```
https://raw.githubusercontent.com/hl2guide/combined-adblock-lists/refs/heads/main/cosmetic_combined_filterlist.txt
```

[![Python CI - analyse with Pylint, lint with flake8, format with black](https://github.com/hl2guide/combined-adblock-lists/actions/workflows/python_ci.yml/badge.svg)](https://github.com/hl2guide/combined-adblock-lists/actions/workflows/python_ci.yml)
[![Python Run - run a script and then save to GitHub repo](https://github.com/hl2guide/combined-adblock-lists/actions/workflows/python_run_script.yml/badge.svg)](https://github.com/hl2guide/combined-adblock-lists/actions/workflows/python_run_script.yml)

## Details

- Includes specific filters lists from _AdBlockPlus_, _AdGuard_, _Brave_, _EasyList_, _EasyPrivacy_, _Fanboy_, _uBlock_ and _YouTube Cleanup_
    - (can be viewed in the `create_list_v2.py` file.)
- All domain blocking rules are excluded from the list
    - _Does not work in AdGuard Home or similar domain-based software_
- Comments and duplicate lines are ignored and the list is sorted
- The list is approximately 10MB in size
- Python code runs on GitHub directly using GitHub Actions
    - Updates every 3 hours, every day

## Testing v2

I'm currently testing **v2** that uses threading and many workers to speed up the Python script.

Item | Improvement
---------|---------
 `create_list_v2.py` execution time | from 25 seconds to 3 seconds
 total build and run time | from 30 seconds to about 13 seconds
 frequency of generation (hours) | 4 changed to 3