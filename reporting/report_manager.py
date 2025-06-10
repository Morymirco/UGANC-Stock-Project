import sqlite3

def get_etat_stocks(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.code_article, a.designation, s.quantite
        FROM Articles a
        LEFT JOIN Stock s ON a.code_article = s.code_article;
    """)
    return cursor.fetchall()

def get_historique_mouvements(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.date_mvt, m.type, m.code_article, m.quantite
        FROM Mouvements m
        ORDER BY m.date_mvt DESC;
    """)
    return cursor.fetchall()

def get_valeur_totale_stock(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(s.quantite * a.prix_achat) AS valeur_totale
        FROM Stock s
        JOIN Articles a ON s.code_article = a.code_article;
    """)
    return cursor.fetchone()[0]

def get_articles_plus_vendus(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.designation, SUM(m.quantite) AS total_vendu
        FROM Mouvements m
        JOIN Articles a ON m.code_article = a.code_article
        WHERE m.type = 'sortie'
        GROUP BY a.code_article
        ORDER BY total_vendu DESC
        LIMIT 10;
    """)
    return cursor.fetchall()