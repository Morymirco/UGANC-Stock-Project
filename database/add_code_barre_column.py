import sqlite3

conn = sqlite3.connect("stock_app.db")  # adapte le nom si besoin
cursor = conn.cursor()
try:
    cursor.execute("ALTER TABLE Articles ADD COLUMN code_barre TEXT;")
    print("Colonne code_barre ajoutée avec succès.")
except sqlite3.OperationalError as e:
    print("Erreur ou colonne déjà existante :", e)
conn.commit()
conn.close()