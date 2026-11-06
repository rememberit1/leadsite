# Home Call Relay (leadsite)

## Overview

Local SEO / lead-gen website for **Home Call Relay**, a free homeowner referral network. The live apex is **https://homecallrelay.com**. This repo is configured in `wrangler.toml` as Cloudflare Pages project `silverspring-plumbing-pros`.

## Purpose

Help homeowners in Silver Spring and nearby Montgomery County, MD find plumbing help, while capturing form leads and call-button clicks for the referral business. Content is organized under a plumbing market hub.

## Features / pages

Generated into `public/`:

- `/` — brand home (“Get Connected With a Local Pro”)
- `/plumbing/silver-spring/` — market hub
- `/plumbing/silver-spring/services/` — service index plus pages (emergency plumber, drain cleaning, water heater, leak detection, sewer line, sump pump, toilet/faucet, …)
- `/plumbing/silver-spring/areas/` — area pages (Silver Spring, Takoma Park, Wheaton, Kensington, Four Corners, White Oak, Aspen Hill, Forest Glen, …)
- `/plumbing/silver-spring/guides/` — homeowner guides (WSSC high bill, water-heater permits, sewer backup who-pays, …)
- `/thank-you/` — form confirmation
- `404.html`, `robots.txt`, `sitemap.xml`, `llms.txt`

Cloudflare Pages Functions under `functions/api/`:

- `lead.js` — form lead intake
- `call-click.js` — call-button click tracking
- `stats.js` — lightweight stats helper

## Tech stack

- Python static site generator (`src/build.py` + `src/content.py`)
- Plain HTML/CSS/JS in `public/`
- Cloudflare Pages + Pages Functions + KV binding `LEADS` (see `wrangler.toml`)
- LocalBusiness / FAQ JSON-LD for SEO

## Run / deploy

```bash
python3 src/build.py          # writes ./public
npx wrangler pages deploy public
# or: npx wrangler pages dev public
```

Set Pages secrets / env as needed for lead and voice handlers (do not commit secrets). Phone numbers and third-party IDs belong in env or your host console, not in git.

## Notes

This public copy omits internal ops notes and prospect lists. Branding notes live in `branding.md`.
