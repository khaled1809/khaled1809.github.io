#!/usr/bin/env python3
"""Generate the static portfolio pages.

The generated HTML is ready to publish as-is on GitHub Pages. No runtime
framework or server-side language is required.
"""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
CONTENT_PATH = ROOT / "content" / "portfolio.json"
PROJECTS_DIR = ROOT / "projects"


def e(value: Any) -> str:
    """HTML-escape a value."""
    return html.escape(str(value), quote=True)


def prefix(depth: int) -> str:
    return "../" * depth


def asset(path: str, depth: int) -> str:
    return f"{prefix(depth)}{path}"


def icon(name: str, css_class: str = "icon") -> str:
    """Return small accessible decorative SVG icons."""
    paths = {
        "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
        "external": '<path d="M14 5h5v5"/><path d="M10 14 19 5"/><path d="M19 13v6H5V5h6"/>',
        "download": '<path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M5 21h14"/>',
        "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
        "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.69 2.8a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.28-1.28a2 2 0 0 1 2.11-.45c.9.33 1.84.56 2.8.69A2 2 0 0 1 22 16.92z"/>',
        "location": '<path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0z"/><circle cx="12" cy="10" r="2.5"/>',
        "github": '<path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3.3-.4 6.8-1.6 6.8-7A5.4 5.4 0 0 0 19.4 4 5 5 0 0 0 19.3.5S18.2.1 15 1.8a13.4 13.4 0 0 0-7 0C4.8.1 3.7.5 3.7.5A5 5 0 0 0 3.6 4a5.4 5.4 0 0 0-1.4 3.7c0 5.4 3.5 6.6 6.8 7A4.8 4.8 0 0 0 8 18v4"/><path d="M8 19c-3 .9-3-1.5-4-2"/>',
        "linkedin": '<rect x="3" y="9" width="4" height="12"/><path d="M5 3.5a2 2 0 1 0 0 4 2 2 0 0 0 0-4z"/><path d="M11 21v-7a4 4 0 0 1 8 0v7"/><path d="M11 9v12"/>',
        "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.42 1.42M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.42-1.42M17.66 6.34l1.41-1.41"/>',
        "moon": '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>',
        "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
        "close": '<path d="m6 6 12 12M18 6 6 18"/>',
        "check": '<path d="m5 12 4 4L19 6"/>',
        "chevron-left": '<path d="m15 18-6-6 6-6"/>',
        "chevron-right": '<path d="m9 18 6-6-6-6"/>',
        "zoom": '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4M11 8v6M8 11h6"/>',
        "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V4h8v3M3 12h18M10 12v2h4v-2"/>',
        "code": '<path d="m8 9-4 3 4 3M16 9l4 3-4 3M14 5l-4 14"/>',
        "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V4H6.5A2.5 2.5 0 0 0 4 6.5v13z"/><path d="M8 4v13"/>',
    }
    path = paths.get(name, paths["arrow"])
    return (
        f'<svg class="{e(css_class)}" aria-hidden="true" viewBox="0 0 24 24" '
        f'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
        f'stroke-linejoin="round">{path}</svg>'
    )


def page_head(title: str, description: str, depth: int, image: str) -> str:
    css = asset("assets/css/styles.css", depth)
    js = asset("assets/js/site.js", depth)
    favicon = asset("favicon.svg", depth)
    og_image = asset(image, depth)
    return f"""<!doctype html>
<html lang="fr" data-theme="dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{e(description)}">
  <meta name="theme-color" content="#07111f">
  <meta name="color-scheme" content="dark light">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="fr_FR">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:image" content="{e(og_image)}">
  <meta name="twitter:card" content="summary_large_image">
  <title>{e(title)}</title>
  <link rel="icon" href="{e(favicon)}" type="image/svg+xml">
  <link rel="stylesheet" href="{e(css)}">
  <script>
    (() => {{
      document.documentElement.classList.add('js');
      try {{
        const stored = localStorage.getItem('portfolio-theme');
        document.documentElement.dataset.theme = stored || 'dark';
      }} catch (error) {{
        document.documentElement.dataset.theme = 'dark';
      }}
    }})();
  </script>
  <script src="{e(js)}" defer></script>
</head>"""


