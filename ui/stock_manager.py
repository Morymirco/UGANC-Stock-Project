import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkinter import simpledialog

class StockManager(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestion du stock")
        self.geometry("950x500")
        self.conn = sqlite3.connect("stock_app.db")
        self.create_widgets()
        self.refresh_table()
        self.show_alerts()

    def create_widgets(self):
        # Zone d'alerte EN HAUT
        self.alert_label = ttk.Label(self, text="", foreground="red", font=("Arial", 12, "bold"))
        self.alert_label.pack(pady=5)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(btn_frame, text="Entrée de stock", command=self.add_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Sortie de stock", command=self.add_exit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Rapport", command=self.show_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Valeur totale du stock", command=self.show_stock_value).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Articles les plus vendus", command=self.show_top_sellers).pack(side=tk.LEFT, padx=5)

        # Tableau des stocks
        columns = ("code_article", "designation", "quantite", "seuil_alerte")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").capitalize())
            self.tree.column(col, width=120)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        query = """
        SELECT a.code_article, a.designation, IFNULL(s.quantite, 0), a.seuil_alerte
        FROM Articles a
        LEFT JOIN Stock s ON a.code_article = s.code_article
        """
        articles = self.conn.execute(query).fetchall()
        for article in articles:
            self.tree.insert("", tk.END, values=article)

    def add_entry(self):
        self.stock_movement("entrée")

    def add_exit(self):
        self.stock_movement("sortie")

    def stock_movement(self, mouvement_type):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Sélectionnez un article.")
            return
        values = self.tree.item(selected[0])["values"]
        code_article = values[0]
        quantite = simpledialog.askinteger("Quantité", f"Quantité à {'ajouter' if mouvement_type=='entrée' else 'retirer'} pour {code_article} :")
        if quantite is None or quantite <= 0:
            return
        # Met à jour le stock
        cur = self.conn.cursor()
        cur.execute("SELECT quantite FROM Stock WHERE code_article = ?", (code_article,))
        row = cur.fetchone()
        if mouvement_type == "entrée":
            if row:
                cur.execute("UPDATE Stock SET quantite = quantite + ? WHERE code_article = ?", (quantite, code_article))
            else:
                cur.execute("INSERT INTO Stock (code_article, quantite, emplacement) VALUES (?, ?, ?)", (code_article, quantite, "Magasin"))
        else:  # sortie
            if row and row[0] >= quantite:
                cur.execute("UPDATE Stock SET quantite = quantite - ? WHERE code_article = ?", (quantite, code_article))
            else:
                messagebox.showerror("Erreur", "Stock insuffisant.")
                return
        # Ajoute le mouvement
        cur.execute("INSERT INTO Mouvements (type, code_article, quantite, date_mvt, user_id) VALUES (?, ?, ?, datetime('now'), ?)",
                    (mouvement_type, code_article, quantite, 1))
        self.conn.commit()
        self.refresh_table()
        self.show_alerts()
        messagebox.showinfo("Succès", f"{mouvement_type.capitalize()} enregistrée.")

    def show_alerts(self):
        # Affiche les articles sous le seuil d'alerte
        query = """
        SELECT a.code_article, a.designation, IFNULL(s.quantite, 0), a.seuil_alerte
        FROM Articles a
        LEFT JOIN Stock s ON a.code_article = s.code_article
        WHERE IFNULL(s.quantite, 0) <= a.seuil_alerte
        """
        articles = self.conn.execute(query).fetchall()
        if articles:
            alertes = "⚠️ Articles sous le seuil d'alerte :\n"
            for art in articles:
                alertes += f"- {art[0]} ({art[1]}): {art[2]} en stock (seuil {art[3]})\n"
            self.alert_label.config(text=alertes)
        else:
            self.alert_label.config(text="Aucune alerte de stock.")

    def show_report(self):
        # Affiche un rapport simple des mouvements
        win = tk.Toplevel(self)
        win.title("Rapport des mouvements")
        tree = ttk.Treeview(win, columns=("Date", "Type", "Code article", "Quantité"), show="headings")
        for col in ("Date", "Type", "Code article", "Quantité"):
            tree.heading(col, text=col)
            tree.column(col, width=120)
        tree.pack(fill=tk.BOTH, expand=True)
        mouvements = self.conn.execute("SELECT date_mvt, type, code_article, quantite FROM Mouvements ORDER BY date_mvt DESC").fetchall()
        for m in mouvements:
            tree.insert("", tk.END, values=m)

    def show_stock_value(self):
        # Calcule la valeur totale du stock (quantite * prix_vente)
        query = """
        SELECT a.code_article, a.designation, IFNULL(s.quantite, 0), a.prix_vente,
               IFNULL(s.quantite, 0) * a.prix_vente AS valeur
        FROM Articles a
        LEFT JOIN Stock s ON a.code_article = s.code_article
        """
        articles = self.conn.execute(query).fetchall()
        total = sum(row[4] for row in articles)
        win = tk.Toplevel(self)
        win.title("Valeur totale du stock")
        tree = ttk.Treeview(win, columns=("Code article", "Désignation", "Quantité", "Prix vente", "Valeur"), show="headings")
        for col in ("Code article", "Désignation", "Quantité", "Prix vente", "Valeur"):
            tree.heading(col, text=col)
            tree.column(col, width=120)
        tree.pack(fill=tk.BOTH, expand=True)
        for row in articles:
            tree.insert("", tk.END, values=row)
        ttk.Label(win, text=f"Valeur totale du stock : {total:.2f}").pack(pady=10)

    def show_top_sellers(self):
        # Classement des articles par quantité totale sortie
        query = """
        SELECT m.code_article, a.designation, SUM(m.quantite) as total_vendu
        FROM Mouvements m
        JOIN Articles a ON m.code_article = a.code_article
        WHERE m.type = 'sortie'
        GROUP BY m.code_article
        ORDER BY total_vendu DESC
        LIMIT 10
        """
        articles = self.conn.execute(query).fetchall()
        win = tk.Toplevel(self)
        win.title("Articles les plus vendus")
        tree = ttk.Treeview(win, columns=("Code article", "Désignation", "Quantité vendue"), show="headings")
        for col in ("Code article", "Désignation", "Quantité vendue"):
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill=tk.BOTH, expand=True)
        for row in articles:
            tree.insert("", tk.END, values=row)

# Pour ouvrir la gestion du stock depuis le menu principal :
# from ui.stock_manager import StockManager
# StockManager(self.root)