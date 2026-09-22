# Sources & credits

Everything this list was built from — community blocklists, investigations,
vendor documents, breakage reports and the tooling used for enumeration. The
per-domain evidence (which source named which host) lives in the comments of
[`blocklist.txt`](blocklist.txt) itself.

## Community blocklists

- Perflyst / Dandelion Sprout — Smart-TV + AmazonFireTV lists —
  <https://github.com/Perflyst/PiHoleBlocklist>
- hkamran80 — `smart-tv.txt` —
  <https://github.com/hkamran80/blocklists/blob/main/smart-tv.txt> ·
  gist “Pi-hole Blocklist for Smart TVs” —
  <https://gist.github.com/hkamran80/779019103fcd306979411d44c8d38459>
- HaGeZi — DNS blocklists (`native.samsung`, `native.xiaomi`, `native.amazon`,
  pro, TIF) — <https://github.com/hagezi/dns-blocklists>
- 1Hosts Pro — <https://github.com/badmojr/1Hosts>
- The Block List Project — `smart-tv.txt` —
  <https://blocklistproject.github.io/Lists/smart-tv.txt>
- ipanalytics — per-brand clean-TV lists —
  <https://github.com/ipanalytics/Hisense-VIDAA-DNS-Clean-TV-Blocklist>
- samsapti — LG webOS blocklist —
  <https://github.com/samsapti/LG-webOS-Blocklist>
- TheShawnMiranda — LG TV Ad Block —
  <https://github.com/TheShawnMiranda/LG-TV-Ad-Block>
- mboutolleau — block-samsung-tv-telemetry —
  <https://github.com/mboutolleau/block-samsung-tv-telemetry>
- nextdns — native-tracking-domains —
  <https://github.com/nextdns/native-tracking-domains>
- dgomesbr — fightback-consumer-tv (Vizio) —
  <https://github.com/dgomesbr/fightback-consumer-tv>
- Alice6006 — Samsung TV blocklist —
  <https://github.com/Alice6006/adguard_blocklists/blob/main/Samsung-TV_Blocklist.txt>
- jrwren — hosts/vizio —
  <https://github.com/jrwren/hosts/blob/master/vizio>
- SafeNetIoT — ACR —
  <https://github.com/SafeNetIoT/ACR>
- oisd — <https://oisd.nl> · excludes — <https://oisd.nl/excludes.php>
- IPFire DBL — `smart-tv` — <https://www.ipfire.org/dbl/lists/smart-tv>
- AdGuard HostlistsRegistry (`filter_7` = Dandelion Sprout Smart-TV) —
  <https://adguardteam.github.io/HostlistsRegistry/assets/filter_7.txt>
- Gists: casenjo (Sony) —
  <https://gist.github.com/casenjo/586c7b76dd6f7512125fb4e2fb853aae> ·
  ozankiratli (Roku) —
  <https://gist.github.com/ozankiratli/801ba17705e7f2a904d2e443af5a64f8> ·
  Luro02 —
  <https://gist.github.com/Luro02/02254456419c943cda7cb2bac85503b9> ·
  edmon1024 —
  <https://gist.github.com/edmon1024/9995f04f2bb33b72f7d2cb74c4352732> ·
  sidward35 —
  <https://gist.github.com/sidward35/cea28bedd0ec0b1bceec8c2b22c163c4>

## Investigations & research

- UCL — measuring ACR in smart TVs (arXiv:2409.06203) —
  <https://arxiv.org/abs/2409.06203>
- THectic-NL/Blocklists — LG ACR enumeration, PR #6 —
  <https://github.com/THectic-NL/Blocklists/pull/6>
- Ars Technica — LG TVs tracking user activity even when offline (Sept 2026) —
  <https://arstechnica.com/gadgets/2026/09/lg-tv-shown-capable-of-tracking-user-activity-even-when-offline>
- chard.org — selectively blocking Samsung TVs —
  <https://rainbow.chard.org/2017/03/08/selectively-blocking-samsung-tvs-network-access>
- vnutz — idle network activity of a Samsung TV —
  <https://www.vnutz.com/articles/idle_network_activity_of_a_samsung_tv>
- labzilla — forcing DNS through Pi-hole (Tizen DoH) —
  <https://labzilla.io/blog/force-dns-pihole>
- nstoler — stop your Roku from tracking you —
  <https://blog.nstoler.com/2020/09/05/stop-your-roku-from-tracking-you>
- jasonpearce — disable Roku home-screen ads —
  <https://jasonpearce.com/2020/09/16/how-to-disable-ads-on-the-roku-home-screen>
