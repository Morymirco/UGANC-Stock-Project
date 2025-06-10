import barcode
from barcode.writer import ImageWriter
import sqlite3
import os

os.makedirs("barcodes", exist_ok=True)

conn = sqlite3.connect("stock_app.db")
cursor = conn.cursor()
articles = cursor.execute("SELECT code_article FROM Articles").fetchall()

for (code_article,) in articles:
    # Utilise Code128 pour accepter les codes alphanumériques comme "A001"
    code128 = barcode.get('code128', code_article, writer=ImageWriter())
    filename = code128.save(f"barcodes/{code_article}")
    cursor.execute("UPDATE Articles SET code_barre = ? WHERE code_article = ?", (filename, code_article))

conn.commit()
conn.close()
print("Codes-barres générés pour tous les articles.")