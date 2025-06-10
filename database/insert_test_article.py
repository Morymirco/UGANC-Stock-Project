import sqlite3

conn = sqlite3.connect("stock_app.db")
cursor = conn.cursor()

# Vérifie si l'article existe déjà
cursor.execute("SELECT * FROM Articles WHERE code_article = ?", ("A001",))
if cursor.fetchone() is None:
    cursor.execute("""
        INSERT INTO Articles (code_article, designation, categorie, prix_achat, prix_vente, seuil_alerte)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ("A001", "Article Test", "Divers", 100.0, 150.0, 5))
    print("Article 'A001' ajouté.")
else:
    print("Article 'A001' existe déjà.")

conn.commit()
conn.close()