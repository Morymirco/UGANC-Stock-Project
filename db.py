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
        try:
            yield conn
        finally:
            conn.close()

    def initialize(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Création des tables si elles n'existent pas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Utilisateurs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    nom_complet TEXT,
                    last_login DATETIME
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Articles (
                    code_article TEXT PRIMARY KEY,
                    designation TEXT NOT NULL,
                    categorie TEXT,
                    prix_achat REAL,
                    prix_vente REAL,
                    seuil_alerte INTEGER
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Stock (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code_article TEXT,
                    quantite INTEGER,
                    emplacement TEXT,
                    FOREIGN KEY (code_article) REFERENCES Articles(code_article)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Mouvements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT,
                    code_article TEXT,
                    quantite INTEGER,
                    date_mvt DATETIME,
                    user_id INTEGER,
                    FOREIGN KEY (code_article) REFERENCES Articles(code_article),
                    FOREIGN KEY (user_id) REFERENCES Utilisateurs(id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Fournisseurs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    contact TEXT
                )
            """)
            conn.commit()