def site_header(depth: int, active: str = "") -> str:
    home = f"{prefix(depth)}index.html"
    nav_items = [
        ("about", "Profil", f"{home}#about"),
        ("skills", "Compétences", f"{home}#skills"),
        ("journey", "Parcours", f"{home}#journey"),
        ("projects", "Projets", f"{home}#projects"),
    ]
    links = "\n".join(
        f'<a href="{e(href)}" class="nav-link{(" is-active" if key == active else "")}">{e(label)}</a>'
        for key, label, href in nav_items
    )
    return f"""
<a class="skip-link" href="#main-content">Aller au contenu</a>
<header class="site-header" data-site-header>
  <div class="container header-inner">
    <a class="brand" href="{e(home)}" aria-label="Retour à l’accueil de Khaled Djellali">
      <span class="brand-mark" aria-hidden="true">KD</span>
      <span class="brand-copy"><strong>Khaled Djellali</strong><small>Développeur</small></span>
    </a>
    <nav class="primary-nav" id="primary-navigation" aria-label="Navigation principale" data-mobile-nav>
      {links}
      <a class="button button-small button-primary nav-contact" href="{e(home)}#contact">Me contacter {icon('arrow')}</a>
    </nav>
    <div class="header-actions">
      <button class="icon-button theme-toggle" type="button" data-theme-toggle aria-label="Activer le thème clair" title="Changer de thème">
        <span class="theme-icon theme-icon-sun">{icon('sun')}</span>
        <span class="theme-icon theme-icon-moon">{icon('moon')}</span>
      </button>
      <button class="icon-button menu-toggle" type="button" data-menu-toggle aria-controls="primary-navigation" aria-expanded="false" aria-label="Ouvrir le menu">
        <span class="menu-icon-open">{icon('menu')}</span>
        <span class="menu-icon-close">{icon('close')}</span>
      </button>
    </div>
  </div>
</header>"""


def site_footer(profile: dict[str, Any], depth: int) -> str:
    home = f"{prefix(depth)}index.html"
    return f"""
<footer class="site-footer">
  <div class="container footer-grid">
    <div>
      <a class="brand footer-brand" href="{e(home)}">
        <span class="brand-mark" aria-hidden="true">KD</span>
        <span class="brand-copy"><strong>{e(profile['name'])}</strong><small>{e(profile['role'])}</small></span>
      </a>
      <p class="footer-note">Portfolio statique conçu pour être rapide, accessible et directement publiable sur GitHub Pages.</p>
    </div>
    <div class="footer-links" aria-label="Liens de pied de page">
      <a href="{e(profile['github'])}" target="_blank" rel="noopener noreferrer">GitHub {icon('external')}</a>
      <a href="{e(profile['linkedin'])}" target="_blank" rel="noopener noreferrer">LinkedIn {icon('external')}</a>
      <a href="mailto:{e(profile['email'])}">E-mail</a>
    </div>
  </div>
  <div class="container footer-bottom">
    <p>© <span data-current-year></span> {e(profile['name'])}. Tous droits réservés.</p>
    <a href="#top">Retour en haut {icon('chevron-right')}</a>
  </div>
</footer>"""


def tags(items: Iterable[str], limit: int | None = None) -> str:
    selected = list(items)
    if limit is not None:
        selected = selected[:limit]
    return "".join(f'<span class="tech-tag">{e(item)}</span>' for item in selected)


def section_heading(index: str, title: str, intro: str) -> str:
    return f"""
<div class="section-heading" data-reveal>
  <p class="section-number">{e(index)}</p>
  <div>
    <h2>{e(title)}</h2>
    <p>{e(intro)}</p>
  </div>
</div>"""


