# -*- coding: utf-8 -*-
"""Pinterest pins for every calculator and guide of Handy Calcs, in a drip. Free and without Claude.

build.py calls build(...) every time it runs (daily workflow at 8 AM Utah + after calculator changes):

1. Queue (pines/calculadoras/cola.json): every calculator gets 4 pins (EN/ES x design A/B) and every guide 1 pin.
   Anything new (a calculator added to src/calcs.py, a guide added to src/articles/) enters the queue by itself
   and gets a fixed day. At most POR_DIA pins per day, never on a past day, so nothing ever goes out all at once
   (Azu's rule: 2 or 3 a day). A guide pin never goes out before the guide is live.
2. Images (1000x1500 JPG) are drawn with Pillow into site/pines/calculadoras/img/ for the pins already out.
3. Feeds for Pinterest auto-publish (each one goes to its own board):
     /pines/calculadoras/rss-en.xml  -> board "Free Calculators" (English pins + guides)
     /pines/calculadoras/rss-es.xml  -> board "Calculadoras gratis" (Spanish pins)
     /pines/calculadoras/rss.xml     -> both (use it only if you want a single board)
   Each feed shows only the last VENTANA pins, so connecting a feed late never dumps the whole backlog at once.
Links carry utm_source=pinterest so GA4 shows the visits.
"""
import datetime as dt, json, os, textwrap
from email.utils import format_datetime
from xml.sax.saxutils import escape

POR_DIA = 2          # pins per day in this feed (both languages together)
VENTANA = 6          # pins shown in each feed (the newest ones)
W, H = 1000, 1500

COLORS = {           # (dark, light, accent) per category, Handy Calcs teal family
    "restaurant": ("#9a3412", "#fff7ed", "#fb923c"),
    "kitchen":    ("#854d0e", "#fefce8", "#facc15"),
    "work":       ("#1e3a8a", "#eff6ff", "#60a5fa"),
    "money":      ("#115e59", "#ecfdf5", "#34d399"),
    "everyday":   ("#5b21b6", "#f5f3ff", "#a78bfa"),
    "health":     ("#9f1239", "#fff1f2", "#fb7185"),
    "school":     ("#0f766e", "#f0fdfa", "#2dd4bf"),
    "guide":      ("#1c2321", "#f7f7f4", "#fb923c"),
}

TXT = {
    "en": dict(free="FREE CALCULATOR", calc="Calculate", try_="Try the free %s", guide="FREE GUIDE",
               read="Read the guide + free calculator", foot="No sign-up · Private · Free", today="Today"),
    "es": dict(free="CALCULADORA GRATIS", calc="Calcular", try_="Prueba gratis: %s", guide="GUÍA GRATIS",
               read="Lee la guía + calculadora gratis", foot="Sin registro · Privado · Gratis", today="Hoy"),
}

# ------------------------------------------------------------------ fonts
AQUI = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(AQUI)
_FONTS = {
    "bold": ["/usr/share/fonts/opentype/inter/Inter-Bold.otf", os.path.join(ROOT, "herramientas", "fonts", "Carlito-Bold.ttf")],
    "black": ["/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf", "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
              os.path.join(ROOT, "herramientas", "fonts", "Carlito-Bold.ttf")],
    "reg": ["/usr/share/fonts/opentype/inter/Inter-Regular.otf", os.path.join(ROOT, "herramientas", "fonts", "Carlito-Regular.ttf")],
    "semi": ["/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
             os.path.join(ROOT, "herramientas", "fonts", "Carlito-Bold.ttf")],
}

def font(kind, size):
    from PIL import ImageFont
    for p in _FONTS[kind]:
        if os.path.exists(p): return ImageFont.truetype(p, size)
    return ImageFont.load_default()

# ------------------------------------------------------------------ queue
def candidates(calcs, all_articles):
    """(item_id, min_date) in priority order: guides first (they wait for their live day), then design A, then B."""
    out = [("guide-%s" % a["slug"], a["live"]) for a in all_articles]
    for v in ("a", "b"):
        for c in calcs:
            for lang in ("en", "es"):
                out.append(("calc-%s-%s-%s" % (c["id"], lang, v), None))
    return out

