#!/usr/bin/env python3
"""
NomadTechCareer.com — City guide page generator
Run: python3 generate_city_guides.py

Reads data/city-guides.json and generates a static HTML page for each city guide.
Agent instructions: to add a new city guide, add an entry to data/city-guides.json and re-run this script.
"""

import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "city-guides.json"
GUIDES_DIR = BASE_DIR / "city-guides"
ARTICLES_FILE = BASE_DIR / "data" / "articles.json"

SITE_URL = "https://nomadtechcareer.com"
SITE_NAME = "NomadTechCareer"

NAV = """  <nav class="site-nav">
    <div class="nav-inner">
      <a href="/" class="nav-logo">
        <svg class="logo-mark" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><circle cx="12" cy="12" r="9.5" stroke="#E8920A" stroke-width="1.8" fill="none"/><circle cx="12" cy="12" r="2.8" fill="#E8920A"/><line x1="12" y1="1.5" x2="12" y2="5.5" stroke="#E8920A" stroke-width="1.5" stroke-linecap="round"/><line x1="12" y1="18.5" x2="12" y2="22.5" stroke="#E8920A" stroke-width="1.5" stroke-linecap="round"/><line x1="1.5" y1="12" x2="5.5" y2="12" stroke="#E8920A" stroke-width="1.5" stroke-linecap="round"/><line x1="18.5" y1="12" x2="22.5" y2="12" stroke="#E8920A" stroke-width="1.5" stroke-linecap="round"/></svg><span class="nav-logo-text">NomadTechCareer</span>
      </a>
      <button class="nav-toggle" aria-label="Toggle navigation">
        <span></span><span></span><span></span>
      </button>
      <ul class="nav-links">
        <li><a href="/articles/">Articles</a></li>
        <li><a href="/city-guides/">City Guides</a></li>
      </ul>
    </div>
  </nav>"""

FOOTER = """  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <span class="footer-logo-text">NomadTechCareer</span>
        <p>A project by <a href="https://www.linkedin.com/in/gregor-spielmann/" target="_blank" rel="noopener">Gregor Spielmann</a>. Practical guides for tech professionals who work from anywhere.</p>
      </div>
      <div class="footer-col">
        <h4>Content</h4>
        <ul>
          <li><a href="/articles/">Articles</a></li>
          <li><a href="/city-guides/">City Guides</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Connect</h4>
        <ul>
          <li><a href="https://www.linkedin.com/in/gregor-spielmann/" target="_blank" rel="noopener">LinkedIn</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 NomadTechCareer.com &middot; A project by Gregor Spielmann</p>
      <span class="ai-badge">Built with AI</span>
    </div>
  </footer>"""

GOOGLE_FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@600;700;800&display=swap" rel="stylesheet">'


def build_article_schema(guide):
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": guide["title"],
        "description": guide["meta_description"],
        "author": {
            "@type": "Person",
            "name": "Gregor Spielmann",
            "url": "https://www.linkedin.com/in/gregor-spielmann/"
        },
        "publisher": {
            "@type": "Organization",
            "name": SITE_NAME,
            "url": SITE_URL
        },
        "datePublished": guide.get("date", "2026"),
        "url": f"{SITE_URL}/city-guides/{guide['slug']}/"
    }
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'


def build_faq_schema(faqs):
    if not faqs:
        return ""
    items = [{"@type": "Question", "name": faq["q"], "acceptedAnswer": {"@type": "Answer", "text": faq["a"]}} for faq in faqs]
    schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'


def load_articles():
    if ARTICLES_FILE.exists():
        with open(ARTICLES_FILE) as f:
            return json.load(f).get("articles", [])
    return []


def build_quick_facts_html(quick_facts):
    if not quick_facts:
        return ""
    labels = {
        "cost_of_living": "Cost of Living",
        "internet_speed": "Internet Speed",
        "timezone": "Timezone",
        "coworking": "Coworking",
        "visa": "Visa",
        "best_for": "Best For"
    }
    facts_html = ""
    for key, label in labels.items():
        if key in quick_facts:
            facts_html += f"""
      <div class="quick-fact">
        <span class="quick-fact-label">{label}</span>
        <span class="quick-fact-value">{quick_facts[key]}</span>
      </div>"""
    return f"""
    <div class="quick-facts">
{facts_html}
    </div>"""


