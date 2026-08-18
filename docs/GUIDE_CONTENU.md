# Guide de mise à jour du contenu

Le fichier `content/portfolio.json` constitue la source éditoriale du site. Les fichiers HTML ne doivent pas être modifiés directement si le changement doit être conservé lors d’une prochaine génération.

## Profil

La section `profile` contient l’identité, le texte d’introduction, les coordonnées, les liens professionnels, la photo et le CV. Les chemins doivent rester relatifs à la racine du dépôt.

## Compétences

Chaque groupe de `skills` possède :

- `title` : nom du domaine ;
- `description` : manière dont les technologies sont utilisées ;
- `primary` : compétences les plus représentatives ;
- `secondary` : technologies déjà pratiquées ou en approfondissement.

Cette structure évite les pourcentages, souvent difficiles à justifier en entretien.

## Projets

Chaque élément de `projects` contient les informations de la carte d’accueil et de l’étude de cas :

- `slug` : nom du fichier HTML sans espace ni accent ;
- `category` : `ai`, `web`, `software`, `data` ou `mobile` ;
- `cover` et `images` : chemins vers les captures ou schémas de documentation ;
- `problem` et `solution` : contexte et réponse apportée ;
- `architecture` : au moins trois décisions structurantes ;
- `challenges` : difficulté, risque et approche retenue ;
- `learnings` : acquis transférables ;
- `next_steps` : améliorations réalistes ;
- `source_label` et `source_short_label` : libellés optionnels du lien externe lorsque seule une page GitHub générale est disponible.

Après toute modification :

```bash
python tools/build_site.py
python tools/check_site.py
python -m unittest tools.test_portfolio_update tools.test_portfolio_v3 tools.test_portfolio_v4 tools.test_portfolio_v5 -v
```

## Ajouter un projet

1. Ajoute ses captures dans `assets/images/projects/`.
2. Duplique un objet dans le tableau `projects`.
3. Choisis un `slug` unique.
4. Vérifie que chaque chemin d’image existe.
5. Régénère puis contrôle le site avec les commandes ci-dessus.

Le projet apparaîtra automatiquement sur la page d’accueil, dans les filtres et dans la navigation précédent/suivant des études de cas.
