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
