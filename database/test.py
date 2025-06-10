import sqlite3
conn = sqlite3.connect("stock_app.db")
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(Articles)")
print(cursor.fetchall())
cursor.execute("ALTER TABLE Articles ADD COLUMN code_barre TEXT")
conn.commit()
conn.close()
print("Colonne code_barre ajoutée à Articles.")