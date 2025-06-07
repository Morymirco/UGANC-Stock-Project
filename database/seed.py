import bcrypt
from database.db import Database
from datetime import datetime

def seed_data():
    db = Database()
    with db.get_connection() as conn:
        cursor = conn.cursor()
        # Insérer un utilisateur admin
        hashed_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
        cursor.execute("""
            INSERT OR IGNORE INTO Utilisateurs (username, password, role, nom_complet)
            VALUES (?, ?, ?, ?)
        """, ("admin", hashed_password, "Admin", "Administrateur Système"))
        
        # Insérer un article
        cursor.execute("""
            INSERT OR IGNORE INTO Articles (code_article, designation, categorie, prix_achat, prix_vente, seuil_alerte)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("ART001", "Cahier A4", "Papeterie", 2.5, 5.0, 10))
        
        # Insérer un stock
        cursor.execute("""
            INSERT OR IGNORE INTO Stock (code_article, quantite, emplacement)
            VALUES (?, ?, ?)
        """, ("ART001", 100, "Entrepôt A"))
        
        # Insérer un fournisseur
        cursor.execute("""
            INSERT OR IGNORE INTO Fournisseurs (nom, contact)
            VALUES (?, ?)
        """, ("Fournisseur ABC", "contact@abc.com"))
        
        conn.commit()

if __name__ == "__main__":
    seed_data()
