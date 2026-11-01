# Changelog

## v2026.11.01 — monthly maintenance

- **Samsung (default)** — added `dls.di.atlas.samsung.com` +
  `regi.di.atlas.samsung.com` (Device Insight data ingestion on GCP; the
  `atlas.samsung.com` apex is NODATA, so per-host rules are safe) and
  `samsung-beacons.xumo.com` (Xumo FAST beacon, matching the Hisense/Roku
  entries already in the list).
- **Xumo beacon gap closed (default)** — `vizio-`, `philips-`, `panasonic-`
  and `android-tv-beacons.xumo.com` added to their brand sections; all five
  resolve to the same beacon front-end (136.110.193.66), streaming untouched.
- **Xiaomi (OPTIONAL)** — `sdkconfig.xiaomi.com` + the `eu/india/intl/rus`
  variants (ad-SDK/base config) as higher-tradeoff rows; the ad-specific
  `sdkconfig.ad.*` hosts remain in the default tier.
- **Fire TV (OPTIONAL)** — `ads.na.prod.channels.firetv.amazon.dev` +
  `ads.eu.prod.channels.firetv.amazon.dev` (Fire TV Channels ad delivery;
  FAST catalogue tradeoff).
- **Sources** — dropped `nextdns/native-tracking-domains` (upstream repo is
  404; its only entry, `logs.roku.com`, is already covered by our ROKU
  section) from `SOURCES.md` and the monthly watch script. Liveness check now
  uses 4 workers with retries to stop resolver rate-limit false positives.
- Counts: default 222 blocks + 7 regex + 135 exceptions (364 rules); strict
  + 9 OPTIONAL rows enabled (see `tools/build-strict.py` output). Generated
  files rebuilt; validation clean.

Releases are tagged `vYYYY.MM.DD`; the same version appears in the header of
every published list. Generated files (`blocklist-strict.txt`, `pihole/*`) are
rebuilt from `blocklist.txt` — see `tools/`.

## v2026.10.07 — maintenance release

- **LG webOS — Content Store fix (device-verified)**: `rdx2.lgtvsdp.com`,
  `lgtvonline.lge.com`, `eic-ngfts.lge.com` and `lgrecommends.lgappstv.com`
  moved from block rules to `$important` KEEP exceptions — on a live webOS set
  the store failed with a network error (`-102`) while they were blocked. The
  wide `*-gfts`/`*-ngfts` workers and the per-country AWS backends stay
  blocked; being `$important`, the exceptions also win over other subscribed
  lists that block these hosts.
- Counts: default 215 blocks + 7 regex + 135 exceptions (357 rules); strict 324
  + 7 + 135 (466 rules). Generated files rebuilt; validation clean (0 errors).

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
