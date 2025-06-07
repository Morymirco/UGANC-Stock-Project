# Système de Gestion de Stock
Projet de cours pour la 3ème année, Université Gamal Abdel Nasser de Conakry.
Membres : Mory Koulibaly, Cecis Alexis Haba, Karfalla Diaby, Jean Keloua Ouamouno(Jeanos), Ramadan Barry.

## Structure
- `/backend` : Base de données SQLite et logique métier.
- `/frontend` : Interfaces Tkinter.
- `/security` : Authentification bcrypt.
- `/reporting` : Rapports, alertes, codes-barres ZXing.
- `/docs` : Documentation et présentation.

## Technologies
- Python/Tkinter, SQLite, bcrypt, ZXing.

## Installation
- Cloner le dépôt
- Installer les dépendances : `pip install -r requirements.txt`
- Initialiser la base de données : `python database/db.py`
- Exécuter le script principal : `python main.py`

## Utilisation
- Lancer le script principal : `python main.py`
- Se connecter en tant qu'administrateur : `admin/admin123`
- Utiliser les fonctionnalités de gestion des utilisateurs, articles, stocks et mouvements.

## Fonctionnalités
- Gestion des utilisateurs : Création, modification, suppression et affichage des utilisateurs.
- Gestion des articles : Ajout, modification, suppression et affichage des articles.
- Gestion des stocks : Ajout, sortie et affichage des stocks.
- Gestion des mouvements : Ajout, sortie et affichage des mouvements.
- Gestion des fournisseurs : Ajout, modification, suppression et affichage des fournisseurs.
- Gestion des rapports : Génération des rapports, alertes et codes-barres.
- Gestion des utilisateurs : Création, modification, suppression et affichage des utilisateurs.

