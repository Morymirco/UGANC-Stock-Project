import sqlite3
conn = sqlite3.connect("stock_app.db")
cursor = conn.cursor()
cursor.execute("INSERT OR IGNORE INTO Stock (code_article, quantite, emplacement) VALUES (?, ?, ?)", ("A001", 20, "Magasin"))
conn.commit()
conn.close()