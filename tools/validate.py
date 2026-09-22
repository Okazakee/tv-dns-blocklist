#!/usr/bin/env python3
"""Validate the TV DNS Blocklist repository. Usage: python3 tools/validate.py

Runs entirely offline; executed by CI on every push/PR
(.github/workflows/validate.yml). Checks:

  1. syntax + normalization — every active rule is a valid ||domain^ block, a
     bare exact host, a /regex/ rule or an @@...^$important exception;
     domains are lowercase, well-formed and not IP addresses
  2. no duplicate rules
  3. KEEP protection — no exception host is blocked exactly; KEEP hosts that
     sit under a broad zone block are surfaced as warnings (safe while the
     $important exception outranks plain blocks — AdGuard semantics)
  4. regex rules compile (Python re — a close match of the AdGuard subset)
  5. strict tier ⊇ default tier (blocks, regexes, exceptions) and contains no
     leftover commented OPTIONAL rows
  6. generated files (blocklist-strict.txt, pihole/*) match their sources,
     rule by rule
  7. version headers of all generated files match blocklist.txt

Exit code 0 = OK, 1 = errors (printed with file:line).
"""
from __future__ import annotations

import ipaddress
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = ROOT / "blocklist.txt"
STRICT = ROOT / "blocklist-strict.txt"
PIHOLE = ROOT / "pihole"

DOMAIN_RE = re.compile(
    r"^[a-z0-9_]([a-z0-9_-]*[a-z0-9_])?(\.[a-z0-9_]([a-z0-9_-]*[a-z0-9_])?)+$"
)
BLOCK_RE = re.compile(r"^\|\|([^|^@$/ ]+)\^$")
EXC_RE = re.compile(r"^@@(\|\|?)([^|^@$/ ]+)\^\$important$")
VERSION_RE = re.compile(r"^[!#] Version: (.+)$", re.M)

errors: list[str] = []
warnings: list[str] = []


def err(path: Path, ln: int | None, msg: str) -> None:
    errors.append(f"{path.name}:{ln}: {msg}" if ln else f"{path.name}: {msg}")


def warn(path: Path, ln: int | None, msg: str) -> None:
    warnings.append(f"{path.name}:{ln}: {msg}" if ln else f"{path.name}: {msg}")


def check_domain(path: Path, ln: int, d: str) -> bool:
    if not DOMAIN_RE.fullmatch(d):
        if d != d.lower():
            err(path, ln, f"domain not normalized (uppercase): {d!r}")
        else:
            err(path, ln, f"invalid hostname: {d!r}")
        return False
    try:
        ipaddress.ip_address(d)
        err(path, ln, f"IP address used as a domain: {d!r}")
        return False
    except ValueError:
        return True


def parse(path: Path) -> dict:
    data = {
        "block_lines": [],   # raw lines: "||d^" or bare host
        "blocks": [],        # (domain, form, line) form in {"wild", "bare"}
        "regexes": [],       # (pattern, line)
        "regex_lines": [],
        "exc_lines": [],
        "exceptions": [],    # (domain, line)
    }
    for ln, raw in enumerate(path.read_text().splitlines(), 1):
        s = raw.strip()
        if not s or s.startswith("!"):
            continue
        if s.startswith("@@"):
            m = EXC_RE.fullmatch(s)
            if not m:
                err(path, ln, f"malformed exception (want @@||domain^$important): {s!r}")
                continue
            d = m.group(2)
            if check_domain(path, ln, d):
                data["exc_lines"].append(s)
                data["exceptions"].append((d, ln))
        elif s.startswith("||"):
            m = BLOCK_RE.fullmatch(s)
            if not m:
                err(path, ln, f"malformed block rule: {s!r}")
                continue
            d = m.group(1)
            if check_domain(path, ln, d):
                data["block_lines"].append(s)
                data["blocks"].append((d, "wild", ln))
        elif s.startswith("/"):
            if len(s) < 3 or not s.endswith("/"):
                err(path, ln, f"malformed regex rule: {s!r}")
                continue
            pattern = s[1:-1]
            try:
                re.compile(pattern)
            except re.error as exc:
                err(path, ln, f"regex does not compile: {exc}")
                continue
            data["regex_lines"].append(s)
            data["regexes"].append((pattern, ln))
        else:
            if check_domain(path, ln, s):
                data["block_lines"].append(s)
                data["blocks"].append((s, "bare", ln))
    return data


