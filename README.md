# Portfolio de Khaled Djellali

Portfolio statique en français, conçu pour présenter mon profil, mes compétences et mes projets sous forme d’études de cas orientées recrutement.

## Ce qui a été amélioré

- direction visuelle responsive, sobre et professionnelle ;
- compétences regroupées par usage, sans pourcentages arbitraires ;
- dix-neuf pages projet partageables individuellement ;
- sections « difficultés », « décisions techniques », « apprentissages » et « améliorations » ;
- galerie d’images avec agrandissement ;
- navigation mobile, mode clair/sombre, métadonnées SEO et page 404 ;
- structure 100 % statique compatible avec GitHub Pages.

La version actuelle met en avant EventFlow, une plateforme événementielle full-stack développée avec React 19, Express 5, MySQL, MongoDB, Stripe, JWT, QR codes signés, Docker Compose et Nginx. Elle conserve également le jeu 2D Java Swing centré sur Java2D et les patterns State, Observer et Strategy, l’application de visualisation Docker/MongoDB/GraphQL/D3.js et les études de cas issues des travaux pratiques en vision, apprentissage et analyse de données.

## Publier sur GitHub Pages

Aucune installation npm et aucun serveur ne sont nécessaires.

1. Place le contenu de ce dossier à la racine du dépôt GitHub destiné au portfolio.
2. Sur GitHub, ouvre **Settings → Pages**.
3. Dans **Build and deployment**, sélectionne **Deploy from a branch**.
4. Choisis la branche `main` et le dossier `/ (root)`, puis enregistre.
5. Après le prochain push, le site sera publié sur l’adresse GitHub Pages du dépôt.

Le fichier `.nojekyll` demande à GitHub Pages de publier directement les fichiers statiques. Tous les chemins du site sont relatifs : le portfolio fonctionne aussi bien dans un dépôt `utilisateur.github.io` que dans un dépôt publié sous `utilisateur.github.io/nom-du-depot/`.

> GitHub Pages ne peut pas exécuter de PHP, Node.js, MongoDB ou Docker côté serveur. Ces projets sont donc présentés comme études de cas avec leurs architectures et résultats. Une démonstration fonctionnelle de la pile Docker doit être hébergée sur une infrastructure adaptée.

## Modifier le contenu

Le contenu principal se trouve dans :

```text
content/portfolio.json
```

Après une modification, régénère les pages :

```bash
python tools/build_site.py
```

Puis vérifie les liens, les images, la structure HTML et les régressions du portfolio :

```bash
python tools/check_site.py
python -m unittest discover -s tools -p 'test_*.py' -v
```

Le script de génération utilise uniquement la bibliothèque standard de Python. Les pages générées sont directement publiables et ne nécessitent pas Python sur GitHub Pages.

## Fichiers importants

```text
index.html                       Page d’accueil générée
projects/*.html                  Études de cas générées
content/portfolio.json           Profil, compétences et projets
assets/css/styles.css            Design system et responsive
assets/js/site.js                Interactions accessibles
assets/images/                   Portrait et visuels des projets
assets/cv/CvP_Khaled.pdf         CV téléchargeable
tools/build_site.py              Générateur statique
tools/check_site.py              Contrôles avant publication
tools/test_portfolio_update.py   Tests des premiers projets Data
tools/test_portfolio_v3.py       Tests du portrait et des projets IA/NLP
tools/test_portfolio_v4.py       Tests des cinq études de cas Data/IA V4
tools/test_portfolio_v5.py       Tests du jeu Java 2D
tools/test_portfolio_v6.py       Tests de l’étude de cas EventFlow
tools/generate_java_occupation_visuals.py  Générateur des six visuels Java V5
tools/generate_eventflow_visuals.py        Générateur des six schémas EventFlow
docs/SOURCES_PROJETS_V4.md       Traçabilité des fichiers analysés pour la V4
docs/SOURCES_PROJETS_V5.md       Traçabilité du projet Java V5
docs/SOURCES_PROJETS_V6.md       Traçabilité du projet full-stack EventFlow
```

## Avant la publication

Les études de cas ont été rédigées à partir du portfolio initial, des sources, des notebooks et des rapports fournis. Relis chaque formulation technique et ajuste-la si un détail ne correspond pas exactement au rôle que tu as tenu ou au code du dépôt concerné. Un recruteur appréciera davantage une explication précise et défendable qu’une affirmation difficile à démontrer en entretien.

## Visuels de documentation

Les couvertures et schémas d’architecture sont des visuels de documentation créés pour expliquer les flux et responsabilités. Les six visuels EventFlow décrivent l’architecture, les parcours, la réservation, la billetterie et la persistance ; ils ne sont pas présentés comme des captures d’un déploiement réel. Pour les quatre domaines de travaux pratiques, plusieurs galeries intègrent aussi des résultats d’exécution réellement présents dans les notebooks fournis, encadrés sans modifier leurs données. Ils ne doivent pas être présentés comme des résultats généralisables au-delà des jeux et protocoles concernés.
