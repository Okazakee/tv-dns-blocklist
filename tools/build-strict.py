#!/usr/bin/env python3
"""Build blocklist-strict.txt from blocklist.txt.

The strict tier is generated, never hand-edited:

    strict = default rules
           + every OPTIONAL row enabled
           + STRICT_EXTRAS (dead HbbTV entries, measurement zones, app
             telemetry, generic ad networks, unknown-risk hosts)

Usage (from anywhere):

    python3 tools/build-strict.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "blocklist.txt"
DST = ROOT / "blocklist-strict.txt"

def version_of(text: str) -> str:
    m = re.search(r"^! Version: (.+)$", text, re.M)
    return m.group(1).strip() if m else "unversioned"


def header(version: str) -> str:
    return f"""\
! ---------------------------------------------------------------------------
! TV telemetry / ads / ACR blocklist — STRICT TIER (generated file)
! Version: {version}
! Homepage: https://github.com/Okazakee/tv-dns-blocklist · License: MIT
! For AdGuard Home (or any engine with full Adblock syntax; Pi-hole users:
! use the generated pihole/ variants — see README)
!
! GENERATED — do not edit by hand. Edit blocklist.txt, then run:
!   python3 tools/build-strict.py
!
! STRICT = the default list + every OPTIONAL row enabled + extra dead-HbbTV,
! measurement-zone, app-telemetry and generic-ad rules. Expect degraded
! features: notices, ThinQ/IoT extras, store thumbnails, recommendations,
! legacy services and some app keepalives stop working.
! Updates, DRM/playback, boot connectivity, app stores and accounts are STILL
! protected — a list that bricks the TV is a bug, not a tier.
! Left out on purpose even here (breaks the app, not "strict"):
!   api.distribution.hulu.com, tv-static.scdn.co (Spotify artwork),
!   xml.opera.com (Opera TV store).
! Sources: full linked list in SOURCES.md —
!   https://github.com/Okazakee/tv-dns-blocklist/blob/main/SOURCES.md
! ---------------------------------------------------------------------------
"""

STRICT_EXTRAS = """
! ============ STRICT EXTRAS ============

! --- Dead/legacy HbbTV entries skipped from the default list ---
||hbbtv-track.redbutton.de^
||hbbtv-1.eurosport.com^
||start.digitaltext.rtl.de^
||hbbtvapp.sonnenklar.tv^
||nbc-jite.nbcuni.com^
||adv.ettoday.net^

! --- Measurement zones (the default blocks only the specific hosts) ---
||ioam.de^
||imrworldwide.com^

! --- Streaming-app telemetry (app-specific; the default leaves apps alone) ---
||customerevents.netflix.com^
||ichnaea.netflix.com^
||settings.crashlytics.com^

! --- Generic ad networks (most DNS lists already cover these) ---
||2mdn.net^
||advertising.com^
||googleads.g.doubleclick.net^

! --- Skipped/unknown-risk hosts (live or resurrectable; harmless to block) ---
||smartshare.lgtvsdp.com^
||lgad.cjpowercast.com.edgesuite.net^
||abtauthprd.samsungcloudsolution.com^
||amauthprd.samsungcloudsolution.com^
||api-hub.samsungyosemite.com^
||us-api.samsungyosemite.com^
||prov.samsungcloudsolution.com^
||cdn.samsungcloudsolution.net^
||managed.xmpp.foxtel.com.au^
||foxtel-prod-events.digitalsmiths.net^
||a1.resources.foxtel.com.au^
||e2.resources.foxtel.com.au^

! --- Platform zone the default keeps because functional hosts live inside ---
||samsungelectronics.com^
"""

REPLACEMENTS = [
    (
        "! ================= OPTIONAL / HIGHER-TRADEOFF =================",
        "! ============ OPTIONAL ROWS — ENABLED IN THIS TIER ============",
    ),
    (
        "! Uncomment only if you accept the listed consequence.",
        "! These rows are ACTIVE here. Features may degrade or break.",
    ),
    (
        "! (all verified as NOT needed for updates)",
        "! (all still verified as NOT needed for updates)",
    ),
]

MARK = "! ============= KEEP-WORKING EXCEPTIONS"


def main() -> None:
    text = SRC.read_text()

    # split off the default list's header (everything before the first brand)
    idx = text.index("! ================= SONY")
    body = text[idx:]

    out_lines = []
    for line in body.splitlines():
        s = line.strip()
        # uncomment optional rows: "!||dom^", "!@@dom^", "!dom" (no space after !)
        if re.match(r"^![|@A-Za-z0-9]", s):
            out_lines.append(s[1:])
            continue
        out_lines.append(line)

    body = "\n".join(out_lines)
    for old, new in REPLACEMENTS:
        body = body.replace(old, new)

    # insert the strict extras right before the exceptions block
    body = body.replace(MARK, STRICT_EXTRAS.lstrip("\n") + "\n" + MARK, 1)

    # dedupe identical rule lines (keep first occurrence), report the count
    seen, deduped, dropped = set(), [], 0
    for line in body.splitlines():
        s = line.strip()
        is_rule = s and not s.startswith("!")
        if is_rule:
            if s in seen:
                dropped += 1
                continue
            seen.add(s)
        deduped.append(line)

    DST.write_text(header(version_of(text)) + "\n".join(deduped) + "\n")
    rules = sum(1 for l in deduped if l.strip() and not l.strip().startswith("!"))
    print(f"wrote {DST.name}: {rules} rules ({dropped} duplicate lines dropped)")


if __name__ == "__main__":
    main()