def check_file(path: Path, data: dict) -> None:
    # duplicates (exact line repeated)
    counts: dict[str, list[int]] = {}
    for ln, raw in enumerate(path.read_text().splitlines(), 1):
        s = raw.strip()
        if not s or s.startswith("!"):
            continue
        counts.setdefault(s, []).append(ln)
    for rule, lns in counts.items():
        if len(lns) > 1:
            err(path, lns[0], f"duplicate rule (also lines {lns[1:]}) : {rule!r}")

    # redundant wild+bare for the same host
    wild = {d for d, f, _ in data["blocks"] if f == "wild"}
    bare = {d for d, f, _ in data["blocks"] if f == "bare"}
    for d in sorted(wild & bare):
        warn(path, None, f"covered twice: {d!r} blocked as both ||domain^ and bare host")

    # KEEP protection: no exception may be blocked exactly; a KEEP host under a
    # broad zone block is surfaced as a warning (it is safe as long as the
    # $important exception is kept — AdGuard: $important outranks plain rules;
    # Pi-hole: subscribed allowlists outrank subscribed denylists).
    for e, eln in data["exceptions"]:
        for d, form, bln in data["blocks"]:
            if e == d:
                err(path, eln, f"KEEP host {e!r} is blocked exactly by a rule with the same domain (line {bln})")
            elif form == "wild" and e.endswith("." + d):
                warn(path, eln, f"KEEP host {e!r} sits under the zone block {d!r} (line {bln}) — relies on the $important exception outranking plain blocks")
    for pattern, pln in data["regexes"]:
        rx = re.compile(pattern)
        for e, eln in data["exceptions"]:
            if rx.search(e):
                warn(path, eln, f"KEEP host {e!r} matches regex {pattern!r} (line {pln}) — relies on the $important exception outranking plain blocks")


def check_strict(default: dict, strict: dict) -> None:
    missing = (set(default["block_lines"]) | set(default["regex_lines"])) - (
        set(strict["block_lines"]) | set(strict["regex_lines"])
    )
    for rule in sorted(missing):
        err(STRICT, None, f"strict tier is missing a default-tier rule: {rule!r}")
    missing_exc = set(default["exc_lines"]) - set(strict["exc_lines"])
    for rule in sorted(missing_exc):
        err(STRICT, None, f"strict tier is missing a default-tier exception: {rule!r}")
    for ln, raw in enumerate(STRICT.read_text().splitlines(), 1):
        if re.match(r"^![|@A-Za-z0-9]", raw.strip()):
            err(STRICT, ln, f"commented OPTIONAL row still present in strict file: {raw.strip()!r}")


def parse_plain(path: Path) -> list[tuple[str, int]]:
    out = []
    for ln, raw in enumerate(path.read_text().splitlines(), 1):
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        out.append((s, ln))
    return out


