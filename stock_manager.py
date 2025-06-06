# core/stock_manager.py
from datetime import datetime
from database.db import Database

class StockManager:
    def __init__(self):
        self.db = Database()

    def ajouter_stock(self, code_article, quantite, emplacement):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Stock (code_article, quantite, emplacement)
                VALUES (?, ?, ?)
            """, (code_article, quantite, emplacement))
            conn.commit()

    def sortie_stock(self, code_article, quantite, user_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT quantite FROM Stock WHERE code_article = ?", (code_article,))
            result = cursor.fetchone()
            if result and result["quantite"] >= quantite:
                cursor.execute("""
                    UPDATE Stock
                    SET quantite = quantite - ?
                    WHERE code_article = ?
                """, (quantite, code_article))
                cursor.execute("""
                    INSERT INTO Mouvements (type, code_article, quantite, date_mvt, user_id)
                    VALUES (?, ?, ?, ?, ?)
                """, ("SORTIE", code_article, quantite, datetime.now(), user_id))
                conn.commit()
                return True
            return False

    def verifier_alertes(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.code_article, a.designation, a.seuil_alerte, s.quantite
                FROM Articles a
                JOIN Stock s ON a.code_article = s.code_article
                WHERE s.quantite <= a.seuil_alerte
            """)
            return [dict(row) for row in cursor.fetchall()]

    def historique_mouvements(self, date_debut=None, date_fin=None):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM Mouvements"
            params = []
            if date_debut and date_fin:
                query += " WHERE date_mvt BETWEEN ? AND ?"
                params = [date_debut, date_fin]
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]