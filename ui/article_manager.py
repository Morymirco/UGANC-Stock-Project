import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageTk
import os
from ui.theme_manager import theme_manager

class ArticleForm(tk.Toplevel):
    def __init__(self, parent, article=None, refresh_callback=None):
        super().__init__(parent)
        self.title("📦 Gestion d'article")
        self.geometry("600x750")
        self.configure(bg=theme_manager.get_color("bg_primary"))
        self.article = article
        self.refresh_callback = refresh_callback
        self.conn = sqlite3.connect("stock_app.db")
        
        # Configuration des styles
        self.setup_styles()
        
        self.create_widgets()
        if article:
            self.fill_fields(article)

    def setup_styles(self):
        """Configure les styles personnalisés pour l'interface"""
        style = ttk.Style()
        
        # Style pour les champs de saisie
        style.configure('Modern.TEntry',
                       font=('Arial', 11),
                       fieldbackground=theme_manager.get_color("bg_input"),
                       borderwidth=1,
                       relief='solid')

    def create_widgets(self):
        # Header stylisé
        header_frame = tk.Frame(self, bg=theme_manager.get_color("accent_success"), height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Contenu du header
        header_content = tk.Frame(header_frame, bg=theme_manager.get_color("accent_success"))
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Titre avec icône
        title_frame = tk.Frame(header_content, bg=theme_manager.get_color("accent_success"))
        title_frame.pack(side=tk.LEFT)
        
        title_icon = tk.Label(title_frame, text="📦", font=('Arial', 20), 
                             bg=theme_manager.get_color("accent_success"), fg='white')
        title_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        action_text = "Modifier l'article" if self.article else "Nouvel article"
        title_label = tk.Label(title_frame, text=action_text, 
                              font=('Arial', 16, 'bold'), bg=theme_manager.get_color("accent_success"), fg='white')
        title_label.pack(side=tk.LEFT)
        
        # Container principal avec scrollbar
        main_container = tk.Frame(self, bg=theme_manager.get_color("bg_primary"))
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Canvas pour le scroll
        canvas = tk.Canvas(main_container, bg=theme_manager.get_color("bg_primary"))
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=theme_manager.get_color("bg_primary"))
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Section formulaire
        form_frame = tk.Frame(scrollable_frame, bg=theme_manager.get_color("bg_secondary"), relief='solid', bd=1)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        form_header = tk.Frame(form_frame, bg=theme_manager.get_color("bg_tertiary"))
        form_header.pack(fill=tk.X)
        
        form_title = tk.Label(form_header, text="📝 Informations de l'article", 
                             font=('Arial', 14, 'bold'), bg=theme_manager.get_color("bg_tertiary"), 
                             fg=theme_manager.get_color("fg_primary"))
        form_title.pack(pady=10)
        
        # Ligne de séparation
        separator = tk.Frame(form_frame, bg=theme_manager.get_color("separator"), height=1)
        separator.pack(fill=tk.X)
        
        # Contenu du formulaire
        content_frame = tk.Frame(form_frame, bg=theme_manager.get_color("bg_secondary"))
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Variables
        self.code_article_var = tk.StringVar()
        self.designation_var = tk.StringVar()
        self.categorie_var = tk.StringVar()
        self.prix_achat_var = tk.DoubleVar()
        self.prix_vente_var = tk.DoubleVar()
        self.seuil_var = tk.IntVar()
        self.code_barre_var = tk.StringVar()

        # Champs de saisie avec style moderne
        fields = [
            ("📋 Code article:", self.code_article_var, "entry"),
            ("📝 Désignation:", self.designation_var, "entry"),
            ("🏷️ Catégorie:", self.categorie_var, "entry"),
            ("💰 Prix d'achat:", self.prix_achat_var, "double"),
            ("💵 Prix de vente:", self.prix_vente_var, "double"),
            ("⚠️ Seuil d'alerte:", self.seuil_var, "int"),
            ("📊 Code-barres:", self.code_barre_var, "readonly")
        ]
        
        self.entries = {}
        
        for i, (label_text, var, field_type) in enumerate(fields):
            # Label
            label = tk.Label(content_frame, text=label_text, 
                           font=('Arial', 11, 'bold'), bg=theme_manager.get_color("bg_secondary"), 
                           fg=theme_manager.get_color("fg_primary"))
            label.grid(row=i, column=0, sticky=tk.W, pady=8, padx=(0, 10))
            
            # Entry
            if field_type == "readonly":
                entry = tk.Entry(content_frame, textvariable=var, font=('Arial', 11), width=35,
                               bg=theme_manager.get_color("bg_input"), fg=theme_manager.get_color("fg_tertiary"),
                               relief='solid', bd=1, state="readonly")
            else:
                entry = tk.Entry(content_frame, textvariable=var, font=('Arial', 11), width=35,
                               bg=theme_manager.get_color("bg_input"), fg=theme_manager.get_color("fg_tertiary"),
                               relief='solid', bd=1)
            
            entry.grid(row=i, column=1, pady=8, sticky=tk.EW)
            content_frame.grid_columnconfigure(1, weight=1)
            self.entries[field_type if field_type != "readonly" else "code_barre"] = entry
        
        # Section code-barres
        barcode_frame = tk.Frame(scrollable_frame, bg=theme_manager.get_color("bg_secondary"), relief='solid', bd=1)
        barcode_frame.pack(fill=tk.BOTH, pady=(0, 20))
        
        barcode_header = tk.Frame(barcode_frame, bg=theme_manager.get_color("bg_tertiary"))
        barcode_header.pack(fill=tk.X)
        
        barcode_title = tk.Label(barcode_header, text="📊 Gestion du code-barres", 
                                font=('Arial', 14, 'bold'), bg=theme_manager.get_color("bg_tertiary"), 
                                fg=theme_manager.get_color("fg_primary"))
        barcode_title.pack(pady=10)
        
        # Ligne de séparation
        separator2 = tk.Frame(barcode_frame, bg=theme_manager.get_color("separator"), height=1)
        separator2.pack(fill=tk.X)
        
        barcode_content = tk.Frame(barcode_frame, bg=theme_manager.get_color("bg_secondary"))
        barcode_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Bouton générer code-barres
        generate_style = theme_manager.get_button_style("info")
        tk.Button(barcode_content, text="🔄 Générer code-barres", command=self.generer_code_barre,
                 font=('Arial', 11, 'bold'), **generate_style, padx=15, pady=8).pack(pady=(0, 15))
        
        # Zone d'affichage du code-barres
        self.barcode_img_label = tk.Label(barcode_content, bg=theme_manager.get_color("bg_secondary"))
        self.barcode_img_label.pack()
        
        # Section boutons d'action
        action_frame = tk.Frame(scrollable_frame, bg=theme_manager.get_color("bg_secondary"), relief='solid', bd=1)
        action_frame.pack(fill=tk.X)
        
        action_content = tk.Frame(action_frame, bg=theme_manager.get_color("bg_secondary"))
        action_content.pack(fill=tk.X, padx=20, pady=20)
        
        # Boutons
        button_frame = tk.Frame(action_content, bg=theme_manager.get_color("bg_secondary"))
        button_frame.pack()
        
        # Bouton Enregistrer
        save_style = theme_manager.get_button_style("success")
        tk.Button(button_frame, text="✅ Enregistrer", command=self.save_article,
                 font=('Arial', 12, 'bold'), **save_style, padx=25, pady=12).pack(side=tk.LEFT, padx=10)
        
        # Bouton Supprimer (si modification)
        if self.article:
            delete_style = theme_manager.get_button_style("danger")
            tk.Button(button_frame, text="🗑️ Supprimer", command=self.delete_article,
                     font=('Arial', 12, 'bold'), **delete_style, padx=25, pady=12).pack(side=tk.LEFT, padx=10)
        
        # Bouton Annuler
        cancel_style = theme_manager.get_button_style("secondary")
        tk.Button(button_frame, text="❌ Annuler", command=self.destroy,
                 font=('Arial', 12), **cancel_style, padx=25, pady=12).pack(side=tk.LEFT, padx=10)
        
        # Pack canvas et scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

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
            img = img.resize((250, 100))
            self.barcode_img = ImageTk.PhotoImage(img)
            self.barcode_img_label.config(image=self.barcode_img)

    def generer_code_barre(self):
        code_article = self.code_article_var.get()
        if not code_article:
            messagebox.showerror("❌ Erreur", "Code article requis pour générer le code-barres")
            return
        
        try:
            os.makedirs("barcodes", exist_ok=True)
            code128 = barcode.get('code128', code_article, writer=ImageWriter())
            filename = code128.save(f"barcodes/{code_article}")
            self.code_barre_var.set(filename)
            
            # Affichage de l'image
            img = Image.open(filename)
            img = img.resize((250, 100))
            self.barcode_img = ImageTk.PhotoImage(img)
            self.barcode_img_label.config(image=self.barcode_img)
            
            messagebox.showinfo("✅ Succès", "Code-barres généré avec succès")
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de la génération du code-barres: {str(e)}")

    def save_article(self):
        # Validation des champs
        if not all([self.code_article_var.get(), self.designation_var.get(), 
                   self.categorie_var.get()]):
            messagebox.showerror("❌ Erreur", "Veuillez remplir tous les champs obligatoires")
            return
        
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
            messagebox.showinfo("✅ Succès", "Article enregistré avec succès")
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de l'enregistrement: {str(e)}")

    def delete_article(self):
        code_article = self.code_article_var.get()
        if not code_article:
            messagebox.showerror("❌ Erreur", "Code article requis")
            return
        
        # Confirmation
        confirm = messagebox.askyesno("⚠️ Confirmation", 
                                     f"Êtes-vous sûr de vouloir supprimer l'article '{code_article}' ?\n\nCette action est irréversible.")
        if not confirm:
            return
        
        try:
            self.conn.execute("DELETE FROM Articles WHERE code_article = ?", (code_article,))
            self.conn.commit()
            messagebox.showinfo("✅ Succès", "Article supprimé avec succès")
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de la suppression: {str(e)}")

