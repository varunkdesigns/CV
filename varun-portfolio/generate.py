#!/usr/bin/env python3
"""
Tiny flat-file CMS generator.

Content lives in content/case-studies.json.
This script renders each entry into case-studies/<slug>.html using the
shared site header/footer/theme so pages stay visually consistent with
the homepage. Re-run after editing the JSON to rebuild the pages.

Usage: python3 generate.py
"""
import json
import os
import html

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(ROOT, "content", "case-studies.json")
OUT_DIR = os.path.join(ROOT, "case-studies")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    case_studies = json.load(f)

by_slug = {c["slug"]: c for c in case_studies}

NAV = """
<header class="nav" id="nav">
  <div class="nav-inner container">
    <a href="../index.html" class="logo">VK<span class="dot">.</span></a>
    <nav class="nav-links" id="navLinks">
      <a href="../index.html#work">Real Projects</a>
      <a href="https://www.behance.net/varunkanojia" target="_blank" rel="noopener">Behance</a>
      <a href="../index.html#testimonials">Testimonials</a>
      <a href="../index.html#contact">Contact</a>
    </nav>
    <div class="nav-actions">
      <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode">
        <svg class="icon-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
        <svg class="icon-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1111.2 3 7 7 0 0021 12.8z"/></svg>
      </button>
      <a class="btn btn-primary btn-sm" href="https://drive.google.com/file/d/1HTufMe9qsli9R8VEX-VsirYOaF5EsAQ_/view?usp=sharing" target="_blank" rel="noopener">Download Resume</a>
      <button class="hamburger" id="hamburger" aria-label="Open menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="mobile-menu" id="mobileMenu">
  <a href="../index.html#work">Real Projects</a>
  <a href="https://www.behance.net/varunkanojia" target="_blank" rel="noopener">Behance</a>
  <a href="../index.html#testimonials">Testimonials</a>
  <a href="../index.html#contact">Contact</a>
  <a class="btn btn-primary" href="https://drive.google.com/file/d/1HTufMe9qsli9R8VEX-VsirYOaF5EsAQ_/view?usp=sharing" target="_blank" rel="noopener">Download Resume</a>
</div>
"""

FOOTER = """
<footer class="footer">
  <div class="container footer-inner">
    <div>
      <a href="../index.html" class="logo">VK<span class="dot">.</span></a>
      <p>Designing intuitive products that help businesses grow and users feel at home.</p>
    </div>
    <div class="footer-links">
      <p class="footer-heading">Socials</p>
      <a href="https://www.linkedin.com/in/varun-kanojia-a55846212/" target="_blank" rel="noopener">LinkedIn</a>
      <a href="https://www.behance.net/varunkanojia" target="_blank" rel="noopener">Behance</a>
    </div>
  </div>
  <div class="container footer-bottom">
    <p>&copy; 2026 Varun Kanojia &middot; All Rights Reserved</p>
  </div>
</footer>
"""


def esc(s):
    return html.escape(s, quote=False)


def render_paragraphs(paragraphs):
    return "\n".join(f"<p>{esc(p)}</p>" for p in paragraphs)


def render_steps(steps):
    out = []
    for i, step in enumerate(steps, start=1):
        out.append(f"""
      <div class="cs-step">
        <div class="cs-step-num">{i:02d}</div>
        <div>
          <h3>{esc(step['title'])}</h3>
          <p>{esc(step['body'])}</p>
        </div>
      </div>""")
    return "\n".join(out)


def render_results(results):
    out = []
    for r in results:
        out.append(f"""
      <div class="cs-result">
        <div class="cs-result-value">{esc(r['value'])}</div>
        <div class="cs-result-label">{esc(r['label'])}</div>
      </div>""")
    return "\n".join(out)


