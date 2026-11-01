#!/usr/bin/env python3
"""
Check a large list of domains concurrently and write only the "successful"
ones to a plain-text file (one domain per line).

Progress messages are printed every 10,000 domains completed.

Examples:
    python check_domains.py domains.txt -o live_domains.txt --concurrency 10000000
    python check_domains.py domains.txt -o live_domains.txt
    python check_domains.py domains.txt -o live.txt -c 80 -t 3
    python check_domains.py domains.txt -o live.txt --require-registered

Requirements:
    pip install python-whois     # only needed for --require-registered
"""

from __future__ import annotations

import argparse
import asyncio
import socket
import sys
from pathlib import Path

try:
    import whois as whois_lib  # python-whois
    from whois.parser import PywhoisError
except ImportError:
    whois_lib = None


# --------------------------------------------------------------------------- #
# Input handling
# --------------------------------------------------------------------------- #

def load_domains(path: str) -> list[str]:
    """Read one domain per line, normalise, drop blanks/comments, de-duplicate."""
    seen: set[str] = set()
    domains: list[str] = []

    text = Path(path).read_text(encoding="utf-8", errors="replace")
    for raw in text.splitlines():
        d = raw.strip().lower()
        if not d or d.startswith("#"):
            continue

        # Crude cleanup so URLs pasted into the list still work.
        for prefix in ("http://", "https://"):
            if d.startswith(prefix):
                d = d[len(prefix):]
        d = d.split("/")[0].split("?")[0].split(":")[0].rstrip(".")
        if not d or "." not in d:
            continue

        if d not in seen:
            seen.add(d)
            domains.append(d)

    return domains


# --------------------------------------------------------------------------- #
# Checks
# --------------------------------------------------------------------------- #

async def has_dns(domain: str, timeout: float) -> bool:
    """True if the domain resolves to at least one address."""
    loop = asyncio.get_running_loop()
    try:
        await asyncio.wait_for(
            loop.getaddrinfo(domain, None, proto=socket.IPPROTO_TCP),
            timeout=timeout,
        )
        return True
    except (socket.gaierror, asyncio.TimeoutError, UnicodeError, OSError):
        return False


def _whois_blocking(domain: str) -> bool | None:
    """
    Blocking WHOIS lookup, run in a thread.

    Returns:
        True  -> a registration record was found
        False -> the registry answered and there is no such registration
        None  -> the lookup itself failed (timeout, rate limit, bad TLD, ...)
    """
    try:
        record = whois_lib.whois(domain)
    except PywhoisError:
        # python-whois raises for "no match" responses as well as for real
        # errors, so we cannot distinguish "available" from "failed" here.
        return None

    if record is None:
        return None

    names = record.get("domain_name")
    if isinstance(names, (list, tuple)):
        names = names[0] if names else None

    if names or record.get("registrar"):
        return True
    return False

async def check_one(
    domain: str,
    sem: asyncio.Semaphore,
    timeout: float,
    require_registered: bool,
) -> tuple[str, bool]:
    """
    Checks one.
    """
    async with sem:
        dns_ok = await has_dns(domain, timeout)
        if not dns_ok:
            return domain, False

        if require_registered:
            loop = asyncio.get_running_loop()
            registered = await loop.run_in_executor(None, _whois_blocking, domain)
            # None means "couldn't tell" -- treat as passing rather than
            # silently dropping a domain because a WHOIS server was busy.
            if registered is False:
                return domain, False

        return domain, True


# --------------------------------------------------------------------------- #
# Driver
# --------------------------------------------------------------------------- #

async def run(args: argparse.Namespace) -> int:
    """
    Async.
    """
    if args.require_registered and whois_lib is None:
        print(
            "error: --require-registered needs python-whois (pip install python-whois)",
            file=sys.stderr,
        )
        return 2

    domains = load_domains(args.input)
    if not domains:
        print("error: no usable domains found in input file", file=sys.stderr)
        return 1

    total = len(domains)
    print(
        f"checking {total} unique domains "
        f"(concurrency={args.concurrency}, timeout={args.timeout}s, "
        f"require_registered={args.require_registered})",
        file=sys.stderr,
    )

    sem = asyncio.Semaphore(args.concurrency)
    done = 0
    successes: list[str] = []

    async def worker(domain: str) -> tuple[str, bool]:
        nonlocal done
        result = await check_one(domain, sem, args.timeout, args.require_registered)
        done += 1

        # Progress message every 10,000 domains
        if done % 10000 == 0:
            remaining = total - done
            print(f"  {done}/{total} checked, {remaining} remaining", file=sys.stderr)

        return result

    tasks = [asyncio.create_task(worker(d)) for d in domains]
    for finished in asyncio.as_completed(tasks):
        domain, ok = await finished
        if ok:
            successes.append(domain)

    # Final progress message if we haven't printed one yet
    if total > 0 and done % 10000 != 0:
        print(f"  {done}/{total} checked, 0 remaining", file=sys.stderr)

    successes.sort()

    out_path = Path(args.output)
    out_path.write_text(
        "".join(f"{d}\n" for d in successes),
        encoding="utf-8",
    )

    print(
        f"\n{len(successes)}/{total} domains passed -> {out_path}",
        file=sys.stderr,
    )
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check domains concurrently; write successful ones to a text file.",
    )
    parser.add_argument("input", help="file containing one domain per line")
    parser.add_argument(
        "-o", "--output", default="successful_domains.txt",
        help="output text file (default: %(default)s)",
    )
    parser.add_argument(
        "-c", "--concurrency", type=int, default=50,
        help="max simultaneous lookups (default: %(default)s)",
    )
    parser.add_argument(
        "-t", "--timeout", type=float, default=5.0,
        help="per-lookup timeout in seconds (default: %(default)s)",
    )
    parser.add_argument(
        "--require-registered", action="store_true",
        help="also require a WHOIS record (much slower; registries rate-limit)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="print additional debug info",
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(run(parse_args())))
    except KeyboardInterrupt:
        sys.exit(130)
