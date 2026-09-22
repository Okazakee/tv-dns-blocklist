# TV telemetry blocklist — Sony BRAVIA · LG webOS · Samsung Tizen

Curated DNS blocklist for **Sony BRAVIA**, **LG webOS** and **Samsung Tizen** smart TVs.
It blocks telemetry, usage/ACR (automatic content recognition) tracking, home-screen ads and recommendation beacons — **without breaking** updates, app stores, second-screen/remote, voice search or streaming apps.

Sony + LG rows are verified against real DNS traffic from a Sony BRAVIA and an LG webOS TV; Samsung rows are evidence-based (UCL ACR study, Samsung Ads policy, live resolution checks) and deliberately exclude every host with a documented breakage — see [Verification](#verification).

## Usage

### AdGuard Home
1. *Filters* → *DNS blocklists* → *Add blocklist* → *Add a custom list*
2. Paste:
   ```
   https://raw.githubusercontent.com/Okazakee/tv-dns-blocklist/main/blocklist.txt
   ```

### Pi-hole
*Group Management* → *Adlists* → add the same URL → then run `pihole -g`.

### Other DNS filters
Standard Adblock syntax (`||domain^`, `@@…$important` exceptions, regex rules). Works with any engine that supports host-list/Adblock rules.

## What gets blocked

**Sony BRAVIA**
- `ndmdhs.com` — Sony measurement / config-distribution backends (Nielsen/Sony joint measurement; observed live: `meta` / `bda` / `cdn` / `cert-cdn` / `image.iac` hosts)
- `samba.tv` — Samba TV ACR (content fingerprinting; Sony partner since 2013)
- Device-hashed ad/telemetry hosts (`*.ssm1/2.internet.sony.tv`) + a regex covering future hashes
- Legacy ad/promo endpoints (`flingo.tv`, `facemap.foldlife.net`, `call.me.sel.sony.com`, `sonybivstatic-a.akamaihd.net`, `bravia.dl.playstation.net`)

**LG webOS**
- `lgtvcommon.com` — CDP (content discovery platform): beacons, nudge/promo, user-profile & usage-pattern profiling, ad/ACR overlays (`*.acr.lab`), launcher callbacks
- `lgsmartad.com`, `cjpowercast.com`, `smartclip.net/.com`, `yumenetworks.com` — LG ad delivery
- `alphonso.tv` — LG Ad Solutions ACR ("Live Plus")
- Telemetry upload & recommender data: `rdx2.nextlgsdp.com`, `rdx2.*.lgtvsdp.com`, `lgtvonline.lge.com`
- Content-store ad/stats beacons: `ad/ibs/ibis/ibsstat.lgappstv.com`
- AI/recommendation telemetry workers: `*-gfts.lge.com`, `*-ngfts.lge.com`
- `ueiwsp.com`

**Samsung Tizen**
- `samsungacr.com` (whole zone) + `acr0.samsungcloudsolution.com` (+ `acr<N>` regex) + `acr-<cc>-prd.samsungcloud.tv` (9 regions) — Samsung Ads' own ACR fingerprinting pipeline (study-confirmed)
- `infolink.pavv.co.kr` / `pavv.co.kr` — legacy InfoLink beacon (2013–2015 sets; bursts of ~10k queries/10 min)
- `samsungads.com`, `samsungadhub.com`, `samsungtvads.com`, `tvx.adgrx.com`/`adgrx.com`, `sspapi-prd.samsungrs.com`, `adconsent.samsungrs.com`, `samsungads.adsmeasurement.com`, `img-resize-cdn-prod.samsungnyc.com`, `sca.samsung.com` — Samsung Ads / AdGear ad delivery
- Telemetry & logs: `ureca.samsungapps.com` (in-app analytics SDK), `devicelog.samsungcloudsolution.net`, `prderrordump{hsm,ssm}`, `musicid.*`, `vdterms.*`, `sas.*`, `gamespromotion.*`, `svwindow.*`
- TV Plus session/log beacons: `tvpnlog{o,eu,us,du}.samsungcloud.tv`, `tvpndynamiclog*`, `qoe.samsungcloud.tv` (streaming + EPG stay reachable)
- Third-party/legacy beacons: `connecttv.pelmorex.com` (weather app), `premium-videos.telly.com`, `log/game.internetat.tv`, `pipeaota.com`, `[a-z]pu.samsungelectronics.com` regex, `test.samsungrm.net`

## What is *never* blocked

Protected by `$important` exceptions (this also protects them against other subscribed lists accidentally blocking them):

- Sony: `info.update.sony.net`, `www.sony.net`, `update/reg/service.biv.sony.tv`, `api/metadata.erabu.sony.tv`
- LG: `su.lge.com`, `su-ssl.lge.com`, `snu.lge.com`, `nsu.lge.com` (+ `-dev` variants)
- Samsung: `cdn.samsungcloudsolution.com` (connectivity check + app boot + update check), `time.samsungcloudsolution.com/.net`, `otnprd8-11.samsungcloudsolution.net`, `otn.samsungcloudcdn.com`, `samsungotn.net`, `osb-ussvc(.v2)`/`osb-apps(.v2)`/`gpm.samsungqbe.com` (TV Plus + app store/auth), `configprd/lcprd1/lcprd2.samsungcloudsolution.net`, `sso.internetat.tv`, `sc-auth`/`eu-auth2.samsungosp.com`, `api/hub/img/iap.samsungapps.com`, `d1oxlq5h9kq8q5.cloudfront.net`, `ns11.whois.co.kr`, `www.samsungrm.net`, `tvpnlinupepgp{eu,us}.samsungcloud.tv`, `account.samsung.com`, `samsungcloud.com`

Also intentionally left working: app stores (`lgappstv.com` base, `samsungapps.com` base, `portal.store.sonyentertainmentnetwork.com`), second-screen/mobile app (`lgtvsdp.com` base), store thumbnails (`ngfts.lge.com` bare), voice search (`lgsmartweb.com`), `sony.com` / `lg.com` / `samsung.com`, Samsung DRM/PlayReady licences, TV Plus EPG + UI images (`tvpnlinupepgp*`, `fc`/`ghsimgstore.samsungcloud.tv`).

A commented *OPTIONAL* section at the bottom of `blocklist.txt` holds higher-tradeoff entries (ThinQ/IoT, `nextlgsdp.com`, bare `ngfts.lge.com`, Samsung `fkp`/`oempprd`/`notice*`/`openapi`/push/IoT-cloud/legacy ad hosts, …) — uncomment only if you accept the consequence listed there.

## Limitations

- Some TVs bootstrap their own encrypted DNS (DoH/DoT to `8.8.8.8` / `1.1.1.1`) and some services use hardcoded IPs — those bypass DNS filtering; handle at router/firewall level if needed. Samsung/Tizen sets are known for ignoring DHCP DNS: NAT-redirect `:53` and drop `443/853` to public resolvers on the TV VLAN for real coverage.
- LG's OTA fallback IP `156.147.69.32:8080` is not DNS-blockable.
- Samsung zones are mixed: never block `samsungcloudsolution.com`, `samsungcloudsolution.net`, `samsungqbe.com` or `samsungcloud.tv` wholesale — each contains critical hosts (documented breakages: `cdn.time.samsungcloudsolution.com` → YouTube dies; `samsungqbe.com` → TV Plus + app store; `samsungcloud.tv` → TV Plus EPG/UI images). The list blocks per-host instead.

## Verification

2026-09-22, on a live AdGuard Home instance with real traffic from a Sony BRAVIA + an LG webOS TV:

- all blocked entries return `0.0.0.0`; the device-hash regex was confirmed against synthetic hashes
- all update / app-store / second-screen / voice endpoints resolve normally before **and** after enabling the list
- both TVs kept working normally post-change; telemetry endpoints were observed being blocked in the live query log (e.g. LG `rdx2.*` and Sony `ndmdhs.com` hosts)

2026-09-23, Samsung (resolution-level, no Samsung TV on the test network yet):

- every Samsung blocked row resolves upstream before enabling (so the filter takes effect) and every KEEP row resolves
- zone-safety reviewed host-by-host against documented breakage reports (Perflyst issues #49/#82, oisd excludes, Control D / Pi-hole / Technitium threads)
- device-level verification on a real Tizen set is **pending** — treat the Samsung section as evidence-based, not device-verified

## Sources & credits

Built from community lists, platform recon and independent research:
Perflyst / Dandelion Sprout Smart-TV blocklist · hkamran80/blocklists · HaGeZi `native.samsung` + TIF · The Block List Project (smart-tv/tracking/ads) · samsapti/LG-webOS-Blocklist · TheShawnMiranda/LG-TV-Ad-Block · casenjo (Sony gist) · Level1Techs "LG TV Block Mini-How-to" · oisd excludes · UCL study [arXiv:2409.06203](https://arxiv.org/abs/2409.06203) · netify.ai · Samsung ACR support (ANS10010616) · Samsung Ads privacy notice (policy.samsungrs.com).

## License

MIT — see [LICENSE](LICENSE).