def nav_card(slug, eyebrow, css_class):
    c = by_slug[slug]
    return f"""
    <a class="cs-nav-link {css_class}" href="{c['slug']}.html">
      <span class="cs-nav-eyebrow">{eyebrow}</span>
      <span class="cs-nav-title">{esc(c['title'])}</span>
    </a>"""


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title} — Varun Kanojia</title>
<meta name="description" content="{summary}" />

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../styles.css" />
</head>
<body>
<div class="grain" aria-hidden="true"></div>
{nav}

<main id="top">
  <div class="container breadcrumb">
    <a href="../index.html">Home</a> <span>/</span> <a href="../index.html#work">Work</a> <span>/</span> <span>{title}</span>
  </div>

  <section class="cs-hero container">
    <p class="eyebrow"><span class="eyebrow-dot"></span>{tag}</p>
    <h1>{title}</h1>
    <p class="section-sub">{summary}</p>

    <div class="cs-cover {cover}">
      <svg width="46" height="46" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3"><path d="M12 2c1.5 3 1.5 5-0 8-1.5-3-1.5-5 0-8zM12 22c-1.5-3-1.5-5 0-8 1.5 3 1.5 5 0 8zM2 12c3-1.5 5-1.5 8 0-3 1.5-5 1.5-8 0zM22 12c-3 1.5-5 1.5-8 0 3-1.5 5-1.5 8 0z"/><circle cx="12" cy="12" r="2.4"/></svg>
    </div>

    <div class="cs-meta">
      <div><span class="cs-meta-label">Role</span><span class="cs-meta-value">{role}</span></div>
      <div><span class="cs-meta-label">Timeline</span><span class="cs-meta-value">{timeline}</span></div>
      <div><span class="cs-meta-label">Platform</span><span class="cs-meta-value">{platform}</span></div>
      <div><span class="cs-meta-label">Tools</span><span class="cs-meta-value">{tools}</span></div>
    </div>
  </section>

  <section class="cs-section container">
    {overview}
  </section>

  <section class="cs-section container">
    <h2>{problem_heading}</h2>
    {problem_body}
  </section>

  <section class="cs-section container">
    <h2>{approach_heading}</h2>
    <div class="cs-steps">
      {approach_steps}
    </div>
  </section>

  <section class="cs-section container">
    <h2>{solution_heading}</h2>
    {solution_body}
  </section>

  <section class="container">
    <blockquote class="cs-quote">{pull_quote}</blockquote>
  </section>

  <section class="cs-section container" style="border-top:none;">
    <h2>Results</h2>
    <div class="cs-results">
      {results}
    </div>
  </section>

  <section class="container cs-nav">
    {prev_card}
    {next_card}
  </section>
</main>

{footer}
<script src="../script.js"></script>
</body>
</html>
"""

os.makedirs(OUT_DIR, exist_ok=True)

for c in case_studies:
    page = PAGE_TEMPLATE.format(
        title=esc(c["title"]),
        summary=esc(c["summary"]),
        tag=esc(c["tag"]),
        cover=c["cover"],
        role=esc(c["meta"]["role"]),
        timeline=esc(c["meta"]["timeline"]),
        platform=esc(c["meta"]["platform"]),
        tools=esc(c["meta"]["tools"]),
        overview=render_paragraphs(c["overview"]),
        problem_heading=esc(c["problem"]["heading"]),
        problem_body=render_paragraphs(c["problem"]["body"]),
        approach_heading=esc(c["approach"]["heading"]),
        approach_steps=render_steps(c["approach"]["steps"]),
        solution_heading=esc(c["solution"]["heading"]),
        solution_body=render_paragraphs(c["solution"]["body"]),
        pull_quote=esc(c["pullQuote"]),
        results=render_results(c["results"]),
        prev_card=nav_card(c["prev"], "Previous", "prev"),
        next_card=nav_card(c["next"], "Next", "next"),
        nav=NAV,
        footer=FOOTER,
    )
    out_path = os.path.join(OUT_DIR, f"{c['slug']}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"built {out_path}")

print(f"\n{len(case_studies)} case study pages generated.")
