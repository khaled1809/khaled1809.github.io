#!/usr/bin/env python3
"""Run lightweight static checks before publishing the portfolio."""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel", "data", "javascript"}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.links: list[tuple[str, str]] = []
        self.images: list[dict[str, str]] = []
        self.h1_count = 0
        self.lang = ""
        self.title_depth = 0
        self.title_text = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "html":
            self.lang = values.get("lang", "")
        if "id" in values:
            self.ids.append(values["id"])
        if tag == "h1":
            self.h1_count += 1
        if tag == "title":
            self.title_depth += 1
        if tag in {"a", "link"} and values.get("href"):
            self.links.append((tag, values["href"]))
        if tag in {"img", "script", "source"} and values.get("src"):
            self.links.append((tag, values["src"]))
        if tag == "img":
            self.images.append(values)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self.title_depth:
            self.title_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title_text += data


def local_target(page: Path, raw_url: str) -> Path | None:
    url = urlsplit(raw_url)
    if url.scheme in EXTERNAL_SCHEMES or raw_url.startswith("//"):
        return None
    if not url.path:
        return None
    if url.path.startswith("/"):
        raise ValueError("absolute path")
    decoded = unquote(url.path)
    return (page.parent / decoded).resolve()


def check_page(page: Path) -> list[str]:
    errors: list[str] = []
    text = page.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(text)

    relative = page.relative_to(ROOT)
    if not text.lstrip().lower().startswith("<!doctype html>"):
        errors.append(f"{relative}: doctype HTML manquant")
    if parser.lang != "fr":
        errors.append(f"{relative}: attribut lang=fr manquant")
    if parser.h1_count != 1:
        errors.append(f"{relative}: {parser.h1_count} élément(s) h1, 1 attendu")
    if not parser.title_text.strip():
        errors.append(f"{relative}: titre de page vide")

    duplicates = sorted({identifier for identifier in parser.ids if parser.ids.count(identifier) > 1})
    for identifier in duplicates:
        errors.append(f"{relative}: id dupliqué #{identifier}")

    for image in parser.images:
        if "alt" not in image:
            errors.append(f"{relative}: image sans attribut alt ({image.get('src', 'source inconnue')})")
        elif not image.get("alt") and "data-lightbox-image" not in image:
            errors.append(f"{relative}: texte alternatif vide ({image.get('src', 'source inconnue')})")

    for tag, raw_url in parser.links:
        if raw_url == "#":
            errors.append(f"{relative}: lien vide href=#")
            continue
        if raw_url.startswith("/"):
            errors.append(f"{relative}: chemin absolu incompatible avec un dépôt projet ({raw_url})")
            continue
        try:
            target = local_target(page, raw_url)
        except ValueError:
            errors.append(f"{relative}: chemin absolu ({raw_url})")
            continue
        if target is None:
            continue
        if not target.exists():
            errors.append(f"{relative}: ressource introuvable pour {tag} ({raw_url})")

    if re.search(r"(?:localhost|127\.0\.0\.1)", text, flags=re.IGNORECASE):
        errors.append(f"{relative}: référence locale détectée")

    return errors


def main() -> int:
    data = json.loads((ROOT / "content" / "portfolio.json").read_text(encoding="utf-8"))
    expected_pages = {ROOT / "index.html", ROOT / "404.html"}
    expected_pages.update(ROOT / "projects" / f"{project['slug']}.html" for project in data["projects"])

    errors: list[str] = []
    for page in sorted(expected_pages):
        if not page.is_file():
            errors.append(f"Page générée manquante : {page.relative_to(ROOT)}")
            continue
        errors.extend(check_page(page))

    generated_project_pages = set((ROOT / "projects").glob("*.html"))
    unexpected = generated_project_pages - (expected_pages - {ROOT / "index.html", ROOT / "404.html"})
    for page in sorted(unexpected):
        errors.append(f"Page projet orpheline : {page.relative_to(ROOT)}")

    required_files = [
        ROOT / ".nojekyll",
        ROOT / "assets" / "css" / "styles.css",
        ROOT / "assets" / "js" / "site.js",
        ROOT / "favicon.svg",
    ]
    for path in required_files:
        if not path.exists():
            errors.append(f"Fichier requis manquant : {path.relative_to(ROOT)}")

    if errors:
        print("Static site checks failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Static site checks passed for {len(expected_pages)} HTML pages.")
    print(f"Validated {len(data['projects'])} project studies and all local assets.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
