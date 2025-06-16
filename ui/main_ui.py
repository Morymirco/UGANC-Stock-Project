# ui/main_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from reporting import report_manager
import sqlite3
from ui.article_manager import ArticleManager
from ui.stock_manager import StockManager
from ui.theme_manager import theme_manager

class MainUI:
    def __init__(self, root, auth_manager):
        self.root = root
        self.auth_manager = auth_manager
        
        # Récupérer l'utilisateur connecté
        self.current_user = self.auth_manager.get_current_user()
        
        # Configuration des couleurs et du style
        self.setup_styles()
        
        # Configurer la fenêtre principale
        self.root.title(f"Système de Gestion de Stock - {self.current_user['nom_complet']} ({self.current_user['role']})")
        self.root.geometry("1200x800")
        self.root.configure(bg=theme_manager.get_color("bg_primary"))
        
        # Connexion à la base de données
        self.conn = sqlite3.connect("stock_app.db")
        
        # Créer les widgets
        self.create_widgets()
        
        # Créer le menu
        self.create_menu()
        
        # Rafraîchir les statistiques automatiquement
        self.refresh_stats()
    
    def setup_styles(self):
        """Configure les styles personnalisés pour l'interface"""
        style = ttk.Style()
        
        # Style pour les boutons principaux
        style.configure('Action.TButton',
                       font=('Arial', 10, 'bold'),
                       background=theme_manager.get_color("accent_primary"),
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(15, 8))
        
        style.map('Action.TButton',
                 background=[('active', '#8e44ad'),
                           ('pressed', '#7d3c98')])
        
        # Style pour les boutons secondaires
        style.configure('Secondary.TButton',
                       font=('Arial', 9),
                       background=theme_manager.get_color("bg_tertiary"),
                       foreground=theme_manager.get_color("fg_primary"),
                       borderwidth=0,
                       focuscolor='none',
                       padding=(12, 6))
        
        # Style pour les boutons de succès
        style.configure('Success.TButton',
                       font=('Arial', 10, 'bold'),
                       background=theme_manager.get_color("accent_success"),
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(12, 8))
        
        # Style pour les boutons de danger
        style.configure('Danger.TButton',
                       font=('Arial', 10, 'bold'),
                       background=theme_manager.get_color("accent_danger"),
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(12, 8))
        
        # Style pour les boutons info
        style.configure('Info.TButton',
                       font=('Arial', 10, 'bold'),
                       background=theme_manager.get_color("accent_info"),
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(12, 8))

    def create_widgets(self):
        """Crée les widgets de l'interface principale"""
        # Header stylisé
        header_frame = tk.Frame(self.root, bg=theme_manager.get_color("bg_tertiary"), height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Contenu du header
        header_content = tk.Frame(header_frame, bg=theme_manager.get_color("bg_tertiary"))
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Logo et titre
        title_frame = tk.Frame(header_content, bg=theme_manager.get_color("bg_tertiary"))
        title_frame.pack(side=tk.LEFT)
        
        logo_label = tk.Label(title_frame, text="📦", font=('Arial', 24), 
                             bg=theme_manager.get_color("bg_tertiary"), fg=theme_manager.get_color("fg_primary"))
        logo_label.pack(side=tk.LEFT, padx=(0, 10))
        
        app_title = tk.Label(title_frame, text="Système de Gestion de Stock", 
                            font=('Arial', 18, 'bold'), bg=theme_manager.get_color("bg_tertiary"), 
                            fg=theme_manager.get_color("fg_primary"))
        app_title.pack(side=tk.LEFT)
        
        # Informations utilisateur
        user_frame = tk.Frame(header_content, bg=theme_manager.get_color("bg_tertiary"))
        user_frame.pack(side=tk.RIGHT)
        
        user_icon = tk.Label(user_frame, text="👤", font=('Arial', 16), 
                            bg=theme_manager.get_color("bg_tertiary"), fg=theme_manager.get_color("fg_primary"))
        user_icon.pack(side=tk.LEFT, padx=(0, 5))
        
        user_info = tk.Label(user_frame, text=f"{self.current_user['nom_complet']}\n{self.current_user['role']}", 
                            font=('Arial', 10), bg=theme_manager.get_color("bg_tertiary"), 
                            fg=theme_manager.get_color("fg_secondary"), justify=tk.RIGHT)
        user_info.pack(side=tk.LEFT, padx=(0, 15))
        
        # Bouton déconnexion
        logout_style = theme_manager.get_button_style("danger")
        logout_btn = tk.Button(user_frame, text="🚪 Déconnexion", command=self.logout,
                              font=('Arial', 10), **logout_style, padx=10, pady=5)
        logout_btn.pack(side=tk.RIGHT)
        
        # Container principal
        main_container = tk.Frame(self.root, bg=theme_manager.get_color("bg_primary"))
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Section des statistiques
        stats_frame = tk.Frame(main_container, bg=theme_manager.get_color("bg_card"), relief='solid', bd=1)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        stats_header = tk.Frame(stats_frame, bg=theme_manager.get_color("bg_tertiary"))
        stats_header.pack(fill=tk.X)
        
        stats_title = tk.Label(stats_header, text="📊 Tableau de bord", 
                              font=('Arial', 14, 'bold'), bg=theme_manager.get_color("bg_tertiary"), 
                              fg=theme_manager.get_color("fg_primary"))
        stats_title.pack(side=tk.LEFT, pady=10, padx=15)
        
        # Bouton rafraîchir
        refresh_style = theme_manager.get_button_style("info")
        refresh_btn = tk.Button(stats_header, text="🔄 Actualiser", command=self.refresh_stats,
                               font=('Arial', 9), **refresh_style, padx=10, pady=5)
        refresh_btn.pack(side=tk.RIGHT, pady=10, padx=15)
        
        # Ligne de séparation
        separator = tk.Frame(stats_frame, bg=theme_manager.get_color("separator"), height=1)
        separator.pack(fill=tk.X)
        
        # Contenu des statistiques
        self.stats_content = tk.Frame(stats_frame, bg=theme_manager.get_color("bg_card"))
        self.stats_content.pack(fill=tk.X, padx=20, pady=20)
        
        # Section des actions rapides
        actions_frame = tk.Frame(main_container, bg=theme_manager.get_color("bg_card"), relief='solid', bd=1)
        actions_frame.pack(fill=tk.BOTH, expand=True)
        
        actions_header = tk.Frame(actions_frame, bg=theme_manager.get_color("bg_tertiary"))
        actions_header.pack(fill=tk.X)
        
        actions_title = tk.Label(actions_header, text="🚀 Actions rapides", 
                                font=('Arial', 14, 'bold'), bg=theme_manager.get_color("bg_tertiary"), 
                                fg=theme_manager.get_color("fg_primary"))
        actions_title.pack(pady=10, padx=15)
        
        # Ligne de séparation
        separator2 = tk.Frame(actions_frame, bg=theme_manager.get_color("separator"), height=1)
        separator2.pack(fill=tk.X)
        
        actions_content = tk.Frame(actions_frame, bg=theme_manager.get_color("bg_card"))
        actions_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Boutons d'actions principales
        self.create_action_buttons(actions_content)
        
    def get_stats_data(self):
        """Récupère les données statistiques de la base de données"""
        try:
            # Nombre total d'articles
            total_articles = self.conn.execute("SELECT COUNT(*) FROM Articles").fetchone()[0]
            
            # Stock total (somme des quantités)
            total_stock = self.conn.execute(
                "SELECT IFNULL(SUM(quantite), 0) FROM Stock"
            ).fetchone()[0]
            
            # Produits en rupture (quantité = 0 ou inférieure au seuil)
            rupture_stock = self.conn.execute("""
                SELECT COUNT(*) FROM Articles a 
                LEFT JOIN Stock s ON a.code_article = s.code_article 
                WHERE IFNULL(s.quantite, 0) <= a.seuil_alerte
            """).fetchone()[0]
            
            # Valeur totale du stock
            valeur_stock = self.conn.execute("""
                SELECT IFNULL(SUM(IFNULL(s.quantite, 0) * a.prix_vente), 0) 
                FROM Articles a 
                LEFT JOIN Stock s ON a.code_article = s.code_article
            """).fetchone()[0]
            
            # Mouvements aujourd'hui
            mouvements_today = self.conn.execute("""
                SELECT COUNT(*) FROM Mouvements 
                WHERE DATE(date_mvt) = DATE('now')
            """).fetchone()[0]
            
            # Dernière activité
            last_activity = self.conn.execute("""
                SELECT date_mvt FROM Mouvements 
                ORDER BY date_mvt DESC LIMIT 1
            """).fetchone()
            
            last_activity_text = "Aucune activité" if not last_activity else last_activity[0]
            
            return {
                'total_articles': total_articles,
                'total_stock': total_stock,
                'rupture_stock': rupture_stock,
                'valeur_stock': valeur_stock,
                'mouvements_today': mouvements_today,
                'last_activity': last_activity_text
            }
        except Exception as e:
            print(f"Erreur lors de la récupération des statistiques: {e}")
            return {
                'total_articles': 0,
                'total_stock': 0,
                'rupture_stock': 0,
                'valeur_stock': 0,
                'mouvements_today': 0,
                'last_activity': 'Erreur'
            }
    
    def refresh_stats(self):
        """Rafraîchit les statistiques affichées"""
        # Nettoyer le contenu existant
        for widget in self.stats_content.winfo_children():
            widget.destroy()
        
        # Récupérer les nouvelles données
        stats = self.get_stats_data()
        
        # Créer la grille des statistiques
        stats_grid = tk.Frame(self.stats_content, bg=theme_manager.get_color("bg_card"))
        stats_grid.pack(fill=tk.X)
        
        # Configuration de la grille
        for i in range(3):
            stats_grid.grid_columnconfigure(i, weight=1)
        
        # Créer les cartes de statistiques
        self.create_stat_card(stats_grid, "📦 Total Articles", str(stats['total_articles']), 
                             "Articles enregistrés", 0, 0, theme_manager.get_color("accent_primary"))
        
        self.create_stat_card(stats_grid, "📊 Stock Total", str(stats['total_stock']), 
                             "Unités en stock", 0, 1, theme_manager.get_color("accent_info"))
        
        color_rupture = theme_manager.get_color("accent_danger") if stats['rupture_stock'] > 0 else theme_manager.get_color("accent_success")
        self.create_stat_card(stats_grid, "⚠️ Alertes Stock", str(stats['rupture_stock']), 
                             "Produits en alerte", 0, 2, color_rupture)
        
        self.create_stat_card(stats_grid, "💰 Valeur Stock", f"{stats['valeur_stock']:.2f} €", 
                             "Valeur totale", 1, 0, theme_manager.get_color("accent_success"))
        
        self.create_stat_card(stats_grid, "📈 Mouvements", str(stats['mouvements_today']), 
                             "Aujourd'hui", 1, 1, theme_manager.get_color("accent_warning"))
        
        self.create_stat_card(stats_grid, "🕐 Dernière activité", 
                             stats['last_activity'][:16] if len(stats['last_activity']) > 16 else stats['last_activity'], 
                             "Dernier mouvement", 1, 2, theme_manager.get_color("fg_secondary"))
        
        # Programmer le prochain rafraîchissement (toutes les 30 secondes)
        self.root.after(30000, self.refresh_stats)
    
    def create_stat_card(self, parent, title, value, subtitle, row, col, color):
        """Crée une carte de statistique"""
        card = tk.Frame(parent, bg=theme_manager.get_color("bg_secondary"), relief='solid', bd=1)
        card.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
        parent.grid_columnconfigure(col, weight=1)
        
        # Contenu de la carte
        card_content = tk.Frame(card, bg=theme_manager.get_color("bg_secondary"))
        card_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        title_label = tk.Label(card_content, text=title, font=('Arial', 12, 'bold'), 
                              bg=theme_manager.get_color("bg_secondary"), fg=theme_manager.get_color("fg_primary"))
        title_label.pack(anchor=tk.W)
        
        value_label = tk.Label(card_content, text=value, font=('Arial', 20, 'bold'), 
                              bg=theme_manager.get_color("bg_secondary"), fg=color)
        value_label.pack(anchor=tk.W, pady=(5, 0))
        
        subtitle_label = tk.Label(card_content, text=subtitle, font=('Arial', 9), 
                                 bg=theme_manager.get_color("bg_secondary"), fg=theme_manager.get_color("fg_secondary"))
        subtitle_label.pack(anchor=tk.W)
    
    def create_action_buttons(self, parent):
        """Crée les boutons d'actions rapides"""
        # Première rangée de boutons
        row1 = tk.Frame(parent, bg=theme_manager.get_color("bg_card"))
        row1.pack(fill=tk.X, pady=(0, 15))
        
        # Boutons selon les permissions
        if self.auth_manager.has_permission("admin"):
            admin_style = theme_manager.get_button_style("primary")
            tk.Button(row1, text="👥 Gestion Utilisateurs", command=self.manage_users,
                     font=('Arial', 11, 'bold'), **admin_style, padx=20, pady=12).pack(side=tk.LEFT, padx=(0, 15))
        
        success_style = theme_manager.get_button_style("success")
        tk.Button(row1, text="📦 Gestion Articles", command=self.manage_products,
                 font=('Arial', 11, 'bold'), **success_style, padx=20, pady=12).pack(side=tk.LEFT, padx=(0, 15))
        
        info_style = theme_manager.get_button_style("info")
        tk.Button(row1, text="📊 Gestion Stock", command=self.manage_stock,
                 font=('Arial', 11, 'bold'), **info_style, padx=20, pady=12).pack(side=tk.LEFT, padx=(0, 15))
        
        # Deuxième rangée de boutons
        row2 = tk.Frame(parent, bg=theme_manager.get_color("bg_card"))
        row2.pack(fill=tk.X, pady=(0, 15))
        
        warning_style = theme_manager.get_button_style("warning")
        tk.Button(row2, text="📈 Entrée Stock", command=self.stock_entry,
                 font=('Arial', 10, 'bold'), **warning_style, padx=15, pady=10).pack(side=tk.LEFT, padx=(0, 10))
        
        danger_style = theme_manager.get_button_style("danger")
        tk.Button(row2, text="📉 Sortie Stock", command=self.stock_exit,
                 font=('Arial', 10, 'bold'), **danger_style, padx=15, pady=10).pack(side=tk.LEFT, padx=(0, 10))
        
        secondary_style = theme_manager.get_button_style("secondary")
        tk.Button(row2, text="📋 Historique", command=self.show_all_mouvements,
                 font=('Arial', 10), **secondary_style, padx=15, pady=10).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(row2, text="🔍 Rapports", command=self.show_reports,
                 font=('Arial', 10), **secondary_style, padx=15, pady=10).pack(side=tk.LEFT, padx=(0, 10))
    
    def show_reports(self):
        """Affiche le menu des rapports"""
        reports_window = tk.Toplevel(self.root)
        reports_window.title("📊 Rapports")
        reports_window.geometry("600x400")
        reports_window.configure(bg=theme_manager.get_color("bg_primary"))
        
        # Header
        header_frame = tk.Frame(reports_window, bg=theme_manager.get_color("bg_tertiary"), height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg=theme_manager.get_color("bg_tertiary"))
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        title_label = tk.Label(header_content, text="📊 Rapports et Analyses", 
                              font=('Arial', 16, 'bold'), bg=theme_manager.get_color("bg_tertiary"), 
                              fg=theme_manager.get_color("fg_primary"))
        title_label.pack(side=tk.LEFT)
        
        close_btn = tk.Button(header_content, text="❌ Fermer", command=reports_window.destroy,
                             font=('Arial', 10), **theme_manager.get_button_style("danger"), 
                             padx=10, pady=5)
        close_btn.pack(side=tk.RIGHT)
        
        # Contenu
        content_frame = tk.Frame(reports_window, bg=theme_manager.get_color("bg_card"), relief='solid', bd=1)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        buttons_frame = tk.Frame(content_frame, bg=theme_manager.get_color("bg_card"))
        buttons_frame.pack(expand=True)
        
        # Boutons de rapports
        report_buttons = [
            ("📈 Historique Entrées", self.show_entry_mouvements),
            ("📉 Historique Sorties", self.show_exit_mouvements),
            ("💰 Valeur Stock", lambda: StockManager(self.root).show_stock_value()),
            ("🏆 Top Vendeurs", lambda: StockManager(self.root).show_top_sellers())
        ]
        
        for i, (text, command) in enumerate(report_buttons):
            style = theme_manager.get_button_style("info")
            btn = tk.Button(buttons_frame, text=text, command=command,
                           font=('Arial', 12, 'bold'), **style, padx=25, pady=15)
            btn.pack(pady=10)
    
    def logout(self):
        """Déconnecte l'utilisateur et retourne à l'écran de connexion"""
        self.auth_manager.logout()
        self.root.destroy()
        self.root.master.deiconify()  # Afficher à nouveau la fenêtre de connexion
    
    # Méthodes pour les fonctionnalités (à implémenter)
    def manage_users(self):
        # Importer ici pour éviter les importations circulaires
        from ui.user_management import UserManagementUI
        UserManagementUI(self.root, self.auth_manager)
    
    def manage_products(self):
        ArticleManager(self.root)
    
    def stock_entry(self):
        """Gère les entrées de stock avec interface moderne"""
        self.show_movement_dialog("entrée")
    
    def stock_exit(self):
        """Gère les sorties de stock avec interface moderne"""
        self.show_movement_dialog("sortie")
    
    def show_movement_dialog(self, type_mouvement):
        """Affiche le dialogue moderne pour les mouvements de stock avec disposition optimisée"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"🔄 {type_mouvement.capitalize()} de stock")
        dialog.geometry("900x750")  # Taille plus grande
        dialog.configure(bg=theme_manager.get_color("bg_primary"))
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrer la fenêtre
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Header avec couleur selon le type
        icon = "📈" if type_mouvement == "entrée" else "📉"
        color = theme_manager.get_color("accent_success") if type_mouvement == "entrée" else theme_manager.get_color("accent_danger")
        
        header_frame = tk.Frame(dialog, bg=color, height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg=color)
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        title_label = tk.Label(header_content, text=f"{icon} {type_mouvement.capitalize()} de stock", 
                              font=('Arial', 18, 'bold'), bg=color, fg='white')
        title_label.pack(side=tk.LEFT)
        
        # Bouton fermer
        close_btn = tk.Button(header_content, text="❌", command=dialog.destroy,
                             font=('Arial', 12, 'bold'), bg=theme_manager.get_color("accent_danger"), 
                             fg='white', borderwidth=0, padx=10, pady=5, cursor='hand2')
        close_btn.pack(side=tk.RIGHT)
        
        # Container principal organisé en deux colonnes
        main_container = tk.Frame(dialog, bg=theme_manager.get_color("bg_primary"))
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configuration en grid pour une meilleure répartition
        main_container.grid_columnconfigure(0, weight=2)  # Colonne gauche (articles)
        main_container.grid_columnconfigure(1, weight=1)  # Colonne droite (infos + actions)
        main_container.grid_rowconfigure(0, weight=1)
        
        # ========== COLONNE GAUCHE: SÉLECTION D'ARTICLES ==========
        left_frame = tk.Frame(main_container, bg=theme_manager.get_color("bg_secondary"), relief='solid', bd=1)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        # Header sélection articles
        articles_header = tk.Frame(left_frame, bg=theme_manager.get_color("bg_tertiary"))
        articles_header.pack(fill=tk.X)
        
        articles_title = tk.Label(articles_header, text="📋 Sélectionner un article", 
                                 font=('Arial', 14, 'bold'), bg=theme_manager.get_color("bg_tertiary"), 
                                 fg=theme_manager.get_color("fg_primary"))
        articles_title.pack(side=tk.LEFT, pady=12, padx=15)
        
        # Zone de recherche optimisée
        search_frame = tk.Frame(articles_header, bg=theme_manager.get_color("bg_tertiary"))
        search_frame.pack(side=tk.RIGHT, pady=8, padx=15)
        
        search_label = tk.Label(search_frame, text="🔍", font=('Arial', 12), 
                               bg=theme_manager.get_color("bg_tertiary"), fg=theme_manager.get_color("fg_primary"))
        search_label.pack(side=tk.LEFT, padx=(0, 5))
        
        search_entry = tk.Entry(search_frame, font=('Arial', 10), width=25,
                               bg=theme_manager.get_color("bg_input"), fg=theme_manager.get_color("fg_tertiary"),
                               relief='solid', bd=1)
        search_entry.pack(side=tk.LEFT)
        search_entry.insert(0, "Rechercher par code, nom ou catégorie...")
        
        def on_search_focus_in(event):
            if search_entry.get() == "Rechercher par code, nom ou catégorie...":
                search_entry.delete(0, tk.END)
                search_entry.configure(fg=theme_manager.get_color("fg_primary"))
        
        def on_search_focus_out(event):
            if not search_entry.get():
                search_entry.insert(0, "Rechercher par code, nom ou catégorie...")
                search_entry.configure(fg=theme_manager.get_color("fg_tertiary"))
        
        def on_search_change(event):
            self.filter_articles(articles_tree, search_entry.get())
        
        search_entry.bind("<FocusIn>", on_search_focus_in)
        search_entry.bind("<FocusOut>", on_search_focus_out)
        search_entry.bind("<KeyRelease>", on_search_change)
        
        # Séparateur
        separator1 = tk.Frame(left_frame, bg=theme_manager.get_color("separator"), height=1)
        separator1.pack(fill=tk.X)
        
        # Tableau des articles avec hauteur fixe
        articles_content = tk.Frame(left_frame, bg=theme_manager.get_color("bg_secondary"))
        articles_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configuration du style pour le tableau
        style = ttk.Style()
        style.configure('Articles.Treeview',
                       background=theme_manager.get_color("bg_secondary"),
                       foreground=theme_manager.get_color("fg_primary"),
                       fieldbackground=theme_manager.get_color("bg_secondary"),
                       borderwidth=1,
                       relief='solid',
                       rowheight=25)
        
        style.configure('Articles.Treeview.Heading',
                       background=theme_manager.get_color("bg_tertiary"),
                       foreground=theme_manager.get_color("fg_primary"),
                       relief='solid',
                       borderwidth=1)
        
        columns = ("code", "designation", "categorie", "stock")
        articles_tree = ttk.Treeview(articles_content, columns=columns, show="headings", 
                                    style='Articles.Treeview', height=15)  # Hauteur fixe
        
        # Headers avec icônes
        headers = {
            "code": "📋 Code",
            "designation": "📝 Désignation",
            "categorie": "🏷️ Catégorie", 
            "stock": "📦 Stock"
        }
        
        for col in columns:
            articles_tree.heading(col, text=headers[col])
            if col == "designation":
                articles_tree.column(col, width=200)
            elif col == "code":
                articles_tree.column(col, width=100)
            elif col == "categorie":
                articles_tree.column(col, width=120)
            else:
                articles_tree.column(col, width=80, anchor='center')
        
        # Scrollbars pour le tableau
        articles_v_scrollbar = ttk.Scrollbar(articles_content, orient=tk.VERTICAL, command=articles_tree.yview)
        articles_h_scrollbar = ttk.Scrollbar(articles_content, orient=tk.HORIZONTAL, command=articles_tree.xview)
        articles_tree.configure(yscrollcommand=articles_v_scrollbar.set, xscrollcommand=articles_h_scrollbar.set)
        
        articles_tree.grid(row=0, column=0, sticky='nsew')
        articles_v_scrollbar.grid(row=0, column=1, sticky='ns')
        articles_h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        articles_content.grid_rowconfigure(0, weight=1)
        articles_content.grid_columnconfigure(0, weight=1)
        
        # ========== COLONNE DROITE: INFORMATIONS ET ACTIONS ==========
        right_frame = tk.Frame(main_container, bg=theme_manager.get_color("bg_primary"))
        right_frame.grid(row=0, column=1, sticky='nsew', padx=(10, 0))
        
        # Variable pour stocker l'article sélectionné
        selected_article = {"code": "", "designation": "", "categorie": "", "stock": 0}
        
        # Section informations de l'article sélectionné
        info_frame = tk.Frame(right_frame, bg=theme_manager.get_color("bg_secondary"), relief='solid', bd=1)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        info_header = tk.Frame(info_frame, bg=theme_manager.get_color("bg_tertiary"))
        info_header.pack(fill=tk.X)
        
        info_title = tk.Label(info_header, text="ℹ️ Article sélectionné", 
                             font=('Arial', 13, 'bold'), bg=theme_manager.get_color("bg_tertiary"), 
                             fg=theme_manager.get_color("fg_primary"))
        info_title.pack(pady=10)
        
        separator2 = tk.Frame(info_frame, bg=theme_manager.get_color("separator"), height=1)
        separator2.pack(fill=tk.X)
        
        info_content = tk.Frame(info_frame, bg=theme_manager.get_color("bg_secondary"))
        info_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        article_info_label = tk.Label(info_content, text="👆 Sélectionnez un article dans la liste", 
                                     font=('Arial', 11), bg=theme_manager.get_color("bg_secondary"), 
                                     fg=theme_manager.get_color("fg_tertiary"), justify=tk.LEFT, wraplength=250)
        article_info_label.pack(fill=tk.X)
        
        # Section quantité
        qty_frame = tk.Frame(right_frame, bg=theme_manager.get_color("bg_secondary"), relief='solid', bd=1)
        qty_frame.pack(fill=tk.X, pady=(0, 15))
        
        qty_header = tk.Frame(qty_frame, bg=theme_manager.get_color("bg_tertiary"))
        qty_header.pack(fill=tk.X)
        
        qty_title = tk.Label(qty_header, text="📊 Quantité", 
                            font=('Arial', 13, 'bold'), bg=theme_manager.get_color("bg_tertiary"), 
                            fg=theme_manager.get_color("fg_primary"))
        qty_title.pack(pady=10)
        
        separator3 = tk.Frame(qty_frame, bg=theme_manager.get_color("separator"), height=1)
        separator3.pack(fill=tk.X)
        
        qty_content = tk.Frame(qty_frame, bg=theme_manager.get_color("bg_secondary"))
        qty_content.pack(fill=tk.X, padx=15, pady=15)
        
        qty_label = tk.Label(qty_content, text=f"🔢 Quantité à {type_mouvement}:", 
                            font=('Arial', 11, 'bold'), bg=theme_manager.get_color("bg_secondary"), 
                            fg=theme_manager.get_color("fg_primary"))
        qty_label.pack(anchor=tk.W, pady=(0, 8))
        
        qty_entry = tk.Entry(qty_content, font=('Arial', 12), width=15,
                            bg=theme_manager.get_color("bg_input"), fg=theme_manager.get_color("fg_tertiary"),
                            relief='solid', bd=1, justify='center')
        qty_entry.pack(fill=tk.X)
        qty_entry.insert(0, "1")
        
        # Section boutons - toujours visible en bas
        button_frame = tk.Frame(right_frame, bg=theme_manager.get_color("bg_secondary"), relief='solid', bd=1)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        button_header = tk.Frame(button_frame, bg=theme_manager.get_color("bg_tertiary"))
        button_header.pack(fill=tk.X)
        
        button_title = tk.Label(button_header, text="⚡ Actions", 
                               font=('Arial', 13, 'bold'), bg=theme_manager.get_color("bg_tertiary"), 
                               fg=theme_manager.get_color("fg_primary"))
        button_title.pack(pady=10)
        
        separator4 = tk.Frame(button_frame, bg=theme_manager.get_color("separator"), height=1)
        separator4.pack(fill=tk.X)
        
        button_content = tk.Frame(button_frame, bg=theme_manager.get_color("bg_secondary"))
        button_content.pack(fill=tk.X, padx=15, pady=15)
        
        # Boutons d'action
        save_style = theme_manager.get_button_style("success" if type_mouvement == "entrée" else "danger")
        save_btn = tk.Button(button_content, text=f"✅ Confirmer {type_mouvement}", 
                            command=lambda: self.save_movement_with_selection(type_mouvement, selected_article, qty_entry, dialog),
                            font=('Arial', 11, 'bold'), **save_style, padx=15, pady=12)
        save_btn.pack(fill=tk.X, pady=(0, 10))
        
        cancel_style = theme_manager.get_button_style("secondary")
        cancel_btn = tk.Button(button_content, text="❌ Annuler", command=dialog.destroy,
                              font=('Arial', 11), **cancel_style, padx=15, pady=12)
        cancel_btn.pack(fill=tk.X)
        
        # Fonction de sélection d'article améliorée
        def on_article_select(event):
            selection = articles_tree.selection()
            if selection:
                item = articles_tree.item(selection[0])
                values = item['values']
                
                selected_article["code"] = values[0]
                selected_article["designation"] = values[1]
                selected_article["categorie"] = values[2]
                selected_article["stock"] = int(values[3]) if values[3] else 0
                
                self.update_selected_article_info_improved(selected_article, article_info_label, type_mouvement)
                
                # Focus sur la quantité après sélection
                qty_entry.focus()
                qty_entry.select_range(0, tk.END)
        
        articles_tree.bind("<<TreeviewSelect>>", on_article_select)
        
        # Charger tous les articles
        self.load_all_articles(articles_tree)
        
        # Focus initial sur la recherche
        search_entry.focus()

    def load_all_articles(self, tree):
        """Charge tous les articles dans le tableau"""
        try:
            # Requête pour récupérer tous les articles avec leur stock
            query = """
            SELECT a.code_article, a.designation, a.categorie, COALESCE(s.quantite, 0) as stock
            FROM Articles a
            LEFT JOIN Stock s ON a.code_article = s.code_article
            ORDER BY a.designation
            """
            articles = self.conn.execute(query).fetchall()
            
            # Vider le tableau
            for item in tree.get_children():
                tree.delete(item)
            
            # Ajouter les articles
            for article in articles:
                # Couleur selon le niveau de stock
                tags = ()
                stock = int(article[3]) if article[3] else 0
                if stock == 0:
                    tags = ("red",)
                elif stock < 10:  # Seuil arbitraire
                    tags = ("orange",)
                else:
                    tags = ("green",)
                
                tree.insert("", tk.END, values=article, tags=tags)
            
            # Configuration des couleurs des tags
            tree.tag_configure("red", foreground="#e74c3c")
            tree.tag_configure("orange", foreground="#f39c12") 
            tree.tag_configure("green", foreground="#27ae60")
            
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors du chargement des articles: {str(e)}")

    def filter_articles(self, tree, search_term):
        """Filtre les articles selon le terme de recherche"""
        if search_term == "Rechercher..." or not search_term:
            self.load_all_articles(tree)
            return
        
        try:
            # Requête de recherche
            query = """
            SELECT a.code_article, a.designation, a.categorie, COALESCE(s.quantite, 0) as stock
            FROM Articles a
            LEFT JOIN Stock s ON a.code_article = s.code_article
            WHERE a.code_article LIKE ? OR a.designation LIKE ? OR a.categorie LIKE ?
            ORDER BY a.designation
            """
            search_pattern = f"%{search_term}%"
            articles = self.conn.execute(query, (search_pattern, search_pattern, search_pattern)).fetchall()
            
            # Vider le tableau
            for item in tree.get_children():
                tree.delete(item)
            
            # Ajouter les articles filtrés
            for article in articles:
                tags = ()
                stock = int(article[3]) if article[3] else 0
                if stock == 0:
                    tags = ("red",)
                elif stock < 10:
                    tags = ("orange",)
                else:
                    tags = ("green",)
                
                tree.insert("", tk.END, values=article, tags=tags)
            
            # Configuration des couleurs des tags
            tree.tag_configure("red", foreground="#e74c3c")
            tree.tag_configure("orange", foreground="#f39c12") 
            tree.tag_configure("green", foreground="#27ae60")
            
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de la recherche: {str(e)}")

    def update_selected_article_info_improved(self, article, label, type_mouvement):
        """Met à jour l'affichage des informations de l'article sélectionné avec design amélioré"""
        if article["code"]:
            # Déterminer les couleurs selon le stock
            if article["stock"] == 0:
                stock_color = "#e74c3c"
                stock_icon = "❌"
                stock_status = "ÉPUISÉ"
            elif article["stock"] < 10:
                stock_color = "#f39c12"
                stock_icon = "⚠️"
                stock_status = "FAIBLE"
            else:
                stock_color = "#27ae60"
                stock_icon = "✅"
                stock_status = "NORMAL"
            
            # Texte formaté avec informations détaillées
            info_text = f"""📦 Code: {article['code']}

📝 Désignation:
{article['designation']}

🏷️ Catégorie: {article['categorie']}

📊 Stock actuel: {article['stock']}
{stock_icon} État: {stock_status}"""
            
            # Ajouter des alertes spécifiques pour les sorties
            if type_mouvement == "sortie":
                if article["stock"] == 0:
                    info_text += "\n\n🚫 ATTENTION:\nStock épuisé !"
                elif article["stock"] < 10:
                    info_text += "\n\n⚠️ ATTENTION:\nStock faible"
            
            label.configure(text=info_text, fg=theme_manager.get_color("fg_primary"))
        else:
            label.configure(text="👆 Sélectionnez un article\ndans la liste ci-contre\n\n💡 Utilisez la recherche pour\nfiltrer rapidement", 
                           fg=theme_manager.get_color("fg_tertiary"))

    def save_movement_with_selection(self, type_mouvement, selected_article, qty_entry, dialog):
        """Sauvegarde un mouvement avec l'article sélectionné"""
        if not selected_article["code"]:
            messagebox.showerror("❌ Erreur", "Veuillez sélectionner un article")
            return
        
        try:
            quantite = int(qty_entry.get())
        except ValueError:
            messagebox.showerror("❌ Erreur", "La quantité doit être un nombre entier")
            return
        
        if quantite <= 0:
            messagebox.showerror("❌ Erreur", "La quantité doit être supérieure à 0")
            return
        
        # Pour les sorties, vérifier le stock disponible
        if type_mouvement == "sortie" and selected_article["stock"] < quantite:
            messagebox.showerror("❌ Erreur", f"Stock insuffisant pour cette sortie\nStock disponible: {selected_article['stock']}")
            return
        
        try:
            # Enregistrer le mouvement selon le modèle Mouvement
            self.conn.execute(
                "INSERT INTO Mouvements (type, code_article, quantite, date_mvt, user_id) VALUES (?, ?, ?, datetime('now'), ?)",
                (type_mouvement, selected_article["code"], quantite, self.current_user['id'])
            )
            
            # Mettre à jour le stock
            if type_mouvement == "entrée":
                self.conn.execute(
                    "INSERT OR REPLACE INTO Stock (code_article, quantite) VALUES (?, COALESCE((SELECT quantite FROM Stock WHERE code_article = ?), 0) + ?)",
                    (selected_article["code"], selected_article["code"], quantite)
                )
            else:  # sortie
                self.conn.execute(
                    "UPDATE Stock SET quantite = quantite - ? WHERE code_article = ?",
                    (quantite, selected_article["code"])
                )
            
            self.conn.commit()
            messagebox.showinfo("✅ Succès", f"{type_mouvement.capitalize()} de stock enregistrée avec succès!\n\nArticle: {selected_article['designation']}\nQuantité: {quantite}")
            dialog.destroy()
            
            # Rafraîchir les statistiques
            if hasattr(self, 'refresh_stats'):
                self.refresh_stats()
                
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de l'enregistrement: {str(e)}")
    
    def get_current_datetime(self):
        """Retourne la date et heure actuelles formatées"""
        from datetime import datetime
        return datetime.now().strftime("%d/%m/%Y à %H:%M")
    
    def show_all_mouvements(self):
        """Affiche l'historique complet des mouvements (adapté au modèle)"""
        history_window = tk.Toplevel(self.root)
        history_window.title("📋 Historique des mouvements")
        history_window.geometry("1000x600")
        history_window.configure(bg=theme_manager.get_color("bg_primary"))
        
        # Header
        header_frame = tk.Frame(history_window, bg=theme_manager.get_color("bg_tertiary"), height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg=theme_manager.get_color("bg_tertiary"))
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        title_label = tk.Label(header_content, text="📋 Historique des mouvements de stock", 
                              font=('Arial', 16, 'bold'), bg=theme_manager.get_color("bg_tertiary"), 
                              fg=theme_manager.get_color("fg_primary"))
        title_label.pack(side=tk.LEFT)
        
        close_btn = tk.Button(header_content, text="❌ Fermer", command=history_window.destroy,
                             font=('Arial', 10), **theme_manager.get_button_style("danger"), 
                             padx=15, pady=6)
        close_btn.pack(side=tk.RIGHT)
        
        # Filtres
        filter_frame = tk.Frame(history_window, bg=theme_manager.get_color("bg_secondary"), relief='solid', bd=1)
        filter_frame.pack(fill=tk.X, padx=20, pady=10)
        
        filter_content = tk.Frame(filter_frame, bg=theme_manager.get_color("bg_secondary"))
        filter_content.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(filter_content, text="🔍 Filtres:", font=('Arial', 12, 'bold'),
                bg=theme_manager.get_color("bg_secondary"), fg=theme_manager.get_color("fg_primary")).pack(side=tk.LEFT, padx=(0, 15))
        
        # Filtre par type
        filter_buttons = tk.Frame(filter_content, bg=theme_manager.get_color("bg_secondary"))
        filter_buttons.pack(side=tk.LEFT)
        
        all_style = theme_manager.get_button_style("info")
        tk.Button(filter_buttons, text="📊 Tous", command=lambda: self.filter_movements(movements_tree, "tous"),
                 font=('Arial', 9), **all_style, padx=10, pady=4).pack(side=tk.LEFT, padx=(0, 5))
        
        entry_style = theme_manager.get_button_style("success")
        tk.Button(filter_buttons, text="📈 Entrées", command=lambda: self.filter_movements(movements_tree, "entrée"),
                 font=('Arial', 9), **entry_style, padx=10, pady=4).pack(side=tk.LEFT, padx=(0, 5))
        
        exit_style = theme_manager.get_button_style("danger")
        tk.Button(filter_buttons, text="📉 Sorties", command=lambda: self.filter_movements(movements_tree, "sortie"),
                 font=('Arial', 9), **exit_style, padx=10, pady=4).pack(side=tk.LEFT)
        
        # Tableau
        table_frame = tk.Frame(history_window, bg=theme_manager.get_color("bg_secondary"), relief='solid', bd=1)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Configuration du style pour le tableau
        style = ttk.Style()
        style.configure('History.Treeview',
                       background=theme_manager.get_color("bg_secondary"),
                       foreground=theme_manager.get_color("fg_primary"),
                       fieldbackground=theme_manager.get_color("bg_secondary"),
                       borderwidth=1,
                       relief='solid')
        
        style.configure('History.Treeview.Heading',
                       background=theme_manager.get_color("bg_tertiary"),
                       foreground=theme_manager.get_color("fg_primary"),
                       relief='solid',
                       borderwidth=1)
        
        # Colonnes adaptées au modèle (sans commentaire)
        columns = ("date", "type", "code_article", "designation", "quantite", "user")
        movements_tree = ttk.Treeview(table_frame, columns=columns, show="headings", style='History.Treeview')
        
        # Headers avec icônes
        headers = {
            "date": "🕒 Date/Heure",
            "type": "🔄 Type",
            "code_article": "📋 Code Article",
            "designation": "📝 Désignation",
            "quantite": "📊 Quantité",
            "user": "👤 Utilisateur"
        }
        
        for col in columns:
            movements_tree.heading(col, text=headers[col])
            if col == "designation":
                movements_tree.column(col, width=200)
            elif col == "user":
                movements_tree.column(col, width=150)
            elif col == "date":
                movements_tree.column(col, width=150)
            else:
                movements_tree.column(col, width=120)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=movements_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=movements_tree.xview)
        movements_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        movements_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X, padx=10)
        
        # Charger tous les mouvements
        self.filter_movements(movements_tree, "tous")
    
    def filter_movements(self, tree, filter_type):
        """Filtre les mouvements selon le type (adapté au modèle)"""
        # Vider le tableau
        for item in tree.get_children():
            tree.delete(item)
        
        try:
            # Requête selon le filtre - utilisation des noms corrects du modèle
            if filter_type == "tous":
                query = """
                SELECT m.date_mvt, m.type, m.code_article, a.designation, m.quantite, u.nom_complet
                FROM Mouvements m
                LEFT JOIN Articles a ON m.code_article = a.code_article
                LEFT JOIN Utilisateurs u ON m.user_id = u.id
                ORDER BY m.date_mvt DESC
                """
                params = ()
            else:
                query = """
                SELECT m.date_mvt, m.type, m.code_article, a.designation, m.quantite, u.nom_complet
                FROM Mouvements m
                LEFT JOIN Articles a ON m.code_article = a.code_article
                LEFT JOIN Utilisateurs u ON m.user_id = u.id
                WHERE m.type = ?
                ORDER BY m.date_mvt DESC
                """
                params = (filter_type,)
            
            mouvements = self.conn.execute(query, params).fetchall()
            
            for mouvement in mouvements:
                # Formatter les données pour l'affichage
                date_str = mouvement[0] if mouvement[0] else "N/A"
                type_icon = "📈" if mouvement[1] == "entrée" else "📉"
                type_display = f"{type_icon} {mouvement[1].capitalize()}"
                
                values = (
                    date_str,
                    type_display,
                    mouvement[2] or "N/A",
                    mouvement[3] or "Article supprimé",
                    mouvement[4] or 0,
                    mouvement[5] or "Utilisateur supprimé"
                )
                
                tree.insert("", tk.END, values=values)
                
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors du chargement: {str(e)}")
    
    def manage_stock(self):
        StockManager(self.root)


