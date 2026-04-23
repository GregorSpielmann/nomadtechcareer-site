#!/usr/bin/env python3
"""
NomadTechCareer.com — Article page generator
Run: python3 generate_articles.py

Reads data/articles.json and generates a static HTML page for each article.
Agent instructions: to add a new article, add an entry to data/articles.json and re-run this script.
"""

import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "articles.json"
ARTICLES_DIR = BASE_DIR / "articles"
CITY_GUIDES_FILE = BASE_DIR / "data" / "city-guides.json"

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


def build_article_schema(article):
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article["title"],
        "description": article["meta_description"],
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
        "datePublished": article.get("date", "2026"),
        "url": f"{SITE_URL}/articles/{article['slug']}/"
    }
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'


def build_faq_schema(faqs):
    if not faqs:
        return ""
    items = [{"@type": "Question", "name": faq["q"], "acceptedAnswer": {"@type": "Answer", "text": faq["a"]}} for faq in faqs]
    schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'


def load_city_guides():
    if CITY_GUIDES_FILE.exists():
        with open(CITY_GUIDES_FILE) as f:
            return json.load(f).get("guides", [])
    return []


def generate_article_page(article, all_articles, city_guides):
    # Sections
    sections_html = ""
    for section in article.get("sections", []):
        sections_html += f"""
      <h2>{section['h2']}</h2>
      <p>{section['body']}</p>"""

    # FAQ section
    faqs_html = ""
    if article.get("faqs"):
        items = ""
        for faq in article["faqs"]:
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

    # Related articles (use explicit slugs from data)
    related_slugs = article.get("related_articles", [])
    related_articles = [a for a in all_articles if a["slug"] in related_slugs]
    related_html = ""
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
        related_html = f"""
    <div class="related-section">
      <h2>Related Articles</h2>
      <div class="card-grid card-grid-2">
        {cards}
      </div>
    </div>"""

    # Related city guide
    guide_slug = article.get("related_city_guide", "")
    guide_cta = ""
    if guide_slug:
        guide = next((g for g in city_guides if g["slug"] == guide_slug), None)
        if guide:
            guide_cta = f"""
    <div class="cta-block">
      <h3>Thinking about {guide['title'].replace('Working from ', '')}?</h3>
      <p>Check out our city guide with coworking spaces, costs, visa info, and practical tips.</p>
      <a href="/city-guides/{guide['slug']}/">Read the {guide['title']} guide &rarr;</a>
    </div>"""

    # Schema
    schema = build_article_schema(article)
    if article.get("faqs"):
        schema += "\n" + build_faq_schema(article["faqs"])

    # OG meta
    canonical_url = f"{SITE_URL}/articles/{article['slug']}/"
    og_image = article.get("og_image") or f"{SITE_URL}/assets/og-default.png"
    og_meta = f"""<link rel="canonical" href="{canonical_url}">
  <meta property="og:title" content="{article['seo_title']}">
  <meta property="og:description" content="{article['meta_description']}">
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
  <title>{article['seo_title']} — {SITE_NAME}</title>
  <meta name="description" content="{article['meta_description']}">
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
      <span class="tag">{article['tag']}</span>
      <span class="author">By {article['author']}</span>
      <time>{article['date']}</time>
    </div>

    <h1>{article['title']}</h1>

    <p class="article-intro">{article['intro']}</p>

    <div class="article-content">
{sections_html}
    </div>

{guide_cta}
{faqs_html}
{related_html}
  </main>

{FOOTER}

</body>
</html>"""
    return html


def generate_articles_index(articles):
    if not articles:
        return ""

    # Collect unique tags
    all_tags = []
    for a in articles:
        if a['tag'] not in all_tags:
            all_tags.append(a['tag'])

    filter_buttons = '<button class="filter-btn active" data-filter="all">All</button>\n'
    for tag in all_tags:
        filter_buttons += f'      <button class="filter-btn" data-filter="{tag}">{tag}</button>\n'

    cards = ""
    for article in articles:
        excerpt = article['intro']
        if len(excerpt) > 160:
            excerpt = excerpt[:160].rsplit(' ', 1)[0] + '...'
        cards += f"""
        <a href="/articles/{article['slug']}/" class="card-link" data-category="{article['tag']}">
          <div class="card">
            <div class="card-meta">
              <span class="tag">{article['tag']}</span>
              <time>{article['date']}</time>
            </div>
            <h3>{article['title']}</h3>
            <p>{excerpt}</p>
            <span class="card-cta">Read article &rarr;</span>
          </div>
        </a>"""

    filter_js = """
  <script>
    (function() {
      var btns = document.querySelectorAll('.filter-btn');
      var cards = document.querySelectorAll('.card-link');
      var noResults = document.getElementById('no-results');
      btns.forEach(function(btn) {
        btn.addEventListener('click', function() {
          var filter = this.getAttribute('data-filter');
          btns.forEach(function(b) { b.classList.remove('active'); });
          this.classList.add('active');
          var visible = 0;
          cards.forEach(function(card) {
            if (filter === 'all' || card.getAttribute('data-category') === filter) {
              card.style.display = '';
              visible++;
            } else {
              card.style.display = 'none';
            }
          });
          if (noResults) noResults.style.display = visible === 0 ? 'block' : 'none';
        });
      });
    })();
  </script>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Articles — {SITE_NAME}</title>
  <meta name="description" content="Practical articles on remote work, location independence, and building a tech career from anywhere in the world.">
  <meta property="og:title" content="Articles — {SITE_NAME}">
  <meta property="og:description" content="Practical articles on remote work, location independence, and building a tech career from anywhere.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{SITE_URL}/articles/">
  {GOOGLE_FONTS}
  <link rel="stylesheet" href="/assets/css/main.css">
  <script src="/assets/js/main.js" defer></script>
</head>
<body>
{NAV}

  <div class="hub-header">
    <h1>Articles</h1>
    <p>Practical writing on remote work, location independence, and building a tech career from anywhere.</p>
  </div>

  <section class="section">
    <div class="container">
      <div class="filter-bar">
      {filter_buttons}
      </div>
      <div class="card-grid card-grid-2">
{cards}
      </div>
      <p id="no-results" style="display:none; color: var(--color-muted); padding: 2rem 0;">No articles in this category yet.</p>
    </div>
  </section>

{FOOTER}
{filter_js}
</body>
</html>"""
    return html


def main():
    print(f"Reading articles from {DATA_FILE}")
    with open(DATA_FILE) as f:
        data = json.load(f)

    articles = data["articles"]
    city_guides = load_city_guides()
    print(f"Found {len(articles)} articles to generate")

    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)

    for article in articles:
        slug = article["slug"]
        out_dir = ARTICLES_DIR / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / "index.html"

        html = generate_article_page(article, articles, city_guides)
        with open(out_file, "w") as f:
            f.write(html)
        print(f"  Generated: /articles/{slug}/")

    # Generate index
    index_html = generate_articles_index(articles)
    with open(ARTICLES_DIR / "index.html", "w") as f:
        f.write(index_html)
    print(f"  Generated: /articles/ (index)")

    print(f"\nDone. {len(articles)} articles + 1 index page generated.")


if __name__ == "__main__":
    main()
