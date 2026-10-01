# Changelog

Releases are tagged `vYYYY.MM.DD`; the same version appears in the header of
every published list. Generated files (`blocklist-strict.txt`, `pihole/*`) are
rebuilt from `blocklist.txt` — see `tools/`.

## v2026.10.01 — maintenance release

- **Roku** — added `||ads.rokuapi.net^` (Roku's ad API domain; currently dark —
  no A/CNAME upstream — blocked preventively like the other currently-dark Roku
  hosts).
- **Fire TV (optional → strict)** — `!||aax-ott-sdk.amazon-adsystem.amazon.com^`
  (Amazon OTT ads SDK; live-verified CNAME into the APS ad bid lake
  `s2s-iad.stv.bid-na.ads.aps.amazon-adsystem.com`). Strict tier only — the
  default list is unchanged.
- **Docs** — the HaGeZi canary note now covers both dotted and hyphen forms of
  `h4g3z1-native*` hosts, so upstream renames don't trigger re-evaluation.
- Counts: default 219 blocks + 7 regex + 131 exceptions (357 rules); strict 328
  + 7 + 131 (466 rules). Generated files rebuilt; validation clean (0 errors).

## v2026.09.23 — first tagged release

**Coverage** — telemetry, ads and ACR endpoints of ten platforms, plus
broadcast/HbbTV trackers:

- **Sony BRAVIA** — `ndmdhs.com` measurement backends, Samba TV ACR,
  device-hashed ad hosts (+ regex for future hashes), legacy ad/promo endpoints
- **LG webOS** — ad servers (`lgsmartad.com`, `cjpowercast.com`, `smartclip.*`,
  `yumenetworks.com`), Alphonso ACR, CDP (`lgtvcommon.com`), `rdx2` telemetry,
  recommender/AWS backends, store beacons, `*-gfts`/`*-ngfts` workers
- **Samsung Tizen** — full ACR pipeline (`samsungacr.com`, `acr0` + regex,
  `acr-<cc>-prd`), Samsung Ads/AdGear, log/error dumps, TV Plus beacons,
  legacy InfoLink and third-party beacons
- **Hisense VIDAA** — telemetry journals, monetization backends, ad hosts,
  home-screen promos, FAST beacons
- **Vizio SmartCast** — Inscape ACR zone, ad/telemetry hosts, SmartCast ad
  subdomains (per host — the rest of the zone stays functional)
- **Roku** — log fleet, ad framework, Roku ACR (`ravm.tv`), shared
  measurement hosts
- **Fire TV** — device telemetry, ACR, crash reporting, third-party SDK hosts
- **Philips** — Titan OS ad/promo surfaces, legacy Saphi/Net TV ad endpoints
- **Xiaomi Mi TV** — tracking ingest, PatchWall/TV backends, GITV ad stack
- **Panasonic VIERA** — `myhomescreen.tv` telemetry (app-start hosts
  excepted), Vindico suite
- **Broadcast/HbbTV** — Red Button front-ends, broadcaster HbbTV services,
  audience measurement

**Tiers** — `blocklist.txt` (default, non-breaking; device-verified on Sony +
LG, resolution-level elsewhere) and `blocklist-strict.txt` (generated; every
OPTIONAL row enabled + extras). 131 `$important` KEEP exceptions guard
updates/OTA, app stores, DRM/playback, accounts, time sync, second screen and
voice.

**Pi-hole support** — generated `pihole/block.txt`, `pihole/block-strict.txt`
and `pihole/allow.txt` (the Pi-hole variant; subscribe the allowlist too,
Pi-hole v6+).

**Automation** — CI validation on every push/PR: rule syntax, duplicates,
block/exception collisions, KEEP-host protection, generated-file sync
(`tools/validate.py`). Versioned list headers; sources inventory in
`SOURCES.md`.
