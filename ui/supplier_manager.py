import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from ui.theme_manager import theme_manager

class SupplierForm(tk.Toplevel):
    def __init__(self, parent, supplier=None, refresh_callback=None):
        super().__init__(parent)
        self.title("🏢 Gestion de fournisseur")
        self.geometry("600x600")
        self.configure(bg=theme_manager.get_color("bg_primary"))
        self.supplier = supplier
        self.refresh_callback = refresh_callback
        self.conn = sqlite3.connect("stock_app.db")
        
        # Configuration des styles
        self.setup_styles()
        
        self.create_widgets()
        if supplier:
            self.fill_fields(supplier)

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
        header_frame = tk.Frame(self, bg=theme_manager.get_color("accent_info"), height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Contenu du header
        header_content = tk.Frame(header_frame, bg=theme_manager.get_color("accent_info"))
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Titre avec icône
        title_frame = tk.Frame(header_content, bg=theme_manager.get_color("accent_info"))
        title_frame.pack(side=tk.LEFT)
        
        title_icon = tk.Label(title_frame, text="🏢", font=('Arial', 20), 
                             bg=theme_manager.get_color("accent_info"), fg='white')
        title_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        action_text = "Modifier le fournisseur" if self.supplier else "Nouveau fournisseur"
        title_label = tk.Label(title_frame, text=action_text, 
                              font=('Arial', 16, 'bold'), bg=theme_manager.get_color("accent_info"), fg='white')
        title_label.pack(side=tk.LEFT)
        
        # Container principal avec scrollbar
        main_container = tk.Frame(self, bg=theme_manager.get_color("bg_primary"))
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Section informations fournisseur
        info_frame = tk.Frame(main_container, bg=theme_manager.get_color("bg_secondary"), relief='solid', bd=1)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        info_header = tk.Frame(info_frame, bg=theme_manager.get_color("bg_tertiary"))
        info_header.pack(fill=tk.X)
        
        info_title = tk.Label(info_header, text="📝 Informations du fournisseur", 
                             font=('Arial', 14, 'bold'), bg=theme_manager.get_color("bg_tertiary"), 
                             fg=theme_manager.get_color("fg_primary"))
        info_title.pack(pady=10)
        
        separator1 = tk.Frame(info_frame, bg=theme_manager.get_color("separator"), height=1)
        separator1.pack(fill=tk.X)
        
        info_content = tk.Frame(info_frame, bg=theme_manager.get_color("bg_secondary"))
        info_content.pack(fill=tk.X, padx=20, pady=20)
        
        # Grid pour organiser les champs
        info_content.grid_columnconfigure(1, weight=1)
        
        # Nom du fournisseur
        tk.Label(info_content, text="🏢 Nom du fournisseur:", font=('Arial', 11, 'bold'),
                bg=theme_manager.get_color("bg_secondary"), fg=theme_manager.get_color("fg_primary")).grid(row=0, column=0, sticky="w", pady=5)
        
        self.nom_entry = tk.Entry(info_content, font=('Arial', 11), bg=theme_manager.get_color("bg_input"), 
                                 fg=theme_manager.get_color("fg_tertiary"), relief='solid', bd=1)
        self.nom_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Contact principal
        tk.Label(info_content, text="📞 Contact principal:", font=('Arial', 11, 'bold'),
                bg=theme_manager.get_color("bg_secondary"), fg=theme_manager.get_color("fg_primary")).grid(row=1, column=0, sticky="w", pady=5)
        
        self.contact_entry = tk.Entry(info_content, font=('Arial', 11), bg=theme_manager.get_color("bg_input"), 
                                     fg=theme_manager.get_color("fg_tertiary"), relief='solid', bd=1)
        self.contact_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Email (optionnel)
        tk.Label(info_content, text="📧 Email:", font=('Arial', 11, 'bold'),
                bg=theme_manager.get_color("bg_secondary"), fg=theme_manager.get_color("fg_primary")).grid(row=2, column=0, sticky="w", pady=5)
        
        self.email_entry = tk.Entry(info_content, font=('Arial', 11), bg=theme_manager.get_color("bg_input"), 
                                   fg=theme_manager.get_color("fg_tertiary"), relief='solid', bd=1)
        self.email_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Adresse (optionnel)
        tk.Label(info_content, text="📍 Adresse:", font=('Arial', 11, 'bold'),
                bg=theme_manager.get_color("bg_secondary"), fg=theme_manager.get_color("fg_primary")).grid(row=3, column=0, sticky="nw", pady=5)
        
        self.adresse_text = tk.Text(info_content, font=('Arial', 11), bg=theme_manager.get_color("bg_input"), 
                                   fg=theme_manager.get_color("fg_tertiary"), relief='solid', bd=1, height=3, width=40)
        self.adresse_text.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Section boutons d'action
        action_frame = tk.Frame(main_container, bg=theme_manager.get_color("bg_secondary"), relief='solid', bd=1)
        action_frame.pack(fill=tk.X)
        
        action_header = tk.Frame(action_frame, bg=theme_manager.get_color("bg_tertiary"))
        action_header.pack(fill=tk.X)
        
        action_title = tk.Label(action_header, text="⚡ Actions", 
                               font=('Arial', 14, 'bold'), bg=theme_manager.get_color("bg_tertiary"), 
                               fg=theme_manager.get_color("fg_primary"))
        action_title.pack(pady=10)
        
        separator2 = tk.Frame(action_frame, bg=theme_manager.get_color("separator"), height=1)
        separator2.pack(fill=tk.X)
        
        button_content = tk.Frame(action_frame, bg=theme_manager.get_color("bg_secondary"))
        button_content.pack(fill=tk.X, padx=20, pady=20)
        
        # Boutons
        button_frame = tk.Frame(button_content, bg=theme_manager.get_color("bg_secondary"))
        button_frame.pack()
        
        # Bouton sauvegarder
        save_style = theme_manager.get_button_style("success")
        save_text = "💾 Modifier" if self.supplier else "✅ Créer fournisseur"
        save_btn = tk.Button(button_frame, text=save_text, command=self.save_supplier,
                            font=('Arial', 12, 'bold'), **save_style, padx=25, pady=12)
        save_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Bouton annuler
        cancel_style = theme_manager.get_button_style("secondary")
        cancel_btn = tk.Button(button_frame, text="❌ Annuler", command=self.destroy,
                              font=('Arial', 12), **cancel_style, padx=25, pady=12)
        cancel_btn.pack(side=tk.LEFT)
        
        # Focus sur le nom
        self.nom_entry.focus()

    def fill_fields(self, supplier):
        """Remplit les champs avec les données du fournisseur"""
        self.nom_entry.insert(0, supplier[1])  # nom
        self.contact_entry.insert(0, supplier[2])  # contact
        if len(supplier) > 3 and supplier[3]:  # email
            self.email_entry.insert(0, supplier[3])
        if len(supplier) > 4 and supplier[4]:  # adresse
            self.adresse_text.insert('1.0', supplier[4])

    def save_supplier(self):
        """Sauvegarde le fournisseur"""
        # Récupérer les données
        nom = self.nom_entry.get().strip()
        contact = self.contact_entry.get().strip()
        email = self.email_entry.get().strip()
        adresse = self.adresse_text.get('1.0', tk.END).strip()
        
        # Validation
        if not nom or not contact:
            messagebox.showerror("❌ Erreur", "Le nom et le contact sont obligatoires")
            return
        
        # Validation email simple
        if email and '@' not in email:
            messagebox.showerror("❌ Erreur", "Format email invalide")
            return
        
        try:
            if self.supplier:
                # Modification d'un fournisseur existant
                self.conn.execute("""
                    UPDATE Fournisseurs 
                    SET nom = ?, contact = ?, email = ?, adresse = ?
                    WHERE id = ?
                """, (nom, contact, email or None, adresse or None, self.supplier[0]))
                messagebox.showinfo("✅ Succès", f"Fournisseur '{nom}' modifié avec succès")
            else:
                # Création d'un nouveau fournisseur
                self.conn.execute("""
                    INSERT INTO Fournisseurs (nom, contact, email, adresse)
                    VALUES (?, ?, ?, ?)
                """, (nom, contact, email or None, adresse or None))
                messagebox.showinfo("✅ Succès", f"Fournisseur '{nom}' créé avec succès")
            
            self.conn.commit()
            
            # Rafraîchir la liste si callback défini
            if self.refresh_callback:
                self.refresh_callback()
            
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de la sauvegarde: {str(e)}")


class SupplierManager(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("🏢 Gestion des fournisseurs")
        self.geometry("1200x700")
        self.configure(bg=theme_manager.get_color("bg_primary"))
        self.conn = sqlite3.connect("stock_app.db")
        
        # Créer la table si elle n'existe pas
        self.create_table_if_not_exists()
        
        # Configuration des styles
        self.setup_styles()
        
        self.create_widgets()
        self.refresh_table()

    def create_table_if_not_exists(self):
        """Crée la table Fournisseurs si elle n'existe pas"""
        try:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS Fournisseurs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    contact TEXT NOT NULL,
                    email TEXT,
                    adresse TEXT
                )
            """)
            self.conn.commit()
        except Exception as e:
            print(f"Erreur lors de la création de la table: {e}")

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
        
        title_icon = tk.Label(title_frame, text="🏢", font=('Arial', 20), 
                             bg=theme_manager.get_color("bg_tertiary"), fg=theme_manager.get_color("fg_primary"))
        title_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = tk.Label(title_frame, text="Gestion des Fournisseurs", 
                              font=('Arial', 16, 'bold'), bg=theme_manager.get_color("bg_tertiary"), 
                              fg=theme_manager.get_color("fg_primary"))
        title_label.pack(side=tk.LEFT)
        
        # Boutons d'action
        button_frame = tk.Frame(header_content, bg=theme_manager.get_color("bg_tertiary"))
        button_frame.pack(side=tk.RIGHT)
        
        # Bouton nouveau fournisseur
        new_style = theme_manager.get_button_style("success")
        new_btn = tk.Button(button_frame, text="➕ Nouveau Fournisseur", command=self.new_supplier,
                           font=('Arial', 11, 'bold'), **new_style, padx=15, pady=8)
        new_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton rafraîchir
        refresh_style = theme_manager.get_button_style("info")
        refresh_btn = tk.Button(button_frame, text="🔄 Actualiser", command=self.refresh_table,
                               font=('Arial', 10), **refresh_style, padx=12, pady=8)
        refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton fermer
        close_style = theme_manager.get_button_style("secondary")
        close_btn = tk.Button(button_frame, text="❌ Fermer", command=self.destroy,
                             font=('Arial', 10), **close_style, padx=12, pady=8)
        close_btn.pack(side=tk.LEFT)
        
        # Section des actions
        actions_frame = tk.Frame(self, bg=theme_manager.get_color("bg_secondary"), relief='solid', bd=1)
        actions_frame.pack(fill=tk.X, padx=20, pady=10)
        
        actions_header = tk.Frame(actions_frame, bg=theme_manager.get_color("bg_tertiary"))
        actions_header.pack(fill=tk.X)
        
        actions_title = tk.Label(actions_header, text="🚀 Actions sur les fournisseurs", 
                                font=('Arial', 14, 'bold'), bg=theme_manager.get_color("bg_tertiary"), 
                                fg=theme_manager.get_color("fg_primary"))
        actions_title.pack(pady=10)
        
        separator = tk.Frame(actions_frame, bg=theme_manager.get_color("separator"), height=1)
        separator.pack(fill=tk.X)
        
        btn_content = tk.Frame(actions_frame, bg=theme_manager.get_color("bg_secondary"))
        btn_content.pack(fill=tk.X, padx=20, pady=15)
        
        # Boutons d'actions
        info_style = theme_manager.get_button_style("info")
        tk.Button(btn_content, text="✏️ Modifier", command=self.edit_supplier,
                 font=('Arial', 11, 'bold'), **info_style, padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
        
        danger_style = theme_manager.get_button_style("danger")
        tk.Button(btn_content, text="🗑️ Supprimer", command=self.delete_supplier,
                 font=('Arial', 11, 'bold'), **danger_style, padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
        
        warning_style = theme_manager.get_button_style("warning")
        tk.Button(btn_content, text="📊 Statistiques", command=self.show_supplier_stats,
                 font=('Arial', 11, 'bold'), **warning_style, padx=15, pady=8).pack(side=tk.LEFT)
        
        # Section du tableau
        table_frame = tk.Frame(self, bg=theme_manager.get_color("bg_secondary"), relief='solid', bd=1)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        table_header = tk.Frame(table_frame, bg=theme_manager.get_color("bg_tertiary"))
        table_header.pack(fill=tk.X)
        
        table_title = tk.Label(table_header, text="📋 Liste des fournisseurs", 
                              font=('Arial', 14, 'bold'), bg=theme_manager.get_color("bg_tertiary"), 
                              fg=theme_manager.get_color("fg_primary"))
        table_title.pack(side=tk.LEFT, pady=10, padx=15)
        
        # Compteur
        self.count_label = tk.Label(table_header, text="", font=('Arial', 11),
                                   bg=theme_manager.get_color("bg_tertiary"), fg=theme_manager.get_color("fg_secondary"))
        self.count_label.pack(side=tk.RIGHT, pady=10, padx=15)
        
        separator2 = tk.Frame(table_frame, bg=theme_manager.get_color("separator"), height=1)
        separator2.pack(fill=tk.X)
        
        # Tableau avec scrollbars
        table_content = tk.Frame(table_frame, bg=theme_manager.get_color("bg_secondary"))
        table_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("id", "nom", "contact", "email", "adresse")
        self.tree = ttk.Treeview(table_content, columns=columns, show="headings", style='Treeview')
        
        # Configuration des colonnes avec icônes
        headers = {
            "id": "🔢 ID",
            "nom": "🏢 Nom",
            "contact": "📞 Contact",
            "email": "📧 Email",
            "adresse": "📍 Adresse"
        }
        
        for col in columns:
            self.tree.heading(col, text=headers[col])
            if col == "nom":
                self.tree.column(col, width=200)
            elif col == "contact":
                self.tree.column(col, width=150)
            elif col == "email":
                self.tree.column(col, width=180)
            elif col == "adresse":
                self.tree.column(col, width=250)
            else:
                self.tree.column(col, width=80)
        
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
        self.tree.bind("<Double-1>", lambda e: self.edit_supplier())

    def refresh_table(self):
        """Actualise le tableau des fournisseurs"""
        try:
            # Vider le tableau
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Récupérer les fournisseurs
            suppliers = self.conn.execute("SELECT * FROM Fournisseurs ORDER BY nom").fetchall()
            
            # Ajouter les fournisseurs au tableau
            for supplier in suppliers:
                # Limiter la longueur de l'adresse pour l'affichage
                adresse_display = supplier[4][:50] + "..." if supplier[4] and len(supplier[4]) > 50 else (supplier[4] or "")
                
                values = (
                    supplier[0],  # id
                    supplier[1],  # nom
                    supplier[2],  # contact
                    supplier[3] or "",  # email
                    adresse_display  # adresse
                )
                self.tree.insert("", tk.END, values=values)
            
            # Mettre à jour le compteur
            count = len(suppliers)
            self.count_label.configure(text=f"📊 {count} fournisseur{'s' if count > 1 else ''}")
            
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors du chargement des fournisseurs: {str(e)}")

    def new_supplier(self):
        """Crée un nouveau fournisseur"""
        SupplierForm(self, refresh_callback=self.refresh_table)

    def edit_supplier(self):
        """Modifie le fournisseur sélectionné"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("⚠️ Attention", "Veuillez sélectionner un fournisseur à modifier")
            return
        
        item = self.tree.item(selection[0])
        supplier_id = item['values'][0]
        
        # Récupérer les données complètes du fournisseur
        supplier = self.conn.execute("SELECT * FROM Fournisseurs WHERE id = ?", (supplier_id,)).fetchone()
        if supplier:
            SupplierForm(self, supplier=supplier, refresh_callback=self.refresh_table)

    def delete_supplier(self):
        """Supprime le fournisseur sélectionné"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("⚠️ Attention", "Veuillez sélectionner un fournisseur à supprimer")
            return
        
        item = self.tree.item(selection[0])
        supplier_id = item['values'][0]
        supplier_name = item['values'][1]
        
        # Confirmation
        if messagebox.askyesno("🗑️ Confirmation", 
                              f"Êtes-vous sûr de vouloir supprimer le fournisseur '{supplier_name}' ?\n\nCette action est irréversible."):
            try:
                self.conn.execute("DELETE FROM Fournisseurs WHERE id = ?", (supplier_id,))
                self.conn.commit()
                messagebox.showinfo("✅ Succès", f"Fournisseur '{supplier_name}' supprimé avec succès")
                self.refresh_table()
            except Exception as e:
                messagebox.showerror("❌ Erreur", f"Erreur lors de la suppression: {str(e)}")

    def show_supplier_stats(self):
        """Affiche les statistiques des fournisseurs"""
        try:
            # Compter les fournisseurs
            total_suppliers = self.conn.execute("SELECT COUNT(*) FROM Fournisseurs").fetchone()[0]
            
            # Fournisseurs avec email
            with_email = self.conn.execute("SELECT COUNT(*) FROM Fournisseurs WHERE email IS NOT NULL AND email != ''").fetchone()[0]
            
            # Fournisseurs avec adresse
            with_address = self.conn.execute("SELECT COUNT(*) FROM Fournisseurs WHERE adresse IS NOT NULL AND adresse != ''").fetchone()[0]
            
            stats_text = f"""📊 Statistiques des fournisseurs

🏢 Total fournisseurs: {total_suppliers}
📧 Avec email: {with_email} ({(with_email/total_suppliers*100):.1f}% si total > 0 else 0)
📍 Avec adresse: {with_address} ({(with_address/total_suppliers*100):.1f}% si total > 0 else 0)"""
            
            messagebox.showinfo("📊 Statistiques", stats_text)
            
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors du calcul des statistiques: {str(e)}") 