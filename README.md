# Sony + LG TV telemetry blocklist

Curated DNS blocklist for **Sony BRAVIA** and **LG webOS** smart TVs.
It blocks telemetry, usage/ACR (automatic content recognition) tracking, home-screen ads and recommendation beacons — **without breaking** updates, app stores, second-screen/remote, voice search or streaming apps.

Verified against real DNS traffic from a Sony BRAVIA and an LG webOS TV (see [Verification](#verification)).

## Usage

### AdGuard Home
1. *Filters* → *DNS blocklists* → *Add blocklist* → *Add a custom list*
2. Paste:
   ```
   https://raw.githubusercontent.com/Okazakee/sony-lg-tv-blocklist/main/blocklist.txt
   ```

### Pi-hole
*Group Management* → *Adlists* → add the same URL → then run `pihole -g`.

### Other DNS filters
Standard Adblock syntax (`||domain^`, `@@…$important` exceptions, one regex rule). Works with any engine that supports host-list/Adblock rules.

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

## What is *never* blocked

Protected by `$important` exceptions (this also protects them against other subscribed lists accidentally blocking them):

- Sony: `info.update.sony.net`, `www.sony.net`, `update/reg/service.biv.sony.tv`, `api/metadata.erabu.sony.tv`
- LG: `su.lge.com`, `su-ssl.lge.com`, `snu.lge.com`, `nsu.lge.com` (+ `-dev` variants)

Also intentionally left working: app stores (`lgappstv.com` base, `portal.store.sonyentertainmentnetwork.com`), second-screen/mobile app (`lgtvsdp.com` base), store thumbnails (`ngfts.lge.com` bare), voice search (`lgsmartweb.com`), `sony.com` / `lg.com`.

A commented *OPTIONAL* section at the bottom of `blocklist.txt` holds higher-tradeoff entries (ThinQ/IoT, `nextlgsdp.com`, bare `ngfts.lge.com`, …) — uncomment only if you accept the consequence listed there.

## Limitations

- Some TVs bootstrap their own encrypted DNS (DoH/DoT to `8.8.8.8` / `1.1.1.1`) and some services use hardcoded IPs — those bypass DNS filtering; handle at router/firewall level if needed.
- LG's OTA fallback IP `156.147.69.32:8080` is not DNS-blockable.

## Verification

2026-09-22, on a live AdGuard Home instance with real traffic from a Sony BRAVIA + an LG webOS TV:

- all blocked entries return `0.0.0.0`; the device-hash regex was confirmed against synthetic hashes
- all update / app-store / second-screen / voice endpoints resolve normally before **and** after enabling the list
- both TVs kept working normally post-change; telemetry endpoints were observed being blocked in the live query log (e.g. LG `rdx2.*` and Sony `ndmdhs.com` hosts)

## Sources & credits

Built from community lists, platform recon and independent research:
Perflyst / Dandelion Sprout Smart-TV blocklist · hkamran80/blocklists · samsapti/LG-webOS-Blocklist · TheShawnMiranda/LG-TV-Ad-Block · casenjo (Sony gist) · Level1Techs "LG TV Block Mini-How-to" · UCL study [arXiv:2409.06203](https://arxiv.org/abs/2409.06203) · netify.ai.

## License

MIT — see [LICENSE](LICENSE).
