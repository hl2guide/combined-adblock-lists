"""Check domains from a text file and remove invalid ones."""

import re
import socket
from concurrent.futures import ThreadPoolExecutor
import glob

def domain_exists(domain: str) -> bool:
    """Check if a domain resolves to an IP address."""

    if is_valid_format(domain):
        try:
            socket.gethostbyname(domain)
            return True
        except (socket.gaierror, UnicodeError):
            return False        
    else:
        return False

def is_valid_format(domain: str) -> bool:
    """Check domain syntax (length, chars, structure)."""
    if len(domain) > 253:
        return False
    return bool(DOMAIN_RE.match(domain))

DOMAIN_RE = re.compile(
    r"^(?!-)[a-zA-Z0-9-]{1,63}(?<!-)"   # first label
    r"(\.(?!-)[a-zA-Z0-9-]{1,63}(?<!-))*" # additional labels
    r"\.[a-zA-Z]{2,63}$"                # TLD
)

BLOCKLIST_FILES = glob.glob("blocklist_combined_filterlist.txt_*.txt")   

for b in BLOCKLIST_FILES:
    with open(b, "r", encoding="utf-8") as f:
        domains = [line.strip() for line in f if line.strip()]
    with ThreadPoolExecutor(max_workers=50) as pool:
        valid = [d for d, ok in zip(domains, pool.map(domain_exists, domains)) if ok]
    with open(b, "w", encoding="utf-8") as f:
        f.write("\n".join(valid) + "\n")
    print(f"Cleaned blocklist file: {b}")
    print()
print('Python script completed.')
print()
