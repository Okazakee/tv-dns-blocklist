# TV DNS Blocklist

Curated DNS blocklist for smart-TV telemetry, ads and ACR (automatic content
recognition) tracking. It blocks first-party analytics, viewing-data collection
and home-screen ad endpoints — **without breaking** updates, app stores,
second-screen/remote, voice search or streaming apps.

Covered platforms: **Sony BRAVIA · LG webOS · Samsung Tizen · Hisense VIDAA ·
Vizio SmartCast (Inscape) · Roku · Amazon Fire TV · Philips (Titan OS / Net TV)
· Xiaomi Mi TV · Panasonic VIERA** — including their ACR partners (Samba TV,
Alphonso, Inscape, Roku ACR, Amazon ACR, Samsung Ads) and ad delivery systems.

## Usage

### AdGuard Home
*Filters* → *DNS blocklists* → *Add blocklist* → *Add a custom list*, then paste:

```text
https://raw.githubusercontent.com/Okazakee/tv-dns-blocklist/main/blocklist.txt
```

### Pi-hole
*Group Management* → *Adlists* → add the same URL → `pihole -g`.

### Other DNS filters
Standard Adblock syntax — `||domain^` blocks, `@@…$important` exceptions and
regex rules. Works with any engine that supports host-list or Adblock rules.

## Repository layout

```text
tv-dns-blocklist/
├── blocklist.txt   # the list (Adblock syntax; comments document every choice)
├── README.md
└── LICENSE         # MIT
```

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
hosts excepted) and `x2.vindicosuite.com`.

## What is never blocked

Everything needed to update, install, authenticate and play is protected with
`$important` exceptions — they also win over other subscribed lists that
wrongly block these hosts. Highlights:

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
- all 199 blocked rules + 130 `$important` exceptions parse cleanly; no
  exception overlaps a blocked host (no accidental unblocking)
- zone safety reviewed host-by-host against documented breakage reports
- device-level verification on real sets is **pending** — treat these sections
  as evidence-based, not device-verified

## Sources

Built from community lists, platform recon and independent research:
Perflyst / Dandelion Sprout Smart-TV + AmazonFireTV · hkamran80/blocklists ·
HaGeZi `native.*` + pro + TIF · 1Hosts Pro · The Block List Project ·
ipanalytics device-group lists · samsapti/LG-webOS-Blocklist ·
TheShawnMiranda/LG-TV-Ad-Block · casenjo (Sony) · Level1Techs webOS recon ·
oisd excludes · TP Vision "Smart TV Platform providers" ·
[arXiv:2409.06203](https://arxiv.org/abs/2409.06203) (UCL ACR study) ·
netify.ai · Samsung ACR support (ANS10010616) · Samsung Ads privacy notice
(policy.samsungrs.com) · THectic-NL/Blocklists (Sept 2026 LG ACR enumeration,
cross-referenced for the LG recommendation/AWS host families).

## License

MIT — see [LICENSE](LICENSE).
