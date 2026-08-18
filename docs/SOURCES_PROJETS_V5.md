# Sources et traçabilité — Portfolio V5

## Projet ajouté

**Jeu 2D d’occupation maximale — Java Swing & Design Patterns**

Archive analysée : `Jeu2DOccupationMaximaleDEspace.zip`.

Le projet a été extrait dans un répertoire isolé, compilé avec Apache Ant, puis lancé dans un environnement graphique virtuel. Le projet NetBeans déclare un niveau source et cible **Java 17** dans `nbproject/project.properties`. La compilation a également été validée avec le JDK disponible dans l’environnement de contrôle.

## Fichiers consultés

### Composition et interface

- `src/jeu2doccupationmaximaledespace/Main.java` : création de `GameModel`, `GamePanel` et `MouseController`, sélection des quatre modes avec les boutons Swing, génération initiale des obstacles et construction de la fenêtre 800 × 600.
- `src/jeu2doccupationmaximaledespace/view/GamePanel.java` : dessin Java2D, anti-aliasing, obstacles rouges, formes joueur bleues, aperçu semi-transparent, score et nombre de formes restantes.

### Modèle géométrique

- `model/GameModel.java` : groupes obstacles/joueur, limite `maxPlayerShapes = 4`, score fondé sur la surface totale et stratégie de génération.
- `model/Shape.java` : contrat polymorphe `area()` et `intersects(Shape)`.
- `model/Circle.java` : aire du cercle, collision cercle–cercle et délégation du cas cercle–rectangle.
- `model/Rectangle.java` : aire, collision rectangle–rectangle par recouvrement AABB et collision rectangle–cercle avec le point le plus proche obtenu par `clamp`.
- `model/Point.java` : distance euclidienne, translation et copie.
- `model/ShapeGroup.java` : collection défensive, surface totale, détection d’intersection avec le groupe et propagation des changements des formes.

### Interactions et design patterns

- `controller/MouseController.java` et `MouseState.java` : délégation des événements souris selon le pattern State.
- `CreateCircleState.java` : premier clic pour le centre, rayon calculé depuis la souris, aperçu puis validation au second clic.
- `CreateRectangleState.java` : création dans toutes les directions grâce à `Math.min` et `Math.abs`.
- `MoveState.java` : sélection par hit-testing et conservation de l’offset pour éviter un saut visuel pendant le drag.
- `DeleteState.java` : suppression d’une forme joueur par test d’appartenance.
- `model/ShapeGenerationStrategy.java` et `RandomShapeStrategy.java` : génération interchangeable, objectif de cinq obstacles et plafond de 300 tentatives.
- `model/FixedShapeStrategy.java` : classe présente mais non implémentée dans la version fournie.
- `model/AbstractModelEcoutable.java` et `observer/ModelListener.java` : mécanisme Observer utilisé pour déclencher les rafraîchissements.

## Vérifications réalisées sur l’application

- compilation de 19 fichiers source avec Apache Ant ;
- création du JAR exécutable ;
- lancement de l’interface Swing ;
- génération aléatoire des obstacles ;
- création de quatre formes joueur par interactions souris ;
- mise à jour du score et passage du compteur de quatre à zéro forme restante ;
- capture réelle utilisée dans la galerie du portfolio.

## Réserves appliquées dans l’étude de cas

L’étude de cas ne présente pas comme terminées les fonctionnalités absentes ou partielles :

- les méthodes de collision protègent la génération des obstacles, mais la création et le déplacement des formes joueur ne consultent pas encore ces règles ; des superpositions restent donc possibles ;
- les limites du plateau ne sont pas validées pendant la création ou le déplacement ;
- la stratégie `FixedShapeStrategy` est encore vide ;
- la génération utilise des dimensions fixes de 800 × 600 plutôt que la taille utile réelle du panneau, ce qui peut produire un élément partiellement masqué par les bordures ou la barre de contrôle ;
- aucune condition de victoire ni aire d’union n’est calculée : le score additionne simplement les aires individuelles ;
- le dossier `test` fourni ne contient pas de suite JUnit exploitable ;
- le lancement n’est pas explicitement encapsulé dans `SwingUtilities.invokeLater`.

Ces éléments apparaissent dans le portfolio comme limites identifiées et pistes d’amélioration, et non comme fonctionnalités déjà disponibles.

## Visuels ajoutés

- `java-occupation-overview.png` : couverture documentaire avec la capture réelle et les principales caractéristiques ;
- `java-occupation-application.png` : application compilée et exécutée, encadrée sans modifier les données affichées ;
- `assets/images/projects/java-occupation-source-capture.png` : capture source conservée dans le dépôt pour rendre la génération des visuels reproductible ;
- `java-occupation-architecture.png` : séparation des responsabilités et design patterns ;
- `java-occupation-states.png` : fonctionnement des quatre états de la souris ;
- `java-occupation-collisions.png` : trois familles de collisions et limite actuelle ;
- `java-occupation-score.png` : calcul du score, quota de formes et stratégie de génération.

Les schémas sont des visuels de documentation. Seule l’image de l’interface est issue d’une exécution réelle de l’application.
