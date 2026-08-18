#!/usr/bin/env python3
"""Regression tests for the EventFlow full-stack case study."""
from __future__ import annotations
import importlib.util
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SLUG = "eventflow-fullstack"
spec = importlib.util.spec_from_file_location("build_site", ROOT / "tools" / "build_site.py")
assert spec and spec.loader
build_site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_site)

class PortfolioV6Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "content" / "portfolio.json").read_text(encoding="utf-8"))
        cls.projects = {project["slug"]: project for project in cls.data["projects"]}

    def test_portfolio_contains_nineteen_projects_and_eventflow_is_featured_first(self):
        self.assertEqual(19, len(self.data["projects"]))
        self.assertEqual("19", self.data["metrics"][0]["value"])
        self.assertEqual("45+", self.data["metrics"][2]["value"])
        self.assertEqual(SLUG, self.data["projects"][0]["slug"])

    def test_home_links_to_eventflow_and_updates_the_dynamic_count(self):
        home = build_site.render_home(self.data)
        self.assertIn("19 projets affichés", home)
        self.assertIn(f'href="projects/{SLUG}.html"', home)
        self.assertIn("EventFlow — Plateforme événementielle full-stack sécurisée", home)

    def test_eventflow_case_study_matches_the_supplied_monorepo(self):
        project = self.projects[SLUG]
        self.assertEqual("web", project["category"])
        for technology in ("React 19", "Vite", "Express 5", "MySQL", "MongoDB", "Mongoose", "JWT", "Zod", "Stripe Checkout", "HMAC SHA-256", "Nginx", "Docker Compose"):
            self.assertIn(technology, project["stack"])
        combined = " ".join([project["problem"], project["solution"], *(item["title"] + " " + item["text"] for item in project["architecture"]), *(item["title"] + " " + item["text"] + " " + item["resolution"] for item in project["challenges"]), *project["learnings"], *project["next_steps"]]).lower()
        for evidence in ("findoneandupdate", "$expr", "ticketsreserved", "paymentfinalizing", "order, sequence", "timingsafeequal", "express.raw", "dernier administrateur", "healthchecks", "corps brut"):
            self.assertIn(evidence, combined)

    def test_eventflow_is_transparent_about_verification_scope(self):
        project = self.projects[SLUG]
        combined = " ".join([project["solution"], *(item["text"] + " " + item["resolution"] for item in project["challenges"]), *project["next_steps"]]).lower()
        for evidence in ("8 tests node", "39 fichiers", "docker", "build vite", "non exécut"):
            self.assertIn(evidence, combined)

    def test_eventflow_case_study_has_recruiter_ready_depth(self):
        project = self.projects[SLUG]
        self.assertGreaterEqual(len(project["architecture"]), 6)
        self.assertGreaterEqual(len(project["challenges"]), 7)
        self.assertGreaterEqual(len(project["learnings"]), 8)
        self.assertGreaterEqual(len(project["next_steps"]), 7)
        self.assertGreaterEqual(len(project["images"]), 6)
        self.assertEqual("Voir mon GitHub", project["source_label"])

    def test_skills_surface_eventflow_technologies(self):
        skills = [skill for group in self.data["skills"] for skill in [*group["primary"], *group["secondary"]]]
        for skill in ("React 19", "Express 5", "React Router", "Mongoose", "JWT", "Zod", "Stripe Checkout", "Webhooks", "HMAC SHA-256", "Nginx", "RBAC", "Tests Node"):
            self.assertIn(skill, skills)

    def test_all_eventflow_assets_exist(self):
        project = self.projects[SLUG]
        for image in [project["cover"], *project["images"]]:
            self.assertTrue((ROOT / image).is_file(), image)

    def test_eventflow_visual_generator_is_self_contained(self):
        path = ROOT / "tools" / "generate_eventflow_visuals.py"
        self.assertTrue(path.is_file())
        self.assertNotIn("/mnt/data", path.read_text(encoding="utf-8"))
        for filename in ("eventflow-overview.png", "eventflow-architecture.png", "eventflow-user-journeys.png", "eventflow-payment-flow.png", "eventflow-ticket-security.png", "eventflow-polyglot-storage.png"):
            self.assertTrue((ROOT / "assets" / "images" / "projects" / filename).is_file(), filename)

    def test_v6_source_traceability_document_exists(self):
        path = ROOT / "docs" / "SOURCES_PROJETS_V6.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for source_name in ("paymentService.js", "ticketService.js", "ticketSignature.js", "siteRepository.js", "docker-compose.yml", "client/src/App.jsx", "docs/VALIDATION.md"):
            self.assertIn(source_name, text)

if __name__ == "__main__":
    unittest.main(verbosity=2)
