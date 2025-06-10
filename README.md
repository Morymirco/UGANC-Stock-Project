# Système de Gestion de Stock

Projet de gestion de stock réalisé à l’Université Gamal Abdel Nasser de Conakry.

**Auteurs** : Mory Koulibaly, Cecis Alexis Haba, Karfalla Diaby, Jean Keloua Ouamouno (Jeanos), Mamadou Ramadane Barry.

---

## Structure du projet

- `/backend` : Base de données SQLite et logique métier
- `/frontend` : Interfaces graphiques Tkinter
- `/security` : Authentification sécurisée (bcrypt)
- `/reporting` : Rapports, alertes, codes-barres
- `/docs` : Documentation et présentation

## Technologies utilisées

- Python 3
- Tkinter (interface graphique)
- SQLite (base de données)
- bcrypt (authentification)
- python-barcode, opencv-python, pyzbar (gestion des codes-barres)

---

## Installation

1. **Cloner le dépôt**

   ```bash
   git clone https://github.com//Morymirco/UGANC-Stock-Project.git
   cd UGANC-Stock-Project
   ```

2. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

3. **Initialiser la base de données**

   ```bash
   python database/db.py
   ```

4. **Lancer l’application**
   ```bash
   python main.py
   ```

---

## Utilisation

- Se connecter avec l’utilisateur par défaut :  
  **Identifiant** : `admin`  
  **Mot de passe** : `admin123`
- Naviguer dans l’application pour gérer :
  - Utilisateurs
  - Articles
  - Stocks
  - Mouvements
  - Fournisseurs
  - Rapports et alertes
  - Codes-barres (génération et scan)

---

## Fonctionnalités principales

- **Gestion des utilisateurs** : Création, modification, suppression, rôles et authentification sécurisée.
- **Gestion des articles** : Ajout, modification, suppression, génération et affichage de codes-barres.
- **Gestion des stocks** : Entrées/sorties, affichage des quantités, alertes de stock faible.
- **Gestion des mouvements** : Historique détaillé des entrées et sorties.
- **Gestion des fournisseurs** : Ajout, modification, suppression, affichage.
- **Rapports** :
  - Valeur totale du stock (quantité × prix de vente)
  - Articles les plus vendus (basé sur les sorties)
  - Alertes automatiques sur les articles sous le seuil
- **Codes-barres** :
  - Génération automatique (Code128)
  - Scan via webcam pour retrouver un article
  - Affichage de l’image du code-barres dans l’interface

---

## Contribution

- Forkez le projet, créez une branche, proposez vos améliorations via pull request.
- Merci de documenter vos ajouts dans `/docs`.

---

## Licence

Projet académique – usage pédagogique uniquement.

---

**Pour toute question ou suggestion, contactez l’un des auteurs.**
