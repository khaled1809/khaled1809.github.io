# Sources et traçabilité — Portfolio V7

## Projet ajouté : NexaBoard

L’étude de cas `nexaboard-project-management` a été construite à partir de l’archive fournie `nexaboard-project-management(1).zip`. Les formulations du portfolio ont été vérifiées contre les fichiers ci-dessous.

### Présentation générale et périmètre

- `README.md` : stack, fonctionnalités, architecture, commandes de lancement et limites de production.
- `docs/ARCHITECTURE.md` : séparation SPA/API/persistance, stores Pinia, permissions et déplacement Kanban transactionnel.
- `docs/API.md` : endpoints d’authentification, projets, tâches, commentaires, équipe et dashboard.
- `docs/SECURITY.md` : access token en mémoire, refresh cookie HttpOnly, rotation, liste noire, autorisations et mot de passe oublié.
- `docs/VALIDATION.md` : commandes prévues, couverture des tests fournis et limites de l’environnement d’origine.

### Frontend Vue.js 3 / TypeScript

- `frontend/src/App.vue` et `frontend/src/main.ts` : initialisation de la SPA.
- `frontend/src/router/index.ts` : routes publiques, privées et gardes de navigation.
- `frontend/src/api/client.ts` : client Axios, access token en mémoire, intercepteurs 401, `refreshPromise` et reprise de requête.
- `frontend/src/api/index.ts` : services REST typés par domaine.
- `frontend/src/stores/auth.ts` : bootstrap de session, connexion, inscription, déconnexion et profil.
- `frontend/src/stores/projects.ts`, `frontend/src/stores/tasks.ts` et `frontend/src/stores/dashboard.ts` : état Pinia, mise à jour optimiste et rollback.
- `frontend/src/components/tasks/KanbanBoard.vue` : colonnes TODO / IN_PROGRESS / DONE et drag & drop avec `vuedraggable`.
- `frontend/src/components/dashboard/StatusChart.vue` : graphique doughnut avec Chart.js et `vue-chartjs`.
- `frontend/src/views/DashboardView.vue` : KPIs, progression des projets, échéances et activité récente.
- `frontend/src/views/ProjectDetailView.vue` : Kanban, vue d’ensemble, équipe, commentaires et formulaires.
- `frontend/src/types/index.ts` : contrats TypeScript pour utilisateurs, projets, tâches, commentaires, activités et dashboard.

### Backend Django REST Framework

- `backend/apps/accounts/models.py` : modèle utilisateur, e-mail unique et rôles `ADMIN`, `MANAGER`, `MEMBER`.
- `backend/apps/accounts/serializers.py` : inscription, authentification, profil et reset de mot de passe.
- `backend/apps/accounts/views.py` : cookie refresh HttpOnly, rotation, blacklist, connexion, déconnexion et réinitialisation.
- `backend/apps/workspace/models.py` : `Project`, `ProjectMembership`, `Task`, `Comment` et `Activity`, contraintes et index.
- `backend/apps/workspace/serializers.py` : synchronisation des membres, validation des dates, assignation limitée au projet et positions de tâches.
- `backend/apps/workspace/views.py` : querysets accessibles, permissions, gestion des membres, commentaires, journal et action Kanban `move` fondée sur `transaction.atomic`, `select_for_update` et `bulk_update`.
- `backend/core/permissions.py` : permissions objet pour projets, tâches et commentaires.
- `backend/apps/dashboard/views.py` : agrégations limitées aux projets accessibles, retards, progression, priorités, échéances et activité.
- `backend/config/settings.py` : SimpleJWT, rotation, blacklist, drf-spectacular, CORS, CSRF et attributs du cookie.
- `backend/config/urls.py` : routes REST, Swagger, OpenAPI, healthcheck et Django Admin.

### Livraison et qualité

- `docker-compose.yml` : PostgreSQL 17, backend Django/Gunicorn, frontend Nginx, volume et healthchecks.
- `backend/Dockerfile` et `backend/entrypoint.sh` : image Python, migrations, seed optionnel et démarrage Gunicorn.
- `frontend/Dockerfile` et `frontend/nginx.conf` : build Vite, service statique, fallback SPA et reverse proxy `/api/`.
- `.github/workflows/ci.yml` : jobs backend et frontend avec tests, contrôle des migrations et build.
- `docs/postman/NexaBoard.postman_collection.json` : collection d’appels API.
- `backend/apps/accounts/tests/test_auth_api.py` : 3 tests d’authentification.
- `backend/apps/workspace/tests/test_project_api.py` : 2 tests de projets et permissions.
- `backend/apps/workspace/tests/test_task_api.py` : 2 tests de tâches, déplacement et commentaires.
- `backend/apps/dashboard/tests/test_dashboard_api.py` : 1 test du dashboard.
- `frontend/src/components/common/__tests__/ProgressBar.spec.ts` et `frontend/src/utils/__tests__/format.spec.ts` : 3 tests Vitest.

## Portée des validations réalisées pour le portfolio

Les dépendances PyPI et npm n’étaient pas téléchargeables et Docker n’était pas installé dans l’environnement de génération. Les **8 tests Django** et **3 tests Vitest** sont donc bien présents dans le projet, mais ils ne sont pas présentés comme exécutés.

Les contrôles effectivement rejoués portent sur :

- la compilation syntaxique des **43 fichiers Python** avec le compilateur Python ;
- l’analyse syntaxique des scripts TypeScript et des blocs `<script setup lang="ts">` des **43 fichiers TypeScript/Vue** avec le compilateur TypeScript disponible localement ;
- la validité des fichiers JSON fournis ;
- la présence des modèles, routes, tests, Dockerfiles, healthchecks, documentation OpenAPI et workflow GitHub Actions cités dans l’étude de cas.

Le build Vite, les migrations Django, la génération OpenAPI, les tests d’exécution et le démarrage Docker doivent être rejoués sur une machine disposant des dépendances et de Docker.

## Visuels

Les fichiers `nexaboard-overview.png`, `nexaboard-architecture.png`, `nexaboard-kanban-transaction.png`, `nexaboard-auth-security.png`, `nexaboard-data-model.png` et `nexaboard-ci-deployment.png` sont des **schémas et reconstitutions de documentation** générés à partir de l’architecture et des composants du code. Ils ne sont pas présentés comme des captures d’un déploiement exécuté dans l’environnement de livraison.
