# database/db.py
import sqlite3
from contextlib import contextmanager

class Database:
    def __init__(self, db_name="stock_app.db"):
        self.db_name = db_name

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par nom
        conn.execute("PRAGMA foreign_keys = ON")  # Activer les contraintes de clés étrangères
        try:
            yield conn
        finally:
            conn.close()

    def initialize(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Table Utilisateurs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Utilisateurs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('Admin', 'Gestionnaire', 'Vendeur')),
                    nom_complet TEXT,
                    last_login DATETIME
                )
            """)
            # Table Fournisseurs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Fournisseurs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    contact TEXT
                )
            """)
            # Table Articles (avec clé étrangère vers Fournisseurs)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Articles (
                    code_article TEXT PRIMARY KEY,
                    designation TEXT NOT NULL,
                    categorie TEXT,
                    prix_achat REAL,
                    prix_vente REAL,
                    seuil_alerte INTEGER,
                    fournisseur_id INTEGER NOT NULL,
                    FOREIGN KEY (fournisseur_id) 
                    REFERENCES Fournisseurs(id) 
                    ON DELETE RESTRICT 
                    ON UPDATE CASCADE
                )
            """)
            # Table Stock
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Stock (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code_article TEXT,
                    quantite INTEGER NOT NULL CHECK(quantite >= 0),
                    emplacement TEXT,
                    FOREIGN KEY (code_article) 
                    REFERENCES Articles(code_article) 
                    ON DELETE RESTRICT 
                    ON UPDATE CASCADE
                )
            """)
            # Table Mouvements
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Mouvements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL CHECK(type IN ('ENTREE', 'SORTIE')),
                    code_article TEXT,
                    quantite INTEGER NOT NULL CHECK(quantite > 0),
                    date_mvt DATETIME,
                    user_id INTEGER,
                    FOREIGN KEY (code_article) 
                    REFERENCES Articles(code_article) 
                    ON DELETE RESTRICT 
                    ON UPDATE CASCADE,
                    FOREIGN KEY (user_id) 
                    REFERENCES Utilisateurs(id) 
                    ON DELETE SET NULL 
                    ON UPDATE CASCADE
                )
            """)
            conn.commit()