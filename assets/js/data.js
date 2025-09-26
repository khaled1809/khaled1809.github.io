// assets/js/data.js
window.KHALED_DATA = {
  profile: {
    name: "Khaled DJELLALI",
    subtitle: "Développeur — Master 1 Architecte de Systèmes d’Information (ETNA)",
    location: "Paris",
    email: "khaleddjellali189@gmail.com",
    phone: "07 44 40 46 29",
    about: `Actuellement en Master 1 – spécialisation Développement (Architecte de
Systèmes d’Information) à l’ETNA (École des Technologies Numériques
Avancées), en alternance (3 semaines en entreprise / 1 semaine à l’école).
Sérieux et motivé, je suis à la recherche d’une entreprise pour effectuer mon
alternance tout en développant mes compétences techniques et professionnelles`,
    photo: "assets/images/khaled1809.jpg",
    cv: "assets/cv/CvP_Khaled.pdf" 
  },
  skills: [
    {name:"Python", level: 95},
    {name:"Java", level: 95},
    {name:"C", level: 90},
    {name:"C++", level: 80},
    {name:"HTML", level: 95},
    {name:"CSS", level: 95},
    {name:"PHP", level: 90},

    {name:"JavaScript", level: 90},
    {name:"React", level: 85},
    {name:"Node.js", level: 80},
    {name:"Vue.js", level: 60},

    {name:"MySQL", level: 90},
    {name:"PostgreSQL", level: 85},
    {name:"MongoDB.js", level: 80},

    {name:"Git", level: 95},
    {name:"Docker", level: 85},
    {name:"Postman", level: 85},

    {name:"NumPy", level: 85},
    {name:"MatPlotlib", level: 85},
    {name:"Pandas", level: 85},
    {name:"Haskell", level: 70},
    {name:"Pascal", level: 60},

    {name:"Power BI", level: 60},
    {name:"Scala", level: 60},
    {name:"XGBoost.js", level: 60},
    {name:"R", level: 60},

    {name:"Linux", level: 85},
    {name:"Bash", level: 85}
    


  ],
  experiences: [
    { date: "à partir de Octobre 2025", title: "Master 1 Architecte de systèmes d’information - Développement application logicielle -", 
      univ : "Ecole des technologies numériques avancées ( ETNA)" ,
      points: [
     
    ]},
    { date: "2023 -- 2025", title: "Licence en Informatique Générale", 
      univ : "Université de Caen Normandie",
      points: [
      
    ]},
    { date: "2020 - 2023", title: "Licence en Informatique",
      univ : "Université de Béjaia",
      points: [
      
    ]}
  ],

  
  projects: [
    
    {
    name: "Site des Pays",
    desc: "Application web en PHP/MySQL permettant de gérer une base de données des pays du monde (CRUD complet).",
    code: "https://github.com/khaled1809/PaysDuMonde", 
    longDesc: "🌍 Site des Pays du Monde – Description du projet\n\nLe Site des Pays du Monde est une application web dynamique réalisée en HTML, CSS, PHP et MySQL. Elle permet de gérer une base de données contenant des informations sur différents pays à travers un système CRUD complet (ajout, consultation, modification, suppression).\n\nL’utilisateur peut parcourir une liste de pays présentée sur une page d’accueil intuitive, puis cliquer sur un pays pour accéder à une page détaillée. Chaque fiche présente le drapeau du pays, une description textuelle, sa population ainsi que sa surface. Des formulaires sécurisés permettent d’ajouter de nouveaux pays, de modifier les informations existantes ou de supprimer un pays de la base.\n\nSur le plan technique, le projet utilise une base MySQL pour stocker les données et un fichier de configuration centralisé (config.php) pour gérer la connexion. Les drapeaux sont organisés dans un répertoire d’images tandis que les descriptions sont stockées dans des fichiers texte, offrant une structure claire et facile à maintenir. L’architecture du site combine une interface simple côté front-end (HTML/CSS) avec une logique serveur côté back-end (PHP), permettant une mise à jour des données en temps réel.\n\nCe projet illustre parfaitement la création d’une application web complète mêlant interface utilisateur, gestion de contenu multimédia et intégration d’une base de données relationnelle. Il constitue une excellente base pour l’apprentissage du développement web dynamique .",
    images: [
      "assets/images/projects/pays1.png",
      "assets/images/projects/pays2.png",
      "assets/images/projects/pays3.png",
      "assets/images/projects/pays4.png",
      "assets/images/projects/pays5.png",
      "assets/images/projects/pays6.png",
      "assets/images/projects/pays7.png",
      "assets/images/projects/pays8.png",
      "assets/images/projects/pays9.png",
      "assets/images/projects/pays10.png",
      "assets/images/projects/pays11.png",
      "assets/images/projects/pays12.png",
      "assets/images/projects/pays13.png",
      "assets/images/projects/pays14.png",
      "assets/images/projects/pays15.png"

    ]
    },

    {
    name: "Site des Animaux",
    desc: "Application web en PHP/MySQL avec architecture MVC pour gérer une base de données d’animaux (CRUD complet).",
    code: "https://github.com/khaled1809/Animaux",
    longDesc: "🐾 Site des Animaux – Description du projet\n\nLe Site des Animaux est une application web développée en HTML, CSS, PHP et MySQL, reposant sur le modèle architectural MVC (Model–View–Controller). Ce projet met en avant une organisation du code modulaire tout en offrant une gestion complète d’une base de données d’animaux.\n\nL’application permet d’ajouter de nouveaux animaux, d’afficher la liste des animaux enregistrés et de consulter la fiche détaillée de chaque animal. Chaque fiche contient le nom de l’animal, son espèce, son âge ainsi qu’une photo. Grâce à une interface simple et intuitive, l’utilisateur peut parcourir les animaux existants, en créer de nouveaux, ou en supprimer de la base de données.\n\nSur le plan technique, le projet est structuré en plusieurs couches :\n- Model : gère la logique métier et les interactions avec la base de données (création, récupération, mise à jour, suppression des données). \n- View : affiche les pages web et les données sous une interface HTML/CSS responsive.\n- Controller : coordonne les actions de l’utilisateur (ajout, consultation, suppression) et la mise à jour du modèle et de la vue.\n\nLes données sont stockées dans une base MySQL, tandis que la configuration de connexion est centralisée pour faciliter le déploiement. Des classes spécialisées assurent une séparation nette des responsabilités et une maintenance simplifiée.\n\nCe projet illustre parfaitement la mise en pratique du pattern MVC dans le cadre d’un site web dynamique, en combinant une interface utilisateur conviviale, une structure back-end propre et une gestion efficace des données. Il constitue une excellente base pour l’apprentissage de la programmation orientée objet en PHP, la conception MVC et la manipulation de bases de données relationnelles.",
    images: [
      "assets/images/projects/animal4.png",
      "assets/images/projects/animal1.png",
      "assets/images/projects/animal2.png",
      "assets/images/projects/animal3.png",
      "assets/images/projects/animal5.png"
    ]
    },

    {
    name: "Jeu de Stratégie Java",
    desc: "Jeu de stratégie au tour par tour en Java avec IA, génération de labyrinthe et multiples design patterns.",
    code: "https://github.com/khaled1809/JeuStrategie", 
    longDesc: "🎮 Jeu de Stratégie \n\nCe projet est un jeu de stratégie au tour par tour développé entièrement en Java, combinant réflexion, tactique et programmation orientée objet. Le joueur évolue sur une grille dynamique générée aléatoirement sous forme de labyrinthe grâce à un algorithme de backtracking, garantissant une carte unique à chaque partie. \n\n  Principe du jeu\nChaque joueur (humain ou contrôlé par une IA) dispose d’un personnage capable de se déplacer, d’attaquer, de se défendre et de collecter des ressources (munitions, soins, bonus). Le but est de rester le dernier en vie ou d’atteindre des objectifs définis selon le mode de jeu. La partie se déroule en tours successifs, où chaque joueur effectue ses actions avant de laisser la main à l’adversaire.\n\n  Mécaniques de jeu\n- Déplacements : chaque tour, un joueur peut se déplacer dans les directions autorisées par la grille (en évitant les murs, pièges ou zones interdites).\n- Attaques : les armes disponibles (pistolets, bombes, etc.) possèdent des comportements spécifiques (tir directionnel, explosion en zone) et nécessitent des munitions.\n- Défense et stratégie : il est possible de lever un bouclier ou de se positionner derrière des obstacles pour éviter les dégâts.\n- Objets et bonus : des cases spéciales distribuent des bonus de santé, des munitions ou des améliorations temporaires.\n- Pièges : des mines et pièges cachés peuvent surprendre l’adversaire et renverser la situation.\n\n 🧠 Système de Stratégies\nLes joueurs, qu’ils soient humains ou IA, peuvent adopter différentes stratégies implémentées via le design pattern Strategy :\n- Aggressive : recherche l’attaque frontale et la confrontation directe.\n- Defensive : privilégie la survie, en évitant les affrontements et en collectant des ressources.\n- Random : agit de manière imprévisible pour déstabiliser l’adversaire.\n- Offensive ciblée : combine collecte de ressources et attaques précises pour éliminer rapidement les menaces prioritaires.\n\n 🏗️ Architecture logicielle\nLe projet illustre une conception logicielle avancée avec une architecture MVC (Model-View-Controller) et l’intégration de nombreux design patterns :\n- Singleton : assure une instance unique du jeu et de la grille.\n- Observer : synchronise en temps réel le modèle (logique de jeu) et la vue (interface graphique).\n- Strategy : gère les comportements dynamiques des joueurs et des armes.\n- Command : encapsule chaque action (tir, déplacement, défense) sous forme d’objet exécutable.\n- State : permet aux cases de la grille de changer de comportement en fonction de leur contenu (joueur, bombe, bonus, etc.).\n- Composite : déléguant l’interaction d’un joueur à l’objet contenu dans chaque case.\n- Template Method : définit un squelette d’action pour les armes, laissant les sous-classes personnaliser l’exécution (ex : Bomb vs Gun).\n- Facade : centralise la gestion des entités du jeu (joueurs, armes) via des gestionnaires dédiés.\n\n 💻 Interface et gameplay\nLe jeu peut être lancé en mode terminal pour une version texte ou en interface graphique (Java Swing/JavaFX) offrant une vue complète du plateau :\n- Grille dynamique : représentation visuelle des murs, bonus, pièges et positions des joueurs.\n- Panneau de contrôle : permet de lancer les actions (tir, mouvement, défense) ou de passer le tour.\n- Journal des actions : affiche en temps réel les mouvements, attaques et événements clés.\n\n ⚡ Points forts\n- Labyrinthe unique à chaque partie grâce à l’algorithme de génération procédurale.\n- IA adaptable avec plusieurs styles de jeu, offrant une rejouabilité élevée.\n- Architecture robuste et modulaire, facilitant l’ajout de nouvelles armes, stratégies ou types de cases.\n- Mode multijoueur local (selon configuration) permettant des parties contre d’autres joueurs humains ou des IA.\n\nCe projet illustre l’application concrète de concepts avancés de programmation orientée objet, la conception modulaire et la maîtrise de multiples design patterns. Il constitue une base solide pour développer des jeux plus complexes.",
    images: [
      "assets/images/projects/strat4.png",
      "assets/images/projects/strat1.png",
      "assets/images/projects/strat2.png",
      "assets/images/projects/strat3.png",
      "assets/images/projects/strat5.png",
      "assets/images/projects/strat6.png",
      "assets/images/projects/strat7.png",
      "assets/images/projects/strat8.png"
    ]
    },

    {
    name: "Jeu de la Vie",
    desc: "Simulation du célèbre automate cellulaire de John Conway en Java avec interface graphique et génération aléatoire.",
    code: "https://github.com/khaled1809/GameOfLife",
    longDesc: "🧬 Jeu de la Vie – Simulation d’automate cellulaire\n\nCe projet est une implémentation complète du Jeu de la Vie de John Conway, développé en Java, qui simule l’évolution d’une population de cellules selon des règles simples mais générant des comportements complexes. Il permet de visualiser en temps réel l’émergence de motifs dynamiques, stables ou chaotiques, dans une grille bidimensionnelle.\n\n 🌱 Principe du jeu\nLe Jeu de la Vie n’est pas un véritable « jeu » mais un automate cellulaire :\n- L’univers est une grille composée de cellules pouvant être *vivantes* ou *mortes*.\n- À chaque génération, l’état de chaque cellule dépend de ses voisins immédiats selon 4 règles :\n  1. Une cellule vivante avec moins de 2 voisins vivants meurt (sous-population).\n  2. Une cellule vivante avec 2 ou 3 voisins vivants survit.\n  3. Une cellule vivante avec plus de 3 voisins vivants meurt (surpopulation).\n  4. Une cellule morte avec exactement 3 voisins vivants devient vivante (reproduction).\n\nÀ partir d’une configuration initiale (fixe ou aléatoire), l’évolution génère des structures étonnantes : oscillateurs, vaisseaux glisseurs (gliders), figures stables, etc.\n\n ⚙️ Fonctionnalités\n- Grille paramétrable : définition de la taille de la grille et du taux d’occupation initial.\n- Évolution automatique : calcul et affichage des générations en temps réel.\n- Contrôles interactifs : boutons *Start*, *Pause*, *Reset* pour gérer la simulation.\n- Mode aléatoire : génération d’une configuration initiale aléatoire.\n- Placement manuel : possibilité d’activer/désactiver des cellules avant le lancement.\n\n 🏗️ Architecture du projet\nLe projet adopte une conception orientée objet claire, facilitant la compréhension et l’extension :\n- Model : gère l’état interne de la grille et l’application des règles d’évolution.\n- View : interface graphique (Java Swing/JavaFX) permettant de visualiser la grille et d’interagir avec la simulation.\n- Controller : assure la communication entre la vue et le modèle, en déclenchant les mises à jour à chaque génération.\n\n 💡 Points techniques\n- Mise en œuvre du pattern Observer pour mettre à jour l’interface en temps réel lorsque la grille évolue.\n- Gestion efficace des générations successives pour un rendu fluide.\n- Code modulaire permettant d’ajouter facilement de nouvelles règles ou variantes (par exemple HighLife, Seeds, etc.).\n\n 🎯 Objectif pédagogique\nCe projet démontre comment un ensemble de règles très simples peut produire des comportements complexes et imprévisibles, illustrant des concepts clés de :\n- Programmation orientée objet (Java),\n- Algorithmes de simulation,\n- Conception logicielle (séparation Model/View/Controller).\n\nLe Jeu de la Vie est une expérience fascinante de complexité émergente : une population évolue spontanément en motifs ordonnés ou chaotiques, offrant une infinité de résultats à partir d’entrées simples.",
    images: [
      "assets/images/projects/life1.png",
      "assets/images/projects/life2.png",
      "assets/images/projects/life3.png",
      "assets/images/projects/life4.png",
      "assets/images/projects/life5.png",
      "assets/images/projects/life6.png",
      "assets/images/projects/life7.png"
      
    ]
    },

    {
    name: "Jeu de Puzzle Coulissant",
    desc: "Jeu de taquin en Java avec interface graphique et mode terminal, architecture MVC complète.",
    code: "https://github.com/khaled1809/JeuPuzzle",
    longDesc: "🧩 Puzzle Coulissant – Jeu de Taquin\n\nCe projet est une implémentation en Java du classique jeu de taquin (ou puzzle coulissant), combinant programmation orientée objet, conception MVC et interaction utilisateur via une interface graphique ou un mode terminal. Le joueur doit reconstituer un puzzle en déplaçant des cases numérotées dans une grille en utilisant la case vide disponible.\n\n  Principe du jeu\nLe jeu se déroule sur une grille de n × m cases, dont une case est vide :\n- Le plateau contient les chiffres de 1 à 8 et une case vide .\n- Le but est de réorganiser les chiffres en ordre croissant (ou de reconstituer une image, selon l’extension) en déplaçant successivement les cases adjacentes vers la case vide.\n- Les déplacements possibles sont : haut, bas, gauche ou droite, mais uniquement si la case voisine est vide.\n- La partie est gagnée lorsque la grille atteint la configuration finale ordonnée.\n\n 🕹️ Fonctionnalités\n- Mélange intelligent : le puzzle est mélangé en effectuant une série de déplacements valides pour garantir une configuration *toujours solvable*.\n- Double mode de contrôle :\n  - Interface graphique : clic sur une case adjacente à la case vide ou utilisation des touches (Z/Q/S/D ou flèches) pour déplacer une case.\n  - Mode terminal : affichage du puzzle dans la console avec contrôle au clavier.\n- Compteur de coups : suivi en temps réel du nombre de déplacements effectués.\n- Mise en évidence : (extension) surlignage des cases déplaçables au survol de la souris pour une meilleure lisibilité.\n- Extension image (optionnelle) : découpage d’une image en `n × m` morceaux pour créer un puzzle visuel tout en conservant la même logique interne.\n\n 🏗️ Architecture logicielle\nLe projet suit une conception MVC (Model – View – Controller), garantissant une séparation claire des responsabilités :\n- Modèle (`ModeleTaquin`) : gère la logique du jeu (mélange, déplacement, détection de victoire, compteur de coups). Il est indépendant de l’interface, ce qui permet d’utiliser le même cœur pour le mode terminal et l’interface graphique.\n- Vue (`FrameJeu`, `FenetreJeu`, `VueTerminal`) : gère l’affichage, que ce soit en Swing ou en console.\n- Contrôleur (`ControleurTaquin`, `Ecouteur`) : fait le lien entre les actions de l’utilisateur (clics ou touches clavier) et les mises à jour du modèle.\n\n ⚡ Points techniques\n- Architecture MVC : séparation stricte entre le modèle (logique), la vue (affichage) et le contrôleur (interactions).\n- Algorithme de mélange solvable : la grille est mélangée uniquement via des déplacements successifs de la case vide, garantissant une solution possible à chaque partie.\n- Gestion d’événements : écouteurs clavier et souris (classes `CliqueClavier` et `CliqueSouris`) pour détecter les actions en temps réel.\n- Flexibilité : le modèle peut être utilisé tel quel pour créer des variantes (taille de grille, image découpée, nouveaux modes de jeu).\n- Performance : affichage fluide et réactif même sur des grilles de grande taille.\n- Mode console : version terminal indépendante de la vue graphique, idéale pour les tests et les environnements légers.\n\n 💻 Modes de jeu\n- Mode terminal : jouable directement en console, avec affichage textuel et commandes clavier.\n- Interface graphique : propose un plateau interactif, un compteur de coups et des surlignages dynamiques.\n\n 🚀 Extensions possibles\n- Image personnalisée : remplacement des numéros par des morceaux d’image, permettant de recréer un puzzle visuel.\n- Indicateur de difficulté : ajout de niveaux de mélange (facile, moyen, difficile) avec un nombre de mouvements de mélange configurable.\n- Historique des coups : possibilité de revenir en arrière ou de visualiser la solution optimale.\n\nCe projet illustre la puissance de l’architecture MVC et l’importance de la modularité, en proposant un jeu à la fois pédagogique et divertissant qui peut évoluer en de nombreuses variantes (mode image, tailles de grille, IA de résolution).",
    images: [
      "assets/images/projects/puzle1.png",
      "assets/images/projects/puzle2.png"    
    ]
    },


    {
    name: "Visualisation d’Algorithmes de Tri",
      desc: "Comparaison interactive des algorithmes de tri.",
    code: "https://github.com/khaled1809/AlgoTri",
    longDesc: "📊 Étude des Algorithmes de Tri\n\nCe projet est une analyse approfondie des performances de plusieurs algorithmes de tri implémentés en Python. Il permet de mesurer l’efficacité de chaque algorithme selon différents paramètres : taille des données, niveau de désordre, distribution statistique et entropie de Shannon. L’objectif est d’évaluer et de comparer des algorithmes classiques sur des jeux de données variés, tout en visualisant leurs comportements et leurs performances.\n\n 🎯 Objectif\nComprendre comment la structure des données (désordre, entropie, distribution) influence le temps d’exécution, le nombre de comparaisons et les accès mémoire des algorithmes de tri.\n\n ⚡ Fonctionnalités\n- Génération de données selon différentes distributions (uniforme, gaussienne, normale, exponentielle).\n- Application de fonctions de désordre (taux, blocs, ordre inverse, entropie de Shannon) garantissant des scénarios variés.\n- Implémentation et comparaison de 5 algorithmes de tri : Bubble Sort, Selection Sort, Merge Sort, Heap Sort, Bucket Sort.\n- Mesures précises : temps d’exécution, nombre de comparaisons, nombre d’accès mémoire.\n- Exportation des résultats sous forme de tableaux CSV et visualisation via des graphiques et animations (taille, désordre, entropie).\n\n 🏗️ Architecture\n- Scripts Python modulaires (génération de données, fonctions de désordre, algorithmes de tri, affichage graphique).\n- Organisation claire des résultats dans des dossiers data/ (données et résultats) et log/ (journaux d’expérimentation).\n- Utilisation de bibliothèques puissantes comme NumPy, Pandas et Matplotlib pour la manipulation des données et la création des graphiques.\n\n 💡 Points forts\n- Étude expérimentale permettant de confronter la théorie (complexité) à la pratique (temps réel).\n- Visualisation claire de l’évolution des performances en fonction de la taille des données, du désordre et de l’entropie.\n- Architecture flexible facilitant l’ajout de nouveaux algorithmes ou de nouvelles méthodes de génération de données.\n\nCe projet constitue une ressource pédagogique idéale pour explorer les concepts de complexité algorithmique, d’analyse de performance et de traitement de données en Python.",
    images: [
      "assets/images/projects/visu2.png",
      "assets/images/projects/visu1.png",
      "assets/images/projects/visu3.png",
      "assets/images/projects/visu4.png",
      "assets/images/projects/visu5.png",
      "assets/images/projects/visu6.png",
      "assets/images/projects/visu7.png",
      "assets/images/projects/visu8.png",
      "assets/images/projects/visu9.png",
      "assets/images/projects/visu10.png",
      "assets/images/projects/visu11.png"

    ]
    },
    {
      name: "Application Mobile de Gestion des Tâches",
      desc: "Application mobile en React Native avec API REST sécurisée (JWT) pour gérer des listes de tâches et des catégories personnalisées.",
      code: "https://github.com/khaled1809/MobileAppli",
      longDesc: "📱 Application Mobile de Gestion des Tâches\n\nCette application est une solution complète pour organiser les tâches quotidiennes et les classer par catégories (sport, courses, devoirs, etc.). Développée avec React Native, elle offre une expérience fluide sur Android et iOS, combinant une interface moderne et une logique métier robuste.\n\n 🎯 Principe et fonctionnalités\n- Création, suppression et renommage de catégories de tâches (ex. Sport, Courses, Devoirs…).\n- Ajout, suppression et mise à jour de tâches individuelles (ex. Squat, Footing, Mathématiques…).\n- Possibilité de cocher/décocher les tâches terminées ou en cours.\n- Filtrage des tâches (toutes, en cours, terminées).\n- Boutons pour cocher ou décocher toutes les tâches d’un seul geste.\n- Affichage d’une barre de progression dynamique montrant le pourcentage de tâches complétées.\n\n ⚡ Points techniques\n- React Native (Expo) : développement multiplateforme (Android/iOS) avec une interface réactive et performante.\n- API REST sécurisée : interaction avec un back-end via des appels asynchrones (fetch/async/await).\n- Authentification JWT (JSON Web Token) : protection des endpoints pour sécuriser l’accès aux données utilisateur.\n- Context API : gestion globale de l’état (utilisateur, token, données) sans passer par Redux.\n- Navigation : utilisation de React Navigation pour la gestion des écrans (connexion, listes, détails).\n- Composants réutilisables : architecture basée sur des composants modulaires (ListTodoList, TodoList, TodoItem) pour simplifier la maintenance et l’extension.\n- Progress Bar animée : mise à jour en temps réel du pourcentage de tâches accomplies.\n\n 🏗️ Architecture du projet\n- api/ : gestion des requêtes HTTP (création/suppression de listes et tâches, authentification).\n- components/ : composants UI réutilisables (ListTodoList, TodoList, TodoItem, SignIn/SignUp).\n- Context/ : stockage global des informations utilisateur et du token JWT.\n- Screen/ : écrans principaux (Connexion, Inscription, Accueil, Détails des listes).\n- assets/ : ressources graphiques (icônes, images, arrière-plans).\n\n 🚀 Points forts\n- Synchronisation en temps réel des données entre l’API et l’interface.\n- Sécurité renforcée grâce à l’authentification par jeton JWT.\n- Design clair et ergonomique optimisé pour une utilisation mobile quotidienne.\n- Code modulable et extensible, permettant l’ajout futur de nouvelles fonctionnalités (rappels, notifications push, etc.).\n\nCette application illustre l’intégration d’une API sécurisée avec une architecture React Native moderne, offrant une base solide pour développer des applications mobiles complètes et évolutives.",
      images: [
        "assets/images/projects/mobile1.png",
        "assets/images/projects/mobile2.png",
        "assets/images/projects/mobile3.png",
        "assets/images/projects/mobile4.png",
        "assets/images/projects/mobile5.png",
        "assets/images/projects/mobile6.png",
        "assets/images/projects/mobile7.png",
        "assets/images/projects/mobile8.png",
        "assets/images/projects/mobile9.png",
        "assets/images/projects/mobile10.png",
        "assets/images/projects/mobile11.png",
        "assets/images/projects/mobile12.png",
        "assets/images/projects/mobile13.png",
        "assets/images/projects/mobile14.png",
        "assets/images/projects/mobile15.png",
        "assets/images/projects/mobile16.png"
       
      ]
    }

  ]
};
