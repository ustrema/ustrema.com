#!/usr/bin/env python3
"""Build the ustrema.com coming-soon site.

Renders src/template.html into index.html (EN) and bg/index.html (BG), and
writes 404.html, sitemap.xml, robots.txt, llms.txt and manifest.webmanifest.
Standard library only:  python3 build.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://ustrema.com"
LASTMOD = "2026-10-14"

KNOWS = [
    "Microsoft Power Platform", "Power Platform governance", "Power Apps", "Power Automate",
    "Power BI", "Dataverse", "Microsoft Copilot Studio", "Copilot and AI agent governance",
    "Microsoft Purview", "Microsoft Dynamics 365", "Managed Environments", "Data loss prevention (DLP) policies",
    "Center of Excellence (CoE)",
]

STRINGS = {
    "en": {
        "path": "/", "base": "", "og_locale": "en_US", "og_locale_alt": "bg_BG",
        "title": "Ustrema · Power Platform, Copilot & Dynamics 365 practice",
        "og_title": "Ustrema · Momentum with direction.",
        "desc": "Ustrema is a Sofia-based Microsoft Power Platform, Copilot and Dynamics 365 practice. Governance first, then delivery that scales. Launching soon.",
        "og_alt": "Ustrema logo with the line Momentum with direction.",
        "skip": "Skip to content",
        "soon": "Opening soon",
        "lang_label": "Language",
        "h1": "Momentum with direction.",
        "sub": "Senior Microsoft Power Platform, Copilot and Dynamics 365 practice. Governance first, then delivery that scales.",
        "cta": "Say hello", "subject": "Hello Ustrema",
        "copy": "Copy", "copied": "Copied", "copied_status": "Email address copied",
        "doors_label": "What we do",
        "doors": [
            ("Govern", "Know what is in your tenant. Fix it without stopping your makers."),
            ("Build", "Apps, automations and dashboards, built properly the first time."),
            ("Scale with AI", "Copilot and agents that only see what they should."),
        ],
        "who": "© 2026 Ustrema (oo-STREH-mah), Sofia",
        "tm": "Microsoft, Power Platform, Copilot and Dynamics 365 are trademarks of the Microsoft group of companies.",
    },
    "bg": {
        "path": "/bg/", "base": "../", "og_locale": "bg_BG", "og_locale_alt": "en_US",
        "title": "Устрема · Power Platform, Copilot и Dynamics 365 практика",
        "og_title": "Устрема · Устрем с посока.",
        "desc": "Устрема е практика за Microsoft Power Platform, Copilot и Dynamics 365 от София. Първо контрол, после мащаб. Очаквайте ни скоро.",
        "og_alt": "Логото на Устрема с надпис Устрем с посока.",
        "skip": "Към съдържанието",
        "soon": "Очаквайте скоро",
        "lang_label": "Език",
        "h1": "Устрем с посока.",
        "sub": "Експертна практика за Microsoft Power Platform, Copilot и Dynamics 365. Първо контрол, после мащаб.",
        "cta": "Пишете ни", "subject": "Здравейте, Устрема",
        "copy": "Копирай", "copied": "Копирано", "copied_status": "Имейл адресът е копиран",
        "doors_label": "С какво помагаме",
        "doors": [
            ("Контрол", "Знайте какво има във Вашия tenant. Подредете го, без да спирате екипите."),
            ("Изграждане", "Приложения, автоматизации и табла, направени правилно още първия път."),
            ("Мащаб с AI", "Copilot и агенти, които виждат само това, което трябва."),
        ],
        "who": "© 2026 Устрема (у-СТРЕ-ма), София",
        "tm": "Microsoft, Power Platform, Copilot и Dynamics 365 са търговски марки на групата компании Microsoft.",
    },
}


def jsonld(lang, s):
    url = SITE + s["path"]
    graph = [
        {
            "@type": "Organization",
            "@id": SITE + "/#org",
            "name": "Ustrema",
            "alternateName": ["Устрема", "USTREMA LTD", "УСТРЕМА ООД"],
            "legalName": "USTREMA LTD",
            "url": SITE + "/",
            "logo": {"@type": "ImageObject", "url": SITE + "/assets/icon-512.png", "width": 512, "height": 512},
            "image": SITE + "/assets/og.jpg",
            "description": STRINGS["en"]["desc"],
            "slogan": "Momentum with direction.",
            "email": "hello@ustrema.com",
            "foundingDate": "2026-09-30",
            "foundingLocation": {"@type": "Place", "name": "Sofia, Bulgaria"},
            "address": {"@type": "PostalAddress", "addressLocality": "Sofia", "addressCountry": "BG"},
            "areaServed": [{"@type": "Country", "name": "Bulgaria"}, {"@type": "Place", "name": "European Union"}],
            "knowsAbout": KNOWS,
            "knowsLanguage": ["en", "bg"],
            "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "email": "hello@ustrema.com",
                             "availableLanguage": ["English", "Bulgarian"]},
            "sameAs": ["https://github.com/ustrema"],
        },
        {
            "@type": "WebSite",
            "@id": SITE + "/#website",
            "url": SITE + "/",
            "name": "Ustrema",
            "inLanguage": ["en", "bg"],
            "publisher": {"@id": SITE + "/#org"},
        },
        {
            "@type": "WebPage",
            "@id": url + "#page",
            "url": url,
            "name": s["title"],
            "description": s["desc"],
            "inLanguage": lang,
            "isPartOf": {"@id": SITE + "/#website"},
            "about": {"@id": SITE + "/#org"},
            "primaryImageOfPage": SITE + "/assets/og.jpg",
            "dateModified": LASTMOD,
        },
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


def lang_links(lang, s):
    items = []
    for code, label, name in (("en", "EN", "English"), ("bg", "BG", "Български")):
        href = ("./" if code == "en" else "bg/") if lang == "en" else ("../" if code == "en" else "./")
        cur = ' aria-current="page"' if code == lang else ""
        items.append(f'<a href="{href}" hreflang="{code}" lang="{code}"{cur}>{label}<span class="sr"> {name}</span></a>')
    return "\n      ".join(items)


# Layout + background combinations. "v0" is what is live; v1-v5 are the proposals under review.
VARIANTS = {
    "v0": {"name": "Live today", "logo": "hero", "lead": False, "mode": {"name": "pins", "interact": True}},
    "v1": {"name": "Quiet pins", "logo": "header", "lead": False, "mode": {"name": "pins", "calm": True}},
    "v2": {"name": "Current", "logo": "hero", "lead": True, "mode": {"name": "arcs"}},
    "v3": {"name": "Horizon", "logo": "header", "lead": False, "mode": {"name": "horizon"}},
    "v4": {"name": "Sheen", "logo": "header", "lead": False, "mode": {"name": "lines"}},
    "v5": {"name": "Signal+", "logo": "hero", "lead": True, "mode": {"name": "dots"}},
}
PROD_VARIANT = "v5"


def logo_html(small):
    cls = "logo logo--sm" if small else "logo"
    frag = (ROOT / "src/logo.svgfrag").read_text()
    return f'<div class="{cls}" role="img" aria-label="Ustrema"><div class="logo-3d">\n      {frag}\n    </div></div>'


def label_html(s):
    return f'<p class="label"><span class="pulse" aria-hidden="true"><i></i><i></i><i></i></span>{html.escape(s["soon"])}</p>'


def preview_bar(current, lang):
    up = "../../" if lang == "bg" else "../"
    tail = "bg/" if lang == "bg" else ""
    links = "".join(
        f'<a href="{up}{k}/{tail}"{" aria-current=\"page\"" if k == current else ""}>{k.upper()} {html.escape(v["name"])}</a>'
        for k, v in VARIANTS.items() if k != "v0")
    return ('<nav class="pv" aria-label="Preview variants" style="position:fixed;z-index:20;left:50%;top:10px;transform:translateX(-50%);'
            'display:flex;gap:2px;padding:4px;background:rgba(29,20,41,.82);border:1px solid rgba(244,241,236,.18);'
            'font:500 11px/1 JetBrains Mono,monospace;letter-spacing:.06em;backdrop-filter:blur(8px)">'
            f'<a href="{up}">ALL</a>{links}</nav>'
            '<style>.pv a{color:rgba(244,241,236,.72);text-decoration:none;padding:8px 10px;white-space:nowrap}'
            '.pv a:hover{color:#F4F1EC}.pv a[aria-current]{background:#F4F1EC;color:#1D1429}'
            '@media(max-width:900px){.pv{top:auto!important;bottom:8px;max-width:calc(100vw - 16px);overflow-x:auto}}</style>')


def keep_mode(tpl, name):
    """Ship only the selected background mode's code; drop the other entries of the modes object."""
    block = re.compile(r"(    /\*(?:(?!\*/).)*?\*/\n)?    (\w+): \(\(\) => \{\n.*?\n    \}\)\(\),?\n", re.S)
    found = [m.group(2) for m in block.finditer(tpl)]
    assert name in found, f"mode {name} not found in template ({found})"
    return block.sub(lambda m: m.group(0) if m.group(2) == name else "", tpl)


