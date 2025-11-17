# combined-adblock-lists

A combined filter list of the very best cosmetic rules for use in Adblockers like **uBlock Origin** and **AdGuard**.

- Python code runs on GitHub directly using GitHub Actions
- Updates every 4 hours, every day
- Includes specific filters lists from _Brave_, _uBlock_, _AdGuard_, _EasyList_, _EasyPrivacy_ and _YouTube Cleanup_
    - (can be viewed in the `create_list.py` file.)
- All domain blocking rules are excluded from the list
- Duplicate lines are ignored and the list is sorted
- The list is approximately 10MB in size

## Direct raw text link

```
https://raw.githubusercontent.com/hl2guide/combined-adblock-lists/refs/heads/main/cosmetic_combined_filterlist.txt
```

[![Python CI - analyse with Pylint, lint with flake8, format with black](https://github.com/hl2guide/combined-adblock-lists/actions/workflows/python_ci.yml/badge.svg)](https://github.com/hl2guide/combined-adblock-lists/actions/workflows/python_ci.yml)

[![Python Run - run a script and then save to GitHub repo](https://github.com/hl2guide/combined-adblock-lists/actions/workflows/python_run_script.yml/badge.svg)](https://github.com/hl2guide/combined-adblock-lists/actions/workflows/python_run_script.yml)