def generate_guide_page(guide, all_guides, all_articles):
    # Quick facts
    quick_facts_html = build_quick_facts_html(guide.get("quick_facts", {}))

    # Sections
    sections_html = ""
    for section in guide.get("sections", []):
        sections_html += f"""
      <h2>{section['h2']}</h2>
      <p>{section['body']}</p>"""

    # FAQ section
    faqs_html = ""
    if guide.get("faqs"):
        items = ""
        for faq in guide["faqs"]:
            items += f"""
        <div class="faq-item">
          <h4>{faq['q']}</h4>
          <p>{faq['a']}</p>
        </div>"""
        faqs_html = f"""
      <div class="faq-block">
        <h2>Frequently Asked Questions</h2>
        {items}
      </div>"""

    # Related articles (use explicit slugs)
    related_article_slugs = guide.get("related_articles", [])
    related_articles = [a for a in all_articles if a["slug"] in related_article_slugs]
    related_articles_html = ""
    if related_articles:
        cards = ""
        for r in related_articles:
            excerpt = r['intro'][:140] + '...' if len(r['intro']) > 140 else r['intro']
            cards += f"""
          <a href="/articles/{r['slug']}/" class="card-link">
            <div class="card">
              <span class="tag">{r['tag']}</span>
              <h3>{r['title']}</h3>
              <p>{excerpt}</p>
              <span class="card-cta">Read article &rarr;</span>
            </div>
          </a>"""
        related_articles_html = f"""
    <div class="related-section">
      <h2>Related Articles</h2>
      <div class="card-grid card-grid-2">
        {cards}
      </div>
    </div>"""

    # Related city guides (use explicit slugs)
    related_guide_slugs = guide.get("related_city_guides", [])
    related_guides = [g for g in all_guides if g["slug"] in related_guide_slugs]
    related_guides_html = ""
    if related_guides:
        cards = ""
        for r in related_guides:
            cards += f"""
          <a href="/city-guides/{r['slug']}/" class="card-link">
            <div class="card">
              <span class="tag">{r['tag']}</span>
              <h3>{r['title']}</h3>
              <p>{r['intro'][:140]}...</p>
              <span class="card-cta">Read guide &rarr;</span>
            </div>
          </a>"""
        related_guides_html = f"""
    <div class="related-section" style="margin-top:32px;">
      <h2>More City Guides</h2>
      <div class="card-grid card-grid-2">
        {cards}
      </div>
    </div>"""

    # Schema
    schema = build_article_schema(guide)
    if guide.get("faqs"):
        schema += "\n" + build_faq_schema(guide["faqs"])

    # OG meta
    canonical_url = f"{SITE_URL}/city-guides/{guide['slug']}/"
    og_image = guide.get("og_image") or f"{SITE_URL}/assets/og-default.png"
    og_meta = f"""<link rel="canonical" href="{canonical_url}">
  <meta property="og:title" content="{guide['seo_title']}">
  <meta property="og:description" content="{guide['meta_description']}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:image" content="{og_image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{og_image}">"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{guide['seo_title']} — {SITE_NAME}</title>
  <meta name="description" content="{guide['meta_description']}">
  {og_meta}
  {GOOGLE_FONTS}
  <link rel="stylesheet" href="/assets/css/main.css">
  <script src="/assets/js/main.js" defer></script>
  {schema}
</head>
<body>
{NAV}

  <main class="article-page">
    <div class="article-meta">
      <span class="tag">{guide['tag']}</span>
      <span class="author">By {guide['author']}</span>
      <time>{guide['date']}</time>
    </div>

    <h1>{guide['title']}</h1>

    <p class="article-intro">{guide['intro']}</p>

{quick_facts_html}

    <div class="article-content">
{sections_html}
    </div>

{faqs_html}
{related_articles_html}
{related_guides_html}
  </main>

{FOOTER}

</body>
</html>"""
    return html


def generate_guides_index(guides):
    cards = ""
    for guide in guides:
        excerpt = guide['intro']
        if len(excerpt) > 160:
            excerpt = excerpt[:160].rsplit(' ', 1)[0] + '...'

        # Build a mini quick-facts preview
        qf = guide.get("quick_facts", {})
        facts_preview = ""
        if qf:
            facts_preview = f'<div class="card-meta" style="margin-top:8px;"><span>{qf.get("cost_of_living", "")}</span> <span>{qf.get("timezone", "")}</span></div>'

        cards += f"""
        <a href="/city-guides/{guide['slug']}/" class="card-link">
          <div class="card">
            <span class="tag">{guide['tag']}</span>
            <h3>{guide['title']}</h3>
            <p>{excerpt}</p>
            {facts_preview}
            <span class="card-cta">Read guide &rarr;</span>
          </div>
        </a>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>City Guides — {SITE_NAME}</title>
  <meta name="description" content="In-depth city guides for tech professionals working remotely. Coworking, internet, costs, visas, and daily life in the world's best cities for remote work.">
  <meta property="og:title" content="City Guides — {SITE_NAME}">
  <meta property="og:description" content="City guides for tech professionals working remotely from around the world.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{SITE_URL}/city-guides/">
  {GOOGLE_FONTS}
  <link rel="stylesheet" href="/assets/css/main.css">
  <script src="/assets/js/main.js" defer></script>
</head>
<body>
{NAV}

  <div class="hub-header">
    <h1>City Guides</h1>
    <p>Practical, detailed guides to the best cities for remote tech work. Coworking, costs, visas, and what daily life actually looks like.</p>
  </div>

  <section class="section">
    <div class="container">
      <div class="card-grid card-grid-2">
{cards}
      </div>
    </div>
  </section>

{FOOTER}

</body>
</html>"""
    return html


def main():
    print(f"Reading city guides from {DATA_FILE}")
    with open(DATA_FILE) as f:
        data = json.load(f)

    guides = data["guides"]
    articles = load_articles()
    print(f"Found {len(guides)} city guides to generate")

    GUIDES_DIR.mkdir(parents=True, exist_ok=True)

    for guide in guides:
        slug = guide["slug"]
        out_dir = GUIDES_DIR / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / "index.html"

        html = generate_guide_page(guide, guides, articles)
        with open(out_file, "w") as f:
            f.write(html)
        print(f"  Generated: /city-guides/{slug}/")

    # Generate index
    index_html = generate_guides_index(guides)
    with open(GUIDES_DIR / "index.html", "w") as f:
        f.write(index_html)
    print(f"  Generated: /city-guides/ (index)")

    print(f"\nDone. {len(guides)} city guides + 1 index page generated.")


if __name__ == "__main__":
    main()
