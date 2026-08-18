#!/usr/bin/env python3
"""Regression tests for the Java 2D maximum-space occupation case study."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "jeu-2d-occupation-maximale"

spec = importlib.util.spec_from_file_location("build_site", ROOT / "tools" / "build_site.py")
assert spec and spec.loader
build_site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_site)


class PortfolioV5Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads((ROOT / "content" / "portfolio.json").read_text(encoding="utf-8"))
        cls.projects = {project["slug"]: project for project in cls.data["projects"]}

    def test_portfolio_contains_eighteen_projects_and_new_project_is_featured_first(self) -> None:
        self.assertEqual(18, len(self.data["projects"]))
        self.assertEqual("18", self.data["metrics"][0]["value"])
        self.assertEqual(SLUG, self.data["projects"][0]["slug"])

    def test_home_links_to_the_java_game_and_updates_the_dynamic_count(self) -> None:
        home = build_site.render_home(self.data)
        self.assertIn("18 projets affichés", home)
        self.assertIn(f'href="projects/{SLUG}.html"', home)
        self.assertIn("Jeu 2D d’occupation maximale", home)

    def test_java_game_case_study_matches_the_supplied_source_code(self) -> None:
        project = self.projects[SLUG]
        self.assertEqual("Jeu 2D d’occupation maximale — Java Swing & Design Patterns", project["title"])
        self.assertEqual("software", project["category"])
        for technology in (
            "Java 17",
            "Java Swing",
            "Java2D",
            "MVC",
            "State",
            "Observer",
            "Strategy",
            "Géométrie 2D",
        ):
            self.assertIn(technology, project["stack"])

        combined = " ".join(
            [
                project["problem"],
                project["solution"],
                *(item["title"] + " " + item["text"] for item in project["architecture"]),
                *(item["title"] + " " + item["text"] + " " + item["resolution"] for item in project["challenges"]),
                *project["learnings"],
                *project["next_steps"],
            ]
        ).lower()
        for evidence in (
            "quatre formes",
            "cinq obstacles",
            "prévisualisation",
            "anti-aliasing",
            "cercle–cercle",
            "rectangle–rectangle",
            "cercle–rectangle",
            "surface totale",
        ):
            self.assertIn(evidence, combined)

    def test_case_study_is_transparent_about_current_gameplay_limits(self) -> None:
        project = self.projects[SLUG]
        combined = " ".join(
            [
                project["solution"],
                *(item["text"] + " " + item["resolution"] for item in project["challenges"]),
                *project["next_steps"],
            ]
        ).lower()
        self.assertIn("pas encore", combined)
        self.assertIn("superposition", combined)
        self.assertIn("limites du plateau", combined)
        self.assertIn("condition de victoire", combined)
        self.assertIn("fixedshapestrategy", combined)

    def test_case_study_has_recruiter_ready_depth(self) -> None:
        project = self.projects[SLUG]
        self.assertGreaterEqual(len(project["architecture"]), 5)
        self.assertGreaterEqual(len(project["challenges"]), 5)
        self.assertGreaterEqual(len(project["learnings"]), 6)
        self.assertGreaterEqual(len(project["next_steps"]), 5)
        self.assertGreaterEqual(len(project["images"]), 6)
        self.assertEqual("Voir mon GitHub", project["source_label"])

    def test_software_skills_surface_java2d_and_behavioral_patterns(self) -> None:
        software = next(group for group in self.data["skills"] if group["title"].startswith("Logiciel"))
        tools = software["primary"] + software["secondary"]
        for skill in ("Java Swing", "Java2D", "State", "Observer", "Strategy"):
            self.assertIn(skill, tools)

    def test_all_java_game_assets_exist(self) -> None:
        project = self.projects[SLUG]
        for image in [project["cover"], *project["images"]]:
            self.assertTrue((ROOT / image).is_file(), image)

    def test_visual_generator_is_self_contained_in_the_repository(self) -> None:
        generator = (ROOT / "tools" / "generate_java_occupation_visuals.py").read_text(encoding="utf-8")
        self.assertNotIn("/mnt/data", generator)
        self.assertTrue((ROOT / "assets" / "images" / "projects" / "java-occupation-source-capture.png").is_file())

    def test_v5_source_traceability_document_exists_and_names_key_classes(self) -> None:
        path = ROOT / "docs" / "SOURCES_PROJETS_V5.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for class_name in (
            "GameModel.java",
            "GamePanel.java",
            "MouseController.java",
            "RandomShapeStrategy.java",
            "Circle.java",
            "Rectangle.java",
        ):
            self.assertIn(class_name, text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
