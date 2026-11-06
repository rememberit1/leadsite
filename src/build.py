#!/usr/bin/env python3
"""Static site generator. Run: python3 src/build.py  -> writes ./public"""
import json, os, shutil, html, datetime, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import SITE, SERVICES, AREAS, GUIDES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public")
TODAY = datetime.date.today().isoformat()
B = SITE["base_url"]; P = SITE["phone_display"]; T = SITE["phone_tel"]
e = html.escape
import re as _re
H = "/plumbing/silver-spring"   # market hub: /<trade>/<market>/...
HUB_NAME = "Silver Spring Plumbing"
_PFX = _re.compile(r'(["\'(]|https://homecallrelay\.com)/(services|areas|guides)/')
def mp(x):
    """Map legacy site-relative paths (/services/, /areas/, /guides/) to the market hub."""
    return _PFX.sub(lambda m: m.group(1) + H + "/" + m.group(2) + "/", x)
def mpath(path):
    return H + path if _re.match(r"^/(services|areas|guides)/", path) else path

def biz_schema():
    return {"@context": "https://schema.org", "@type": "LocalBusiness", "@id": B + "/#business",
            "name": SITE["brand"], "url": B + "/", "telephone": T,
            "description": "Free homeowner referral network. Currently connecting homeowners in " + SITE["region"] + " and nearby Montgomery County with local plumbers.",
            "areaServed": [{"@type": "Place", "name": a["name"] + ", MD"} for a in AREAS],
            "openingHours": "Mo-Su 00:00-23:59"}

def faq_schema(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": B + u} for i, (n, u) in enumerate(items)]}

def call_btn(cls="btn"):
    return f'<a class="{cls}" href="tel:{T}" data-call>Call {P}</a>'

def form(service=""):
    opts = "".join(f'<option{" selected" if s["name"]==service else ""}>{e(s["name"])}</option>' for s in SERVICES)
    return f'''<form class="quote" method="post" action="/api/lead">
<h2>Request a call back</h2>
<label>Name<input name="name" required autocomplete="name"></label>
<label>Phone<input name="phone" type="tel" required autocomplete="tel"></label>
<label>ZIP code<input name="zip" inputmode="numeric" pattern="[0-9]{{5}}" required></label>
<label>What do you need?<select name="service">{opts}<option>Other</option></select></label>
<label>Details (optional)<textarea name="message" rows="3"></textarea></label>
<input type="text" name="company" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<input type="hidden" name="page" value="">
<div class="cf-turnstile" data-sitekey="0x4AAAAAAFgn444whBJJNPMd"></div>
<button type="submit">Send request</button>
<p class="small">Or call now: <a href="tel:{T}" data-call>{P}</a>. By submitting you agree to be contacted about your request.</p>
</form>'''

BEACON = f"<script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{\"token\": \"{SITE.get('cf_beacon_token','')}\"}}'></script>" if SITE.get('cf_beacon_token') else ''
NAV = ('<nav><a href="/">Home</a><a href="/plumbing/silver-spring/">Silver Spring</a><a href="/services/">Services</a><a href="/areas/">Areas</a>'
       '<a href="/guides/">Guides</a></nav>')

def page(path, title, desc, h1, main, schemas, crumb):
    path = mpath(path)
    crumb = [(n, mpath(u)) for n, u in crumb]
    if path.startswith(H + "/"):
        rest = [c for c in crumb if c[1] not in ("/", H + "/")]
        crumb = [("Home", "/"), (HUB_NAME, H + "/")] + rest
    brand = SITE["brand"]
    if brand not in title:
        title = title.replace(P, brand) if P in title else f"{title} | {brand}"
    disc = SITE["disclosure"] + (" " + SITE["disclosure_plumbing_md"] if path.startswith(H) or path == "/" else "")
    url = B + path
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>'
                   for s in [biz_schema(), crumbs(crumb)] + schemas)
    doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="google-site-verification" content="OzSxe7b4QJ18SqpLxO2e0uEKpxnOUQe1bHbIuiaRpb4" />