class ArticleManager(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("📦 Gestion des Articles")
        self.geometry("1200x700")
        self.configure(bg=theme_manager.get_color("bg_primary"))
        self.conn = sqlite3.connect("stock_app.db")
        
        # Configuration des styles
        self.setup_styles()
        
        self.create_widgets()
        self.refresh_table()

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
        
        title_icon = tk.Label(title_frame, text="📦", font=('Arial', 20), 
                             bg=theme_manager.get_color("bg_tertiary"), fg=theme_manager.get_color("fg_primary"))
        title_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = tk.Label(title_frame, text="Gestion des Articles", 
                              font=('Arial', 16, 'bold'), bg=theme_manager.get_color("bg_tertiary"), 
                              fg=theme_manager.get_color("fg_primary"))
        title_label.pack(side=tk.LEFT)
        
        # Bouton retour
        back_style = theme_manager.get_button_style("secondary")
        back_btn = tk.Button(header_content, text="← Retour", command=self.destroy,
                            font=('Arial', 10), **back_style, padx=15, pady=6)
        back_btn.pack(side=tk.RIGHT)

        # Section des actions
        actions_frame = tk.Frame(self, bg=theme_manager.get_color("bg_secondary"), relief='solid', bd=1)
        actions_frame.pack(fill=tk.X, padx=20, pady=10)
        
        actions_header = tk.Frame(actions_frame, bg=theme_manager.get_color("bg_tertiary"))
        actions_header.pack(fill=tk.X)
        
        actions_title = tk.Label(actions_header, text="🚀 Actions sur les articles", 
                                font=('Arial', 14, 'bold'), bg=theme_manager.get_color("bg_tertiary"), 
                                fg=theme_manager.get_color("fg_primary"))
        actions_title.pack(pady=10)
        
        # Ligne de séparation
        separator = tk.Frame(actions_frame, bg=theme_manager.get_color("separator"), height=1)
        separator.pack(fill=tk.X)
        
        # Contenu des actions
        btn_content = tk.Frame(actions_frame, bg=theme_manager.get_color("bg_secondary"))
        btn_content.pack(fill=tk.X, padx=20, pady=15)
        
        # Boutons d'actions
        success_style = theme_manager.get_button_style("success")
        tk.Button(btn_content, text="➕ Ajouter un article", command=self.add_article,
                 font=('Arial', 11, 'bold'), **success_style, padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
        
        info_style = theme_manager.get_button_style("info")
        tk.Button(btn_content, text="✏️ Modifier", command=self.edit_article,
                 font=('Arial', 11, 'bold'), **info_style, padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
        
        danger_style = theme_manager.get_button_style("danger")
        tk.Button(btn_content, text="🗑️ Supprimer", command=self.delete_article,
                 font=('Arial', 11, 'bold'), **danger_style, padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
        
        warning_style = theme_manager.get_button_style("warning")
        tk.Button(btn_content, text="📱 Scanner", command=self.scan_and_select_article,
                 font=('Arial', 11, 'bold'), **warning_style, padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))

        # Section du tableau
        table_frame = tk.Frame(self, bg=theme_manager.get_color("bg_secondary"), relief='solid', bd=1)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        table_header = tk.Frame(table_frame, bg=theme_manager.get_color("bg_tertiary"))
        table_header.pack(fill=tk.X)
        
        table_title = tk.Label(table_header, text="📋 Liste des articles", 
                              font=('Arial', 14, 'bold'), bg=theme_manager.get_color("bg_tertiary"), 
                              fg=theme_manager.get_color("fg_primary"))
        table_title.pack(pady=10)
        
        # Ligne de séparation
        separator2 = tk.Frame(table_frame, bg=theme_manager.get_color("separator"), height=1)
        separator2.pack(fill=tk.X)
        
        # Tableau avec scrollbars
        table_content = tk.Frame(table_frame, bg=theme_manager.get_color("bg_secondary"))
        table_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("code_article", "designation", "categorie", "prix_achat", "prix_vente", "seuil_alerte", "code_barre")
        self.tree = ttk.Treeview(table_content, columns=columns, show="headings", style='Treeview')
        
        # Configuration des colonnes avec icônes
        headers = {
            "code_article": "📋 Code",
            "designation": "📝 Désignation", 
            "categorie": "🏷️ Catégorie",
            "prix_achat": "💰 Prix Achat",
            "prix_vente": "💵 Prix Vente",
            "seuil_alerte": "⚠️ Seuil",
            "code_barre": "📊 Code-barres"
        }
        
        for col in columns:
            self.tree.heading(col, text=headers[col])
            if col == "designation":
                self.tree.column(col, width=200)
            elif col == "code_barre":
                self.tree.column(col, width=150)
            else:
                self.tree.column(col, width=100)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_content, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_content, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Placement
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        table_content.grid_rowconfigure(0, weight=1)
        table_content.grid_columnconfigure(0, weight=1)
        
        # Double-clic pour éditer
        self.tree.bind("<Double-1>", lambda e: self.edit_article())

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        try:
            articles = self.conn.execute(
                "SELECT code_article, designation, categorie, prix_achat, prix_vente, seuil_alerte, code_barre FROM Articles"
            ).fetchall()
            
            for article in articles:
                # Tronquer le chemin du code-barres pour l'affichage
                display_article = list(article)
                if display_article[6]:
                    display_article[6] = os.path.basename(display_article[6])
                
                self.tree.insert("", tk.END, values=display_article)
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors du chargement des articles: {str(e)}")

    def add_article(self):
        def refresh(): 
            self.refresh_table()
        ArticleForm(self, refresh_callback=refresh)

    def edit_article(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("⚠️ Attention", "Veuillez sélectionner un article à modifier.")
            return
        
        values = self.tree.item(selected[0])["values"]
        
        # Récupérer l'article complet avec le chemin complet du code-barres
        code_article = values[0]
        article_complete = self.conn.execute(
            "SELECT code_article, designation, categorie, prix_achat, prix_vente, seuil_alerte, code_barre FROM Articles WHERE code_article = ?",
            (code_article,)
        ).fetchone()
        
        def refresh(): 
            self.refresh_table()
        ArticleForm(self, article=article_complete, refresh_callback=refresh)

    def delete_article(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("⚠️ Attention", "Veuillez sélectionner un article à supprimer.")
            return
        
        code_article = self.tree.item(selected[0])["values"][0]
        designation = self.tree.item(selected[0])["values"][1]
        
        # Confirmation
        confirm = messagebox.askyesno("⚠️ Confirmation", 
                                     f"Êtes-vous sûr de vouloir supprimer l'article :\n\n"
                                     f"Code: {code_article}\n"
                                     f"Désignation: {designation}\n\n"
                                     f"Cette action est irréversible.")
        if not confirm:
            return
        
        try:
            self.conn.execute("DELETE FROM Articles WHERE code_article = ?", (code_article,))
            self.conn.commit()
            self.refresh_table()
            messagebox.showinfo("✅ Succès", "Article supprimé avec succès.")
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de la suppression: {str(e)}")

    def scan_and_select_article(self):
        try:
            import cv2
            from pyzbar.pyzbar import decode
        except ImportError:
            messagebox.showerror("❌ Erreur", "Les bibliothèques OpenCV et pyzbar sont requises pour le scanner.\n\nInstallez-les avec:\npip install opencv-python pyzbar")
            return
        
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                messagebox.showerror("❌ Erreur", "Impossible d'accéder à la caméra.")
                return
            
            messagebox.showinfo("📱 Scanner", "Scanner activé!\n\nPointez la caméra vers un code-barres.\nAppuyez sur 'Échap' pour annuler.")
            
            code = None
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Décodage des codes-barres
                for barcode in decode(frame):
                    code = barcode.data.decode('utf-8')
                    cap.release()
                    cv2.destroyAllWindows()
                    
                    # Recherche dans le tableau
                    found = False
                    for row_id in self.tree.get_children():
                        values = self.tree.item(row_id)["values"]
                        if str(values[0]) == code:  # Recherche par code article
                            self.tree.selection_set(row_id)
                            self.tree.see(row_id)
                            messagebox.showinfo("✅ Article trouvé", f"Article avec code '{code}' sélectionné.")
                            found = True
                            break
                    
                    if not found:
                        messagebox.showwarning("⚠️ Non trouvé", f"Aucun article avec le code '{code}' trouvé.")
                    return
                
                # Affichage du flux vidéo
                cv2.imshow('📱 Scanner Code-barres - Appuyez sur Échap pour quitter', frame)
                
                # Sortie avec la touche Échap
                if cv2.waitKey(1) & 0xFF == 27:
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors du scan: {str(e)}")

# Pour ouvrir la gestion des articles depuis le menu principal :
# from ui.article_form import ArticleManager
# ArticleManager(self.root)