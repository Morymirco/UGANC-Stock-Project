import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageTk
import os

class ArticleForm(tk.Toplevel):
    def __init__(self, parent, article=None, refresh_callback=None):
        super().__init__(parent)
        self.title("Ajouter / Modifier un article")
        self.geometry("400x500")
        self.article = article
        self.refresh_callback = refresh_callback
        self.conn = sqlite3.connect("stock_app.db")
        self.create_widgets()
        if article:
            self.fill_fields(article)

    def create_widgets(self):
        self.code_article_var = tk.StringVar()
        self.designation_var = tk.StringVar()
        self.categorie_var = tk.StringVar()
        self.prix_achat_var = tk.DoubleVar()
        self.prix_vente_var = tk.DoubleVar()
        self.seuil_var = tk.IntVar()
        self.code_barre_var = tk.StringVar()

        ttk.Label(self, text="Code article").pack()
        ttk.Entry(self, textvariable=self.code_article_var).pack()
        ttk.Label(self, text="Désignation").pack()
        ttk.Entry(self, textvariable=self.designation_var).pack()
        ttk.Label(self, text="Catégorie").pack()
        ttk.Entry(self, textvariable=self.categorie_var).pack()
        ttk.Label(self, text="Prix achat").pack()
        ttk.Entry(self, textvariable=self.prix_achat_var).pack()
        ttk.Label(self, text="Prix vente").pack()
        ttk.Entry(self, textvariable=self.prix_vente_var).pack()
        ttk.Label(self, text="Seuil alerte").pack()
        ttk.Entry(self, textvariable=self.seuil_var).pack()
        ttk.Label(self, text="Code-barres").pack()
        ttk.Entry(self, textvariable=self.code_barre_var, state="readonly").pack()

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Générer code-barres", command=self.generer_code_barre).pack(side=tk.LEFT, padx=5)
        
        self.barcode_img_label = ttk.Label(self)
        self.barcode_img_label.pack(pady=10)

        ttk.Button(self, text="Enregistrer", command=self.save_article).pack(pady=10)
        if self.article:
            ttk.Button(self, text="Supprimer", command=self.delete_article).pack(pady=5)

    def fill_fields(self, article):
        self.code_article_var.set(article[0])
        self.designation_var.set(article[1])
        self.categorie_var.set(article[2])
        self.prix_achat_var.set(article[3])
        self.prix_vente_var.set(article[4])
        self.seuil_var.set(article[5])
        self.code_barre_var.set(article[6])
        if article[6] and os.path.exists(article[6]):
            img = Image.open(article[6])
            img = img.resize((200, 80))
            self.barcode_img = ImageTk.PhotoImage(img)
            self.barcode_img_label.config(image=self.barcode_img)

    def generer_code_barre(self):
        code_article = self.code_article_var.get()
        if not code_article:
            messagebox.showerror("Erreur", "Code article requis")
            return
        os.makedirs("barcodes", exist_ok=True)
        code128 = barcode.get('code128', code_article, writer=ImageWriter())
        filename = code128.save(f"barcodes/{code_article}")
        self.code_barre_var.set(filename)
        # Affichage de l'image
        img = Image.open(filename)
        img = img.resize((200, 80))
        self.barcode_img = ImageTk.PhotoImage(img)
        self.barcode_img_label.config(image=self.barcode_img)

    def scanner_code_barre(self):
        import cv2
        from pyzbar.pyzbar import decode
        cap = cv2.VideoCapture(0)
        code = None
        while True:
            ret, frame = cap.read()
            for barcode in decode(frame):
                code = barcode.data.decode('utf-8')
                cap.release()
                cv2.destroyAllWindows()
                self.code_article_var.set(code)
                messagebox.showinfo("Code-barres détecté", f"Code : {code}")
                return
            cv2.imshow('Scanner code-barre', frame)
            if cv2.waitKey(1) == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

    def save_article(self):
        data = (
            self.code_article_var.get(),
            self.designation_var.get(),
            self.categorie_var.get(),
            self.prix_achat_var.get(),
            self.prix_vente_var.get(),
            self.seuil_var.get(),
            self.code_barre_var.get()
        )
        try:
            self.conn.execute(
                "INSERT OR REPLACE INTO Articles (code_article, designation, categorie, prix_achat, prix_vente, seuil_alerte, code_barre) VALUES (?, ?, ?, ?, ?, ?, ?)",
                data
            )
            self.conn.commit()
            messagebox.showinfo("Succès", "Article enregistré")
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def delete_article(self):
        code_article = self.code_article_var.get()
        if not code_article:
            messagebox.showerror("Erreur", "Code article requis")
            return
        self.conn.execute("DELETE FROM Articles WHERE code_article = ?", (code_article,))
        self.conn.commit()
        messagebox.showinfo("Succès", "Article supprimé")
        if self.refresh_callback:
            self.refresh_callback()
        self.destroy()

class ArticleManager(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestion des articles")
        self.geometry("900x400")
        self.conn = sqlite3.connect("stock_app.db")
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(btn_frame, text="Ajouter", command=self.add_article).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Modifier", command=self.edit_article).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Supprimer", command=self.delete_article).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Scanner code-barres", command=self.scan_and_select_article).pack(side=tk.LEFT, padx=5)

        # Tableau des articles
        columns = ("code_article", "designation", "categorie", "prix_achat", "prix_vente", "seuil_alerte", "code_barre")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").capitalize())
            self.tree.column(col, width=120)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        articles = self.conn.execute("SELECT code_article, designation, categorie, prix_achat, prix_vente, seuil_alerte, code_barre FROM Articles").fetchall()
        for article in articles:
            self.tree.insert("", tk.END, values=article)

    def add_article(self):
        def refresh(): self.refresh_table()
        ArticleForm(self, refresh_callback=refresh)

    def edit_article(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Sélectionnez un article à modifier.")
            return
        values = self.tree.item(selected[0])["values"]
        def refresh(): self.refresh_table()
        ArticleForm(self, article=values, refresh_callback=refresh)

    def delete_article(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Sélectionnez un article à supprimer.")
            return
        code_article = self.tree.item(selected[0])["values"][0]
        self.conn.execute("DELETE FROM Articles WHERE code_article = ?", (code_article,))
        self.conn.commit()
        self.refresh_table()
        messagebox.showinfo("Succès", "Article supprimé.")

    def scan_and_select_article(self):
        import cv2
        from pyzbar.pyzbar import decode
        cap = cv2.VideoCapture(0)
        code = None
        while True:
            ret, frame = cap.read()
            for barcode in decode(frame):
                code = barcode.data.decode('utf-8')
                cap.release()
                cv2.destroyAllWindows()
                # Recherche dans le tableau
                for row_id in self.tree.get_children():
                    values = self.tree.item(row_id)["values"]
                    if str(values[6]) == code or (values[6] and code in str(values[6])):
                        self.tree.selection_set(row_id)
                        self.tree.see(row_id)
                        messagebox.showinfo("Article trouvé", f"Article avec code-barres {code} sélectionné.")
                        return
                messagebox.showwarning("Non trouvé", f"Aucun article avec le code-barres {code}.")
                return
            cv2.imshow('Scanner code-barre', frame)
            if cv2.waitKey(1) == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

# Pour ouvrir la gestion des articles depuis le menu principal :
# from ui.article_form import ArticleManager
# ArticleManager(self.root)