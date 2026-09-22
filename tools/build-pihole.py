#!/usr/bin/env python3
"""Build Pi-hole outputs from blocklist.txt / blocklist-strict.txt.

Pi-hole gravity understands plain domains and the ABP wildcard rule
``||domain^`` (block the domain and its subdomains) — nothing else. The
AdGuard-only constructs used by the source lists (@@ exceptions, $important,
regex rules) are ignored by Pi-hole, so the AdGuard lists can NOT be consumed
by Pi-hole as-is. This script generates dedicated outputs:

    pihole/block.txt         default tier blocks   (from blocklist.txt)
    pihole/block-strict.txt  strict tier blocks    (from blocklist-strict.txt)
    pihole/allow.txt         KEEP-WORKING exceptions as exact allowlist
                             entries (subscribe it as an allowlist, v6+)

GENERATED — never hand-edit. Run from anywhere:

    python3 tools/build-pihole.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "blocklist.txt"
SRC_STRICT = ROOT / "blocklist-strict.txt"
OUTDIR = ROOT / "pihole"

KEEP_MARK = "! ============= KEEP-WORKING EXCEPTIONS"
OPTIONAL_MARK = "! ================= OPTIONAL / HIGHER-TRADEOFF"
SONY_MARK = "! ================= SONY"

BLOCK_HEADER = """\
# ---------------------------------------------------------------------------
# TV DNS Blocklist — Pi-hole blocklist ({tier} tier) — GENERATED FILE
# Version: {version}
# Source: {source}
# Homepage: https://github.com/Okazakee/tv-dns-blocklist · License: MIT
#
# GENERATED — do not edit. Edit {source}, then run: python3 tools/build-pihole.py
#
# Pi-hole variant of the {source} list. Pi-hole gravity supports plain domains
# and the wildcard rule ||domain^ only, so the AdGuard-only parts are handled
# like this:
#   · @@ ... $important exceptions -> pihole/allow.txt (add it as a subscribed
#     allowlist — Pi-hole v6+)
#   · regex rules are omitted (commented where they occur; they need Pi-hole's
#     own regex denylist, which cannot be shipped inside a subscribed list)
# Everything below is the source list minus those parts.
# ---------------------------------------------------------------------------
"""

ALLOW_HEADER = """\
# ---------------------------------------------------------------------------
# TV DNS Blocklist — Pi-hole KEEP-WORKING allowlist — GENERATED FILE
# Version: {version}
# Source: blocklist.txt (KEEP-WORKING exceptions)
# Homepage: https://github.com/Okazakee/tv-dns-blocklist · License: MIT
#
# GENERATED — do not edit. Run: python3 tools/build-pihole.py
#
# Add this file as a *subscribed allowlist* (Pi-hole v6+; Settings → Lists).
# Its entries are exact domains and take precedence over subscribed
# blocklists, protecting updates/OTA, app stores, DRM/playback, boot
# connectivity, accounts, time sync, second screen and voice hosts.
# ---------------------------------------------------------------------------
"""


def version_of(text: str) -> str:
    m = re.search(r"^! Version: (.+)$", text, re.M)
    return m.group(1).strip() if m else "unversioned"


def classify(text: str) -> tuple[list[str], list[str], list[str]]:
    """Return (blocks, regexes, exceptions) as raw active rule lines."""
    blocks, regexes, exceptions = [], [], []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("!"):
            continue
        if s.startswith("@@"):
            exceptions.append(s)
        elif s.startswith("/") and s.endswith("/"):
            regexes.append(s)
        else:
            blocks.append(s)
    return blocks, regexes, exceptions


def exception_domain(rule: str) -> str:
    d = rule[2:]  # strip @@
    if d.startswith("||"):
        d = d[2:]
    elif d.startswith("|"):
        d = d[1:]
    if d.endswith("$important"):
        d = d[: -len("$important")]
    if d.endswith("^"):
        d = d[:-1]
    return d


def transform_body(body: str, version: str, exc_count: int) -> str:
    lines = []
    for line in body.splitlines():
        s = line.strip()
        if not s:
            lines.append("")
        elif s.startswith("@@"):
            continue  # moved to pihole/allow.txt
        elif s.startswith("/") and s.endswith("/"):
            lines.append(f"# [pi-hole] AdGuard-only regex rule omitted: {s}")
        elif s.startswith("!"):
            if s.startswith(KEEP_MARK):
                lines.append(
                    f"# ===== KEEP-WORKING EXCEPTIONS ({exc_count}) → moved to "
                    f"pihole/allow.txt; add it as a subscribed allowlist ====="
                )
            else:
                lines.append("#" + s[1:])
        else:
            lines.append(s)
    return "\n".join(lines)


def main() -> None:
    src_text = SRC.read_text()
    strict_text = SRC_STRICT.read_text()
    version = version_of(src_text)

    d_blocks, d_regex, d_exc = classify(src_text)
    s_blocks, s_regex, s_exc = classify(strict_text)

    d_exc_domains = [exception_domain(e) for e in d_exc]
    s_exc_domains = set(exception_domain(e) for e in s_exc)
    if s_exc_domains != set(d_exc_domains):
        raise SystemExit(
            "blocklist-strict.txt and blocklist.txt disagree on exceptions — "
            "run python3 tools/build-strict.py first"
        )

    OUTDIR.mkdir(exist_ok=True)

    # ---- block.txt (default tier) -----------------------------------------
    body = src_text[src_text.index(SONY_MARK):]
    out = BLOCK_HEADER.format(tier="default", version=version, source="blocklist.txt")
    out += transform_body(body, version, len(d_exc)) + "\n"
    (OUTDIR / "block.txt").write_text(out)
    print(
        f"wrote pihole/block.txt: {len(d_blocks)} blocks, "
        f"{len(d_regex)} regex omitted, {len(d_exc)} exceptions -> allow.txt"
    )

    # ---- block-strict.txt --------------------------------------------------
    body = strict_text[strict_text.index(SONY_MARK):]
    out = BLOCK_HEADER.format(tier="strict", version=version, source="blocklist-strict.txt")
    out += transform_body(body, version, len(s_exc)) + "\n"
    (OUTDIR / "block-strict.txt").write_text(out)
    print(
        f"wrote pihole/block-strict.txt: {len(s_blocks)} blocks, "
        f"{len(s_regex)} regex omitted, {len(s_exc)} exceptions -> allow.txt"
    )

    # ---- allow.txt ---------------------------------------------------------
    region = src_text[src_text.index(KEEP_MARK): src_text.index(OPTIONAL_MARK)]
    region_exc = [ln.strip() for ln in region.splitlines() if ln.strip().startswith("@@")]
    if len(region_exc) != len(d_exc):
        raise SystemExit("exceptions found outside the KEEP-WORKING section — fixes needed")

    seen, lines = set(), []
    for line in region.splitlines():
        s = line.strip()
        if not s:
            lines.append("")
        elif s.startswith("@@"):
            dom = exception_domain(s)
            if dom not in seen:
                seen.add(dom)
                lines.append(dom)
        else:
            lines.append("#" + s[1:])

    out = ALLOW_HEADER.format(version=version) + "\n".join(lines) + "\n"
    (OUTDIR / "allow.txt").write_text(out)
    print(f"wrote pihole/allow.txt: {len(seen)} allow entries")


if __name__ == "__main__":
    main()
