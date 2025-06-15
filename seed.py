# database/seed.py
import bcrypt
from database.db import Database
from datetime import datetime

def seed_data():
    db = Database()
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Insérer un utilisateur admin
        hashed_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
        cursor.execute("""
            INSERT OR IGNORE INTO Utilisateurs (username, password, role, nom_complet)
            VALUES (?, ?, ?, ?)
        """, ("admin", hashed_password, "Admin", "Administrateur Système"))
        
        # 2. Insérer un fournisseur
        cursor.execute("""
            INSERT OR IGNORE INTO Fournisseurs (nom, contact)
            VALUES (?, ?)
        """, ("Fournisseur ABC", "contact@abc.com"))
        
        # Récupérer l'ID du fournisseur
        cursor.execute("SELECT id FROM Fournisseurs WHERE nom = ?", ("Fournisseur ABC",))
        fournisseur_id = cursor.fetchone()["id"]
        
        # 3. Insérer un article (lié au fournisseur)
        cursor.execute("""
            INSERT OR IGNORE INTO Articles (code_article, designation, categorie, prix_achat, prix_vente, seuil_alerte, fournisseur_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("ART001", "Cahier A4", "Papeterie", 2.5, 5.0, 10, fournisseur_id))
        
        # 4. Insérer un stock (après l'article)
        cursor.execute("""
            INSERT OR IGNORE INTO Stock (code_article, quantite, emplacement)
            VALUES (?, ?, ?)
        """, ("ART001", 100, "Entrepôt A"))
        
        # 5. Insérer un mouvement (après l'article et l'utilisateur)
        cursor.execute("""
            INSERT OR IGNORE INTO Mouvements (type, code_article, quantite, date_mvt, user_id)
            VALUES (?, ?, ?, ?, ?)
        """, ("ENTREE", "ART001", 100, datetime.now(), 1))
        
        conn.commit()

if __name__ == "__main__":
    seed_data()