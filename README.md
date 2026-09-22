# TV telemetry blocklist — Sony · LG · Samsung · Hisense · Vizio · Roku · Fire TV · Philips · Xiaomi · Panasonic

Curated DNS blocklist for smart TVs and streaming platforms.
It blocks telemetry, usage/ACR (automatic content recognition) tracking, home-screen ads and recommendation beacons — **without breaking** updates, app stores, second-screen/remote, voice search or streaming apps.

Sony + LG rows are verified against real DNS traffic from a Sony BRAVIA and an LG webOS TV. Samsung and the other brands are evidence-based (vendor policy documents, the UCL ACR study, community lists, certificate transparency logs, live resolution checks) and deliberately exclude every host with a documented breakage — see [Verification](#verification).

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
- `ndmdhs.com` — Sony measurement / config-distribution backends (observed live: `meta` / `bda` / `cdn` / `cert-cdn` / `image.iac` hosts)
- `samba.tv` — Samba TV ACR (content fingerprinting; Sony partner since 2013)
- Device-hashed ad/telemetry hosts (`*.ssm1/2.internet.sony.tv`) + a regex covering future hashes
- Legacy ad/promo endpoints (`flingo.tv`, `facemap.foldlife.net`, `call.me.sel.sony.com`, `sonybivstatic-a.akamaihd.net`, `bravia.dl.playstation.net`)

**LG webOS**
- `lgtvcommon.com` — CDP (content discovery platform): beacons, nudge/promo, user-profile & usage-pattern profiling, ad/ACR overlays, launcher callbacks
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

**Hisense VIDAA**
- Telemetry/diagnostic journals: `*-jrnl-eu.vidaahub.com`, `api-logsdk` / `unified-ter*` / `unified-exc` / `api-cloudfalcon` / `api-gps-eu` on `hismarttv.com`
- Ad/monetization backends: `rpt/rsc-ads` + `rpt/rsc-mntz` + `monetization-*` on `vidaahub.com`, `ad-cmp` / `ad-imp` / `ad-download*` on `hismarttv.com`, `ads-portal-cdn.vidaatv.net`, `tracking-vss`, `abtest-tv`
- Home-screen promos/recommendations: `recommend-ui*`, `recommender-launcher`, `api-4know-eu`, `api-shoppingguider`
- FAST + third-party: `hisense(-lite)-beacons.xumo.com`, `acr.unruly.co`, `api.thetake.com`, `trvdp.com`, `de.ioam.de`

**Vizio SmartCast / Inscape**
- `tvinteractive.tv` (whole zone) — Inscape (Vizio's ACR subsidiary): capture, control, metadata, viewing-event ingest, Project OAR
- `ads.vizio.com`, `sstreams.ads.vizio.com`, `al-smetrics.vizio.com`, `rlog4.vizio.com`, `rlog_sem.vizio.com`, `vizio.adsmeasurement.com`
- SmartCast ad/telemetry subdomains: `impression-proxy-prod`, `content-engagement-metrics`, `personalization-prod`, `experiments-prod`, `ad-broker-prod`, `promotions-prod` (per-host — the rest of the zone stays functional)
- Legacy VIA/VIA+ era: `digitalhomeservices.yahoo.com`, `widgets.yahoo.com`

**Roku**
- Telemetry/logging: `logs.roku.com` (Scribe/Cooper log fleet), `track/traces/bif/userdata/assets/logs.sr.roku.com`, `amarillo.sb.roku.com`, `samples.voice.cti.roku.com`, `cloudservices.roku.com`, `analytics.roku.com`, `beacon*.web.roku.com`, `pixel.web.roku.com`, `customer-feedbacks.web.roku.com`, `amoeba-plus.web.roku.com`, `wwwimg.roku.com`
- Ads: `ads.roku.com` (+ `p.`/`i.`), `ads-*.delivery.roku.com`, `adservices.roku.com`, `advertising*.roku.com`, `ads.gcp.roku.com`, `adsmanager.roku.com`
- ACR + measurement: `ravm.tv`, `acr.roku.com`, `roku.adsmeasurement.com`, `admeasurement.com` (shared Nielsen platform), `roku-beacons.xumo.com`

**Amazon Fire TV**
- Device telemetry/ACR/crash reporting: `device-metrics-us.amazon.com`, `unagi.amazon.com`, `minerva.devices.a2z.com`, `insights.video.a2z.com`, `notify.firetv.bugsnag.appstore.a2z.com`, `bugs.firebat.prime-video.amazon.dev`, `mobileanalytics.us-east-1.amazonaws.com`, `web.diagnostic.networking.aws.dev`, `api.statsig.com`, `mobile-collector.newrelic.com`, `config.ioam.de`, `device-messaging-na.amazon.com`, `mas-sdk.amazon.com`
- Amazon ad system + low-confidence hosts live in the OPTIONAL section (shared web-wide infra — enabling them affects non-TV traffic too)

**Philips (Titan OS / Net TV)**
- `ads.titanos.tv`, `philips-android-promo.titanos.tv`, `android-promo.titanos.tv` — Titan OS (2024+) ad/promo surfaces
- Legacy Saphi/Net TV: `ad.nettvservices.com`, `legacyportal.nettvservices.com`, `nettv.corio.com` (ad endpoints named by TP Vision's own provider documents)

**Xiaomi Mi TV / PatchWall**
- Tracking/telemetry: `mitv.tracking.intl.miui.com`, `tracking.intl.miui.com`, `data.mistat.intl.miui.com`, `sdkconfig.ad.*.xiaomi.com`, `sys.tv.india.xiaomi.com`
- TV backends/ads: `tvboss/pull.mitv/dvb/ptmi/hook.gitv.pandora.xiaomi.com`, `adx.tv.mi.com`, `h5.tv.mi.com`, `in.tv.global.mi.com`, `api.cupid.ptqy.gitv.tv`, `pb.bi.gitv.tv`, `tv.app.migc.xiaomi.com`

**Panasonic VIERA** (bonus)
- `myhomescreen.tv` — telemetry/content-collection platform (app-start hosts excepted)
- `x2.vindicosuite.com` — ad/analytics beacon

## What is *never* blocked

Protected by `$important` exceptions (this also protects them against other subscribed lists accidentally blocking them):

- Sony: `info.update.sony.net`, `www.sony.net`, `update/reg/service.biv.sony.tv`, `api/metadata.erabu.sony.tv`
- LG: `su.lge.com`, `su-ssl.lge.com`, `snu.lge.com`, `nsu.lge.com` (+ `-dev` variants)
- Samsung: `cdn.samsungcloudsolution.com` (connectivity check + app boot + update check), `time.samsungcloudsolution.com/.net`, `otnprd8-11.samsungcloudsolution.net`, `otn.samsungcloudcdn.com`, `samsungotn.net`, `osb-ussvc(.v2)`/`osb-apps(.v2)`/`gpm.samsungqbe.com` (TV Plus + app store/auth), `configprd/lcprd1/lcprd2.samsungcloudsolution.net`, `sso.internetat.tv`, `sc-auth`/`eu-auth2.samsungosp.com`, `api/hub/img/iap.samsungapps.com`, `d1oxlq5h9kq8q5.cloudfront.net`, `ns11.whois.co.kr`, `www.samsungrm.net`, `tvpnlinupepgp{eu,us}.samsungcloud.tv`, `account.samsung.com`, `samsungcloud.com`
- Hisense: `upgrade-eu`/`download-upgrade`/`cdn-plugin-sync-upgrade-juui`/`app-appstore`/`msg-eu`/`auth-phone-eu`/`auth-account`/`drm`/`voiceservice-eu`/`home-launcher`/`synctime` on `hismarttv.com`, `ota-tv`/`appstore-vidaa`/`hub-msg`/`params-msg-eu`/`vod-strm` on `vidaahub.com`, `my.vidaa.com`, `castreceiver.vidaatv.net`
- Vizio: `api`/`images`/`announcements`/`scfs`/`platform.vizio.com`, `vizio.pool.ntp.org` (hardcoded NTP), `osu.vudip.vizio.com`, `prod.{device-registration,redwolf,cs}.*.vizio.com`, `api`/`user-authorization-prod`/`video-api-prod`/`watchfreeplus-epg-prod`/`voice-search-prod`/`catalog-prod.smartcasttv.com`
- Roku: `api.roku.com`, `api.rokutime.com`, `image.roku.com`, `therokuchannel.roku.com`, `api.rpay.roku.com`, `rpm.billing.roku.com`, `tvupdate.roku.com`, `channels.roku.com`, `configsvc.cs.roku.com`, `{themes-service,api2,navigation,epgreg,playback-detail}.sr.roku.com`, `tis/voice-public.cti.roku.com`, `prod.mobile.roku.com`, `my.roku.com`
- Fire TV: `fireoscaptiveportal.com`, `firetvcaptiveportal.com`, `dp-discovery-na-ext`/`dcape-na`/`arcus-uswest.amazon.com`, `api.amazonalexa.com`, `avs-alexa-18-na.amazon.com`, `ftvr-na.amazon.com`, `msh`/`mas-ext`/`mas-ssr`/`fls-na.amazon.com`, `softwareupdates.amazon.com`, `amzdigital-a.akamaihd.net`, `atv-ps.amazon.com`, `api.amazonvideo.com`, `appstore.amazon.com`, `ftv-smtv.ntp-fireos.com`, `amazonadsi-a.akamaihd.net`
- Philips: `deviceportal.nettvservices.com`, `epg.corio.com`, `api.titanos.tv`, `www.ecdinterface.philips.com` (Hue bridge)
- Xiaomi: `market.xiaomi.com` (app store), `ota.ptqy.gitv.tv`, `account.xiaomi.com`, `tvepg.pandora.xiaomi.com`, `video.kts.g.mi.com`, `api.io.mi.com`, `authbe.sec.intl.miui.com`
- Panasonic: `mhc-ajax-eu(-s2)`/`mhc-xpana-eu(-s2).myhomescreen.tv`

Also intentionally left working: app stores (`lgappstv.com` base, `samsungapps.com` base, `portal.store.sonyentertainmentnetwork.com`), second-screen/mobile app (`lgtvsdp.com` base), store thumbnails (`ngfts.lge.com` bare), voice search (`lgsmartweb.com`), `sony.com` / `lg.com` / `samsung.com`, Samsung DRM/PlayReady licences, TV Plus EPG + UI images (`tvpnlinupepgp*`, `fc`/`ghsimgstore.samsungcloud.tv`).

A commented *OPTIONAL* section at the bottom of `blocklist.txt` holds higher-tradeoff entries (ThinQ/IoT, `nextlgsdp.com`, Samsung `fkp`/`oempprd`/`notice*`/`openapi`/push/IoT-cloud, Amazon ad system, ZEASN `zeasn.tv`, Panasonic `vcs.vdspf.com`, legacy hosts, …) — uncomment only if you accept the consequence listed there.

## Limitations

- Some TVs bootstrap their own encrypted DNS (DoH/DoT to `8.8.8.8` / `1.1.1.1`) and some services use hardcoded IPs — those bypass DNS filtering; handle at router/firewall level if needed. Tizen/SmartCast/VIDAA sets are known for ignoring DHCP DNS: NAT-redirect `:53` and drop `443/853` to public resolvers on the TV VLAN for real coverage.
- LG's OTA fallback IP `156.147.69.32:8080` is not DNS-blockable.
- Some zones are mixed: never block `samsungcloudsolution.com`, `samsungcloudsolution.net`, `samsungqbe.com`, `samsungcloud.tv`, `smartcasttv.com`, `vizio.com`, `roku.com`, `vidaahub.com`, `hismarttv.com` or `titanos.tv` wholesale — each contains critical hosts (documented breakages: `cdn.time.samsungcloudsolution.com` → YouTube dies; `samsungqbe.com` → TV Plus + app store; `samsungcloud.tv` → TV Plus EPG/UI images; `api.vizio.com` → SmartCast dies). The list blocks per-host instead.
- `h4g3z1-native.roku.web.app` (and similar `h4g3z1-*` hosts) appear in some lists but are a **false-positive canary**, not a tracker — do not copy them.

## Verification

2026-09-22, on a live AdGuard Home instance with real traffic from a Sony BRAVIA + an LG webOS TV:

- all blocked entries return `0.0.0.0`; the device-hash regex was confirmed against synthetic hashes
- all update / app-store / second-screen / voice endpoints resolve normally before **and** after enabling the list
- both TVs kept working normally post-change; telemetry endpoints were observed being blocked in the live query log (e.g. LG `rdx2.*` and Sony `ndmdhs.com` hosts)

2026-09-23, Samsung + the other brands (resolution-level, no device of those platforms on the test network yet):

- every blocked row resolves upstream before enabling (so the filter takes effect) and every KEEP row resolves
- zone-safety reviewed host-by-host against documented breakage reports (Perflyst issues #49/#82, oisd excludes, Control D / Pi-hole / Technitium threads)
- all 199 blocked entries + 130 `$important` exceptions parse cleanly in AdGuard syntax; no exception overlaps a blocked host (no accidental unblocking)
- device-level verification on real sets is **pending** for Samsung, Hisense, Vizio, Roku, Fire TV, Philips, Xiaomi, Panasonic — treat those sections as evidence-based, not device-verified

## Sources & credits

Built from community lists, platform recon and independent research:
Perflyst / Dandelion Sprout Smart-TV + AmazonFireTV blocklists · hkamran80/blocklists · HaGeZi `native.*` + pro + TIF · 1Hosts Pro · The Block List Project (smart-tv/tracking/ads) · ipanalytics device-group lists · samsapti/LG-webOS-Blocklist · TheShawnMiranda/LG-TV-Ad-Block · casenjo (Sony gist) · Level1Techs "LG TV Block Mini-How-to" · oisd excludes · UCL study [arXiv:2409.06203](https://arxiv.org/abs/2409.06203) · netify.ai · TP Vision "Smart TV Platform providers" · Samsung ACR support (ANS10010616) · Samsung Ads privacy notice (policy.samsungrs.com).

## License

MIT — see [LICENSE](LICENSE).
