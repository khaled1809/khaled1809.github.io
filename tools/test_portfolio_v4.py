#!/usr/bin/env python3
"""Regression tests for the Docker data-visualisation project and four coursework domains."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEW_SLUGS = (
    "visualisation-ventes-docker-graphql",
    "vision-par-ordinateur",
    "apprentissage-profond",
    "apprentissage-avance",
    "analyse-donnees-statistiques",
)

spec = importlib.util.spec_from_file_location("build_site", ROOT / "tools" / "build_site.py")
assert spec and spec.loader
build_site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_site)


class PortfolioV4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads((ROOT / "content" / "portfolio.json").read_text(encoding="utf-8"))
        cls.projects = {project["slug"]: project for project in cls.data["projects"]}

    def test_portfolio_retains_v4_projects_and_metrics_can_grow(self) -> None:
        self.assertGreaterEqual(len(self.data["projects"]), 18)
        self.assertEqual(str(len(self.data["projects"])), self.data["metrics"][0]["value"])
        self.assertGreaterEqual(int(self.data["metrics"][1]["value"]), 7)
        self.assertGreaterEqual(int(self.data["metrics"][2]["value"].rstrip("+")), 40)
        for slug in NEW_SLUGS:
            self.assertIn(slug, self.projects)

    def test_home_exposes_the_extended_ai_filter_and_all_new_pages(self) -> None:
        home = build_site.render_home(self.data)
        self.assertIn('data-project-filter="ai"', home)
        self.assertIn(">IA &amp; ML</button>", home)
        self.assertIn(f"{len(self.data["projects"])} projets affichés", home)
        for slug in NEW_SLUGS:
            self.assertIn(f'href="projects/{slug}.html"', home)

    def test_docker_data_visualisation_case_study_matches_the_supplied_code(self) -> None:
        project = self.projects["visualisation-ventes-docker-graphql"]
        self.assertEqual("data", project["category"])
        for technology in (
            "Docker Compose",
            "MongoDB",
            "GraphQL",
            "Apollo Server",
            "Node.js",
            "D3.js",
            "TopoJSON",
        ):
            self.assertIn(technology, project["stack"])
        combined = " ".join(
            [
                project["problem"],
                project["solution"],
                *(item["text"] + " " + item["resolution"] for item in project["challenges"]),
            ]
        ).lower()
        for evidence in ("$facet", "$match", "prestationsbydpt", "departmentstats"):
            self.assertIn(evidence, combined)
        self.assertNotIn("localhost", combined)
        self.assertGreaterEqual(len(project["architecture"]), 4)
        self.assertGreaterEqual(len(project["challenges"]), 4)
        self.assertGreaterEqual(len(project["learnings"]), 5)
        self.assertGreaterEqual(len(project["images"]), 5)

    def test_computer_vision_case_study_covers_the_completed_notebooks(self) -> None:
        project = self.projects["vision-par-ordinateur"]
        self.assertEqual("ai", project["category"])
        for technology in (
            "OpenCV",
            "NumPy",
            "SciPy",
            "scikit-image",
            "Canny",
            "Hough",
            "Harris",
            "Morphologie mathématique",
        ):
            self.assertIn(technology, project["stack"])
        combined = " ".join([project["solution"], *project["learnings"]]).lower()
        for concept in ("otsu", "squelett", "regionprops", "sobel"):
            self.assertIn(concept, combined)
        self.assertGreaterEqual(len(project["architecture"]), 4)
        self.assertGreaterEqual(len(project["challenges"]), 4)
        self.assertGreaterEqual(len(project["images"]), 5)

    def test_deep_learning_case_study_is_technical_and_transparent_about_results(self) -> None:
        project = self.projects["apprentissage-profond"]
        self.assertEqual("ai", project["category"])
        for technology in (
            "PyTorch",
            "PyTorch Lightning",
            "Torchvision",
            "Torchmetrics",
            "timm",
            "TensorBoard",
            "ResNet18",
        ):
            self.assertIn(technology, project["stack"])
        combined = " ".join(
            [project["problem"], project["solution"], *project["learnings"], *project["next_steps"]]
        ).lower()
        for concept in ("haar", "gtsrb", "forda", "cifar-10"):
            self.assertIn(concept, combined)
        self.assertTrue("sous-ensemble" in combined or "taille limitée" in combined)
        self.assertGreaterEqual(len(project["architecture"]), 4)
        self.assertGreaterEqual(len(project["challenges"]), 4)
        self.assertGreaterEqual(len(project["images"]), 5)

    def test_advanced_learning_case_study_covers_ensemble_rl_and_xai(self) -> None:
        project = self.projects["apprentissage-avance"]
        self.assertEqual("ai", project["category"])
        for technology in (
            "AdaBoost",
            "SVM",
            "GridSearchCV",
            "Gymnasium",
            "SARSA",
            "Q-learning",
            "PyTorch",
            "XAI",
        ):
            self.assertIn(technology, project["stack"])
        combined = " ".join([project["solution"], *project["learnings"], *project["next_steps"]]).lower()
        for concept in ("frozenlake", "replay", "réseau cible", "saliency", "rise"):
            self.assertIn(concept, combined)
        self.assertGreaterEqual(len(project["architecture"]), 4)
        self.assertGreaterEqual(len(project["challenges"]), 4)
        self.assertGreaterEqual(len(project["images"]), 5)

    def test_data_analysis_case_study_covers_statistics_regression_pca_and_clustering(self) -> None:
        project = self.projects["analyse-donnees-statistiques"]
        self.assertEqual("data", project["category"])
        for technology in (
            "Pandas",
            "NumPy",
            "SciPy",
            "scikit-learn",
            "ACP / PCA",
            "K-means",
            "EM / GMM",
            "Régression linéaire",
            "Test du χ²",
            "Mallows Cp",
        ):
            self.assertIn(technology, project["stack"])
        combined = " ".join([project["solution"], *project["learnings"]]).lower()
        for concept in ("old faithful", "onion", "levier", "reconstruction"):
            self.assertIn(concept, combined)
        self.assertGreaterEqual(len(project["architecture"]), 4)
        self.assertGreaterEqual(len(project["challenges"]), 4)
        self.assertGreaterEqual(len(project["images"]), 5)

    def test_new_project_assets_exist(self) -> None:
        for slug in NEW_SLUGS:
            project = self.projects[slug]
            for image in [project["cover"], *project["images"]]:
                self.assertTrue((ROOT / image).is_file(), image)


if __name__ == "__main__":
    unittest.main(verbosity=2)
