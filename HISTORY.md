# 2026-06-22
- Improved the github actions to retry simple failed steps

# 2026-05-28
- Added new list to blocklist
- Split blocklist to 80MB text files

# 2026-05-17

- Added more bad hosts to the blocklist
- Added government tracker blockers to the blocklist
- Added ShadowWhisperer blocklists

# 2026-05-05

- Fixed YouTube issues (monitoring)

# 2026-04-21

- Added some new lists
- Fixed a Byte Order Mark (BOM) problem caused by a few messier URLs

# 2026-02-27

- Added version string
- Testing increased number of workers in Python file

# 2026-02-25

- Added more languages : Dutch, Russian, Polish, Arabic etc.

# 2026-02-09

- Fixed unreliable URLs and found alternative
- Added major languages support : German, French, Korean etc

# Tested

Item | Improvement
---------|---------
`create_list_v2.py` execution time | from 25 seconds to about 2.5 seconds
total build and run time | from 30 seconds to about 19 seconds
frequency of generation (hours) | 3 changed to 6
GitHub Action | uses job caching to speed up runs
