#!/usr/bin/env python3
"""Regression tests for the two added data projects and the simplified hero."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location("build_site", ROOT / "tools" / "build_site.py")
assert spec and spec.loader
build_site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_site)


class PortfolioUpdateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads((ROOT / "content" / "portfolio.json").read_text(encoding="utf-8"))
        cls.projects = {project["slug"]: project for project in cls.data["projects"]}

    def test_portfolio_retains_the_added_projects_and_metric_matches_content(self) -> None:
        self.assertGreaterEqual(len(self.data["projects"]), 18)
        self.assertEqual(str(len(self.data["projects"])), self.data["metrics"][0]["value"])
        self.assertEqual("projets documentés", self.data["metrics"][0]["label"])

    def test_advanced_database_case_study_is_complete(self) -> None:
        project = self.projects["entrepot-donnees-apache-hop-olap"]
        self.assertEqual("data", project["category"])
        self.assertIn("Apache Hop", project["stack"])
        self.assertIn("MDX", project["stack"])
        self.assertGreaterEqual(len(project["architecture"]), 3)
        self.assertGreaterEqual(len(project["challenges"]), 3)
        self.assertGreaterEqual(len(project["learnings"]), 4)
        self.assertGreaterEqual(len(project["images"]), 4)
        self.assertEqual("Voir mon GitHub", project["source_label"])

    def test_streamscope_case_study_is_complete(self) -> None:
        project = self.projects["streamscope-power-bi"]
        self.assertEqual("data", project["category"])
        self.assertIn("Power BI", project["stack"])
        self.assertIn("DAX", project["stack"])
        self.assertIn("Power Query", project["stack"])
        self.assertGreaterEqual(len(project["architecture"]), 3)
        self.assertGreaterEqual(len(project["challenges"]), 3)
        self.assertGreaterEqual(len(project["learnings"]), 4)
        self.assertGreaterEqual(len(project["images"]), 5)
        self.assertEqual("Voir mon GitHub", project["source_label"])

    def test_home_hero_has_no_floating_formation_or_domains_notes(self) -> None:
        home = build_site.render_home(self.data)
        self.assertNotIn('class="floating-note', home)
        self.assertNotIn("Formation actuelle", home)
        self.assertNotIn("Master ASI — ETNA", home)
        self.assertNotIn("<small>Domaines</small>", home)

    def test_home_project_count_is_generated_from_content(self) -> None:
        home = build_site.render_home(self.data)
        self.assertIn(f"{len(self.data["projects"])} projets affichés", home)
        self.assertIn("projects/entrepot-donnees-apache-hop-olap.html", home)
        self.assertIn("projects/streamscope-power-bi.html", home)

    def test_new_projects_use_the_configured_github_labels(self) -> None:
        home = build_site.render_home(self.data)
        for slug in ("entrepot-donnees-apache-hop-olap", "streamscope-power-bi"):
            project = self.projects[slug]
            page = build_site.render_project(
                self.data, project, self.data["projects"].index(project)
            )
            self.assertIn(">Voir mon GitHub ", page)
            self.assertIn(f'href="projects/{slug}.html"', home)
        self.assertGreaterEqual(home.count(" GitHub</a>"), 2)

    def test_project_grid_uses_a_uniform_three_column_layout(self) -> None:
        css = (ROOT / "assets" / "css" / "styles.css").read_text(encoding="utf-8")
        self.assertIn("grid-column: span 4", css)
        self.assertNotIn(".project-card-8", css)
        self.assertNotIn(".project-card-9", css)

    def test_new_project_assets_exist(self) -> None:
        for slug in ("entrepot-donnees-apache-hop-olap", "streamscope-power-bi"):
            project = self.projects[slug]
            for image in [project["cover"], *project["images"]]:
                self.assertTrue((ROOT / image).is_file(), image)


if __name__ == "__main__":
    unittest.main(verbosity=2)
