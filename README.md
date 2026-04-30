# CCG Parser Web App

Ce projet implémente un parseur en grammaires catégorielles combinatoires (CCG) avec une interface web interactive.

L’application permet d’entrer une phrase, d’analyser sa structure syntaxique et de visualiser les dérivations produites.

## Architecture

- Backend : Python (Flask) — implémentation du parseur CCG  
- Frontend : HTML / CSS / JavaScript — interface utilisateur et visualisation  

Le système sépare la logique linguistique (parsing) et l’affichage.

## Lancement

1. Installer les dépendances :

```bash
pip install -r requirements.txt
```

2. Lancer le serveur :

```bash
python app.py
```

3. Ouvrir dans le navigateur :

```
http://127.0.0.1:5000
```

## Fonctionnalités

- attribution de catégories lexicales  
- application des règles CCG (application, composition, type raising)  
- génération de dérivations  
- gestion de l’ambiguïté  
- visualisation des arbres  

## Remarques

Ce projet est un prototype pédagogique.  
Il utilise un lexique limité et ne repose pas sur de modèle probabiliste.
