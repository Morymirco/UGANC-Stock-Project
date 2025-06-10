import sqlite3
conn = sqlite3.connect("stock_app.db")
cursor = conn.cursor()
print("Articles :", cursor.execute("SELECT * FROM Articles").fetchall())
print("Mouvements :", cursor.execute("SELECT * FROM Mouvements").fetchall())
print("Stock :", cursor.execute("SELECT * FROM Stock").fetchall())
conn.close()