<meta name="google-site-verification" content="uzaPmgFGGa747XvhIbNub-2Tj_jj8KEpkSk1YMQib8c" />
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}"><meta property="og:type" content="website"><meta property="og:site_name" content="{e(SITE["brand"])}">
<meta name="robots" content="index,follow,max-snippet:-1">
<link rel="stylesheet" href="/styles.css">
{ld}
</head><body>
<header><div class="wrap"><a class="logo" href="/">{e(SITE["brand"])}</a>{NAV}{call_btn("btn sm")}</div></header>
<main class="wrap">
<p class="crumbs">{" › ".join(f'<a href="{u}">{e(n)}</a>' for n, u in crumb)}</p>
<h1>{e(h1)}</h1>
{main}
</main>
<footer><div class="wrap"><p><strong>{e(SITE["brand"])}</strong> · Free homeowner referral network · Now serving plumbing in {", ".join(a["name"] for a in AREAS)}, MD · <a href="tel:{T}" data-call>{P}</a></p>
<p class="small">{e(disc)}</p><p class="small">Last updated {TODAY}.</p></div></footer>
<a class="callbar" href="tel:{T}" data-call>📞 Call {P}</a>
<script src="/app.js" defer></script>
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
{BEACON}
</body></html>'''
    doc = mp(doc)
    d = os.path.join(OUT, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w") as f:
        f.write(doc)
    PAGES.append(path)

def quick(text):
    return f'<div class="quick"><strong>Quick answer:</strong> {e(text)}</div>'

def sections(body):
    out = []
    for h, items in body:
        out.append(f"<h2>{e(h)}</h2>")
        if len(items) == 1:
            out.append(f"<p>{items[0]}</p>")
        else:
            out.append("<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>")
    return "\n".join(out)

def faq_html(faq):
    return "<h2>Frequently asked questions</h2>" + "".join(
        f"<details><summary>{e(q)}</summary><p>{a}</p></details>" for q, a in faq)  # answers are trusted, may contain links

def links(title, items):
    return f'<h2>{e(title)}</h2><ul class="grid">' + "".join(f'<li><a href="{u}">{e(n)}</a></li>' for n, u in items) + "</ul>"

SVC_LINKS = [(s["name"], f'/services/{s["slug"]}/') for s in SERVICES]
AREA_LINKS = [(f'Plumber in {a["name"]}', f'/areas/{a["slug"]}/') for a in AREAS]
GUIDE_LINKS = [(g["h1"], f'/guides/{g["slug"]}/') for g in GUIDES]
PAGES = []

def build():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for f in ("styles.css", "app.js"):
        shutil.copy(os.path.join(ROOT, "src", f), OUT)

    # Home
    main = (f'<p class="lead">Plumbing problem in Silver Spring or nearby Montgomery County? Call <a href="tel:{T}" data-call>{P}</a> and leave a short message (name, ZIP, the problem), or send a request, and we\'ll connect you with a local WSSC-registered plumber.</p>'
            f'<p>{call_btn()}</p>' + form()
            + links("Plumbing services", SVC_LINKS) + links("Areas we cover", AREA_LINKS)
            + links("Homeowner guides", GUIDE_LINKS)
            + '<h2>Before you hire any plumber in Montgomery County</h2><ul>'
              '<li>Ask for their <strong>WSSC Water registration number</strong>. It\'s required for plumbing and sewer work in Montgomery and Prince George\'s counties.</li>'
              '<li>For underground water or sewer line work, confirm a <strong>registered master plumber</strong> will pull a WSSC permit.</li>'
              '<li>Get the price in writing before work starts, and ask for camera video on any sewer diagnosis.</li></ul>')
    page(H + "/", f'Silver Spring Plumber | Local Plumbing Help | {P}', "Need a plumber in Silver Spring, Takoma Park, Wheaton or Kensington, MD? Call " + P + " to be connected with a local WSSC-registered plumber. Free referral service.",
         "Plumber in Silver Spring, MD: Fast Help, Any Hour", main, [], [("Home", "/")])

    # Network home (location-neutral)
    net = (f'<p class="lead">{e(SITE["brand"])} is a free referral network that connects homeowners with independent local home-service providers. Call <a href="tel:{T}" data-call>{P}</a> or send a request and we\'ll connect you.</p>'
           f'<p>{call_btn()}</p>'
           + links("Where we operate", [("Plumbing in Silver Spring, MD", H + "/")] + AREA_LINKS)
           + links("Plumbing services (Silver Spring area)", SVC_LINKS)
           + links("Homeowner guides", GUIDE_LINKS)
           + '<h2>How it works</h2><ul><li>Tell us what\'s wrong, by phone or the form.</li>'
             '<li>We pass your request to an independent local provider who serves your area.</li>'
             '<li>The provider contacts you directly to quote and schedule. Our service is free to homeowners.</li></ul>'
           + form())
    page("/", f'{SITE["brand"]} | Free Referrals to Local Home Service Pros', "Home Call Relay connects homeowners with independent local home-service providers. Now serving plumbing in Silver Spring, Takoma Park, Wheaton and Kensington, MD.",
         f'{SITE["brand"]}: Get Connected With a Local Pro', net, [], [("Home", "/")])

    # Services index + pages
    page("/services/", "Plumbing Services in Silver Spring, MD", "Emergency plumbing, drain cleaning, water heaters, leak detection, sewer lines and more in Silver Spring, MD.",
         "Plumbing Services in Silver Spring, MD", links("Services", SVC_LINKS) + form(), [], [("Home", "/"), ("Services", "/services/")])
    for s in SERVICES:
        rel_g = [(g["h1"], f'/guides/{g["slug"]}/') for g in GUIDES if s["slug"] in g.get("related_services", [])]
        main = (quick(s["quick"]) + f"<p>{call_btn()}</p>" + sections(s["body"]) + form(s["name"]) + faq_html(s["faq"])
                + (links("Related guides", rel_g) if rel_g else "")
                + links(f'{s["name"]} by area', [(f'{s["name"]} in {a["name"]}', f'/areas/{a["slug"]}/') for a in AREAS]))
        svc = {"@context": "https://schema.org", "@type": "Service", "serviceType": s["name"],
               "provider": {"@id": B + "/#business"}, "areaServed": [a["name"] + ", MD" for a in AREAS],
               "url": B + f'/services/{s["slug"]}/'}
        page(f'/services/{s["slug"]}/', s["title"], s["desc"], s["h1"], main, [svc, faq_schema(s["faq"])],
             [("Home", "/"), ("Services", "/services/"), (s["name"], f'/services/{s["slug"]}/')])

    # Areas
    page("/areas/", "Plumbing Service Areas | Silver Spring & Montgomery County, MD", "Areas we cover: Silver Spring, Takoma Park, Wheaton, Kensington, Four Corners, Forest Glen, White Oak and Aspen Hill, MD.",
         "Areas We Cover", links("Service areas", AREA_LINKS), [], [("Home", "/"), ("Areas", "/areas/")])
    for a in AREAS:
        n = a["name"]
        faq = [(f"Do plumbers in {n} need to be WSSC-registered?", f"Yes. {n} is in WSSC Water's service area, and plumbers and sewer drain cleaners must be WSSC Water-registered. Ask for the registration number." if a["slug"] != "takoma-park" else "On the Maryland side, yes. Plumbers must be WSSC Water-registered. Addresses in Takoma, DC fall under DC Water and DC licensing."),
               (f"Who do I call for a sewer backup in {n}?", "Call WSSC Water's 24-hour emergency line (301-206-4002) and a registered plumber. The plumber determines whether the blockage is on your side or WSSC's side."),
               (f"What should I do first in a plumbing emergency in {n}?", f'Shut off the main water valve for a burst pipe or major leak, and stop running water if sewage is backing up. Then call a plumber. Our <a href="{mp("/services/emergency-plumber/")}">emergency plumbing checklist</a> covers the first 10 minutes.'),
               (f"Do I need a permit for a water heater or sewer line repair in {n}?", f'Replacing a gas water heater ($180 WSSC Short Form permit) or repairing an underground water or sewer line requires a WSSC Water permit and inspection. Like-for-like electric water heater swaps are usually exempt. See our <a href="{mp("/guides/water-heater-permit-wssc-montgomery-county/")}">water heater permit guide</a> and <a href="{mp("/services/sewer-line-repair/")}">sewer line repair guide</a>.'),
               (f"What ZIP codes does this cover?", f"{n}: {a['zips']}.")]
        main = (f'<p class="lead">{e(a["intro"])}</p><p>{call_btn()}</p>'
                + f"<h2>Plumbing issues common in {e(n)} homes</h2><ul>" + "".join(f"<li>{e(x)}</li>" for x in a["local"]) + "</ul>"
                + f'<p><strong>Neighborhoods:</strong> {e(a["hoods"])}. <strong>ZIP codes:</strong> {e(a["zips"])}.</p>'
                + links(f"Plumbing services in {n}", [(f'{s["name"]} in {n}', f'/services/{s["slug"]}/') for s in SERVICES])
                + form() + faq_html(faq) + links("Homeowner guides", GUIDE_LINKS)
                + links("Nearby areas", [(x["name"], f'/areas/{x["slug"]}/') for x in AREAS if x is not a]))
        page(f'/areas/{a["slug"]}/', f"Plumber in {n}, MD | Local Plumbing Help | {P}",
             f"Need a plumber in {n}, MD ({a['zips'].split(',')[0]})? Call {P}. Local plumbing guide for {n} homes: sewer laterals, water heaters, leaks and more.",
             f"Plumber in {n}, MD", main, [faq_schema(faq)],
             [("Home", "/"), ("Areas", "/areas/"), (n, f'/areas/{a["slug"]}/')])

    # Guides
    page("/guides/", "Plumbing Guides for Silver Spring Homeowners", "Answers to common plumbing questions in Silver Spring and Montgomery County, MD.",
         "Homeowner Plumbing Guides", links("Guides", GUIDE_LINKS), [], [("Home", "/"), ("Guides", "/guides/")])
    for g in GUIDES:
        rel = [(s["name"], f'/services/{s["slug"]}/') for s in SERVICES if s["slug"] in g.get("related_services", [])]
        src = "<h2>Sources</h2><ul>" + "".join(f'<li><a href="{u}" rel="nofollow noopener">{e(n)}</a></li>' for n, u in g["sources"]) + "</ul>"
        main = (f'<p class="small">Question: <em>{e(g["question"])}</em> · Published {g["date"]} · Updated {TODAY}</p>'
                + quick(g["quick"]) + f"<p>{call_btn()}</p>" + sections(g["body"]) + form() + faq_html(g["faq"]) + src
                + links("Related services", rel) + links("Areas", AREA_LINKS))
        art = {"@context": "https://schema.org", "@type": "Article", "headline": g["h1"], "datePublished": g["date"],
               "dateModified": TODAY, "author": {"@type": "Organization", "name": SITE["brand"]},
               "publisher": {"@id": B + "/#business"}, "mainEntityOfPage": B + f'/guides/{g["slug"]}/'}
        schemas = [art, faq_schema(g["faq"])]
        if g.get("howto"):
            schemas.append({"@context": "https://schema.org", "@type": "HowTo", "name": g["h1"],
                            "step": [{"@type": "HowToStep", "position": i + 1, "text": x} for i, x in enumerate(g["howto"])]})
        page(f'/guides/{g["slug"]}/', g["title"], g["desc"], g["h1"], main, schemas,
             [("Home", "/"), ("Guides", "/guides/"), (g["h1"][:40] + "…", f'/guides/{g["slug"]}/')])

    page("/thank-you/", "Thanks, we got your request", "Request received.", "Thanks, we got your request",
         f'<p>We\'ll call you back shortly. If it\'s an emergency, call now: {call_btn()}</p>', [], [("Home", "/")])
    PAGES.remove("/thank-you/")

    # sitemap / robots / llms.txt / headers / 404
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"<url><loc>{B}{p}</loc><lastmod>{TODAY}</lastmod></url>" for p in sorted(PAGES, key=lambda x: (x != "/", x))]
    sm.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(sm))
    open(os.path.join(OUT, "robots.txt"), "w").write(
        "User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /thank-you/\n\n"
        "# AI search crawlers explicitly welcome\nUser-agent: OAI-SearchBot\nAllow: /\nUser-agent: GPTBot\nAllow: /\n"
        "User-agent: ChatGPT-User\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\n\n"
        f"Sitemap: {B}/sitemap.xml\n")
    llms = [f"# {SITE['brand']}", f"> Free homeowner referral network connecting homeowners with independent local home-service providers. Currently serving plumbing in Silver Spring, MD and nearby Montgomery County ({B}{H}/). Phone {P}.", "", "## Services (Silver Spring, MD plumbing)"]
    llms += [f"- [{s['name']}]({B}/services/{s['slug']}/): {s['quick']}" for s in SERVICES]
    llms += ["", "## Areas"] + [f"- [{a['name']}, MD]({B}/areas/{a['slug']}/)" for a in AREAS]
    llms += ["", "## Guides"] + [f"- [{g['h1']}]({B}/guides/{g['slug']}/): {g['quick']}" for g in GUIDES]
    open(os.path.join(OUT, "llms.txt"), "w").write(mp("\n".join(llms) + "\n"))
    open(os.path.join(OUT, "_headers"), "w").write(
        "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n"
        "/styles.css\n  Cache-Control: public, max-age=86400\n/app.js\n  Cache-Control: public, max-age=86400\n")
    open(os.path.join(OUT, "404.html"), "w").write(
        f'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="google-site-verification" content="OzSxe7b4QJ18SqpLxO2e0uEKpxnOUQe1bHbIuiaRpb4" /><meta name="google-site-verification" content="uzaPmgFGGa747XvhIbNub-2Tj_jj8KEpkSk1YMQib8c" /><meta name="robots" content="noindex"><title>Page not found | {SITE["brand"]}</title><link rel="stylesheet" href="/styles.css"><main class="wrap"><p><strong>{e(SITE["brand"])}</strong></p><h1>Page not found</h1><p><a href="/">Home</a> · <a href="/plumbing/silver-spring/">Silver Spring plumbing</a> · <a href="tel:{T}" data-call>Call {P}</a></p></main><script src="/app.js" defer></script>')
    print(f"Built {len(PAGES)} indexable pages -> {OUT}")

if __name__ == "__main__":
    build()
