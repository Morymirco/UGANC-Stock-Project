import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("stock_app.db")
cursor = conn.cursor()

# Remplace "A001" par un code_article existant dans ta table Articles
code_article = "A001"
user_id = 1  # Remplace par un id utilisateur existant

# Générer 5 entrées
for i in range(5):
    cursor.execute("""
        INSERT INTO Mouvements (type, code_article, quantite, date_mvt, user_id)
        VALUES (?, ?, ?, ?, ?)
    """, (
        "entrée",
        code_article,
        10 + i,  # Quantité différente à chaque fois
        (datetime.now() - timedelta(days=5-i)).strftime("%Y-%m-%d %H:%M:%S"),
        user_id
    ))

# Générer 5 sorties
for i in range(5):
    cursor.execute("""
        INSERT INTO Mouvements (type, code_article, quantite, date_mvt, user_id)
        VALUES (?, ?, ?, ?, ?)
    """, (
        "sortie",
        code_article,
        3 + i,  # Quantité différente à chaque fois
        (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S"),
        user_id
    ))

    conn.commit()
conn.close()
print("10 mouvements insérés (5 entrées, 5 sorties)")