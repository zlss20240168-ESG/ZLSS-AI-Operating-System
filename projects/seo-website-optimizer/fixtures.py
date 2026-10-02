BASE_HEAD = """<!doctype html><html lang="{lang}"><head><meta charset="utf-8">
<title>{title}</title>{meta}{canonical}{viewport}{og}{schema}</head><body>{body}</body></html>"""

def page(title="Acme",lang="en",description="Acme services",robots="index,follow",canonical="https://example.com/",
         viewport=True,h1="Acme Services",extra_body="",schema=True,cta=True,image_alt="Factory"):
    meta=f'<meta name="description" content="{description}"><meta name="robots" content="{robots}">'
    can=f'<link rel="canonical" href="{canonical}">' if canonical is not None else ""
    vp='<meta name="viewport" content="width=device-width,initial-scale=1">' if viewport else ""
    og=f'<meta property="og:title" content="{title}"><meta property="og:description" content="{description}"><meta property="og:image" content="/hero.jpg">'
    sc='<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"Acme"}</script>' if schema else ""
    cta='<a href="/contact">Contact us</a><form action="/quote"></form>' if cta else '<a href="#">More</a>'
    body=f'<h1>{h1}</h1><h2>Solutions</h2><p>We provide industrial services for customers.</p><img src="/hero.jpg" alt="{image_alt}">{cta}{extra_body}'
    return BASE_HEAD.format(lang=lang,title=title,meta=meta,canonical=can,viewport=vp,og=og,schema=sc,body=body)

FIXTURES={
"F01_baseline": page(),
"F02_noindex": page(robots="noindex,nofollow"),
"F03_no_description": page(description=""),
"F04_no_canonical": page(canonical=None),
"F05_missing_h1": page(h1=""),
"F06_missing_alt": page(image_alt=""),
"F07_broken_cta": page(cta=False),
"F08_no_viewport": page(viewport=False),
"F09_no_schema": page(schema=False),
"F10_multilingual_zh": page(lang="zh-TW",title="艾克米服務",h1="艾克米服務"),
"F11_price_v1": page(extra_body="<p>Plan: USD 100</p>"),
"F12_price_v2": page(extra_body="<p>Plan: USD 120</p>")
}