#!/usr/bin/env python3
"""Validate an allowlist before publishing it. Syntax checks do not prove site ownership or safety."""
import ipaddress
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = ROOT / 'allowlist.txt'
DOMAIN = re.compile(r'(?=.{1,253}\Z)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z](?:[a-z0-9-]{0,61}[a-z0-9])?\Z')
MAX_BYTES = 512 * 1024


def main():
    contents = PATH.read_bytes()
    if len(contents) > MAX_BYTES:
        sys.exit('FAIL: allowlist.txt is larger than 512 KiB')
    try:
        lines = contents.decode('utf-8', errors='strict').splitlines()
    except UnicodeError as exc:
        sys.exit(f'FAIL: invalid UTF-8: {exc}')

    seen = set()
    for number, original in enumerate(lines, 1):
        domain = original.strip()
        if not domain or domain.startswith('#'):
            continue
        if domain != original or not DOMAIN.fullmatch(domain):
            sys.exit(f'FAIL: line {number}: invalid domain {original!r}; use ASCII lowercase hostnames, no scheme/wildcards/paths')
        try:
            ipaddress.ip_address(domain)
        except ValueError:
            pass
        else:
            sys.exit(f'FAIL: line {number}: IP address not allowed')
        if domain in seen:
            sys.exit(f'FAIL: line {number}: duplicate {domain}')
        seen.add(domain)

    if len(seen) < 10:
        sys.exit(f'FAIL: too few domains ({len(seen)}). Refusing dangerous empty/near-empty allowlist')
    if len(seen) > 10000:
        sys.exit('FAIL: more than 10000 domains')
    print(f'PASS: {len(seen)} unique, syntactically valid domains. Ownership NOT verified.')


if __name__ == '__main__':
    main()