def render_home(data: dict[str, Any]) -> str:
    profile = data["profile"]
    metrics_html = "".join(
        f'<div class="metric"><strong>{e(item["value"])}</strong><span>{e(item["label"])}</span></div>'
        for item in data["metrics"]
    )
    about_html = "".join(f"<p>{e(paragraph)}</p>" for paragraph in profile["about"])
    strengths_html = "".join(
        f"""<li data-reveal>
          <span class="strength-index">0{i}</span>
          <div><h3>{e(item['title'])}</h3><p>{e(item['text'])}</p></div>
        </li>"""
        for i, item in enumerate(data["strengths"], 1)
    )
    skills_html = "".join(
        f"""<article class="skill-row" data-reveal>
          <div class="skill-row-copy">
            <h3>{e(group['title'])}</h3>
            <p>{e(group['description'])}</p>
          </div>
          <div class="skill-row-tags">
            <div class="tag-group tag-group-primary">{tags(group['primary'])}</div>
            <div class="tag-group tag-group-secondary">{tags(group['secondary'])}</div>
          </div>
        </article>"""
        for group in data["skills"]
    )
    education_html = "".join(
        f"""<li class="timeline-entry" data-reveal>
          <div class="timeline-marker" aria-hidden="true"></div>
          <div class="timeline-date">{e(item['date'])}</div>
          <article class="timeline-card">
            <h3>{e(item['title'])}</h3>
            <p class="timeline-place">{e(item['place'])}</p>
            <ul>{''.join(f'<li>{e(detail)}</li>' for detail in item['details'])}</ul>
          </article>
        </li>"""
        for item in data["education"]
    )
    category_labels = {
        "all": "Tous",
        "ai": "IA & ML",
        "web": "Web",
        "software": "Logiciel",
        "data": "Data",
        "mobile": "Mobile",
    }
    filters_html = "".join(
        f'<button type="button" class="filter-button{(" is-active" if key == "all" else "")}" data-project-filter="{e(key)}" aria-pressed="{str(key == "all").lower()}">{e(label)}</button>'
        for key, label in category_labels.items()
    )
    projects_html = "".join(
        f"""<article class="project-card" data-project-card data-category="{e(project['category'])}" data-reveal>
          <a class="project-media" href="projects/{e(project['slug'])}.html" aria-label="Voir l’étude de cas : {e(project['title'])}">
            <img src="{e(project['cover'])}" alt="Aperçu du projet {e(project['title'])}" loading="lazy" width="1200" height="720">
            <span class="project-media-action" aria-hidden="true">{icon('arrow')}</span>
          </a>
          <div class="project-card-body">
            <div class="project-card-meta"><span>{e(project['category_label'])}</span><span>{e(project['architecture_label'])}</span></div>
            <h3><a href="projects/{e(project['slug'])}.html">{e(project['title'])}</a></h3>
            <p>{e(project['card_summary'])}</p>
            <div class="tag-group">{tags(project['stack'], 4)}</div>
            <div class="project-card-actions">
              <a class="text-link" href="projects/{e(project['slug'])}.html">Étude de cas {icon('arrow')}</a>
              <a class="icon-text-link" href="{e(project['github'])}" target="_blank" rel="noopener noreferrer" aria-label="{e(project.get('source_aria_label', 'Ressource GitHub associée à ' + project['title']))}">{icon('github')} {e(project.get('source_short_label', 'Code'))}</a>
            </div>
          </div>
        </article>"""
        for project in data["projects"]
    )

    title = f"{profile['name']} — {profile['role']}"
    description = "Portfolio de Khaled Djellali : projets logiciel, web, mobile, data, visualisation, machine learning, vision par ordinateur et IA."
    return f"""{page_head(title, description, 0, profile['photo'])}
<body class="home-page" id="top">
{site_header(0, active="")}
<main id="main-content">
  <section class="hero" aria-labelledby="hero-title">
    <div class="hero-grid-overlay" aria-hidden="true"></div>
    <div class="container hero-layout">
      <div class="hero-copy" data-reveal>
        <h1 id="hero-title"><span>{e(profile['name'])}</span>{e(profile['role'])}</h1>
        <p class="hero-headline">{e(profile['headline'])}</p>
        <p class="hero-intro">{e(profile['intro'])}</p>
        <div class="hero-actions">
          <a class="button button-primary" href="#projects">Découvrir mes projets {icon('arrow')}</a>
          <a class="button button-secondary" href="{e(profile['cv'])}" download>Télécharger mon CV {icon('download')}</a>
        </div>
        <div class="availability-block">
          <span class="availability-dot" aria-hidden="true"></span>
          <div><strong>{e(profile['availability'])}</strong><span>{e(profile['schedule'])}</span></div>
        </div>
        <div class="hero-socials" aria-label="Réseaux professionnels">
          <a href="{e(profile['github'])}" target="_blank" rel="noopener noreferrer">{icon('github')} GitHub</a>
          <a href="{e(profile['linkedin'])}" target="_blank" rel="noopener noreferrer">{icon('linkedin')} LinkedIn</a>
          <span>{icon('location')} {e(profile['location'])}</span>
        </div>
      </div>
      <div class="hero-visual" data-reveal>
        <div class="portrait-shell">
          <div class="portrait-backdrop" aria-hidden="true"></div>
          <img src="{e(profile['photo'])}" alt="Portrait professionnel de {e(profile['name'])}" width="374" height="412" fetchpriority="high">
        </div>
      </div>
    </div>
    <div class="container hero-metrics" data-reveal>{metrics_html}</div>
  </section>

  <section class="section about-section" id="about">
    <div class="container">
      {section_heading('01', 'Profil', 'Un parcours construit autour de la programmation, de la conception et de projets concrets.')}
      <div class="about-layout">
        <div class="about-copy prose" data-reveal>{about_html}</div>
        <ol class="strength-list">{strengths_html}</ol>
      </div>
    </div>
  </section>

  <section class="section section-soft" id="skills">
    <div class="container">
      {section_heading('02', 'Compétences', 'Une présentation par domaines d’usage plutôt que des pourcentages difficiles à justifier.')}
      <div class="skills-list">{skills_html}</div>
    </div>
  </section>

  <section class="section" id="journey">
    <div class="container">
      {section_heading('03', 'Parcours', 'Une progression universitaire entre fondamentaux, génie logiciel et architecture applicative.')}
      <ol class="timeline">{education_html}</ol>
    </div>
  </section>

  <section class="section projects-section" id="projects">
    <div class="container">
      <div class="projects-heading-row">
        {section_heading('04', 'Projets sélectionnés', 'Chaque projet est présenté comme une étude de cas : objectif, architecture, difficultés et apprentissages.')}
        <div class="project-filters" aria-label="Filtrer les projets">{filters_html}</div>
      </div>
      <p class="filter-status" data-filter-status aria-live="polite">{len(data['projects'])} projets affichés</p>
      <div class="projects-grid" data-project-grid>{projects_html}</div>
    </div>
  </section>

  <section class="section contact-section" id="contact">
    <div class="container contact-panel" data-reveal>
      <div class="contact-copy">
        <p class="section-number">05</p>
        <h2>Construisons quelque chose d’utile.</h2>
        <p>Je suis disponible pour échanger à propos d’une alternance, d’une mission de développement ou de mes projets.</p>
      </div>
      <div class="contact-actions">
        <a class="button button-light" href="mailto:{e(profile['email'])}">{icon('mail')} {e(profile['email'])}</a>
        <a class="button button-outline-light" href="tel:{e(profile['phone_href'])}">{icon('phone')} {e(profile['phone'])}</a>
      </div>
    </div>
  </section>
</main>
{site_footer(profile, 0)}
</body>
</html>
"""


