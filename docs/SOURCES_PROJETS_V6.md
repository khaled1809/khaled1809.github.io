# Sources et traçabilité — Portfolio V6

Ce document relie l’étude de cas **EventFlow — Plateforme événementielle full-stack sécurisée** aux fichiers effectivement présents dans l’archive `eventflow-fullstack(1).zip`. Les formulations du portfolio décrivent le code et la documentation fournis ; elles n’inventent ni dépôt public, ni mesure de production, ni déploiement réellement observé.

## Périmètre fonctionnel et architecture générale

- `README.md` : fonctionnalités, rôles, parcours, routes API, démarrage Docker et fonctionnement Stripe/mock.
- `docs/SPECIFICATION.md` : périmètre fonctionnel, critères d’acceptation et contraintes du projet.
- `docs/ARCHITECTURE.md` : découpage client/API, choix MySQL et MongoDB, sécurité, paiement et billetterie.
- `docker-compose.yml` : services `client`, `server`, `mysql` et `mongo`, volumes persistants, variables d’environnement, dépendances et healthchecks.
- `client/nginx.conf` : service du bundle React, fallback SPA et reverse proxy de `/api` vers Express.

## Client React

- `client/src/App.jsx` : routes publiques, routes authentifiées et routes administrateur.
- `client/src/context/AuthContext.jsx` : restauration de session avec `/auth/me`, connexion, inscription et déconnexion.
- `client/src/components/ProtectedRoute.jsx` : protection des écrans selon l’authentification et le rôle.
- `client/src/lib/api.js` : client HTTP utilisé par les pages React.
- `client/src/pages/HomePage.jsx`, `EventsPage.jsx` et `EventDetailsPage.jsx` : catalogue public et détail d’un événement.
- `client/src/pages/PaymentSuccessPage.jsx` et `TicketsPage.jsx` : confirmation du paiement et consultation des billets.
- `client/src/pages/AdminEventsPage.jsx`, `SitesPage.jsx`, `UsersPage.jsx` et `TicketVerifyPage.jsx` : administration des événements, sites, rôles et contrôles QR.
- `client/src/styles.css` : design responsive de la SPA.

## API, validation et autorisations

- `server/src/app.js` : initialisation Express, sécurité HTTP, CORS, limitation de débit, route webhook en `express.raw()` avant `express.json()` et montage de l’API.
- `server/src/middleware/auth.js` : lecture du JWT depuis le cookie HTTP-only ou le Bearer token et contrôle des rôles.
- `server/src/middleware/rateLimiters.js` : limitation des requêtes sensibles.
- `server/src/middleware/validate.js` et `server/src/validators/schemas.js` : validation Zod des paramètres, requêtes et corps HTTP.
- `server/src/utils/jwt.js` : création et vérification des jetons JWT.
- `server/src/utils/permissions.js` : règles d’accès testables indépendamment des contrôleurs.
- `server/src/controllers/userController.js` : gestion des rôles et protection contre la rétrogradation du dernier administrateur.

## Persistance MySQL et MongoDB

- `server/src/repositories/siteRepository.js` : CRUD des sites avec requêtes MySQL paramétrées.
- `docker/mysql/init.sql` : création initiale de la table relationnelle.
- `server/src/models/User.js` : utilisateurs, mots de passe hachés et rôles.
- `server/src/models/Event.js` : capacité, `ticketsReserved`, `ticketsSold`, publication et archivage.
- `server/src/models/Order.js` : états de commande et marqueurs `inventoryCommitted`, `reservationReleased`, `paymentFinalizing` et `ticketsIssued`.
- `server/src/models/Ticket.js` : billets, statut et index unique sur `(order, sequence)`.
- `server/src/config/mysql.js` et `server/src/config/mongo.js` : connexions séparées aux deux moteurs de données.

## Réservation, paiement et billetterie

- `server/src/services/paymentService.js` : réservation atomique avec `Event.findOneAndUpdate`, condition `$expr`, incrément de `ticketsReserved`, création Stripe/mock, finalisation idempotente, émission des billets et restitution des places.
- `server/src/controllers/paymentController.js` et `server/src/routes/paymentRoutes.js` : checkout, confirmation et webhook.
- `server/src/config/stripe.js` : initialisation conditionnelle de Stripe.
- `server/src/utils/ticketSignature.js` : HMAC SHA-256 et comparaison constante avec `timingSafeEqual`.
- `server/src/services/ticketService.js` : création du payload QR, vérification et transition atomique du statut `valid` vers `used`.
- `server/src/controllers/ticketController.js` et `server/src/routes/ticketRoutes.js` : consultation, génération du QR et contrôle des billets.

## Validation fournie dans l’archive

- `server/tests/permissions.test.js` : permissions et rôles.
- `server/tests/slug.test.js` : normalisation des slugs.
- `server/tests/ticket-signature.test.js` : signature HMAC, comparaison et payload QR.
- `server/scripts/check-syntax.js` : validation syntaxique des fichiers JavaScript du serveur.
- `docs/postman/EventFlow.postman_collection.json` et `docs/postman/EventFlow.local.postman_environment.json` : scénarios API documentés.
- `docs/VALIDATION.md` : rapport indiquant **8 tests Node réussis** et un contrôle syntaxique réussi sur **39 fichiers JavaScript serveur**.

## Limites de validation conservées dans le portfolio

La documentation fournie précise que le registre npm et Docker n’étaient pas disponibles dans l’environnement de génération initial. La page du portfolio indique donc honnêtement que le téléchargement des dépendances, le build Vite, le démarrage des quatre conteneurs, la collection Postman contre MySQL/MongoDB actifs et le véritable parcours Stripe doivent être rejoués sur une machine équipée. Les visuels EventFlow sont des schémas de documentation technique, et non des captures prétendant montrer un déploiement réel.

Le bouton GitHub reste temporairement dirigé vers le profil général de Khaled Djellali, car aucune URL publique exacte du dépôt EventFlow n’était présente dans l’archive.
