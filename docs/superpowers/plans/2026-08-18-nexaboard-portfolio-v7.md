# NexaBoard Portfolio V7 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ajouter NexaBoard comme vingtième étude de cas professionnelle et livrer un ZIP V7 compatible GitHub Pages.

**Architecture:** Le contenu reste piloté par `content/portfolio.json` et généré par `tools/build_site.py`. Un générateur PIL autonome produit six visuels techniques. Les tests V7 valident le contenu, les métriques, les assets et la traçabilité avant génération et empaquetage.

**Tech Stack:** Python 3, JSON, HTML/CSS/JavaScript statiques, Pillow, unittest, Chromium.

## Global Constraints

- Le site final reste entièrement statique et compatible avec GitHub Pages.
- Aucune URL de dépôt NexaBoard ne doit être inventée ; le bouton pointe vers le profil GitHub existant.
- Les tests d’exécution du projet NexaBoard ne doivent pas être revendiqués comme exécutés sans dépendances.
- Les visuels doivent être présentés comme des schémas ou reconstitutions de documentation, pas comme de fausses captures d’un déploiement réel.

---

### Task 1: Tests de régression V7

**Files:**
- Create: `tools/test_portfolio_v7.py`

- [x] Écrire les tests qui exigent 20 projets, NexaBoard en première position, la stack, la profondeur éditoriale, les visuels et la traçabilité.
- [x] Exécuter `python tools/test_portfolio_v7.py` et confirmer l’échec attendu avant implémentation.

### Task 2: Contenu et compétences

**Files:**
- Modify: `content/portfolio.json`
- Create: `docs/SOURCES_PROJETS_V7.md`

- [ ] Ajouter l’étude de cas NexaBoard en première position.
- [ ] Mettre à jour les métriques, le profil et les compétences.
- [ ] Documenter les fichiers sources et les limites de validation.

### Task 3: Visuels NexaBoard

**Files:**
- Create: `tools/generate_nexaboard_visuals.py`
- Create: `assets/images/projects/nexaboard-*.png`

- [ ] Implémenter un générateur PIL autonome dans le système graphique existant.
- [ ] Générer six images 1400 × 850 et vérifier leur lisibilité.

### Task 4: Génération et validation du site

**Files:**
- Regenerate: `index.html`, `404.html`, `projects/*.html`

- [ ] Exécuter le générateur de visuels.
- [ ] Exécuter `python tools/build_site.py`.
- [ ] Exécuter tous les tests Python du portfolio et `python tools/check_site.py`.
- [ ] Contrôler la syntaxe JavaScript et Python.

### Task 5: QA navigateur et livraison

**Files:**
- Create: `/mnt/data/apercu-nexaboard-portfolio-v7.png`
- Create: `/mnt/data/portfolio-khaled-github-pages-v7.zip`
- Create: `/mnt/data/portfolio-khaled-github-pages-v7.sha256`

- [ ] Servir le site localement et vérifier l’accueil ainsi que la page NexaBoard sur ordinateur et mobile.
- [ ] Capturer un aperçu représentatif.
- [ ] Créer le ZIP sans dossier parent, tester l’archive, l’extraire et rejouer les validations.
- [ ] Calculer l’empreinte SHA-256.