def render_project(data: dict[str, Any], project: dict[str, Any], index: int) -> str:
    profile = data["profile"]
    projects = data["projects"]
    previous_project = projects[index - 1] if index > 0 else projects[-1]
    next_project = projects[(index + 1) % len(projects)]
    depth = 1

    architecture_html = "".join(
        f"""<article class="architecture-item" data-reveal>
          <span class="architecture-number">0{i}</span>
          <h3>{e(item['title'])}</h3>
          <p>{e(item['text'])}</p>
        </article>"""
        for i, item in enumerate(project["architecture"], 1)
    )
    challenges_html = "".join(
        f"""<article class="challenge-card" data-reveal>
          <span class="challenge-label">Difficulté {i}</span>
          <h3>{e(item['title'])}</h3>
          <p>{e(item['text'])}</p>
          <div class="challenge-resolution"><strong>Approche retenue</strong><p>{e(item['resolution'])}</p></div>
        </article>"""
        for i, item in enumerate(project["challenges"], 1)
    )
    learnings_html = "".join(
        f'<li data-reveal><span>{icon("check")}</span><p>{e(item)}</p></li>' for item in project["learnings"]
    )
    next_steps_html = "".join(f"<li>{e(item)}</li>" for item in project["next_steps"])
    gallery_html = "".join(
        f"""<button class="gallery-item gallery-item-{i + 1}" type="button" data-gallery-item data-src="{e(asset(src, depth))}" data-alt="Visuel {i + 1} du projet {e(project['title'])}">
          <img src="{e(asset(src, depth))}" alt="Visuel {i + 1} du projet {e(project['title'])}" loading="lazy">
          <span class="gallery-zoom" aria-hidden="true">{icon('zoom')}</span>
        </button>"""
        for i, src in enumerate(project["images"])
    )
    facts = [
        ("Rôle", project["role"]),
        ("Type", project["type"]),
        ("Architecture", project["architecture_label"]),
        ("Technologies", " · ".join(project["stack"])),
    ]
    facts_html = "".join(
        f'<div class="project-fact"><dt>{e(label)}</dt><dd>{e(value)}</dd></div>' for label, value in facts
    )
    title = f"{project['title']} — Étude de cas | {profile['name']}"
    description = project["summary"]
    return f"""{page_head(title, description, depth, project['cover'])}
<body class="project-page" id="top">
{site_header(depth, active="projects")}
<main id="main-content">
  <section class="project-hero">
    <div class="project-hero-grid" aria-hidden="true"></div>
    <div class="container">
      <nav class="breadcrumb" aria-label="Fil d’Ariane">
        <a href="../index.html">Accueil</a><span aria-hidden="true">/</span><a href="../index.html#projects">Projets</a><span aria-hidden="true">/</span><span aria-current="page">{e(project['title'])}</span>
      </nav>
      <div class="project-hero-layout">
        <div class="project-hero-copy" data-reveal>
          <p class="project-category">{e(project['category_label'])}</p>
          <h1>{e(project['title'])}</h1>
          <p class="project-summary">{e(project['summary'])}</p>
          <div class="tag-group tag-group-large">{tags(project['stack'])}</div>
          <div class="project-hero-actions">
            <a class="button button-primary" href="{e(project['github'])}" target="_blank" rel="noopener noreferrer">{e(project.get('source_label', 'Voir le code source'))} {icon('external')}</a>
            <a class="button button-secondary" href="../index.html#projects">Retour aux projets {icon('chevron-left')}</a>
          </div>
        </div>
        <figure class="project-cover" data-reveal>
          <img src="{e(asset(project['cover'], depth))}" alt="Aperçu principal du projet {e(project['title'])}" width="1400" height="850">
        </figure>
      </div>
      <dl class="project-facts" data-reveal>{facts_html}</dl>
    </div>
  </section>

  <section class="case-section">
    <div class="container case-layout">
      <article class="case-main">
        <div class="case-block" data-reveal>
          <p class="case-kicker">Contexte</p>
          <h2>Le besoin à résoudre</h2>
          <p>{e(project['problem'])}</p>
        </div>
        <div class="case-block" data-reveal>
          <p class="case-kicker">Approche</p>
          <h2>La solution mise en place</h2>
          <p>{e(project['solution'])}</p>
        </div>
      </article>
      <aside class="case-sidebar" data-reveal>
        <div class="sidebar-card">
          <span class="sidebar-icon">{icon('briefcase')}</span>
          <h2>Ce que ce projet démontre</h2>
          <p>Ma capacité à analyser un problème, organiser les responsabilités et expliquer les compromis techniques au-delà du simple résultat visuel.</p>
          <a class="text-link" href="mailto:{e(profile['email'])}?subject={e('Échange à propos du projet ' + project['title'])}">Échanger sur ce projet {icon('arrow')}</a>
        </div>
      </aside>
    </div>
  </section>

  <section class="case-section section-soft">
    <div class="container">
      <div class="case-heading" data-reveal><p class="case-kicker">Architecture</p><h2>Comment le projet est structuré</h2></div>
      <div class="architecture-grid">{architecture_html}</div>
    </div>
  </section>

  <section class="case-section">
    <div class="container">
      <div class="case-heading" data-reveal><p class="case-kicker">Résolution de problèmes</p><h2>Difficultés rencontrées et décisions prises</h2><p>Les points ci-dessous donnent de la visibilité sur le raisonnement technique, pas seulement sur les fonctionnalités finales.</p></div>
      <div class="challenges-grid">{challenges_html}</div>
    </div>
  </section>

  <section class="case-section learnings-section">
    <div class="container learnings-layout">
      <div class="case-heading" data-reveal><p class="case-kicker">Progression</p><h2>Ce que j’ai appris</h2><p>Des acquis réutilisables dans d’autres projets et dans un contexte professionnel.</p></div>
      <ul class="learnings-list">{learnings_html}</ul>
    </div>
  </section>

  <section class="case-section section-soft">
    <div class="container">
      <div class="case-heading" data-reveal><p class="case-kicker">Galerie</p><h2>Le projet en images</h2><p>Cliquez sur un visuel pour l’agrandir.</p></div>
      <div class="project-gallery">{gallery_html}</div>
    </div>
  </section>

  <section class="case-section">
    <div class="container improvement-panel" data-reveal>
      <div><p class="case-kicker">Prise de recul</p><h2>Ce que j’améliorerais dans une prochaine version</h2></div>
      <ol>{next_steps_html}</ol>
    </div>
  </section>

  <nav class="project-pagination container" aria-label="Navigation entre les projets">
    <a href="{e(previous_project['slug'])}.html" class="pagination-link pagination-previous">
      {icon('chevron-left')}<span><small>Projet précédent</small><strong>{e(previous_project['title'])}</strong></span>
    </a>
    <a href="{e(next_project['slug'])}.html" class="pagination-link pagination-next">
      <span><small>Projet suivant</small><strong>{e(next_project['title'])}</strong></span>{icon('chevron-right')}
    </a>
  </nav>
</main>

<dialog class="lightbox" data-lightbox aria-label="Aperçu agrandi du visuel">
  <button class="icon-button lightbox-close" type="button" data-lightbox-close aria-label="Fermer l’aperçu">{icon('close')}</button>
  <figure><img src="" alt="" data-lightbox-image><figcaption data-lightbox-caption></figcaption></figure>
</dialog>
{site_footer(profile, depth)}
</body>
</html>
"""