def check_pihole(default: dict, strict: dict) -> None:
    # block.txt
    block = parse_plain(PIHOLE / "block.txt")
    for s, ln in block:
        if not (BLOCK_RE.fullmatch(s) or DOMAIN_RE.fullmatch(s)):
            err(PIHOLE / "block.txt", ln, f"invalid Pi-hole block entry: {s!r}")
    got = {s for s, _ in block}
    want = set(default["block_lines"])
    for s in sorted(want - got):
        err(PIHOLE / "block.txt", None, f"missing from Pi-hole blocklist: {s!r}")
    for s in sorted(got - want):
        err(PIHOLE / "block.txt", None, f"unexpected entry (not in blocklist.txt): {s!r}")

    # block-strict.txt
    block_s = parse_plain(PIHOLE / "block-strict.txt")
    for s, ln in block_s:
        if not (BLOCK_RE.fullmatch(s) or DOMAIN_RE.fullmatch(s)):
            err(PIHOLE / "block-strict.txt", ln, f"invalid Pi-hole block entry: {s!r}")
    got = {s for s, _ in block_s}
    want = set(strict["block_lines"])
    for s in sorted(want - got):
        err(PIHOLE / "block-strict.txt", None, f"missing from Pi-hole strict blocklist: {s!r}")
    for s in sorted(got - want):
        err(PIHOLE / "block-strict.txt", None, f"unexpected entry (not in blocklist-strict.txt): {s!r}")

    # allow.txt
    allow = parse_plain(PIHOLE / "allow.txt")
    for s, ln in allow:
        if not DOMAIN_RE.fullmatch(s):
            err(PIHOLE / "allow.txt", ln, f"invalid allow entry: {s!r}")
    got = {s for s, _ in allow}
    want = {d for d, _ in default["exceptions"]}
    for s in sorted(want - got):
        err(PIHOLE / "allow.txt", None, f"missing KEEP host: {s!r}")
    for s in sorted(got - want):
        err(PIHOLE / "allow.txt", None, f"unexpected allow entry (not an exception): {s!r}")


def check_versions(default_text: str) -> None:
    m = VERSION_RE.search(default_text)
    if not m:
        err(DEFAULT, None, "no '! Version:' header found")
        return
    version = m.group(1).strip()
    for path in (STRICT, PIHOLE / "block.txt", PIHOLE / "block-strict.txt", PIHOLE / "allow.txt"):
        m2 = VERSION_RE.search(path.read_text())
        if not m2:
            err(path, None, "no Version header found")
        elif m2.group(1).strip() != version:
            err(path, None, f"version {m2.group(1).strip()!r} != blocklist.txt {version!r}")


def counts_line(name: str, data: dict) -> str:
    wild = sum(1 for _, f, _ in data["blocks"] if f == "wild")
    bare = sum(1 for _, f, _ in data["blocks"] if f == "bare")
    return (
        f"{name}: {len(data['blocks'])} blocks ({wild} wild + {bare} exact) · "
        f"{len(data['regexes'])} regex · {len(data['exceptions'])} exceptions"
    )


def main() -> int:
    for path in (DEFAULT, STRICT, PIHOLE / "block.txt", PIHOLE / "block-strict.txt", PIHOLE / "allow.txt"):
        if not path.exists():
            err(path, None, "file missing")

    default = parse(DEFAULT)
    strict = parse(STRICT)
    check_file(DEFAULT, default)
    check_file(STRICT, strict)
    check_strict(default, strict)
    check_pihole(default, strict)
    check_versions(DEFAULT.read_text())

    # sanity ranges
    if len(default["blocks"]) < 100:
        warn(DEFAULT, None, f"suspiciously few block rules ({len(default['blocks'])})")
    if len(default["exceptions"]) < 50:
        warn(DEFAULT, None, f"suspiciously few exceptions ({len(default['exceptions'])})")
    if len(strict["blocks"]) < len(default["blocks"]):
        err(STRICT, None, "strict tier has fewer block rules than the default tier")

    print("== TV DNS Blocklist validation ==")
    print(counts_line("default", default))
    print(counts_line("strict ", strict))
    print(
        f"pihole : block {len(parse_plain(PIHOLE / 'block.txt'))} · "
        f"block-strict {len(parse_plain(PIHOLE / 'block-strict.txt'))} · "
        f"allow {len(parse_plain(PIHOLE / 'allow.txt'))}"
    )
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if errors:
        print(f"FAILED — {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"OK — 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
