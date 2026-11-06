# Brand + domain shortlist (location-neutral)
Checked 2026-10-19, ~11:15-11:25 AM ET. Nothing bought, nobody contacted.

Brief (from Ben): no town/county/state in the name; must work for a national network of city pages
(e.g. brand.com/silver-spring/) and ideally stretch to other trades later. Clearly plumbing-related, short,
easy to say on the phone, .com preferred, honest for a referral/lead service (not posing as a licensed plumber).

How verified:
- Availability: Verisign RDAP (404 = unregistered) AND Cloudflare Registrar `POST /accounts/{id}/registrar/domain-check`
  (authoritative registry check, read-only). Every domain below returned registrable=true, tier=standard.
- Price: from that same Cloudflare check: **.com $10.46/yr registration, $10.46/yr renewal** (.net $11.86/yr).
- Conflicts: web search for each name (US-wide). This is NOT a USPTO trademark search; run one at tmsearch.uspto.gov before buying.

## Ranked shortlist

| # | Name | Domain | Available? | Price (CF, verified) | Conflict notes | Why |
|---|------|--------|-----------|----------------------|----------------|-----|
| 1 | **Plumber Relay** | plumberrelay.com (also plumbersrelay.com free) | Yes (RDAP 404 + CF registrable) | $10.46/yr | No US plumbing business found. "Relay" is the name of an Australian AI receptionist product for plumbers (Leva, B2B, AU only). Hamilton Relay (telecom relay, unrelated). | Says exactly what it is (we relay your call to a local plumber), honest for a referral service, easy on the phone; pattern stretches to "Roofer Relay"/"HVAC Relay" as separate sites (roofrelay.com/hvacrelay.com are taken). |
| 2 | **Plumber Signal** | plumbersignal.com | Yes (RDAP 404 + CF) | $10.46/yr | No exact match. Search noise from "Plumber Signal Hill" (a CA referral site named after Signal Hill, CA) and "Signal Plumbing" (UK). | Cleanest on conflicts, distinctive, keyword "plumber" up front. Slightly less self-explanatory than Relay. |
| 3 | **Plumb Helpline** | plumbhelpline.com | Yes (RDAP 404 + CF) | $10.46/yr | No exact match. Crowded generic space ("plumbing helpline" used descriptively by referral sites like PlumbRelief, PlumbDispatch24); "Plumbhelp" is a UK firm. | Sounds like a helpline, which fits a call-routing service. "Plumb" can be misheard on the phone. |
| 4 | **Home Call Relay** | homecallrelay.com | Yes (RDAP 404 + CF) | $10.46/yr | No exact match. "HomeCall of Rockville, MD" is an LHC Group home-health agency (different industry, same county); "Housecall Pro" is a big home-services software brand, so mild confusion risk. | The one name that covers every trade (plumbing, roofing, HVAC) under one brand: homecallrelay.com/plumbing/silver-spring/. Less keyword-rich for "plumber". |
| 5 | **Plumber Dial** | plumberdial.com | Yes (RDAP 404 + CF) | $10.46/yr | Close to "Dial A Plumber", used by several small US plumbers incl. **Dial A Plumber LLC, Stevensville, MD**, plus Detroit MI, Corvallis OR; dialaplumber.au in Australia. | Very phone-friendly, but the MD near-match is a real risk. |
| 6 | **The Plumber Line** | theplumberline.com | Yes (RDAP 404 + CF) | $10.46/yr | homerepairdispatch.com (a national referral competitor) calls its number "the plumber line"; sounds like "Plumb Line", a common plumber name (e.g. Plumb Line Plumbing, Richmond VA; The Plumb Line LLC, NC). "The Plumbing Line Inc." is a licensed LA plumber. | Great on the phone but the most confusable. |
| 7 | **Clog Call** | clogcall.com | Yes (RDAP 404 + CF) | $10.46/yr | No exact match ("PlumbCall" is Australian; "Clog Pro" is Portland/Vancouver). | Catchy and memorable, but reads as drains-only, weak for water heaters/sewer and won't stretch to other trades. |

## Dropped after checks
- Taken domains: plumbcall, plumberline, plumbline, plumbhub, plumbmatch, plumbersnearby, callaplumber, plumberconnect, plumbfinder, plumbrelay, plumbsignal, plumbtrust, prorelay, homefixline, tradeline, etc. (all RDAP 200).
- Available but conflicting: Plumb Pronto (Pronto Plumbing in Central PA, Atlanta, San Diego, Denver), Plumb Compass (Compass Plumbing in Northern VA, FL, OR, WA, IL), Plumber Bridge (Bridge Plumbing UT/AZ), Plumber Direct Line (Direct Line Plumbing, AL), Plumber Connector (PlumbersConnect referral site), Ring Plumber (ringaplumber.com US referral + UK), The Plumbing Line (licensed LA plumber), Plumb Beacon (Beacon Plumbing is a large WA/OR company), MoCo-anything (MoCo Plumbing LLC, Germantown MD).

## Top pick
**Plumber Relay, plumberrelay.com ($10.46/yr at Cloudflare, verified).** It's honest about being a referral service,
has no US plumbing conflict found, is easy to say ("Plumber Relay dot com"), and works nationally with city pages
(/silver-spring/, /takoma-park/, later /arlington/). Consider also grabbing plumbersrelay.com ($10.46) so nobody
takes the plural. Runner-up: Plumber Signal. If Ben wants one umbrella brand for all trades, Home Call Relay.

## What switching involves
1. Buy the domain in Cloudflare Registrar (dashboard: Domain Registration > Register Domains). ~$10.46/yr; needs Ben's
   approval and his card on the Cloudflare account. WHOIS privacy is included.
2. Attach it to the Pages project `silverspring-plumbing-pros`: Pages > Custom domains > add `plumberrelay.com` and
   `www.plumberrelay.com` (DNS records auto-created since the zone is on Cloudflare). Keep the .pages.dev URL working
   and 301 it to the new domain (in _worker.js) so nothing breaks.
3. Rebuild: change the brand name everywhere in src/content.py / build.py (titles, H1s, footer disclosure, voicemail
   greeting in src/worker_template.js "Thanks for calling ..."), canonical URLs, Open Graph URLs, JSON-LD schema
   (name/url), sitemap.xml and robots.txt sitemap line, llms.txt. Restructure URLs for a network if desired
   (e.g. /silver-spring/ hub). Update Twilio VoiceUrl to the new domain (or keep pages.dev since it still resolves).
4. Search Console: add the new domain as a URL-prefix property (`https://plumberrelay.com/`); the existing
   google-site-verification meta tag is already on every page and will verify it, or use a Domain property via
   DNS TXT. Submit the new sitemap.xml, then use Change of Address from the old property if the 301s are in place.
5. Update outreach templates (outreach/) and the email signature to the new brand/URL before the next pitches.