def update_queue(path, calcs, all_articles, today):
    data = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    inicio = dt.date.fromisoformat(data.get("inicio", "2026-11-17"))
    items = data.get("items", [])
    known = {i["id"] for i in items}
    per_day = {}
    for i in items: per_day[i["fecha"]] = per_day.get(i["fecha"], 0) + 1
    added = 0
    for iid, min_date in candidates(calcs, all_articles):
        if iid in known: continue
        d = max(inicio, today, min_date or inicio)
        while per_day.get(d.isoformat(), 0) >= POR_DIA: d += dt.timedelta(days=1)
        items.append({"id": iid, "fecha": d.isoformat()}); known.add(iid)
        per_day[d.isoformat()] = per_day.get(d.isoformat(), 0) + 1; added += 1
    items.sort(key=lambda i: (i["fecha"], i["id"].startswith("calc"), i["id"]))
    data = {"_nota": "Cola de pines de Handy Calcs. La arma tools/pines_calculadoras.py; no hace falta editarla a mano.",
            "inicio": inicio.isoformat(), "por_dia": POR_DIA, "items": items}
    if added or not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=1); f.write("\n")
    return items

# ------------------------------------------------------------------ drawing helpers
def wrap(d, text, fnt, width, max_lines):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines[-1] and d.textlength(lines[-1] + "…", font=fnt) > width: lines[-1] = lines[-1].rsplit(" ", 1)[0]
        lines[-1] = lines[-1].rstrip(",.;:") + "…"
    return lines

def fit_headline(d, text, width, max_lines, start=118, low=60):
    s = start
    while s > low:
        f = font("black", s)
        ls = wrap(d, text, f, width, 99)
        if len(ls) <= max_lines and all(d.textlength(l, font=f) <= width for l in ls): return f, ls
        s -= 4
    f = font("black", low)
    return f, wrap(d, text, f, width, max_lines)

