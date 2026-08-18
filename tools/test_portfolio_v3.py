#!/usr/bin/env python3
"""Regression tests for the three AI/NLP projects and the new portrait."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEW_PORTRAIT_SHA256 = "b9fdb8217c82313eead03352f26d5c7923cf17c1003c44669dde15aaa2f24858"
NEW_SLUGS = (
    "semantic-dna-provenance",
    "reecriture-oulipo-nlp",
    "moteur-deduction-csp",
)

spec = importlib.util.spec_from_file_location("build_site", ROOT / "tools" / "build_site.py")
assert spec and spec.loader
build_site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_site)


class PortfolioV3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads((ROOT / "content" / "portfolio.json").read_text(encoding="utf-8"))
        cls.projects = {project["slug"]: project for project in cls.data["projects"]}

    def test_portfolio_contains_eighteen_projects_and_updated_metrics(self) -> None:
        self.assertEqual(18, len(self.data["projects"]))
        self.assertEqual("18", self.data["metrics"][0]["value"])
        self.assertEqual("7", self.data["metrics"][1]["value"])
        self.assertEqual("40+", self.data["metrics"][2]["value"])
        self.assertEqual(list(NEW_SLUGS), [project["slug"] for project in self.data["projects"][6:9]])

    def test_new_portrait_replaces_the_previous_photo(self) -> None:
        portrait = ROOT / self.data["profile"]["photo"]
        digest = hashlib.sha256(portrait.read_bytes()).hexdigest()
        self.assertEqual(NEW_PORTRAIT_SHA256, digest)

    def test_ai_filter_is_available_on_home_page(self) -> None:
        home = build_site.render_home(self.data)
        self.assertIn('data-project-filter="ai"', home)
        self.assertIn(">IA &amp; ML</button>", home)
        self.assertIn("18 projets affichés", home)

    def test_numbered_project_layout_classes_are_removed(self) -> None:
        home = build_site.render_home(self.data)
        css = (ROOT / "assets" / "css" / "styles.css").read_text(encoding="utf-8")
        self.assertNotIn("project-card-1", home)
        self.assertNotIn(".project-card-1", css)
        self.assertIn("grid-column: span 4", css)

    def test_csp_case_study_is_complete_and_technically_grounded(self) -> None:
        project = self.projects["moteur-deduction-csp"]
        self.assertEqual("ai", project["category"])
        for technology in ("Python", "CSP", "AC-3", "Backtracking", "MRV"):
            self.assertIn(technology, project["stack"])
        self.assertIn("réduction", project["solution"].lower())
        self.assertTrue(any("risque" in item["title"].lower() for item in project["challenges"]))
        self.assertGreaterEqual(len(project["architecture"]), 3)
        self.assertGreaterEqual(len(project["challenges"]), 3)
        self.assertGreaterEqual(len(project["learnings"]), 4)
        self.assertGreaterEqual(len(project["images"]), 5)

    def test_oulipo_case_study_is_complete_and_technically_grounded(self) -> None:
        project = self.projects["reecriture-oulipo-nlp"]
        self.assertEqual("ai", project["category"])
        for technology in ("Python", "spaCy", "WordNet", "Embeddings", "Tkinter"):
            self.assertIn(technology, project["stack"])
        self.assertIn("lipogramme", project["solution"].lower())
        self.assertTrue(any("élision" in item["title"].lower() for item in project["challenges"]))
        self.assertGreaterEqual(len(project["architecture"]), 3)
        self.assertGreaterEqual(len(project["challenges"]), 3)
        self.assertGreaterEqual(len(project["learnings"]), 4)
        self.assertGreaterEqual(len(project["images"]), 5)

    def test_semantic_dna_case_study_is_complete_and_transparent_about_evaluation(self) -> None:
        project = self.projects["semantic-dna-provenance"]
        self.assertEqual("ai", project["category"])
        for technology in ("Python", "spaCy", "Sentence-BERT", "scikit-learn", "LightGBM"):
            self.assertIn(technology, project["stack"])
        combined = " ".join(
            [project["problem"], project["solution"], *project["learnings"], *project["next_steps"]]
        ).lower()
        self.assertIn("corpus", combined)
        self.assertIn("98", combined)
        self.assertTrue(any("seuil" in item["title"].lower() for item in project["challenges"]))
        self.assertTrue(any("biais" in (item["text"] + " " + item["resolution"]).lower() for item in project["challenges"]))
        self.assertGreaterEqual(len(project["architecture"]), 3)
        self.assertGreaterEqual(len(project["challenges"]), 3)
        self.assertGreaterEqual(len(project["learnings"]), 4)
        self.assertGreaterEqual(len(project["images"]), 6)

    def test_new_project_assets_exist(self) -> None:
        for slug in NEW_SLUGS:
            project = self.projects[slug]
            for image in [project["cover"], *project["images"]]:
                self.assertTrue((ROOT / image).is_file(), image)


if __name__ == "__main__":
    unittest.main(verbosity=2)
