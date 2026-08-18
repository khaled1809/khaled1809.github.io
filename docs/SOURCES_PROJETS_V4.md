# Traçabilité des cinq études de cas ajoutées

Ce document indique les fichiers réellement consultés pour rédiger les nouvelles pages du portfolio. Il permet de distinguer les éléments observés dans les sources, les résultats présents dans les notebooks et les améliorations proposées pour une prochaine version.

## Visualisation de ventes — Docker, GraphQL & D3.js

Fichiers analysés dans `site.zip` :

- `tp8/stack.yml` : quatre services Docker, ports, montage de l’interface et volume MongoDB ;
- `tp8/graphql/index.js` : démarrage d’Apollo Server ;
- `tp8/graphql/model.graphql` : types et requêtes GraphQL ;
- `tp8/graphql/resolvers.js` : connexion MongoDB, pipelines d’agrégation, filtre `$match` dynamique et requête `$facet` ;
- `tp8/ui/france.html` : carte, KPI, graphique, légende, sélection, détails départementaux et états asynchrones ;
- `tp8/ui/prestation.html`, `prestation_bar.html` et `bar.html` : vues complémentaires et exercices D3.js.

Les identifiants présents dans la configuration pédagogique n’ont pas été reproduits dans les pages publiques. La migration vers des variables d’environnement est présentée comme amélioration, car les sources utilisent encore une configuration locale de TP.

## Vision par ordinateur

Notebooks principalement utilisés :

- `RENDU_DJELLALI_khaled_TP_3_1.ipynb` : convolution, lissage, filtres gaussiens, Sobel, Prewitt, Laplacien et LoG ;
- `RENDU_DJELLALI_khaled_TP_3_2.ipynb` : seuillage, morphologie, transformée de distance et squelettisation ;
- `RENDU_DJELLALI_khaled_TP_4.ipynb` : Harris, contours, segmentation, `regionprops`, Hough lignes et cercles ;
- `TPN_VO_25_26.ipynb` : explorations complémentaires sur histogrammes, HSV et détection de formes.

Le dernier notebook contient des parties incomplètes ou à corriger. Elles sont donc présentées comme pistes expérimentales et non comme fonctionnalités finalisées.

## Apprentissage profond

Notebooks analysés :

- `TP1.ipynb` : opérateurs PyTorch et décomposition/reconstruction de Haar ;
- `tp2.ipynb` : premier réseau sur Iris, DataLoader, optimisation, TensorBoard et comparaison SVM ;
- `TP_3.ipynb` : DataModule Lightning, GTSRB, augmentation, ResNet18, Torchmetrics et checkpoints ;
- `ford_io.ipynb` : chargement FordA, visualisation, loaders, baseline et export ;
- `TPN.ipynb` : CIFAR-10, MLP, CNN et expérimentation `resnet18d` avec `timm`.

Les métriques GTSRB varient selon le checkpoint et le split enregistrés. Le portfolio conserve cette réserve et ne transforme pas un résultat obtenu sur 84 images en promesse de généralisation.

## Apprentissage avancé

Notebooks analysés :

- `TP5Souley.ipynb` : AdaBoost scikit-learn, baselines, recherche de paramètres et réimplémentation pédagogique ;
- `TP5_2026 (1).ipynb` : Wine, standardisation, PCA, SVM et GridSearchCV ;
- `TP_renforcement_Khaled_DJELLALI.ipynb` : FrozenLake, SARSA, Q-learning, replay memory et réseau cible ;
- `xai_image_classification_student.ipynb` : inversion de modèle, gradient de saillance et masques de type RISE.

Les sections One-vs-One et certaines boucles XAI ne sont pas entièrement finalisées. Le portfolio les identifie dans les améliorations plutôt que de les présenter comme achevées.

## Analyse de données

Notebooks analysés :

- `DJELLALI_KHALED_TP6.ipynb` : statistiques descriptives, CDF/PDF et KDE ;
- `DJELLALI_KHALED_TP3A.ipynb` : tableaux de contingence, χ² et corrélation ;
- `DJELLALI_KHALED_TP3B.ipynb` : représentation Onion par enveloppes convexes ;
- `TP_05_01_Khaled_DJELLALI.ipynb` et `TP_05_02_Khaled_DJELLALI.ipynb` : ACP manuelle, variance expliquée et reconstruction d’image ;
- `Khaled_DJELLALI_TP_08A.ipynb` : régression, résidus, levier et influence ;
- `Khaled_DJELLALI_TP_08B.ipynb` : sélection de variables par Mallows Cp ;
- `DJELLALI_KHALED_TP11.ipynb` : K-means et EM/GMM implémentés sur Old Faithful.

Les chiffres cités sont rattachés aux sorties enregistrées dans les notebooks. Ils servent à expliquer le protocole et le diagnostic, pas à annoncer une performance universelle.
