# core/produit_manager.py
from database.db import Database

class ProduitManager:
    def __init__(self):
        self.db = Database()

    def ajouter_article(self, code_article, designation, categorie, prix_achat, prix_vente, seuil_alerte):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Articles (code_article, designation, categorie, prix_achat, prix_vente, seuil_alerte)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (code_article, designation, categorie, prix_achat, prix_vente, seuil_alerte))
            conn.commit()

    def modifier_article(self, code_article, designation, categorie, prix_achat, prix_vente, seuil_alerte):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Articles
                SET designation = ?, categorie = ?, prix_achat = ?, prix_vente = ?, seuil_alerte = ?
                WHERE code_article = ?
            """, (designation, categorie, prix_achat, prix_vente, seuil_alerte, code_article))
            conn.commit()

    def supprimer_article(self, code_article):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Articles WHERE code_article = ?", (code_article,))
            conn.commit()

    def lister_articles(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Articles")
            return [dict(row) for row in cursor.fetchall()]
