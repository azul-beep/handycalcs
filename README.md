# Handy Calcs

Free bilingual (EN/ES) calculators site. Static, no build tools needed except Python 3.

- Edit IDs (GA4, Meta Pixel, AdSense, Search Console) and affiliate links at the top of `build.py`.
- `python3 build.py` regenerates `site/`.
- Deploy: Cloudflare Pages, build command empty (or `python3 build.py`), output directory `site`.
- Calculator PRs only change `src/` and `build.py` (not `site/`), so they never conflict with the daily publishing bot. When they are merged, `.github/workflows/rearmar-web.yml` rebuilds `site/` and commits it; the daily IndexNow job then pings the new URLs.

## Printable calendars (calendarios/)

- `calendarios/calendarios-AAAA/` is made by `calendarios/regenerar.py`; `build.py` copies it into `site/`, fills GA4/AdSense/privacy and adds it to the menu, footer and sitemap.
- Drip rule (Azu): pins go out 2 or 3 a day. `rss-completo.xml` is the queue, `tools/goteo.py` writes `rss.xml` with what is already out; start days in `calendarios/goteo.json`.
- Pinterest reads the stable feed `https://gethandycalcs.pages.dev/calendarios-rss.xml` (always the newest year).
- GitHub Actions: `imprimibles-diario.yml` (daily at 8 AM Utah: printables + drip, file imprimibles-diario.yml) and `calendarios.yml` (every Oct 1, next year's pack). They need this folder to be a GitHub repo connected to Cloudflare Pages (build command empty, output `site`).

## Free tools guide (herramientas/) and printables (imprimibles/)

- `herramientas/generar.py` builds `/herramientas-gratis/` (Spanish guide, 11 pages) with the drip from `herramientas/goteo-inicio.txt`; GA4/AdSense come from CONFIG through its `--ga4/--pixel/--adsense` flags. Monthly link check: `herramientas-mensual.yml`.
- `imprimibles/generar.py diario` makes the daily puzzle and the bilingual worksheets (needs cairosvg, pypdf, pillow + libcairo2). GA4/AdSense are read from CONFIG in `imprimibles/motor/comun.py`. `build.py` copies them to `/imprimibles/`. `imprimibles/colorear/` is a separate site and is not published here.
- Everything daily runs in `.github/workflows/imprimibles-diario.yml` (no Claude, free).

## Pinterest-only pin feeds (pines/)

- `pines/<name>/` holds `pines-en/`, `pines-es/` and `rss-completo.xml` (the queue). Start days are in `pines/goteo.json` (navidad 2026-11-18, agenda-2027 2026-11-20). `build.py` publishes `/pines/<name>/rss.xml` with the drip; add those feeds to Pinterest auto-publish.

## Free online tools (/tools/ and /es/herramientas/)

- 25 tools (QR codes, image compress/resize/convert, word counter, case converter, name wheel, team maker, giveaway picker, password, timer, unit and time zone converters, color palettes, name generator, pet age, invoice PDF…), English and Spanish. Everything runs in the visitor's browser: nothing is uploaded.
- Definitions and texts: `src/tools.py`. Widgets: `src/tools.js` + `src/tools.css`. QR library: `src/vendor/qrcode.js` (Kazuhiko Arase, MIT).
- Drip (Azu's rule): tools 1 and 2 go live on `TOOLS_START` in `build.py` (2026-11-16), then one more tool per day (EN + ES) with the daily workflow. To add tools, append entries with the next `n`.
- Monitor: `.github/workflows/herramientas-salud.yml` runs `tools/revisar_herramientas.py` every day and opens a GitHub issue (email) if a page that should be live is missing or broken.

## Pinterest pins for every calculator and guide (pines/calculadoras/)

- `tools/pines_calculadoras.py` (called by `build.py`) gives every calculator 4 pins (EN/ES x design A "calculator card" and B "question + answer") and every guide 1 pin. Images (1000x1500) are drawn with Pillow into `site/pines/calculadoras/img/`.
- Queue with a fixed day per pin: `pines/calculadoras/cola.json` (2 pins a day, never on a past day). New calculators in `src/calcs.py` and new guides in `src/articles/` join the queue by themselves; a guide pin never goes out before the guide.
- Feeds for Pinterest auto-publish (each feed shows only the newest 6 pins, so connecting late never dumps the backlog): `/pines/calculadoras/rss-en.xml` (board "Free Calculators"), `/pines/calculadoras/rss-es.xml` (board "Calculadoras gratis"), `/pines/calculadoras/rss.xml` (both).
- Links carry `utm_source=pinterest&utm_campaign=pin-calc-a|pin-calc-b|pin-guide` for GA4. Preview all designs: `python3 tools/pines_calculadoras.py /tmp/preview`.
