#!/usr/bin/env python3
"""Build the ustrema.com coming-soon site.

Renders src/template.html into index.html (EN) and bg/index.html (BG), and
writes 404.html, sitemap.xml, robots.txt, llms.txt and manifest.webmanifest.
Standard library only:  python3 build.py
"""
import html
import json
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


def render(lang):
    s = STRINGS[lang]
    e = html.escape
    tpl = (ROOT / "src/template.html").read_text()
    words = " ".join(f'<span class="wi" style="--i:{i}">{e(w)}</span>' for i, w in enumerate(s["h1"].split(" ")))
    rep = {
        "lang": lang, "base": s["base"], "title": e(s["title"]), "desc": e(s["desc"]),
        "canonical": SITE + s["path"], "og_locale": s["og_locale"], "og_locale_alt": s["og_locale_alt"],
        "og_title": e(s["og_title"]), "og_alt": e(s["og_alt"]), "skip": e(s["skip"]), "soon": e(s["soon"]),
        "lang_label": e(s["lang_label"]), "lang_links": lang_links(lang, s),
        "logo": (ROOT / "src/logo.svgfrag").read_text(), "h1_words": words, "sub": e(s["sub"]),
        "cta": e(s["cta"]), "subject": s["subject"].replace(" ", "%20").replace(",", "%2C"),
        "copy": e(s["copy"]), "doors_label": e(s["doors_label"]),
        "d0t": e(s["doors"][0][0]), "d1t": e(s["doors"][1][0]), "d2t": e(s["doors"][2][0]),
        "door0": e(s["doors"][0][1]), "who": e(s["who"]), "tm": e(s["tm"]),
        "doors_json": json.dumps([d[1] for d in s["doors"]], ensure_ascii=False),
        "copy_json": json.dumps({"idle": s["copy"], "done": s["copied"], "status": s["copied_status"]}, ensure_ascii=False),
        "jsonld": jsonld(lang, s),
    }
    for k, v in rep.items():
        tpl = tpl.replace("{{" + k + "}}", v)
    assert "{{" not in tpl, "unreplaced placeholder"
    assert "—" not in tpl and "–" not in tpl, "no em or en dashes in copy"
    out = ROOT / s["path"].strip("/") / "index.html" if s["path"] != "/" else ROOT / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(tpl)
    print("wrote", out.relative_to(ROOT))


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
    render("en")
    render("bg")
    extras()
