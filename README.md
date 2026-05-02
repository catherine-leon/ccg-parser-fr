# CCG Parser — Grammaires de Catégories Combinatoires

Parseur de grammaires de catégories combinatoires (CCG) pour le français, développé dans le cadre du cours de Formalismes pour le TAL (UGA, 2025-2026).

## Description

Le système explore l'ensemble des dérivations syntaxiques possibles pour une phrase donnée, en identifiant à la fois les analyses complètes (menant à S) et les chemins partiels ayant abouti à une impasse. Il implémente six règles de combinaison : application droite (App>), application gauche (App<), composition harmonique droite (Comp>B), composition harmonique gauche (Comp<B), coordination (<*>) et montée catégorielle (TypeR).

L'interface visualise les dérivations sous forme de diagrammes SVG interactifs, reproduisant la notation standard des grammaires CCG.

## Structure du projet
ccg-parser/
├── parser.py            # Logique CCG : lexique, règles, algorithme CYK
├── base_lexique.py      # Lexique de base (phrases du cours)
├── gorafi_lexique.py    # Lexique étendu (phrases du Gorafi)
├── app.py               # API Flask — parseur principal (port 5000)
├── gorafi_app.py        # API Flask — parseur Gorafi (port 5001)
├── requirements.txt
├── templates/
│   ├── index.html       # Interface principale
│   └── gorafi.html      # Interface Gorafi
└── static/
├── app.js           # Rendu SVG, appels API
└── style.css

## Installation et lancement

```bash
pip install -r requirements.txt
```

Parseur principal (phrases du cours) :
```bash
python app.py
```
Ouvrir : http://127.0.0.1:5000

Parseur Gorafi :
```bash
python gorafi_app.py
```
Ouvrir : http://127.0.0.1:5001

## Fonctionnalités

- Analyse CYK bottom-up avec toutes les règles CCG
- Montée catégorielle (Type Raising) sur tous les spans NP, pas seulement les feuilles
- Visualisation SVG des dérivations avec codes couleur par règle
- Affichage des analyses partielles (impasses) avec identification du point de blocage
- Métriques : nombre d'analyses complètes, d'impasses réelles, temps de calcul
- Éditeur de lexique dynamique (ajout/suppression de mots en direct)
- Tableau récapitulatif sur toutes les phrases du corpus

## Lexique

Le lexique de base couvre une soixantaine d'entrées : noms propres, déterminants, verbes (intransitifs, transitifs, ditransitifs, à complétive), auxiliaires, adverbes, adjectifs, prépositions, conjonctions et pronoms relatifs. Le lexique Gorafi ajoute une vingtaine d'entrées supplémentaires pour l'analyse du texte authentique.

## Architecture

Le backend Python (`parser.py`) contient toute la logique linguistique et expose une API REST via Flask. Le frontend JavaScript (`app.js`) se limite à l'interaction et à la visualisation — il n'effectue aucun parsing. Cette séparation permet d'utiliser `parser.py` de manière autonome, notamment depuis un notebook Jupyter.

## Règles CCG implémentées

| Règle | Schéma | Description |
|-------|--------|-------------|
| App>  | X/Y + Y → X | Application droite |
| App<  | Y + X\Y → X | Application gauche |
| Comp>B | X/Y + Y/Z → X/Z | Composition harmonique droite |
| Comp<B | Y\Z + X\Y → X\Z | Composition harmonique gauche |
| <*>   | X + X\X/X + X → X | Coordination (règle ternaire) |
| TypeR | X → T/(T\X) | Montée catégorielle |