- edwardangert — Pi-hole block/allow lists (Fire TV) —
  <https://edwardangert.com/docs/pi-hole/block-allow-lists>
- XDA — smart devices sneaking around Pi-hole (DoH bypass) —
  <https://www.xda-developers.com/some-smart-devices-sneaking-around-pi-hole-blocking-them-was-easier>
- modemguides — how to stop smart TV tracking (ACR guide) —
  <https://www.modemguides.com/blogs/modemguides-blog/how-to-stop-smart-tv-tracking-acr-guide>
- privacygear — smart TV privacy / ACR —
  <https://privacygear.nl/en/guides/smart-tv-privacy-acr-disable>
- Level1Techs — LG TV block mini-how-to —
  <https://forum.level1techs.com/t/lg-tv-block-mini-how-to/255178>

## Vendor documents

- Samsung — what is ACR (ANS10010616) —
  <https://www.samsung.com/us/support/answer/ANS10010616>
- Samsung Ads privacy notice — <https://policy.samsungrs.com>
- TP Vision — Smart TV platform providers —
  <https://www.tpvision.com/policy/Smart_TV_Platformproviders.pdf> ·
  suppliers — <https://www.tpvision.com/policy/smarttv_suppliers.pdf>
- Roku — ACR service policy —
  <https://docs.roku.com/published/acrservicepolicy/en/CA>
- Titan OS — ads — <https://www.titanos.tv/ads>
- VIDAA — Data Act notice — <https://www.vidaa.com/data-act-notice>
- Vizio/Inscape — <https://platformplus.vizio.com/inscape> ·
  FTC settlement (2017) —
  <https://www.ftc.gov/news-events/news/press-releases/2017/02/vizio-pay-22-million-ftc-state-new-jersey-settle-charges-it-collected-viewing-histories-11-million>
- Xumo — Hisense Channels press release —
  <https://www.xumo.com/press/introducing-hisense-channels-a-new-streaming-service-for-hisense-smart-t-vs-powered-by-xumo-enterprise>
- Amazon — device metrics help page —
  <https://www.amazon.com/gp/help/customer/display.html?nodeId=GPFTD7F3EVCLUD3C>
- Xiaomi — Mi TV support article —
  <https://www.mi.com/global/support/article/KA-124771>

## Breakage & troubleshooting reports

- Pi-hole discourse — Samsung TV apps won't open with Pi-hole on —
  <https://discourse.pi-hole.net/t/samsung-tv-apps-wont-open-with-pihole-on/29621>
- r/pihole — 10,000 blocked requests in 10 minutes (Samsung TV) —
  <https://www.reddit.com/r/pihole/comments/dy5ge5/10000_blocked_requests_in_10_minutes_samsung_tv>
- Perflyst issues — #39 <https://github.com/Perflyst/PiHoleBlocklist/issues/39> ·
  #49 <https://github.com/Perflyst/PiHoleBlocklist/issues/49> ·
  #82 <https://github.com/Perflyst/PiHoleBlocklist/issues/82> ·
  #98 <https://github.com/Perflyst/PiHoleBlocklist/issues/98> ·
  #106 <https://github.com/Perflyst/PiHoleBlocklist/issues/106>
- HaGeZi issues —
  #5839 <https://github.com/hagezi/dns-blocklists/issues/5839> ·
  #11466 <https://github.com/hagezi/dns-blocklists/issues/11466>
- Technitium DNS server — issue #1781 —
  <https://github.com/TechnitiumSoftware/DnsServer/issues/1781>
- anudeepND/whitelist — issue #115 —
  <https://github.com/anudeepND/whitelist/issues/115>
- lightswitch05/hosts — issue #230 —
  <https://github.com/lightswitch05/hosts/issues/230>
- GoodbyeAds — issue #200 —
  <https://github.com/jerryn70/GoodbyeAds/issues/200>
- IPFire community — Amazon Prime Video —
  <https://community.ipfire.org/t/amazon-prime-video/15867>
- Control D discussion — Samsung store blocking —
  <https://docs.controld.com/discuss/6731ca54c20e630074db7831>
- r/nextdns — app store on Samsung TV —
  <https://www.reddit.com/r/nextdns/comments/13kpfsm/nextdns_blocking_app_store_on_samsung_tv_running>
- r/Adblock — Titan OS —
  <https://www.reddit.com/r/Adblock/comments/1hx3cea/titanos_adblock>

## Tooling used for enumeration

- crt.sh — certificate transparency search — <https://crt.sh>
- Cert Spotter API — <https://api.certspotter.com>
- HackerTarget host search — <https://hackertarget.com>
- netify.ai — per-domain hostname intelligence — <https://www.netify.ai>
