# core/produit_manager.py
from database.db import Database

class ProduitManager:
    def __init__(self):
        self.db = Database()

    def ajouter_article(self, code_article, designation, categorie, prix_achat, prix_vente, seuil_alerte, fournisseur_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Articles (code_article, designation, categorie, prix_achat, prix_vente, seuil_alerte, fournisseur_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (code_article, designation, categorie, prix_achat, prix_vente, seuil_alerte, fournisseur_id))
            conn.commit()

    def modifier_article(self, code_article, designation, categorie, prix_achat, prix_vente, seuil_alerte, fournisseur_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Articles
                SET designation = ?, categorie = ?, prix_achat = ?, prix_vente = ?, seuil_alerte = ?, fournisseur_id = ?
                WHERE code_article = ?
            """, (designation, categorie, prix_achat, prix_vente, seuil_alerte, fournisseur_id, code_article))
            conn.commit()

    def supprimer_article(self, code_article):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Articles WHERE code_article = ?", (code_article,))
            conn.commit()

    def lister_articles(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.*, f.nom AS fournisseur_nom 
                FROM Articles a 
                JOIN Fournisseurs f ON a.fournisseur_id = f.id
            """)
            return [dict(row) for row in cursor.fetchall()]