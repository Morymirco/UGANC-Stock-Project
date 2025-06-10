import sqlite3
conn = sqlite3.connect("stock_app.db")
cursor = conn.cursor()
res = cursor.execute("SELECT a.code_article, a.designation, s.quantite FROM Articles a LEFT JOIN Stock s ON a.code_article = s.code_article;").fetchall()
print(res)
conn.close()