def render(lang, variant=PROD_VARIANT, out_root=None, base_prefix="", preview=False):
    s = STRINGS[lang]
    v = VARIANTS[variant]
    e = html.escape
    tpl = (ROOT / "src/template.html").read_text()
    words = " ".join(f'<span class="wi" style="--i:{i}">{e(w)}</span>' for i, w in enumerate(s["h1"].split(" ")))
    header_logo = v["logo"] == "header"
    rep = {
        "lang": lang, "base": base_prefix + s["base"], "title": e(s["title"]), "desc": e(s["desc"]),
        "html_class": "lead" if v["lead"] else "",
        "header_left": logo_html(True) if header_logo else label_html(s),
        "hero_top": label_html(s) if header_logo else logo_html(False),
        "preview_bar": preview_bar(variant, lang) if preview else "",
        "mode_json": json.dumps(v["mode"]),
        "canonical": SITE + s["path"], "og_locale": s["og_locale"], "og_locale_alt": s["og_locale_alt"],
        "og_title": e(s["og_title"]), "og_alt": e(s["og_alt"]), "skip": e(s["skip"]),
        "lang_label": e(s["lang_label"]), "lang_links": lang_links(lang, s),
        "h1_words": words, "sub": e(s["sub"]),
        "cta": e(s["cta"]), "subject": s["subject"].replace(" ", "%20").replace(",", "%2C"),
        "copy": e(s["copy"]), "doors_label": e(s["doors_label"]),
        "d0t": e(s["doors"][0][0]), "d1t": e(s["doors"][1][0]), "d2t": e(s["doors"][2][0]),
        "door0": e(s["doors"][0][1]), "who": e(s["who"]), "tm": e(s["tm"]),
        "doors_json": json.dumps([d[1] for d in s["doors"]], ensure_ascii=False),
        "copy_json": json.dumps({"idle": s["copy"], "done": s["copied"], "status": s["copied_status"]}, ensure_ascii=False),
        "jsonld": jsonld(lang, s),
    }
    for k, val in rep.items():
        tpl = tpl.replace("{{" + k + "}}", val)
    tpl = keep_mode(tpl, v["mode"]["name"])
    assert "{{" not in tpl, "unreplaced placeholder"
    assert "—" not in tpl and "–" not in tpl, "no em or en dashes in copy"
    if preview:
        tpl = tpl.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
    root = out_root or ROOT
    out = root / s["path"].strip("/") / "index.html" if s["path"] != "/" else root / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(tpl)
    print("wrote", out.relative_to(ROOT))