def render_404(data: dict[str, Any]) -> str:
    profile = data["profile"]
    title = f"Page introuvable — {profile['name']}"
    description = "La page demandée n’existe pas ou a été déplacée."
    return f"""{page_head(title, description, 0, profile['photo'])}
<body class="error-page" id="top">
{site_header(0)}
<main id="main-content" class="error-main">
  <div class="container error-content" data-reveal>
    <p class="error-code">404</p>
    <h1>Cette page n’existe pas.</h1>
    <p>Le lien est peut-être ancien ou l’adresse contient une erreur.</p>
    <a class="button button-primary" href="index.html">Retour au portfolio {icon('arrow')}</a>
  </div>
</main>
{site_footer(profile, 0)}
</body>
</html>
"""


def validate_content(data: dict[str, Any]) -> None:
    required_profile = ["name", "role", "email", "github", "linkedin", "photo", "cv"]
    for field in required_profile:
        if not data.get("profile", {}).get(field):
            raise ValueError(f"Missing profile field: {field}")

    slugs: set[str] = set()
    for project in data.get("projects", []):
        slug = project.get("slug")
        if not slug or slug in slugs:
            raise ValueError(f"Invalid or duplicate project slug: {slug!r}")
        slugs.add(slug)
        for image in [project.get("cover"), *project.get("images", [])]:
            if not image or not (ROOT / image).is_file():
                raise FileNotFoundError(f"Missing image for {slug}: {image}")

    for path in [data["profile"]["photo"], data["profile"]["cv"]]:
        if not (ROOT / path).is_file():
            raise FileNotFoundError(f"Missing profile asset: {path}")


def main() -> None:
    data = json.loads(CONTENT_PATH.read_text(encoding="utf-8"))
    validate_content(data)
    PROJECTS_DIR.mkdir(exist_ok=True)

    (ROOT / "index.html").write_text(render_home(data), encoding="utf-8")
    for index, project in enumerate(data["projects"]):
        output = PROJECTS_DIR / f"{project['slug']}.html"
        output.write_text(render_project(data, project, index), encoding="utf-8")
    (ROOT / "404.html").write_text(render_404(data), encoding="utf-8")

    print(f"Generated index.html, 404.html and {len(data['projects'])} project pages.")


if __name__ == "__main__":
    main()
