import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkinter import simpledialog
from ui.theme_manager import theme_manager

class StockManager(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestion du stock")
        self.geometry("1200x700")
        self.configure(bg=theme_manager.get_color("bg_primary"))
        self.conn = sqlite3.connect("stock_app.db")
        
        # Configuration des styles
        self.setup_styles()
        
        self.create_widgets()
        self.refresh_table()
        self.show_alerts()

    def setup_styles(self):
        """Configure les styles personnalisés pour l'interface"""
        style = ttk.Style()
        
        # Configuration du thème dark pour Treeview
        style.theme_use('clam')
        
        style.configure('Treeview',
                       background=theme_manager.get_color("bg_secondary"),
                       foreground=theme_manager.get_color("fg_primary"),
                       fieldbackground=theme_manager.get_color("bg_secondary"),
                       borderwidth=1,
                       relief='solid')
        
        style.configure('Treeview.Heading',
                       background=theme_manager.get_color("bg_tertiary"),
                       foreground=theme_manager.get_color("fg_primary"),
                       relief='solid',
                       borderwidth=1)
        
        style.map('Treeview',
                 background=[('selected', theme_manager.get_color("accent_primary"))])
        
        style.map('Treeview.Heading',
                 background=[('active', theme_manager.get_color("accent_info"))])

    def create_widgets(self):
        # Header stylisé
        header_frame = tk.Frame(self, bg=theme_manager.get_color("bg_tertiary"), height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Contenu du header
        header_content = tk.Frame(header_frame, bg=theme_manager.get_color("bg_tertiary"))
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Titre avec icône
        title_frame = tk.Frame(header_content, bg=theme_manager.get_color("bg_tertiary"))
        title_frame.pack(side=tk.LEFT)
        
        title_icon = tk.Label(title_frame, text="📊", font=('Arial', 20), 
                             bg=theme_manager.get_color("bg_tertiary"), fg=theme_manager.get_color("fg_primary"))
        title_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = tk.Label(title_frame, text="Gestion du Stock", 
                              font=('Arial', 16, 'bold'), bg=theme_manager.get_color("bg_tertiary"), 
                              fg=theme_manager.get_color("fg_primary"))
        title_label.pack(side=tk.LEFT)
        
        # Bouton retour
        back_style = theme_manager.get_button_style("secondary")
        back_btn = tk.Button(header_content, text="← Retour", command=self.destroy,
                            font=('Arial', 10), **back_style, padx=15, pady=6)
        back_btn.pack(side=tk.RIGHT)

        # Zone d'alerte
        self.alert_frame = tk.Frame(self, bg=theme_manager.get_color("bg_primary"))
        self.alert_frame.pack(fill=tk.X, padx=20, pady=(10, 0))
        
        self.alert_label = tk.Label(self.alert_frame, text="", 
                                   font=("Arial", 12, "bold"), bg=theme_manager.get_color("bg_primary"))
        self.alert_label.pack()

        # Section des actions
        actions_frame = tk.Frame(self, bg=theme_manager.get_color("bg_secondary"), relief='solid', bd=1)
        actions_frame.pack(fill=tk.X, padx=20, pady=10)
        
        actions_header = tk.Frame(actions_frame, bg=theme_manager.get_color("bg_tertiary"))
        actions_header.pack(fill=tk.X)
        
        actions_title = tk.Label(actions_header, text="🚀 Actions rapides", 
                                font=('Arial', 14, 'bold'), bg=theme_manager.get_color("bg_tertiary"), 
                                fg=theme_manager.get_color("fg_primary"))
        actions_title.pack(pady=10)
        
        # Ligne de séparation
        separator = tk.Frame(actions_frame, bg=theme_manager.get_color("separator"), height=1)
        separator.pack(fill=tk.X)
        
        # Contenu des actions
        btn_content = tk.Frame(actions_frame, bg=theme_manager.get_color("bg_secondary"))
        btn_content.pack(fill=tk.X, padx=20, pady=15)
        
        # Première rangée de boutons
        btn_row1 = tk.Frame(btn_content, bg=theme_manager.get_color("bg_secondary"))
        btn_row1.pack(fill=tk.X, pady=(0, 10))
        
        success_style = theme_manager.get_button_style("success")
        tk.Button(btn_row1, text="📈 Entrée de stock", command=self.add_entry,
                 font=('Arial', 11, 'bold'), **success_style, padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
        
        danger_style = theme_manager.get_button_style("danger")
        tk.Button(btn_row1, text="📉 Sortie de stock", command=self.add_exit,
                 font=('Arial', 11, 'bold'), **danger_style, padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
        
        info_style = theme_manager.get_button_style("info")
        tk.Button(btn_row1, text="📋 Rapport", command=self.show_report,
                 font=('Arial', 11, 'bold'), **info_style, padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
        
        # Deuxième rangée de boutons
        btn_row2 = tk.Frame(btn_content, bg=theme_manager.get_color("bg_secondary"))
        btn_row2.pack(fill=tk.X)
        
        warning_style = theme_manager.get_button_style("warning")
        tk.Button(btn_row2, text="💰 Valeur totale du stock", command=self.show_stock_value,
                 font=('Arial', 10, 'bold'), **warning_style, padx=12, pady=6).pack(side=tk.LEFT, padx=(0, 8))
        
        primary_style = theme_manager.get_button_style("primary")
        tk.Button(btn_row2, text="🏆 Articles les plus vendus", command=self.show_top_sellers,
                 font=('Arial', 10, 'bold'), **primary_style, padx=12, pady=6).pack(side=tk.LEFT, padx=(0, 8))

        # Section du tableau
        table_frame = tk.Frame(self, bg=theme_manager.get_color("bg_secondary"), relief='solid', bd=1)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        table_header = tk.Frame(table_frame, bg=theme_manager.get_color("bg_tertiary"))
        table_header.pack(fill=tk.X)
        
        table_title = tk.Label(table_header, text="📦 État actuel du stock", 
                              font=('Arial', 14, 'bold'), bg=theme_manager.get_color("bg_tertiary"), 
                              fg=theme_manager.get_color("fg_primary"))
        table_title.pack(pady=10)
        
        # Ligne de séparation
        separator2 = tk.Frame(table_frame, bg=theme_manager.get_color("separator"), height=1)
        separator2.pack(fill=tk.X)
        
        # Tableau des stocks avec scrollbar
        table_content = tk.Frame(table_frame, bg=theme_manager.get_color("bg_secondary"))
        table_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tableau avec scrollbars
        columns = ("code_article", "designation", "quantite", "seuil_alerte")
        self.tree = ttk.Treeview(table_content, columns=columns, show="headings", style='Treeview')
        
        # Configuration des colonnes
        self.tree.heading("code_article", text="📋 Code Article")
        self.tree.heading("designation", text="📝 Désignation")
        self.tree.heading("quantite", text="📊 Quantité")
        self.tree.heading("seuil_alerte", text="⚠️ Seuil d'Alerte")
        
        self.tree.column("code_article", width=120)
        self.tree.column("designation", width=250)
        self.tree.column("quantite", width=100)
        self.tree.column("seuil_alerte", width=120)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_content, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_content, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Placement du tableau et scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        table_content.grid_rowconfigure(0, weight=1)
        table_content.grid_columnconfigure(0, weight=1)

    def refresh_table(self):
        """Rafraîchit le tableau des stocks"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        query = """
        SELECT a.code_article, a.designation, 
               COALESCE(s.quantite, 0) as quantite, 
               a.seuil_alerte
        FROM Articles a
        LEFT JOIN Stock s ON a.code_article = s.code_article
        ORDER BY a.designation
        """
        stocks = self.conn.execute(query).fetchall()
        
        for stock in stocks:
            # Colorer les lignes selon le niveau de stock
            if stock[2] <= stock[3]:  # Stock sous le seuil
                tags = ('alerte',)
            elif stock[2] <= stock[3] * 1.5:  # Stock faible
                tags = ('faible',)
            else:
                tags = ('normal',)
            
            self.tree.insert("", tk.END, values=stock, tags=tags)
        
        # Configuration des tags pour les couleurs
        self.tree.tag_configure('alerte', background=theme_manager.get_color("accent_danger"), 
                               foreground='white')
        self.tree.tag_configure('faible', background=theme_manager.get_color("accent_warning"), 
                               foreground='white')
        self.tree.tag_configure('normal', background=theme_manager.get_color("bg_secondary"))

    def show_alerts(self):
        """Affiche les alertes de stock"""
        query = """
        SELECT a.code_article, a.designation, 
               COALESCE(s.quantite, 0) as quantite, 
               a.seuil_alerte
        FROM Articles a
        LEFT JOIN Stock s ON a.code_article = s.code_article
        WHERE COALESCE(s.quantite, 0) <= a.seuil_alerte
        ORDER BY COALESCE(s.quantite, 0) ASC
        """
        alertes = self.conn.execute(query).fetchall()
        
        if alertes:
            alert_text = f"⚠️ ALERTE: {len(alertes)} article(s) en rupture de stock ou en quantité faible!"
            self.alert_label.configure(text=alert_text, fg=theme_manager.get_color("accent_danger"))
        else:
            self.alert_label.configure(text="✅ Tous les stocks sont au niveau optimal", 
                                     fg=theme_manager.get_color("accent_success"))

    def add_entry(self):
        """Ajoute une entrée de stock"""
        self.show_movement_dialog("entrée")

    def add_exit(self):
        """Ajoute une sortie de stock"""
        self.show_movement_dialog("sortie")

    def show_movement_dialog(self, type_mouvement):
        """Affiche la boîte de dialogue pour les mouvements de stock"""
        dialog = tk.Toplevel(self)
        dialog.title(f"📊 {type_mouvement.capitalize()} de stock")
        dialog.geometry("500x400")
        dialog.configure(bg=theme_manager.get_color("bg_primary"))
        dialog.transient(self)
        dialog.grab_set()
        
        # Centrer la fenêtre
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Header
        icon = "📈" if type_mouvement == "entrée" else "📉"
        color = theme_manager.get_color("accent_success") if type_mouvement == "entrée" else theme_manager.get_color("accent_danger")
        
        header_frame = tk.Frame(dialog, bg=color, height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg=color)
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        title_label = tk.Label(header_content, text=f"{icon} {type_mouvement.capitalize()} de stock", 
                              font=('Arial', 16, 'bold'), bg=color, fg='white')
        title_label.pack(side=tk.LEFT)
        
        # Contenu principal
        main_frame = tk.Frame(dialog, bg=theme_manager.get_color("bg_secondary"), relief='solid', bd=1)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        content_frame = tk.Frame(main_frame, bg=theme_manager.get_color("bg_secondary"))
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Champs de saisie
        tk.Label(content_frame, text="📋 Code article:", font=('Arial', 11, 'bold'),
                bg=theme_manager.get_color("bg_secondary"), fg=theme_manager.get_color("fg_primary")).pack(anchor=tk.W, pady=(0, 5))
        
        code_entry = tk.Entry(content_frame, font=('Arial', 11), width=30,
                             bg=theme_manager.get_color("bg_input"), fg=theme_manager.get_color("fg_tertiary"),
                             relief='solid', bd=1)
        code_entry.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(content_frame, text="📊 Quantité:", font=('Arial', 11, 'bold'),
                bg=theme_manager.get_color("bg_secondary"), fg=theme_manager.get_color("fg_primary")).pack(anchor=tk.W, pady=(0, 5))
        
        qty_entry = tk.Entry(content_frame, font=('Arial', 11), width=30,
                            bg=theme_manager.get_color("bg_input"), fg=theme_manager.get_color("fg_tertiary"),
                            relief='solid', bd=1)
        qty_entry.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(content_frame, text="📝 Commentaire (optionnel):", font=('Arial', 11, 'bold'),
                bg=theme_manager.get_color("bg_secondary"), fg=theme_manager.get_color("fg_primary")).pack(anchor=tk.W, pady=(0, 5))
        
        comment_text = tk.Text(content_frame, font=('Arial', 10), height=4, width=30,
                              bg=theme_manager.get_color("bg_input"), fg=theme_manager.get_color("fg_tertiary"),
                              relief='solid', bd=1)
        comment_text.pack(fill=tk.X, pady=(0, 20))
        
        # Boutons
        button_frame = tk.Frame(content_frame, bg=theme_manager.get_color("bg_secondary"))
        button_frame.pack(fill=tk.X)
        
        def save_movement():
            code_article = code_entry.get().strip()
            try:
                quantite = int(qty_entry.get())
            except ValueError:
                messagebox.showerror("❌ Erreur", "La quantité doit être un nombre entier")
                return
            
            if not code_article or quantite <= 0:
                messagebox.showerror("❌ Erreur", "Veuillez remplir tous les champs avec des valeurs valides")
                return
            
            try:
                # Vérifier si l'article existe
                article = self.conn.execute("SELECT * FROM Articles WHERE code_article = ?", (code_article,)).fetchone()
                if not article:
                    messagebox.showerror("❌ Erreur", f"L'article avec le code '{code_article}' n'existe pas")
                    return
                
                # Enregistrer le mouvement
                self.conn.execute(
                    "INSERT INTO Mouvements (code_article, type, quantite, date_heure) VALUES (?, ?, ?, datetime('now'))",
                    (code_article, type_mouvement, quantite)
                )
                
                # Mettre à jour le stock
                if type_mouvement == "entrée":
                    self.conn.execute(
                        "INSERT OR REPLACE INTO Stock (code_article, quantite) VALUES (?, COALESCE((SELECT quantite FROM Stock WHERE code_article = ?), 0) + ?)",
                        (code_article, code_article, quantite)
                    )
                else:  # sortie
                    current_stock = self.conn.execute("SELECT quantite FROM Stock WHERE code_article = ?", (code_article,)).fetchone()
                    if not current_stock or current_stock[0] < quantite:
                        messagebox.showerror("❌ Erreur", "Stock insuffisant pour cette sortie")
                        return
                    
                    self.conn.execute(
                        "UPDATE Stock SET quantite = quantite - ? WHERE code_article = ?",
                        (quantite, code_article)
                    )
                
                self.conn.commit()
                messagebox.showinfo("✅ Succès", f"{type_mouvement.capitalize()} de stock enregistrée")
                dialog.destroy()
                self.refresh_table()
                self.show_alerts()
                
            except Exception as e:
                messagebox.showerror("❌ Erreur", f"Erreur lors de l'enregistrement: {str(e)}")
        
        save_style = theme_manager.get_button_style("success")
        tk.Button(button_frame, text="✅ Enregistrer", command=save_movement,
                 font=('Arial', 11, 'bold'), **save_style, padx=20, pady=10).pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_style = theme_manager.get_button_style("secondary")
        tk.Button(button_frame, text="❌ Annuler", command=dialog.destroy,
                 font=('Arial', 11), **cancel_style, padx=20, pady=10).pack(side=tk.LEFT)
        
        # Focus sur le premier champ
        code_entry.focus()

    def show_report(self):
        # Affiche un rapport moderne des mouvements
        win = tk.Toplevel(self)
        win.title("📊 Rapport des mouvements")
        win.geometry("900x600")
        win.configure(bg='#f8f9fa')
        
        # Header
        header_frame = tk.Frame(win, bg='#343a40', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#343a40')
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        title_label = tk.Label(header_content, text="📊 Rapport des mouvements", 
                              font=('Arial', 16, 'bold'), bg='#343a40', fg='white')
        title_label.pack(side=tk.LEFT)
        
        close_btn = tk.Button(header_content, text="← Retour", 
                             command=win.destroy, font=('Arial', 10),
                             bg='#6c757d', fg='white', borderwidth=0,
                             padx=15, pady=6, cursor='hand2')
        close_btn.pack(side=tk.RIGHT)
        
        # Contenu
        content_frame = tk.Frame(win, bg='white', relief='solid', bd=1)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Tableau
        tree = ttk.Treeview(content_frame, columns=("Date", "Type", "Code article", "Quantité"), show="headings")
        for col in ("Date", "Type", "Code article", "Quantité"):
            tree.heading(col, text=f"📅 {col}" if col == "Date" else f"📦 {col}" if col == "Code article" else f"🔢 {col}" if col == "Quantité" else f"🔄 {col}")
            tree.column(col, width=200)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        mouvements = self.conn.execute("SELECT date_mvt, type, code_article, quantite FROM Mouvements ORDER BY date_mvt DESC").fetchall()
        for m in mouvements:
            tree.insert("", tk.END, values=m)

    def show_stock_value(self):
        # Fenêtre moderne pour la valeur du stock
        win = tk.Toplevel(self)
        win.title("💰 Valeur totale du stock")
        win.geometry("900x600")
        win.configure(bg='#f8f9fa')
        
        # Header
        header_frame = tk.Frame(win, bg='#343a40', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#343a40')
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        title_label = tk.Label(header_content, text="💰 Valeur totale du stock", 
                              font=('Arial', 16, 'bold'), bg='#343a40', fg='white')
        title_label.pack(side=tk.LEFT)
        
        close_btn = tk.Button(header_content, text="← Retour", 
                             command=win.destroy, font=('Arial', 10),
                             bg='#6c757d', fg='white', borderwidth=0,
                             padx=15, pady=6, cursor='hand2')
        close_btn.pack(side=tk.RIGHT)
        
        # Calcule la valeur totale du stock
        query = """
        SELECT a.code_article, a.designation, IFNULL(s.quantite, 0), a.prix_vente,
               IFNULL(s.quantite, 0) * a.prix_vente AS valeur
        FROM Articles a
        LEFT JOIN Stock s ON a.code_article = s.code_article
        """
        articles = self.conn.execute(query).fetchall()
        total = sum(row[4] for row in articles)
        
        # Contenu
        content_frame = tk.Frame(win, bg='white', relief='solid', bd=1)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Total en haut
        total_frame = tk.Frame(content_frame, bg='#e8f5e8', relief='solid', bd=1)
        total_frame.pack(fill=tk.X, padx=10, pady=10)
        
        total_label = tk.Label(total_frame, text=f"💰 Valeur totale du stock : {total:.2f} €", 
                              font=('Arial', 16, 'bold'), bg='#e8f5e8', fg='#155724')
        total_label.pack(pady=15)
        
        # Tableau
        tree = ttk.Treeview(content_frame, columns=("Code article", "Désignation", "Quantité", "Prix vente", "Valeur"), show="headings")
        headers = [("Code article", "📋"), ("Désignation", "📝"), ("Quantité", "📦"), ("Prix vente", "💰"), ("Valeur", "💵")]
        for col, icon in headers:
            tree.heading(col, text=f"{icon} {col}")
            tree.column(col, width=150)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for row in articles:
            tree.insert("", tk.END, values=row)

    def show_top_sellers(self):
        # Fenêtre moderne pour les articles les plus vendus
        win = tk.Toplevel(self)
        win.title("🏆 Articles les plus vendus")
        win.geometry("800x600")
        win.configure(bg='#f8f9fa')
        
        # Header
        header_frame = tk.Frame(win, bg='#343a40', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#343a40')
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        title_label = tk.Label(header_content, text="🏆 Articles les plus vendus", 
                              font=('Arial', 16, 'bold'), bg='#343a40', fg='white')
        title_label.pack(side=tk.LEFT)
        
        close_btn = tk.Button(header_content, text="← Retour", 
                             command=win.destroy, font=('Arial', 10),
                             bg='#6c757d', fg='white', borderwidth=0,
                             padx=15, pady=6, cursor='hand2')
        close_btn.pack(side=tk.RIGHT)
        
        # Contenu
        content_frame = tk.Frame(win, bg='white', relief='solid', bd=1)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
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
        
        # Tableau avec style classement
        tree = ttk.Treeview(content_frame, columns=("Rang", "Code article", "Désignation", "Quantité vendue"), show="headings")
        tree.heading("Rang", text="🏆 Rang")
        tree.heading("Code article", text="📋 Code article")
        tree.heading("Désignation", text="📝 Désignation")
        tree.heading("Quantité vendue", text="📊 Quantité vendue")
        
        tree.column("Rang", width=80)
        tree.column("Code article", width=120)
        tree.column("Désignation", width=250)
        tree.column("Quantité vendue", width=150)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for i, row in enumerate(articles, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            tree.insert("", tk.END, values=(medal, row[0], row[1], row[2]))

# Pour ouvrir la gestion du stock depuis le menu principal :
# from ui.stock_manager import StockManager
# StockManager(self.root)