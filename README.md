# TV DNS Blocklist

Curated DNS blocklist for smart-TV telemetry, ads and ACR (automatic content
recognition) tracking — **non-breaking by design**: it blocks first-party
analytics, viewing-data collection and home-screen ad endpoints while updates,
app stores, DRM/playback, second screen and voice search keep working.

- **What keeps working** — updates/OTA, app stores, DRM & playback, EPG,
  accounts, time sync, second screen, voice — protected with `$important`
  exceptions that also win over other subscribed lists.
- **What it blocks** — per-platform analytics, ACR and ad endpoints on ten
  platforms: Sony BRAVIA · LG webOS · Samsung Tizen · Hisense VIDAA · Vizio
  SmartCast (Inscape) · Roku · Fire TV · Philips (Titan OS / Net TV) · Xiaomi
  Mi TV · Panasonic VIERA — incl. ACR partners (Samba TV, Alphonso, Inscape,
  Roku ACR, Amazon ACR, Samsung Ads) and broadcast/HbbTV tracking.
- **How far it's verified** — device-verified on real Sony BRAVIA and LG webOS
  sets; resolution-level for the other platforms (see
  [Verification](#verification)).

Two tiers, one repo: **`blocklist.txt`** (default, non-breaking) and
**`blocklist-strict.txt`** (aggressive, opt-in — see [Tiers](#tiers)) — plus
generated **Pi-hole** variants (see [Usage](#usage)).

## Usage

**Start with `blocklist.txt`** — the default, non-breaking tier and what this
repo is built around. Pick `blocklist-strict.txt` only if you knowingly accept
degraded features (see [Tiers](#tiers)).

### AdGuard Home
*Filters* → *DNS blocklists* → *Add blocklist* → *Add a custom list*, then paste
**one** of:

```text
# default tier — recommended, non-breaking
https://raw.githubusercontent.com/Okazakee/tv-dns-blocklist/main/blocklist.txt

# strict tier — opt-in, may degrade features
https://raw.githubusercontent.com/Okazakee/tv-dns-blocklist/main/blocklist-strict.txt
```

### Pi-hole
Use the generated Pi-hole variant — **not** the AdGuard files (gravity only
understands plain domains and `||domain^` wildcard rules; exceptions,
`$important` and regex rules would be ignored):

```text
# blocklist — default tier
https://raw.githubusercontent.com/Okazakee/tv-dns-blocklist/main/pihole/block.txt
# blocklist — strict tier (pick this OR the default, not both)
https://raw.githubusercontent.com/Okazakee/tv-dns-blocklist/main/pihole/block-strict.txt
# allowlist — add this too; it protects updates / stores / DRM (Pi-hole v6+)
https://raw.githubusercontent.com/Okazakee/tv-dns-blocklist/main/pihole/allow.txt
```

*Settings → Lists*: add the blocklist URL as a **blocklist** and the allowlist
URL as an **allowlist** (subscribed allowlists require Pi-hole v6+), then
`pihole -g`. The 7 regex rules can't live in a subscribed list — add them via
Pi-hole's regex denylist if you want that coverage.

### Other DNS filters
`blocklist.txt` uses full Adblock/AdGuard syntax — `||domain^` blocks,
`@@…$important` exceptions (they outrank plain blocking rules, from any list)
and regex rules. Use it with an engine that implements the full semantics
(e.g. AdGuard Home). Engines with partial Adblock support (Pi-hole) should use
the generated `pihole/` variant instead.

## Repository layout

```text
tv-dns-blocklist/
├── blocklist.txt          # default tier (Adblock syntax; comments document every choice)
├── blocklist-strict.txt   # strict tier (generated — do not edit by hand)
├── pihole/
│   ├── block.txt          # default tier, Pi-hole variant (generated)
│   ├── block-strict.txt   # strict tier, Pi-hole variant (generated)
│   └── allow.txt          # KEEP-WORKING hosts as allowlist (generated — subscribe it!)
├── tools/
│   ├── build-strict.py    # regenerates blocklist-strict.txt from blocklist.txt
│   ├── build-pihole.py    # regenerates the pihole/ outputs
│   └── validate.py        # repo validation (runs in CI on every push)
├── .github/workflows/validate.yml
├── SOURCES.md             # every source, linked
├── CHANGELOG.md
├── README.md
└── LICENSE                # MIT
```

## Tiers

- **`blocklist.txt` (default — recommended)** — telemetry, ads and ACR blocked while keeping
  everything functional: updates, app stores, DRM/playback, second screen,
  voice, EPG. This is the tier device-verified on a Sony BRAVIA and an LG webOS
  TV (see [Verification](#verification)).
- **`blocklist-strict.txt`** — the default **plus** every OPTIONAL row enabled
  and extra rules (dead HbbTV entries, measurement zones, app telemetry,
  generic ad networks, unknown-risk hosts). Expect degraded features: notices,
  ThinQ/IoT extras, store thumbnails, recommendations, legacy services and some
  app keepalives. Updates, DRM/playback, boot connectivity, app stores and
  accounts are **still** protected — a list that bricks the TV is a bug, not a
  tier.

The strict file is generated: edit `blocklist.txt`, then run
`python3 tools/build-strict.py` (it enables every commented OPTIONAL row,
appends the strict extras and deduplicates). The `pihole/` outputs are
generated too (`python3 tools/build-pihole.py`); CI fails if a generated file
is out of sync with its source.

## What gets blocked

**Sony BRAVIA** — measurement/config backends (`ndmdhs.com`), Samba TV ACR,
device-hashed ad hosts (`*.ssm*.internet.sony.tv`, plus a regex for future
hashes) and legacy ad/promo endpoints.

**LG webOS** — ad servers (`lgsmartad.com`, `cjpowercast.com`, `smartclip.*`,
`yumenetworks.com`), Alphonso ACR, the CDP tracking platform
(`lgtvcommon.com`), telemetry/recommender uploads (`rdx2.*`,
`lgtvonline.lge.com`), the recommendation/ad family
(`lgrecommends.lgappstv.com`) and its per-country AWS backends
(`*-lgsmartad-com.aws-prd.net`, `*-rdx2-lgtvsdp-com.aws-prd.net`),
content-store beacons and recommendation workers (`*-gfts`/`*-ngfts.lge.com`).

**Samsung Tizen** — the full ACR pipeline (`samsungacr.com`, `acr0` + `acr<N>`
regex, `acr-<cc>-prd.samsungcloud.tv`), Samsung Ads/AdGear delivery
(`samsungads.com`, `samsungadhub.com`, `adgrx.com`, `samsungrs.com`, …),
on-device logs and error dumps, TV Plus log beacons, legacy InfoLink and
third-party beacons.

**Hisense VIDAA** — telemetry/diagnostic journals (`*-jrnl-eu`, `api-logsdk`,
`unified-ter*`), monetization backends (`rpt/rsc-ads`, `rpt/rsc-mntz`,
`monetization-*`), ad hosts, home-screen promos and FAST beacons.

**Vizio SmartCast** — the Inscape ACR zone (`tvinteractive.tv`), Vizio ad and
telemetry hosts (`ads.vizio.com`, `rlog4`, `al-smetrics`, …) and SmartCast
ad/telemetry subdomains (`impression-proxy`, `ad-broker`, `personalization`,
`experiments`, …) — per host, so the rest of the zone stays functional.

**Roku** — the log fleet (`logs.roku.com`, `*.sr.roku.com`), the ad framework
(`ads.roku.com`, `adservices`, `advertising`, …), Roku's own ACR (`ravm.tv`,
`acr.roku.com`) and shared ad-measurement hosts.

**Amazon Fire TV** — device telemetry, ACR and crash reporting
(`device-metrics-us.amazon.com`, `unagi`, `minerva.devices`, Bugsnag,
`web.diagnostic.networking`, third-party SDK hosts). Amazon's shared ad system
and undocumented hosts live in the OPTIONAL section instead.

**Philips** — Titan OS ad/promo surfaces (`ads.titanos.tv`) and the legacy
Saphi/Net TV ad endpoints named in TP Vision's own provider documents.

**Xiaomi Mi TV** — tracking/telemetry ingest (`mitv.tracking`, `data.mistat`,
`sdkconfig.ad.*`), PatchWall/TV backends and ad endpoints (`adx/h5.tv.mi.com`,
GITV stack).

**Panasonic VIERA** — the `myhomescreen.tv` telemetry platform (app-start
hosts excepted) and the Vindico ad-measurement suite (`vindicosuite.com`).

**Broadcast / HbbTV** — Red Button front-ends, German broadcaster HbbTV
services (`p-hbbtv.superrtl.de`, `tracksrv.zdf.de`, anixe hosts), audience
measurement (INFOnline, AT Internet, Nielsen) and connected-TV app telemetry.

## What is never blocked

Everything needed to update, install, authenticate and play is protected with
`$important` exceptions — they also win over other subscribed lists that
wrongly block these hosts (Pi-hole: the same hosts ship as `pihole/allow.txt`,
add it as a subscribed allowlist). Highlights:

- **Updates / OTA** — Sony `*.biv.sony.tv` + `info.update.sony.net` · LG
  `su`/`snu`/`nsu.lge.com` · Samsung `otnprd8-11` + `samsungotn.net` · Hisense
  `upgrade-eu` / `ota-tv` · Vizio `osu.vudip.vizio.com` · Roku
  `tvupdate.roku.com` · Fire TV `softwareupdates.amazon.com` · Xiaomi
  `ota.ptqy.gitv.tv`
- **App stores & installs** — Samsung `samsungapps.com` + `osb-apps*` · LG
  `lgappstv.com` · Roku `channels.roku.com` · Fire TV `msh` /
  `appstore.amazon.com` · Xiaomi `market.xiaomi.com`
- **Playback, DRM & EPG** — Roku `playback-detail.sr.roku.com` · Vizio
  `watchfreeplus-epg-prod` · Xiaomi `tvepg` · Samsung TV Plus EPG and UI
  images · Widevine/PlayReady licence paths
- **Accounts, time sync, second screen, voice** — per brand, plus the boot
  connectivity checks (`fireoscaptiveportal.com`, `cdn.samsungcloudsolution.com`)
  that TVs depend on

The full list lives in the KEEP-WORKING section of `blocklist.txt`. A commented
OPTIONAL section at the bottom holds higher-tradeoff entries (ThinQ/IoT, Amazon
ad system, ZEASN `zeasn.tv`, legacy hosts, …) — uncomment only if you accept
the consequence listed there.

### Breakage policy

Documented breakage beats coverage: a host with a documented breakage never
enters the default list — if it has to stay reachable it gets an `$important`
exception, and anything else that turns out to break gets narrowed to the exact
subdomain or removed, with the reason documented in `blocklist.txt`. The
higher-tradeoff entries live in the strict tier (opt-in) instead of in your TV.

## Limitations

- Some TVs bootstrap their own encrypted DNS (DoH/DoT to `8.8.8.8` / `1.1.1.1`)
  and some services use hardcoded IPs — those bypass DNS filtering. Tizen,
  SmartCast and VIDAA sets are known for ignoring DHCP DNS; NAT-redirect `:53`
  and drop `443/853` to public resolvers on the TV VLAN for real coverage.
- LG's OTA fallback IP `156.147.69.32:8080` is not DNS-blockable.
- Several zones are mixed — never block `samsungcloudsolution.com/.net`,
  `samsungqbe.com`, `samsungcloud.tv`, `smartcasttv.com`, `vizio.com`,
  `roku.com`, `vidaahub.com`, `hismarttv.com` or `titanos.tv` wholesale
  (documented breakages: `cdn.samsungcloudsolution.com` → YouTube dies,
  `samsungqbe.com` → TV Plus + app store, `api.vizio.com` → SmartCast dies).
  The list blocks per host instead.
- `h4g3z1-native.*.web.app` hosts appear in some public lists but are a
  false-positive canary, not trackers — do not copy them.

## Verification

**2026-09-22 — Sony + LG, device-verified** on a live AdGuard Home instance
with real traffic:

- every blocked entry returns `0.0.0.0`; the device-hash regex was confirmed
  against synthetic hashes
- update / app-store / second-screen / voice endpoints resolve normally before
  and after enabling the list
- both TVs kept working post-change; blocked endpoints were observed in the
  live query log

**2026-09-23 — all other brands, resolution-level** (no device of those
platforms on the test network yet):

- every blocked row resolves upstream before enabling, every KEEP row resolves
- all 218 blocked rules + 131 `$important` exceptions parse cleanly; no
  exception is defeated by an exact block rule (the four Panasonic app-start
  hosts sit under the `myhomescreen.tv` zone block by design — their
  `$important` exception outranks it)
- zone safety reviewed host-by-host against documented breakage reports
- device-level verification on real sets is **pending** — treat these sections
  as evidence-based, not device-verified

**2026-09-23 — strict tier**: generated from `blocklist.txt` (464 rules: 326
blocks + 7 regex + 131 exceptions, every OPTIONAL row enabled, 0 malformed, no
exception/block overlap) and load-tested in a throwaway AdGuard Home instance —
filter fetched, parsed and applied; strict-only hosts return `0.0.0.0` while
update/DRM/store hosts still resolve.

**2026-09-23 — automated**: CI runs `tools/validate.py` on every push/PR —
rule syntax and normalization, duplicate detection, KEEP-protection checks and
a rule-by-rule diff of every generated file against its source.

## Sources

Community blocklists, investigations, vendor documents, breakage reports and
the enumeration tooling behind this list — all links in **[SOURCES.md](SOURCES.md)**.

## License

MIT — see [LICENSE](LICENSE).
