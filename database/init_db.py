from db import Database

db = Database("stock_app.db")  # Assure-toi que le nom correspond à ta base
db.initialize()
print("Tables créées avec succès.")