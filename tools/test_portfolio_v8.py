#!/usr/bin/env python3
"""Regression tests for the corrected education timeline in portfolio V8."""
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


class PortfolioV8EducationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "content" / "portfolio.json").read_text(encoding="utf-8"))

    def test_education_timeline_distinguishes_completed_m1_and_future_etna_training(self):
        education = self.data["education"]
        self.assertGreaterEqual(len(education), 4)

        etna = education[0]
        self.assertEqual("À partir d’octobre 2026", etna["date"])
        self.assertEqual(
            "Master Architecte de Systèmes d’Information — Développement applicatif",
            etna["title"],
        )
        self.assertEqual("ETNA — École des Technologies Numériques Avancées", etna["place"])
        self.assertTrue(any("prévue" in detail.lower() for detail in etna["details"]))

        m1 = education[1]
        self.assertEqual("2025 — 2026", m1["date"])
        self.assertEqual(
            "Master 1 Informatique — Intelligence artificielle et sciences des données",
            m1["title"],
        )
        self.assertEqual("Université de Caen Normandie", m1["place"])

    def test_profile_copy_no_longer_claims_etna_started_in_2025(self):
        profile_text = " ".join(
            [self.data["profile"]["subtitle"], *self.data["profile"]["about"]]
        )
        self.assertNotIn("Depuis octobre 2025", profile_text)
        self.assertNotIn("Actuellement en Master 1 Architecte", profile_text)
        self.assertIn("2025–2026", profile_text)
        self.assertIn("octobre 2026", profile_text)
        self.assertIn("Intelligence artificielle et sciences des données", profile_text)

    def test_rendered_home_displays_both_education_entries_without_stale_date(self):
        home = build_site.render_home(self.data)
        self.assertIn("À partir d’octobre 2026", home)
        self.assertIn("2025 — 2026", home)
        self.assertIn(
            "Master 1 Informatique — Intelligence artificielle et sciences des données",
            home,
        )
        self.assertNotIn("Depuis octobre 2025", home)


if __name__ == "__main__":
    unittest.main(verbosity=2)