def chip(d, x, y, text, bg, fg, size=30):
    f = font("bold", size)
    w = d.textlength(text, font=f)
    d.rounded_rectangle([x, y, x + w + 48, y + size + 30], radius=(size + 30) // 2, fill=bg)
    d.text((x + 24, y + 15), text, font=f, fill=fg)
    return y + size + 30

def footer(d, dark, light, accent, lang, site_host):
    d.rectangle([0, H - 170, W, H], fill=dark)
    # logo mark like the site
    d.rounded_rectangle([70, H - 128, 140, H - 58], radius=16, fill=accent)
    d.text((105, H - 93), "H", font=font("black", 44), fill=dark, anchor="mm")
    d.text((165, H - 98), "Handy Calcs", font=font("black", 44), fill=light, anchor="ls")
    d.text((165, H - 56), site_host, font=font("reg", 28), fill=light, anchor="ls")
    d.text((W - 70, H - 85), TXT[lang]["foot"], font=font("semi", 26), fill=accent, anchor="rm")

def input_value(i, lang):
    k = i["kind"]
    if k == "num":
        v = i["default"]; v = ("{:,}".format(v) if isinstance(v, (int, float)) and abs(v) >= 1000 else str(v))
        u = i.get("unit", "")
        if u == "$": return "$" + v
        return (v + u) if u == "%" else (v + " " + u if u else v)
    if k == "select":
        for o in i["options"]:
            if o[0] == i["default"]: return o[1] if lang == "en" else o[2]
        return ""
    if k == "date": return TXT[lang]["today"] if i["default"] == "today" else i["default"]
    if k == "timerow": return "%s – %s" % (i["default"][0], i["default"][1])
    if k == "text": return str(i["default"])
    return None

def draw_calc_a(c, lang, cats, site_host):
    from PIL import Image, ImageDraw
    dark, light, accent = COLORS.get(c["cat"], COLORS["money"])
    t = c[lang]; im = Image.new("RGB", (W, H), light); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 20], fill=dark)
    y = chip(d, 70, 80, TXT[lang]["free"], dark, light) + 40
    f, ls = fit_headline(d, t["h1"], W - 140, 3, start=136)
    for l in ls: d.text((70, y), l, font=f, fill=dark); y += int(f.size * 1.12)
    y += 20
    fs = font("reg", 42)
    for l in wrap(d, t["intro"], fs, W - 140, 3): d.text((70, y), l, font=fs, fill="#3d4744"); y += 52
    y += 40
    rows = [(i[lang], input_value(i, lang)) for i in c["inputs"] if input_value(i, lang) not in (None, "", "0")][:3]
    while rows and 70 + len(rows) * 128 + 120 > H - 210 - y: rows.pop()
    card_h = 70 + len(rows) * 128 + 120
    card_top = max(y, y + (H - 210 - card_h - y) // 2)
    d.rounded_rectangle([70, card_top, W - 70, card_top + card_h], radius=28, fill="#ffffff", outline="#e3e6e1", width=3)
    yy = card_top + 50
    fl, fv = font("semi", 30), font("bold", 38)
    for lab, val in rows:
        lab = wrap(d, lab, fl, W - 260, 1)[0]
        d.text((115, yy), lab, font=fl, fill="#5b6763")
        d.rounded_rectangle([115, yy + 42, W - 115, yy + 108], radius=14, outline="#cfd5d0", width=3, fill="#ffffff")
        d.text((140, yy + 75), wrap(d, val, fv, W - 290, 1)[0], font=fv, fill="#1c2321", anchor="lm")
        yy += 128
    d.rounded_rectangle([115, yy + 6, W - 115, yy + 86], radius=16, fill=dark)
    d.text((W // 2, yy + 46), TXT[lang]["calc"] + "  →", font=font("black", 40), fill=light, anchor="mm")
    footer(d, dark, light, accent, lang, site_host)
    return im

def draw_calc_b(c, lang, cats, site_host):
    from PIL import Image, ImageDraw
    dark, light, accent = COLORS.get(c["cat"], COLORS["money"])
    t = c[lang]; q, a = t["faq"][0]
    im = Image.new("RGB", (W, H), dark); d = ImageDraw.Draw(im)
    cat = cats.get(c["cat"], ("", ""))[0 if lang == "en" else 1].upper()
    y = chip(d, 70, 90, cat, accent, dark) + 60
    f, ls = fit_headline(d, q, W - 140, 5, start=104, low=56)
    fa = font("reg", 40); al = wrap(d, a, fa, W - 140, 8)
    block = len(ls) * int(f.size * 1.14) + 90 + len(al) * 56
    y += max(0, (H - 370 - y - block) // 3)   # short texts sit a bit lower instead of leaving a hole
    for l in ls: d.text((70, y), l, font=f, fill="#ffffff"); y += int(f.size * 1.14)
    y += 30
    d.rectangle([70, y, 190, y + 10], fill=accent); y += 50
    for l in al: d.text((70, y), l, font=fa, fill=light); y += 56
    # CTA pill
    cta = TXT[lang]["try_"] % t["h1"]
    fc = font("black", 36)
    cta = wrap(d, cta, fc, W - 220, 1)[0]
    by = H - 330
    d.rounded_rectangle([70, by, W - 70, by + 100], radius=50, fill=light)
    d.text((W // 2, by + 50), cta + "  →", font=fc, fill=dark, anchor="mm")
    d.rectangle([0, H - 170, W, H], fill=light)
    footer(d, "#ffffff", dark, dark, lang, site_host)
    return im

def draw_guide(a, site_host):
    from PIL import Image, ImageDraw
    dark, light, accent = COLORS["guide"]
    im = Image.new("RGB", (W, H), light); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 28, H], fill=accent)
    y = chip(d, 90, 90, TXT["en"]["guide"], dark, light) + 50
    f, ls = fit_headline(d, a["h1"][0].upper() + a["h1"][1:], W - 170, 5, start=110, low=60)
    for l in ls: d.text((90, y), l, font=f, fill=dark); y += int(f.size * 1.12)
    y += 30
    d.rectangle([90, y, 210, y + 10], fill=accent); y += 50
    fs = font("reg", 40)
    for l in wrap(d, a["description"], fs, W - 170, 6): d.text((90, y), l, font=fs, fill="#3d4744"); y += 56
    by = H - 330
    d.rounded_rectangle([90, by, W - 70, by + 100], radius=50, fill=dark)
    d.text(((W + 20) // 2, by + 50), TXT["en"]["read"] + "  →", font=font("black", 34), fill=light, anchor="mm")
    footer(d, dark, light, accent, "en", site_host)
    return im

# ------------------------------------------------------------------ item content
def item_info(iid, by_id, arts, site_url):
    """-> dict(lang, title, desc, link, draw) or None if the calculator/guide no longer exists."""
    utm = "?utm_source=pinterest&utm_medium=social&utm_campaign=%s"
    if iid.startswith("guide-"):
        a = arts.get(iid[6:])
        if not a: return None
        return dict(lang="en", title=a.get("title", a["h1"])[:100],
                    desc=(a["description"] + " Free guide with a calculator, no sign-up.")[:500],
                    link=site_url + "/guides/%s/" % a["slug"] + utm % "pin-guide", draw=lambda h: draw_guide(a, h))
    _, rest = iid.split("-", 1)
    cid, lang, v = rest.rsplit("-", 2)
    c = by_id.get(cid)
    if not c: return None
    t = c[lang]
    base = site_url + ("/" if lang == "en" else "/es/") + t["slug"] + "/"
    if v == "a":
        title, desc = t["title"], t["desc"]
    else:
        q, ans = t["faq"][0]
        title = "%s | %s" % (q, t["h1"])
        extra = " Free calculator, no sign-up." if lang == "en" else " Calculadora gratis, sin registro."
        desc = textwrap.shorten(ans, 500 - len(q) - len(extra) - 2, placeholder="…")
        desc = q + " " + desc + extra
    return dict(lang=lang, title=title[:100], desc=desc[:500], link=base + utm % ("pin-calc-" + v),
                draw=(lambda h, c=c, lang=lang, v=v: (draw_calc_a if v == "a" else draw_calc_b)(c, lang, CATS_REF[0], h)))

CATS_REF = [{}]

def rss(path, title, link, desc, lang, items, site_url):
    out = ['<?xml version="1.0" encoding="utf-8"?>',
           '<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">', "<channel>",
           "  <title>%s</title>" % escape(title), "  <link>%s</link>" % escape(link),
           "  <description>%s</description>" % escape(desc), "  <language>%s</language>" % lang]
    for it in items:
        img = site_url + "/pines/calculadoras/img/%s.jpg" % it["id"]
        d = dt.date.fromisoformat(it["fecha"])
        out += ["  <item>", "    <title>%s</title>" % escape(it["title"]), "    <link>%s</link>" % escape(it["link"]),
                "    <description>%s</description>" % escape(it["desc"]),
                '    <guid isPermaLink="false">handycalcs-%s</guid>' % it["id"],
                "    <pubDate>%s</pubDate>" % format_datetime(dt.datetime(d.year, d.month, d.day, 15, 0, tzinfo=dt.timezone.utc)),
                '    <enclosure url="%s" type="image/jpeg" length="0"/>' % img,
                '    <media:content url="%s" medium="image" type="image/jpeg"/>' % img, "  </item>"]
    out += ["</channel>", "</rss>", ""]
    with open(path, "w", encoding="utf-8") as f: f.write("\n".join(out))

# ------------------------------------------------------------------ entry point
def build(out_dir, calcs, cats, all_articles, site_url, today):
    """Called by build.py. Returns the number of pins already out."""
    CATS_REF[0] = cats
    today = dt.date.fromisoformat(today) if isinstance(today, str) else today
    site_url = site_url.rstrip("/")
    host = site_url.split("://", 1)[-1]
    items = update_queue(os.path.join(ROOT, "pines", "calculadoras", "cola.json"), calcs, all_articles, today)
    by_id = {c["id"]: c for c in calcs}
    arts = {a["slug"]: a for a in all_articles}
    dst = os.path.join(out_dir, "pines", "calculadoras"); img_dir = os.path.join(dst, "img")
    os.makedirs(img_dir, exist_ok=True)
    out = []
    for it in items:
        if dt.date.fromisoformat(it["fecha"]) > today: continue
        info = item_info(it["id"], by_id, arts, site_url)
        if not info: continue
        info.update(it); out.append(info)
        info["draw"](host).save(os.path.join(img_dir, it["id"] + ".jpg"), "JPEG", quality=82, optimize=True)
    out.reverse()   # newest first
    en = [i for i in out if i["lang"] == "en"][:VENTANA]
    es = [i for i in out if i["lang"] == "es"][:VENTANA]
    home = site_url + "/"
    rss(os.path.join(dst, "rss-en.xml"), "Handy Calcs: Free Calculators", home,
        "Free calculators for tips, pay, budgets, loans, health, school and recipes.", "en", en, site_url)
    rss(os.path.join(dst, "rss-es.xml"), "Handy Calcs: Calculadoras gratis", site_url + "/es/",
        "Calculadoras gratis para propinas, sueldos, presupuestos, préstamos, salud, escuela y recetas.", "es", es, site_url)
    rss(os.path.join(dst, "rss.xml"), "Handy Calcs pins", home, "Free calculators in English and Spanish.", "en",
        out[:VENTANA], site_url)
    pending = sum(1 for it in items if dt.date.fromisoformat(it["fecha"]) > today)
    last = items[-1]["fecha"] if items else "-"
    print("Pines de calculadoras: %d ya salieron, %d en cola (el último sale el %s)" % (len(out), pending, last))
    return len(out)

if __name__ == "__main__":   # preview: python3 tools/pines_calculadoras.py <out_dir> [YYYY-MM-DD]  (draws ALL pins, no queue change)
    import sys
    sys.path.insert(0, os.path.join(ROOT, "src"))
    from calcs import CALCS, CATS
    CATS_REF[0] = CATS
    o = sys.argv[1] if len(sys.argv) > 1 else "preview-pines"; os.makedirs(o, exist_ok=True)
    for c in CALCS:
        for lang in ("en", "es"):
            draw_calc_a(c, lang, CATS, "gethandycalcs.pages.dev").save(os.path.join(o, "%s-%s-a.jpg" % (c["id"], lang)), quality=86)
            draw_calc_b(c, lang, CATS, "gethandycalcs.pages.dev").save(os.path.join(o, "%s-%s-b.jpg" % (c["id"], lang)), quality=86)
    print("ok", o)
