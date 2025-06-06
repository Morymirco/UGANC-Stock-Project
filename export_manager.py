# core/export_manager.py
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from database.db import Database

class ExportManager:
    def __init__(self):
        self.db = Database()

    def export_stock_excel(self, filename="stock_report.xlsx"):
        with self.db.get_connection() as conn:
            df = pd.read_sql_query("SELECT * FROM Stock JOIN Articles ON Stock.code_article = Articles.code_article", conn)
            df.to_excel(filename, index=False)

    def export_stock_pdf(self, filename="stock_report.pdf"):
        c = canvas.Canvas(filename, pagesize=letter)
        c.drawString(100, 750, "Rapport de Stock")
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Stock JOIN Articles ON Stock.code_article = Articles.code_article")
            y = 700
            for row in cursor.fetchall():
                c.drawString(100, y, f"{row['designation']}: {row['quantite']} unités")
                y -= 20
            c.save()