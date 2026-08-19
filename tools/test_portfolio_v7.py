#!/usr/bin/env python3
"""Regression tests for the NexaBoard full-stack case study."""
from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "nexaboard-project-management"

spec = importlib.util.spec_from_file_location("build_site", ROOT / "tools" / "build_site.py")
assert spec and spec.loader
build_site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_site)


class PortfolioV7Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "content" / "portfolio.json").read_text(encoding="utf-8"))
        cls.projects = {project["slug"]: project for project in cls.data["projects"]}

    def test_portfolio_contains_twenty_projects_and_nexaboard_is_featured_first(self):
        self.assertEqual(20, len(self.data["projects"]))
        self.assertEqual("20", self.data["metrics"][0]["value"])
        self.assertEqual("50+", self.data["metrics"][2]["value"])
        self.assertEqual(SLUG, self.data["projects"][0]["slug"])

    def test_home_links_to_nexaboard_and_updates_the_dynamic_count(self):
        home = build_site.render_home(self.data)
        self.assertIn("20 projets affichés", home)
        self.assertIn(f'href="projects/{SLUG}.html"', home)
        self.assertIn("NexaBoard — Gestion de projets et tâches collaborative", home)

    def test_nexaboard_case_study_matches_the_supplied_monorepo(self):
        project = self.projects[SLUG]
        self.assertEqual("web", project["category"])
        for technology in (
            "Vue.js 3",
            "TypeScript",
            "Pinia",
            "Tailwind CSS 4",
            "Chart.js",
            "vuedraggable",
            "Python",
            "Django 5.2",
            "Django REST Framework",
            "SimpleJWT",
            "PostgreSQL 17",
            "Swagger / OpenAPI",
            "Docker Compose",
            "Nginx",
            "Gunicorn",
            "GitHub Actions",
            "Vitest",
        ):
            self.assertIn(technology, project["stack"])

        combined = " ".join(
            [
                project["problem"],
                project["solution"],
                *(item["title"] + " " + item["text"] for item in project["architecture"]),
                *(
                    item["title"] + " " + item["text"] + " " + item["resolution"]
                    for item in project["challenges"]
                ),
                *project["learnings"],
                *project["next_steps"],
            ]
        ).lower()
        for evidence in (
            "refresh token",
            "httponly",
            "rotation",
            "liste noire",
            "access token",
            "mémoire",
            "transaction.atomic",
            "select_for_update",
            "kanban",
            "optimiste",
            "rollback",
            "admin",
            "manager",
            "membre",
            "mot de passe",
            "chart.js",
            "drf-spectacular",
            "github actions",
        ):
            self.assertIn(evidence, combined)

    def test_nexaboard_is_transparent_about_verification_scope(self):
        project = self.projects[SLUG]
        combined = " ".join(
            [
                project["solution"],
                *(item["text"] + " " + item["resolution"] for item in project["challenges"]),
                *project["next_steps"],
            ]
        ).lower()
        for evidence in (
            "8 tests django",
            "3 tests vitest",
            "43 fichiers python",
            "43 fichiers typescript/vue",
            "dépendances",
            "docker",
            "non exécut",
        ):
            self.assertIn(evidence, combined)

    def test_nexaboard_case_study_has_recruiter_ready_depth(self):
        project = self.projects[SLUG]
        self.assertGreaterEqual(len(project["architecture"]), 7)
        self.assertGreaterEqual(len(project["challenges"]), 7)
        self.assertGreaterEqual(len(project["learnings"]), 9)
        self.assertGreaterEqual(len(project["next_steps"]), 7)
        self.assertGreaterEqual(len(project["images"]), 6)
        self.assertEqual("Voir mon GitHub", project["source_label"])

    def test_skills_surface_nexaboard_technologies(self):
        skills = [skill for group in self.data["skills"] for skill in [*group["primary"], *group["secondary"]]]
        for skill in (
            "Vue.js 3",
            "TypeScript",
            "Pinia",
            "Tailwind CSS 4",
            "Chart.js",
            "Django 5.2",
            "Django REST Framework",
            "SimpleJWT",
            "Swagger / OpenAPI",
            "Gunicorn",
            "GitHub Actions",
            "Vitest",
        ):
            self.assertIn(skill, skills)

    def test_profile_mentions_nexaboard_as_a_professional_full_stack_project(self):
        profile_text = " ".join([self.data["profile"]["intro"], *self.data["profile"]["about"]]).lower()
        for evidence in ("nexaboard", "vue", "django", "postgre", "kanban"):
            self.assertIn(evidence, profile_text)

    def test_all_nexaboard_assets_exist(self):
        project = self.projects[SLUG]
        for image in [project["cover"], *project["images"]]:
            self.assertTrue((ROOT / image).is_file(), image)

    def test_nexaboard_visual_generator_is_self_contained(self):
        path = ROOT / "tools" / "generate_nexaboard_visuals.py"
        self.assertTrue(path.is_file())
        self.assertNotIn("/mnt/data", path.read_text(encoding="utf-8"))
        for filename in (
            "nexaboard-overview.png",
            "nexaboard-architecture.png",
            "nexaboard-kanban-transaction.png",
            "nexaboard-auth-security.png",
            "nexaboard-data-model.png",
            "nexaboard-ci-deployment.png",
        ):
            self.assertTrue((ROOT / "assets" / "images" / "projects" / filename).is_file(), filename)

    def test_v7_source_traceability_document_exists(self):
        path = ROOT / "docs" / "SOURCES_PROJETS_V7.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for source_name in (
            "KanbanBoard.vue",
            "client.ts",
            "workspace/models.py",
            "workspace/views.py",
            "accounts/views.py",
            "dashboard/views.py",
            "docker-compose.yml",
            ".github/workflows/ci.yml",
            "docs/VALIDATION.md",
        ):
            self.assertIn(source_name, text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