def previews():
    """Local-only review builds in preview/ (git-ignored): one folder per variant plus a comparison hub."""
    pv = ROOT / "preview"
    for k in VARIANTS:
        for lang in ("en", "bg"):
            render(lang, k, pv / k, "../../", preview=True)
    cards = "".join(f"""
  <figure>
    <div class="frame"><iframe src="{k}/" title="{k.upper()} {html.escape(v['name'])}" loading="lazy" tabindex="-1"></iframe></div>
    <figcaption><a href="{k}/"><b>{k.upper()}</b> {html.escape(v['name'])}</a><span>{'logo in header, big headline' if v['logo'] == 'header' else ('logo as hero, quiet subtitle' if v['lead'] else 'logo and headline both large')} · {v['mode']['name']}{' + cursor/click' if v['mode'].get('interact') else ''}</span></figcaption>
  </figure>""" for k, v in VARIANTS.items())
    (pv / "index.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex"><title>Ustrema · landing variants</title>
<style>
body{{margin:0;background:#120c1a;color:#F4F1EC;font:15px/1.5 Arial,sans-serif;padding:28px clamp(16px,3vw,40px)}}
h1{{font-size:22px;margin:0 0 4px}} p{{margin:0 0 24px;color:rgba(244,241,236,.7)}}
main{{display:grid;grid-template-columns:repeat(auto-fill,minmax(520px,1fr));gap:28px}}
figure{{margin:0}} .frame{{position:relative;aspect-ratio:16/10;overflow:hidden;border:1px solid rgba(244,241,236,.14)}}
iframe{{position:absolute;left:0;top:0;width:1440px;height:900px;border:0;transform-origin:0 0;pointer-events:none}}
figcaption{{display:flex;flex-direction:column;gap:2px;margin-top:10px}} figcaption a{{color:#F4F1EC;text-decoration:none;font-size:16px}}
figcaption a:hover{{text-decoration:underline}} figcaption span{{color:rgba(244,241,236,.6);font-size:13px}}
</style></head><body>
<h1>Ustrema landing: 5 variants</h1>
<p>Click a title to open it full size. V0 is what is live now, for reference. Each full page has a switcher at the top.</p>
<main>{cards}
</main>
<script>
const fit=()=>document.querySelectorAll('.frame').forEach(f=>f.querySelector('iframe').style.transform='scale('+f.clientWidth/1440+')');
addEventListener('resize',fit);fit();
</script>
</body></html>
""")
    print("wrote preview/index.html")


def extras():
    (ROOT / "sitemap.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>{SITE}/</loc>
    <lastmod>{LASTMOD}</lastmod>
    <xhtml:link rel="alternate" hreflang="en" href="{SITE}/"/>
    <xhtml:link rel="alternate" hreflang="bg" href="{SITE}/bg/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/"/>
  </url>
  <url>
    <loc>{SITE}/bg/</loc>
    <lastmod>{LASTMOD}</lastmod>
    <xhtml:link rel="alternate" hreflang="en" href="{SITE}/"/>
    <xhtml:link rel="alternate" hreflang="bg" href="{SITE}/bg/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/"/>
  </url>
</urlset>
""")
    (ROOT / "robots.txt").write_text(f"""# Search engines and AI answer engines are welcome.
User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: {SITE}/sitemap.xml
""")
    doors = "\n".join(f"- **{t}**: {d}" for t, d in STRINGS["en"]["doors"])
    (ROOT / "llms.txt").write_text(f"""# Ustrema

> {STRINGS["en"]["desc"]}

Ustrema (Устрема, legal name USTREMA LTD / УСТРЕМА ООД) is a Microsoft Power Platform consultancy founded in Sofia, Bulgaria, in September 2026. It works with mid-market and enterprise organisations in Bulgaria and the European Union, in English and Bulgarian. Its tagline is "Momentum with direction." (Bulgarian: "Устрем с посока.").

## What Ustrema does

{doors}

Ustrema starts with governance (environments, data loss prevention policies, ownership, Managed Environments, Center of Excellence) and then builds on Microsoft Power Apps, Power Automate, Power BI, Dataverse, Microsoft Copilot Studio and Microsoft Dynamics 365.

## Status

The full website is launching soon. This page is the current home of the company online.

## Contact

- Email: hello@ustrema.com
- Location: Sofia, Bulgaria
- Languages: English, Bulgarian

## Pages

- [English home]({SITE}/)
- [Bulgarian home]({SITE}/bg/)

Microsoft, Power Platform, Copilot and Dynamics 365 are trademarks of the Microsoft group of companies. Ustrema is an independent company.
""")
    (ROOT / "manifest.webmanifest").write_text(json.dumps({
        "name": "Ustrema", "short_name": "Ustrema", "start_url": "./", "display": "browser",
        "background_color": "#1D1429", "theme_color": "#1D1429",
        "icons": [
            {"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }, indent=2) + "\n")
    print("wrote sitemap.xml, robots.txt, llms.txt, manifest.webmanifest")


if __name__ == "__main__":
    import sys
    if "--preview" in sys.argv:
        previews()
    else:
        render("en")
        render("bg")
        extras()
