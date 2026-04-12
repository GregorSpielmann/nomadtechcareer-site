# NomadTechCareer.com

Practical guides for tech professionals who work from anywhere.

## Architecture

Static site with Python-based page generators. No framework, no build step beyond running the generators.

### Content Types
- **Articles** — Remote work, tools, career advice (`data/articles.json`)
- **City Guides** — Detailed city guides for remote workers (`data/city-guides.json`)

### Generators
```bash
python3 generate_articles.py      # Generates articles/ from data/articles.json
python3 generate_city_guides.py   # Generates city-guides/ from data/city-guides.json
```

### Adding Content
1. Add an entry to the relevant JSON file in `data/`
2. Run the corresponding generator script
3. Update `sitemap.xml` with new URLs
4. Commit and deploy

### Site Structure
```
index.html                        # Homepage
articles/index.html               # Articles hub
articles/{slug}/index.html        # Individual articles
city-guides/index.html            # City guides hub
city-guides/{slug}/index.html     # Individual city guides
assets/css/main.css               # Stylesheet
assets/js/main.js                 # JS utilities
data/articles.json                # Article content
data/city-guides.json             # City guide content
robots.txt                        # Crawler directives
sitemap.xml                       # Sitemap
llms.txt                          # AI-readable site description
```

## Author

A project by [Gregor Spielmann](https://www.linkedin.com/in/gregor-spielmann/).

Built and operated with AI agents.
