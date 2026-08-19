# NexaBoard Portfolio V7 — Design

## Objectif

Ajouter NexaBoard comme vingtième projet et nouvelle étude de cas principale du portfolio, sans modifier le système visuel existant ni introduire de dépendance incompatible avec GitHub Pages.

## Positionnement

Le projet est présenté comme une application collaborative full-stack professionnelle distincte d’EventFlow par sa stack Vue 3 / TypeScript / Django REST Framework / PostgreSQL. La page doit valoriser la conception du Kanban, l’authentification JWT, les permissions multi-niveaux, les agrégations du dashboard, la documentation OpenAPI, la conteneurisation et la CI.

## Architecture éditoriale

- Carte en première position dans la catégorie `web`.
- Étude de cas avec contexte, solution, huit blocs d’architecture, huit difficultés, dix apprentissages et huit évolutions.
- Six visuels cohérents avec le design du portfolio : interface, architecture, déplacement Kanban transactionnel, authentification, modèle métier/permissions et CI/déploiement.
- Traçabilité des affirmations dans `docs/SOURCES_PROJETS_V7.md`.

## Contraintes de fiabilité

Les éléments décrits doivent provenir du ZIP fourni. Les 8 tests Django et 3 tests Vitest sont comptés dans les fichiers, mais ne doivent pas être présentés comme exécutés car les dépendances et Docker ne sont pas disponibles dans l’environnement. Les contrôles statiques réellement exécutés doivent être distingués des tests d’exécution non lancés.

## Mise à jour globale

- 20 projets documentés.
- 50+ technologies pratiquées.
- Ajout des technologies Vue.js 3, TypeScript, Pinia, Tailwind CSS 4, Chart.js, Django 5.2, Django REST Framework, SimpleJWT, Swagger/OpenAPI, Gunicorn, GitHub Actions et Vitest dans les compétences.
- Mise à jour de l’introduction et de la section À propos pour citer NexaBoard.
