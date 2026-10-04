"""Check domains from a text file and remove invalid ones."""

import socket
from concurrent.futures import ThreadPoolExecutor
import glob

def domain_exists(domain: str) -> bool:
    """Check if a domain resolves to an IP address."""
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

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
